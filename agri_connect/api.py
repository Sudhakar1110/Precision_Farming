import json
import re

import frappe
import requests
from frappe.utils import now_datetime, nowdate, time_diff_in_seconds
from frappe.utils.password import get_decrypted_password


# ──────────────────────────────────────────────
# 1. WEATHER: Fetch from OpenWeatherMap
# ──────────────────────────────────────────────


@frappe.whitelist()
def fetch_weather_data(land_unit):
	"""
	Fetches current weather for a Land Unit from OpenWeatherMap API.
	Returns dict with temperature, humidity, wind_speed, weather_condition, precipitation.
	Returns None if GPS coordinates or API key not configured.
	"""
	lu = frappe.get_doc("Land Unit", land_unit)
	lat, lon = None, None

	# Try Land Unit's own gps_coordinates (Geolocation/GeoJSON)
	if lu.gps_coordinates:
		try:
			coords = json.loads(lu.gps_coordinates)["features"][0]["geometry"]["coordinates"]
			lon, lat = coords[0], coords[1]
		except (json.JSONDecodeError, KeyError, IndexError, TypeError):
			frappe.log_error(
				title="Weather Fetch: Bad GPS data",
				message=f"Land Unit {land_unit} has invalid gps_coordinates",
			)

	# Fallback: use linked Location's latitude/longitude
	if (lat is None or lon is None) and lu.location:
		loc = frappe.db.get_value("Location", lu.location, ["latitude", "longitude"], as_dict=True)
		if loc and loc.latitude and loc.longitude:
			lat, lon = loc.latitude, loc.longitude

	if lat is None or lon is None:
		return None

	api_key = get_decrypted_password(
		"Agriculture Settings", "Agriculture Settings", "openweathermap_api_key"
	)
	if not api_key:
		return None

	url = (
		f"https://api.openweathermap.org/data/2.5/weather"
		f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
	)

	try:
		response = requests.get(url, timeout=10)
		response.raise_for_status()
	except requests.RequestException as e:
		frappe.log_error(
			title=f"Weather Fetch Failed: {land_unit}",
			message=str(e),
		)
		return None

	data = response.json()
	return {
		"temperature": data.get("main", {}).get("temp"),
		"humidity": data.get("main", {}).get("humidity"),
		"wind_speed": data.get("wind", {}).get("speed"),
		"weather_condition": data.get("weather", [{}])[0].get("main"),
		"precipitation": data.get("rain", {}).get("1h", 0),
	}


# ──────────────────────────────────────────────
# 2. WEATHER: Daily scheduler
# ──────────────────────────────────────────────


def update_weather_daily():
	"""
	Scheduled task (daily). Fetches weather for all Land Units with GPS
	coordinates and creates Weather Log entries.
	Skips if a Weather Log already exists for the same land unit + date.
	"""
	today = nowdate()
	land_units = frappe.get_all(
		"Land Unit",
		or_filters=[
			["gps_coordinates", "is", "set"],
			["location", "is", "set"],
		],
		fields=["name"],
	)

	for lu in land_units:
		# Duplicate guard: skip if already fetched today
		if frappe.db.exists("Weather Log", {"land_unit": lu.name, "date": today}):
			continue

		try:
			weather_data = fetch_weather_data(lu.name)
		except Exception as e:
			frappe.log_error(
				title=f"Weather Daily: {lu.name}",
				message=str(e),
			)
			continue

		if weather_data:
			frappe.get_doc(
				{
					"doctype": "Weather Log",
					"land_unit": lu.name,
					"date": today,
					"temperature": weather_data.get("temperature"),
					"humidity": weather_data.get("humidity"),
					"wind_speed": weather_data.get("wind_speed"),
					"weather_condition": weather_data.get("weather_condition"),
					"precipitation": weather_data.get("precipitation"),
					"source": "OpenWeatherMap",
				}
			).insert(ignore_permissions=True)

	frappe.db.commit()


# ──────────────────────────────────────────────
# 3. IOT: Public telemetry ingestion endpoint
# ──────────────────────────────────────────────


@frappe.whitelist(allow_guest=True)
def ingest_telemetry(
	sensor_id,
	temperature=None,
	humidity=None,
	soil_moisture=None,
	lux=None,
	battery=None,
):
	"""
	Public API endpoint for IoT sensors to POST telemetry data.
	Endpoint: POST /api/method/agri_connect.api.ingest_telemetry

	No authentication required. Rate limited to 1 reading per sensor per 60 seconds.

	Args:
		sensor_id (str): Required. Alphanumeric sensor identifier.
		temperature (float): Temperature in Celsius.
		humidity (float): Humidity percentage.
		soil_moisture (float): Soil moisture percentage.
		lux (float): Light intensity in Lux.
		battery (float): Battery level percentage.

	Returns:
		dict: {"status": "success", "name": "<document name>"}
	"""
	# --- Input validation ---
	if not sensor_id:
		frappe.throw("sensor_id is required", frappe.ValidationError)

	# Sanitize: allow only alphanumeric, hyphens, underscores
	sensor_id = sensor_id.strip()
	if not re.match(r"^[\w\-]+$", sensor_id):
		frappe.throw("sensor_id contains invalid characters", frappe.ValidationError)

	# Clamp numeric values to sane ranges
	temperature = _clamp_float(temperature, -50, 80)
	humidity = _clamp_float(humidity, 0, 100)
	soil_moisture = _clamp_float(soil_moisture, 0, 100)
	lux = _clamp_float(lux, 0, 200000)
	battery = _clamp_float(battery, 0, 100)

	# --- Rate limiting: 1 reading per sensor per 60 seconds ---
	last_reading = frappe.db.get_value(
		"IoT Sensor Reading",
		{"sensor_id": sensor_id},
		"timestamp",
		order_by="timestamp desc",
	)
	if last_reading:
		seconds_since = time_diff_in_seconds(now_datetime(), last_reading)
		if seconds_since < 60:
			frappe.throw(
				f"Rate limit: sensor {sensor_id} last reported {int(seconds_since)}s ago."
				" Minimum interval: 60s.",
				frappe.ValidationError,
			)

	# --- Lookup Land Unit by exact sensor_id field ---
	land_unit = frappe.db.get_value(
		"Land Unit",
		{"sensor_id": sensor_id},
		"name",
	)
	if not land_unit:
		# Fallback: legacy LIKE match on land_unit_name
		land_unit = frappe.db.get_value(
			"Land Unit",
			{"land_unit_name": ["like", f"%{sensor_id}%"]},
			"name",
		)

	doc = frappe.get_doc(
		{
			"doctype": "IoT Sensor Reading",
			"sensor_id": sensor_id,
			"land_unit": land_unit,
			"temperature": temperature,
			"humidity": humidity,
			"soil_moisture": soil_moisture,
			"light_intensity": lux,
			"battery_level": battery,
		}
	)
	doc.insert(ignore_permissions=True)

	return {"status": "success", "name": doc.name}


def _clamp_float(value, min_val, max_val):
	"""Safely parse and clamp a numeric value. Returns None if not a valid number."""
	if value is None:
		return None
	try:
		value = float(value)
	except (ValueError, TypeError):
		return None
	return max(min_val, min(max_val, value))
