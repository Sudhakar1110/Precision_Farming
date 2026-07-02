import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.api import _clamp_float, fetch_weather_data
from agri_connect.tests.test_fixtures import make_land_unit


class TestWeather(FrappeTestCase):
	def test_clamp_float_normal(self):
		"""Test _clamp_float with valid values."""
		self.assertEqual(_clamp_float(25, -50, 80), 25)
		self.assertEqual(_clamp_float("50.5", 0, 100), 50.5)

	def test_clamp_float_clamping(self):
		"""Test _clamp_float clamps out-of-range values."""
		self.assertEqual(_clamp_float(100, -50, 80), 80)
		self.assertEqual(_clamp_float(-100, -50, 80), -50)

	def test_clamp_float_none(self):
		"""Test _clamp_float returns None for None input."""
		self.assertIsNone(_clamp_float(None, 0, 100))

	def test_clamp_float_invalid(self):
		"""Test _clamp_float returns None for invalid input."""
		self.assertIsNone(_clamp_float("abc", 0, 100))

	def test_fetch_weather_no_coordinates(self):
		"""Test fetch_weather_data returns None when no GPS coordinates."""
		lu = make_land_unit("No GPS Farm")
		result = fetch_weather_data(lu.name)
		self.assertIsNone(result)

	def test_ingest_telemetry_valid(self):
		"""Test ingest_telemetry with valid sensor data."""
		from agri_connect.api import ingest_telemetry
		result = ingest_telemetry(
			sensor_id="TEST-SENSOR-001",
			temperature=25.5,
			humidity=60,
		)
		self.assertEqual(result["status"], "success")
		self.assertTrue(result["name"])

		# Verify the IoT Sensor Reading was created
		doc = frappe.get_doc("IoT Sensor Reading", result["name"])
		self.assertEqual(doc.sensor_id, "TEST-SENSOR-001")
		self.assertEqual(doc.temperature, 25.5)
		self.assertEqual(doc.humidity, 60)

	def test_ingest_telemetry_invalid_sensor_id(self):
		"""Test that invalid sensor_id is rejected."""
		from agri_connect.api import ingest_telemetry
		with self.assertRaises(frappe.ValidationError):
			ingest_telemetry(sensor_id="'; DROP TABLE--")

	def test_ingest_telemetry_rate_limit(self):
		"""Test rate limiting (1 per sensor per 60s)."""
		from agri_connect.api import ingest_telemetry
		# First call should succeed
		result = ingest_telemetry(sensor_id="RATE-LIMIT-SENSOR", temperature=20)
		self.assertEqual(result["status"], "success")

		# Second call within 60s should be rate limited
		with self.assertRaises(frappe.ValidationError):
			ingest_telemetry(sensor_id="RATE-LIMIT-SENSOR", temperature=21)

	def test_ingest_telemetry_clamping(self):
		"""Test that values are clamped to valid ranges."""
		from agri_connect.api import ingest_telemetry
		result = ingest_telemetry(
			sensor_id="CLAMP-SENSOR",
			temperature=999,  # max 80
			humidity=-50,  # min 0
		)
		doc = frappe.get_doc("IoT Sensor Reading", result["name"])
		self.assertEqual(doc.temperature, 80)
		self.assertEqual(doc.humidity, 0)
