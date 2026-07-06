# STANDARD OPERATING PROCEDURE (SOP)
## Precision Farming — Waste Management & Fertilizer Measurement System

**App Name:** Precision Farming  
**Version:** 1.0.0  
**Module:** Precision Farming  
**Domain:** Agriculture  
**Required Apps:** Frappe v15, ERPNext v15 (Agriculture domain)  
**Last Updated:** July 6, 2026

---

## TABLE OF CONTENTS

1. [Application Overview](#1-application-overview)
2. [System Architecture](#2-system-architecture)
3. [Getting Started](#3-getting-started)
4. [Feature 1: Agriculture Waste Management](#4-feature-1-agriculture-waste-management)
5. [Feature 2: Fertilizer Measurement & Management](#5-feature-2-fertilizer-measurement--management)
6. [Quality Control & Compliance](#6-quality-control--compliance)
7. [Workspace Navigation](#7-workspace-navigation)
8. [Scheduled Tasks & Automation](#8-scheduled-tasks--automation)
9. [Setup & Configuration (Fixtures)](#9-setup--configuration-fixtures)
10. [Demo Data](#10-demo-data)
11. [Fix Utilities](#11-fix-utilities)
12. [Troubleshooting](#12-troubleshooting)
13. [Appendix](#13-appendix)

---

## 1. APPLICATION OVERVIEW

### 1.1 Purpose
Precision Farming is a Frappe/ERPNext application designed for managing agricultural waste and fertilizer measurement. It provides a complete digital workflow for:

- **Agriculture Waste Management** — tracking waste collection, composting, recycling, and disposal
- **Fertilizer Measurement & Management** — soil analysis, nutrient gap calculation, fertilizer recommendation, and application tracking

### 1.2 Key Features
- **30 DocTypes** — 14 master/document DocTypes, 9 child tables, 7 setup masters
- **3 Workflow Sections** — Waste Management (Organic), Inorganic Waste, Fertilizer Management
- **7 Fixtures** — auto-loaded on install (Waste Category, Waste Type, Application Method, etc.)
- **5 Automated Tasks** — daily compliance checks, weekly summaries, monthly reports
- **6 Quick Action Shortcuts** — New Waste Record, Composting Batch, Soil Analysis, Fertilizer Recommendation, Fertilizer Application, Compost Application
- **Role-based Access** — Agriculture Manager (full), Agriculture User (create/read/write)

---

## 2. SYSTEM ARCHITECTURE

### 2.1 Technology Stack
- **Framework:** Frappe v15 / ERPNext v15
- **Database:** MariaDB
- **Python:** 3.11+
- **Automated Tasks:** Frappe Scheduler (daily, weekly, monthly)
- **Dependencies:** ERPNext Agriculture module (for Land Unit, Crop, Crop Cycle DocTypes)

### 2.2 DocType Structure

| # | DocType Name | Type | Card Section | Submittable |
|---|-------------|------|-------------|-------------|
| 1 | Waste Record | Document | Waste Collection | ✅ |
| 2 | Waste Category | Setup Master | Waste Collection | ❌ |
| 3 | Waste Type | Setup Master | Waste Collection | ❌ |
| 4 | Waste Record Item | Child Table | — | ❌ |
| 5 | Composting Batch | Document | Composting | ✅ |
| 6 | Compost Ingredient | Child Table | — | ❌ |
| 7 | Compost Turning Event | Child Table | — | ❌ |
| 8 | Compost Application | Document | Composting | ✅ |
| 9 | Compost Quality Check | Document | Composting | ✅ |
| 10 | Quality Check Result | Child Table | — | ❌ |
| 11 | Compost Quality Parameter | Setup Master | Composting | ❌ |
| 12 | Collection Schedule | Document | Disposal & Recycling | ❌ |
| 13 | Recycling Record | Document | Disposal & Recycling | ❌ |
| 14 | Disposal Record | Document | Disposal & Recycling | ❌ |
| 15 | Compliance Record | Document | Compliance & Records | ❌ |
| 16 | Soil Analysis | Document | Soil & Nutrient Analysis | ✅ |
| 17 | Soil Analysis Result | Child Table | — | ❌ |
| 18 | Nutrient Analysis | Document | Soil & Nutrient Analysis | ❌ |
| 19 | Nutrient Gap | Child Table | — | ❌ |
| 20 | Crop Nutrient Standard | Setup Master | Soil & Nutrient Analysis | ❌ |
| 21 | Fertilizer Recommendation | Document | Fertilizer Planning | ✅ |
| 22 | Recommended Product | Child Table | — | ❌ |
| 23 | Fertilizer Application | Document | Fertilizer Planning | ✅ |
| 24 | Fertilizer Application Item | Child Table | — | ❌ |
| 25 | Fertilizer Schedule | Document | Fertilizer Planning | ❌ |
| 26 | Fertilizer Schedule Item | Child Table | — | ❌ |
| 27 | Fertilizer Product | Setup Master | Fertilizer Planning | ❌ |
| 28 | Application Method | Setup Master | Setup | ❌ |
| 29 | Soil Nutrient Threshold | Setup Master | Setup | ❌ |
| 30 | Measurement Verification | Document | Measurement & Verification | ❌ |

### 2.3 Naming Series Convention

| DocType | Prefix | Format |
|---------|--------|--------|
| Waste Record | WR | WR-.YYYY.-.##### |
| Composting Batch | CB | CB-.YYYY.-.##### |
| Compost Application | CA | CA-.YYYY.-.##### |
| Soil Analysis | SA | SA-.YYYY.-.##### |
| Nutrient Analysis | NA | NA-.YYYY.-.##### |
| Fertilizer Recommendation | FR | FR-.YYYY.-.##### |
| Fertilizer Application | FA | FA-.YYYY.-.##### |
| Fertilizer Schedule | FS | FS-.YYYY.-.##### |
| Recycling Record | RR | RR-.YYYY.-.##### |
| Disposal Record | DR | DR-.YYYY.-.##### |
| Collection Schedule | CS | CS-.YYYY.-.##### |
| Compliance Record | CR | CR-.YYYY.-.##### |
| Measurement Verification | MV | MV-.YYYY.-.##### |

> **Note:** Demo data uses `DEMO-*` names (e.g., `DEMO-WR-001`) instead of auto-generated naming series names to ensure cross-references work correctly on submit.

### 2.4 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WORKFLOW OVERVIEW                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🌿 WASTE MANAGEMENT (Organic)                                      │
│  ┌──────────┐    ┌────────────┐    ┌──────────────┐    ┌─────────┐ │
│  │  Waste   │───▶│ Composting │───▶│  Compost     │───▶│ Compost │ │
│  │  Record  │    │   Batch    │    │ Quality Check│    │ Applic. │ │
│  └──────────┘    └────────────┘    └──────────────┘    └─────────┘ │
│                                                                     │
│  ♻️ INORGANIC WASTE                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │  Waste   │───▶│  Recycling   │───▶│   Disposal   │              │
│  │  Record  │    │    Record    │    │    Record    │              │
│  └──────────┘    └──────────────┘    └──────────────┘              │
│                                                                     │
│  🌾 FERTILIZER MANAGEMENT                                           │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────┐  │
│  │  Soil    │───▶│  Nutrient    │───▶│  Fertilizer  │───▶│ Fert │  │
│  │ Analysis │    │  Analysis    │    │Recommendation│    │Applic│  │
│  └──────────┘    └──────────────┘    └──────────────┘    └──────┘  │
│                                                                     │
│  📋 SUPPORTING                                                      │
│  Collection Schedule → Waste Record → Compliance Record             │
│  Fertilizer Schedule → Measurement Verification                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. GETTING STARTED

### 3.1 Installation
```bash
# From the bench directory
bench get-app https://github.com/Sudhakar1110/Precision_Farming.git
bench --site your-site.com install-app precision_farming
bench --site your-site.com migrate
```

### 3.2 Developer Mode Requirement
Frappe v15 requires **Developer Mode** to be enabled for creating and syncing Standard DocTypes. After installation:

```bash
bench --site your-site.com set-config developer_mode 1
bench --site your-site.com migrate
```

You can disable it afterward if preferred:
```bash
bench --site your-site.com set-config developer_mode 0
```

### 3.3 Role Setup
Two roles are automatically created on install:
1. **Agriculture Manager** — Full access (create, read, write, delete, submit, amend, cancel)
2. **Agriculture User** — Create, read, write (no submit/amend/delete on submittable docs)

### 3.4 Domain Activation
The `Agriculture` domain is automatically activated on install. This enables ERPNext's Agriculture module features (Land Unit, Crop, Crop Cycle).

### 3.5 Initial Configuration
Before using the application, verify these 7 fixture masters are loaded (auto-loaded on install):
1. **Waste Categories** — Organic, Inorganic, Hazardous
2. **Waste Types** — 11 types (Crop Residue, Straw, Weeds, etc.)
3. **Application Methods** — Broadcasting, Banding, Foliar Spray, Drip Irrigation, Side Dressing
4. **Compost Quality Parameters** — Temperature, Moisture Content, C:N Ratio, pH Level
5. **Crop Nutrient Standards** — Paddy, Wheat, Cotton, Corn, Sugarcane, Groundnut
6. **Fertilizer Products** — Urea, DAP, MOP, NPK blends, Compost
7. **Soil Nutrient Thresholds** — N, P, K, pH, Organic Matter

---

## 4. FEATURE 1: AGRICULTURE WASTE MANAGEMENT

### 4.1 Organic Waste Workflow
```
Waste Record → Composting Batch → Compost Quality Check → Compost Application
```

#### Step 1: Waste Record (Collection)
1. Navigate to **Waste Collection** card → **Waste Record**
2. Click **+ Add Waste Record**
3. Fill required fields:
   - **Land Unit** — Link to Land Unit (from ERPNext Agriculture)
   - **Collection Date** — Date of waste collection
   - **Location** — Source location description
4. In the **Waste Items** table, add items:
   - **Waste Type** — Select from Waste Type (e.g., Crop Residue, Weeds)
   - **Quantity (kg)** — Weight of each waste type
   - **Source** — Crop Residue, Weeding, Pruning, etc.
5. Read-only fields auto-calculate:
   - **Total Organic Weight (kg)**
   - **Total Inorganic Weight (kg)**
   - **Total Weight (kg)**
   - **Classification Status** — Pending → Classified → Processing → Completed
   - **Waste Category Type** — Organic / Inorganic / Mixed
6. **Submit** to lock the record

#### Step 2: Composting Batch
1. Navigate to **Composting** card → **Composting Batch**
2. Click **+ New Composting Batch**
3. Fill required fields:
   - **Start Date** — When composting begins
   - **Status** — Active / Turning / Curing / Ready / Approved / Rejected
4. Optional fields:
   - **Source Waste Record** — Link to Waste Record
   - **Land Unit** — Link to Land Unit
   - **Batch Name** — Custom label
   - **Composting Method** — Aerobic / Anaerobic / Vermicomposting / Windrow
5. Add **Ingredients** (child table):
   - Waste Type, Quantity (kg), C:N Ratio
6. Track **Turning Events** (child table):
   - Turning Date, Temperature (°C), Moisture (%)
7. Read-only fields:
   - **Total Input (kg)** — Sum of ingredient quantities
   - **Quality Check Passed** — Updated from Compost Quality Check
8. **Submit** to lock

#### Step 3: Compost Quality Check
1. From **Composting** card → **Compost Quality Check**
2. Click **+ New Compost Quality Check**
3. Required fields:
   - **Composting Batch** — Link to the batch being tested
   - **Check Date**
4. Add **Results** (child table):
   - **Parameter** — Select from Compost Quality Parameter
   - **Measured Value** — Test reading
   - Read-only: Acceptable Min/Max, Unit, Pass/Fail status
5. Read-only: **Overall Result** — Pass / Fail / Conditional Pass
6. Optional: Approval section (Approved, Approved By, Approval Date)
7. **Submit** to lock

#### Step 4: Compost Application
1. From **Composting** card → **Compost Application**
2. Click **+ New Compost Application**
3. Required fields:
   - **Composting Batch** — Link to completed batch
   - **Land Unit** — Target field
   - **Application Date**
   - **Quantity Applied (kg)**
4. Optional: **Application Method** — Broadcasting / Banding / Incorporate / Top Dressing
5. **Submit** to lock (status auto-set to "Applied")

### 4.2 Inorganic Waste Workflow
```
Waste Record → Recycling Record  OR  Waste Record → Disposal Record
```

#### Step 5: Recycling Record
1. From **Disposal & Recycling** card → **Recycling Record**
2. Select **Source Waste Record** (optional link)
3. Required: **Recycling Date**, **Quantity (kg)**, **Status**
4. Optional: **Material Type** (Plastic/Metal/Glass/Paper/Fabric/Mixed/Other)
5. Optional: **Recycler / Facility Name**, **Recycling Certificate**
6. Save

#### Step 6: Disposal Record
1. From **Disposal & Recycling** card → **Disposal Record**
2. Required: **Disposal Date**, **Quantity (kg)**
3. Optional: **Source Waste Record**, **Disposal Method** (Landfill/Incineration/Treatment/Other)
4. Optional: **Disposal Facility**, **Hazardous Waste** (checkbox), **Disposal Cost**
5. **Compliance Status** — Compliant / Non-Compliant / Pending Review
6. Save

### 4.3 Collection Schedule & Compliance

#### Collection Schedule
1. From **Disposal & Recycling** card → **Collection Schedule**
2. Required: **Land Unit**, **Scheduled Date**, **Status** (Pending/In Progress/Completed/Cancelled)
3. Optional: **Assigned To** (User), **Notes**
4. Save

#### Compliance Record
1. From **Compliance & Records** card → **Compliance Record**
2. Required: **Compliance Date**, **Status** (Compliant/Non-Compliant/Pending/Expired)
3. Optional: **Waste Record** (link), **Regulation Type** (Environmental/Safety/Transport/Disposal/Recycling)
4. Optional: **Authority Name**, **Certificate Reference**, **Valid Until**
5. Save

---

## 5. FEATURE 2: FERTILIZER MEASUREMENT & MANAGEMENT

### 5.1 Workflow
```
Soil Analysis → Nutrient Analysis → Fertilizer Recommendation → Fertilizer Application
```
Plus supporting: Fertilizer Schedule (planning), Measurement Verification (quality assurance)

#### Step 1: Soil Analysis
1. Navigate to **Soil & Nutrient Analysis** card → **Soil Analysis**
2. Click **+ New Soil Analysis**
3. Required fields:
   - **Land Unit** — Target field
   - **Analysis Date**
4. Optional: **Lab Name**, **Sample Depth (cm)**
5. Add **Soil Analysis Results** (child table):
   - **Nutrient** — Select from Soil Nutrient Threshold (N, P, K, pH, Organic Matter)
   - **Value** — Test reading
   - **Unit** — Auto-filled from threshold
   - Read-only: **Status** — Low / Medium / High (based on thresholds)
6. Read-only summary fields: **Nitrogen (N) Status**, **Phosphorus (P) Status**, **Potassium (K) Status**
7. Optional: **pH Level**, **EC (dS/m)**, **Organic Matter (%)**
8. **Submit** to lock

#### Step 2: Nutrient Analysis
1. From **Soil & Nutrient Analysis** card → **Nutrient Analysis**
2. Required fields:
   - **Land Unit**
   - **Area (hectare)**
   - **Crop Nutrient Standard** — Select standard (Paddy, Wheat, etc.)
   - **Analysis Date**
3. Optional: **Soil Analysis Reference** (link), **Growth Stage**, **Crop** (ERPNext Crop)
4. Read-only auto-calculated fields:
   - **Crop Requirement section**: Total N/P/K Required (kg)
   - **Soil Available section**: Soil N/P/K Available (kg)
   - **Compost Contribution section**: N/P/K from Compost (kg)
5. **Nutrient Gap** child table (read-only):
   - Lists N, P, K with: Crop Requirement, Soil Available, Compost Contribution, Gap to Fill
6. Read-only result fields: **N Gap (kg)**, **P Gap (kg)**, **K Gap (kg)**
7. Save

#### Step 3: Fertilizer Recommendation
1. Navigate to **Fertilizer Planning** card → **Fertilizer Recommendation**
2. Required fields:
   - **Land Unit**
   - **Nutrient Analysis** — Link to the analysis
   - **Recommendation Date**
   - **Status** — Draft / Approved / Applied / Cancelled
3. Optional: **Crop** (link), **Notes**
4. Add **Recommended Products** (child table):
   - **Fertilizer Product** — Select from Fertilizer Product
   - **Target Nutrient** — Nitrogen/Phosphorus/Potassium/Mixed
   - **Gap to Fill (kg)**
   - **Product Quantity (kg)** — Required
   - **Estimated Cost** — Currency
5. Read-only summary: **Total N/P/K to Apply (kg)**, **Estimated Cost**
6. **Submit** to lock (status cannot be Draft after submission)

#### Step 4: Fertilizer Application
1. From **Fertilizer Planning** card → **Fertilizer Application**
2. Required fields:
   - **Fertilizer Recommendation** — Link to approved recommendation
   - **Land Unit**
   - **Application Date**
3. Optional: **Application Method** (Link to Application Method), **Crop**
4. Add **Applied Products** (child table):
   - **Fertilizer Product** — Required
   - **Quantity (kg)** — Required
   - Read-only: **Target Nutrient**, **N/P Applied (kg)**
5. Read-only: **Total Quantity (kg)**, **Status** (Draft/Applied/Cancelled)
6. **Submit** to lock (status auto-set to "Applied")

#### Step 5: Fertilizer Schedule (Planning)
1. From **Fertilizer Planning** card → **Fertilizer Schedule**
2. Required: **Land Unit**
3. Optional: **Start Date**, **End Date**, **Status** (Planned/In Progress/Completed/Cancelled)
4. Add **Schedule Items** (child table):
   - **Planned Date** — Required
   - **Product** (Link to Fertilizer Product)
   - **Quantity (kg)**
   - **Application Method** (Link)
   - **Status** (Pending/Completed/Skipped)
   - **Actual Application** — Link to Fertilizer Application (after completion)
5. Save

#### Step 6: Measurement Verification
1. Navigate to **Measurement & Verification** card → **Measurement Verification**
2. Required fields:
   - **Land Unit**
   - **Verification Date**
   - **Expected Quantity (kg)**
3. Optional: **Crop**, **Actual Quantity (kg)**, **Verified By** (User)
4. Read-only: **Deviation (%)** — Auto-calculated
5. **Status** — Pending / Verified / Needs Adjustment
6. Save

---

## 6. QUALITY CONTROL & COMPLIANCE

### 6.1 Compliance Records
- Track regulatory compliance for waste management and fertilizer usage
- **Regulation Types:** Environmental, Safety, Transport, Disposal, Recycling
- Set validity periods with **Valid Until** date
- System auto-expires records via daily scheduled task (`check_compliance_expiry`)
- Status values: Compliant, Non-Compliant, Pending, Expired

### 6.2 Compost Quality Control
- Define quality parameters with acceptable ranges (min/max)
- Test results auto-calculate Pass/Fail status per parameter
- Overall result (Pass/Fail/Conditional Pass) is read-only
- Approval workflow for quality sign-off

### 6.3 Measurement Verification
- Record field measurements for fertilizer/compost application accuracy
- Compare **Expected Quantity (kg)** vs **Actual Quantity (kg)**
- Deviation percentage auto-calculated
- Status: Pending → Verified / Needs Adjustment

---

## 7. WORKSPACE NAVIGATION

### 7.1 Workspace Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WORKFLOW OVERVIEW                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 🌿 Waste Management          ♻️ Inorganic Waste      🌾 Fertilizer  │
│                              │                       Management    │
│ Waste Collection →           Waste Collection →      Soil Test →   │
│ Composting →                 Recycling →             NPK Analysis →│
│ Field Application            Disposal                Recommendation→│
│                                                       Application   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                AGRICULTURE WASTE MANAGEMENT                         │
├──────────────┬──────────────┬──────────────┬───────────────────────┤
│ Waste        │ Composting   │ Disposal &   │ Compliance &          │
│ Collection   │              │ Recycling    │ Records               │
│              │              │              │                       │
│ • Waste      │ • Composting │ • Collection  │ • Compliance Record   │
│   Record     │   Batch      │   Schedule   │                       │
│ • Waste      │ • Compost    │ • Recycling  │                       │
│   Category   │   Application│   Record     │                       │
│ • Waste Type │ • Compost    │ • Disposal   │                       │
│              │   Quality    │   Record     │                       │
│              │   Check      │              │                       │
│              │ • Compost    │              │                       │
│              │   Quality    │              │                       │
│              │   Parameter  │              │                       │
└──────────────┴──────────────┴──────────────┴───────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                FERTILIZER MEASUREMENT                               │
├──────────────┬──────────────┬──────────────┬───────────────────────┤
│ Soil &       │ Fertilizer   │ Setup        │ Measurement &         │
│ Nutrient     │ Planning     │              │ Verification          │
│ Analysis     │              │              │                       │
│              │              │              │                       │
│ • Soil       │ • Fertilizer │ • Application│ • Measurement         │
│   Analysis   │   Recommend  │   Method     │   Verification        │
│ • Nutrient   │ • Fertilizer │ • Soil       │                       │
│   Analysis   │   Applic.    │   Nutrient   │                       │
│ • Crop       │ • Fertilizer │   Threshold  │                       │
│   Nutrient   │   Schedule   │              │                       │
│   Standard   │ • Fertilizer │              │                       │
│              │   Product    │              │                       │
└──────────────┴──────────────┴──────────────┴───────────────────────┘
```

### 7.2 Quick Action Shortcuts

| Shortcut | Action | Icon | Color |
|----------|--------|------|-------|
| New Waste Record | Opens Waste Record form | list | Green |
| New Composting Batch | Opens Composting Batch form | branch | Blue |
| New Soil Analysis | Opens Soil Analysis form | healthcare | Orange |
| New Fertilizer Recommendation | Opens Fertilizer Recommendation form | clipboard | Purple |
| New Fertilizer Application | Opens Fertilizer Application form | agriculture | Teal |
| New Compost Application | Opens Compost Application form | leaf | Dark Green |

### 7.3 Card Sections & Links

| Section | Card | DocTypes |
|---------|------|----------|
| Agriculture Waste Management | Waste Collection | Waste Record, Waste Category, Waste Type |
| Agriculture Waste Management | Composting | Composting Batch, Compost Application, Compost Quality Check, Compost Quality Parameter |
| Agriculture Waste Management | Disposal & Recycling | Collection Schedule, Recycling Record, Disposal Record |
| Agriculture Waste Management | Compliance & Records | Compliance Record |
| Fertilizer Measurement | Soil & Nutrient Analysis | Soil Analysis, Nutrient Analysis, Crop Nutrient Standard |
| Fertilizer Measurement | Fertilizer Planning | Fertilizer Recommendation, Fertilizer Application, Fertilizer Schedule, Fertilizer Product |
| Fertilizer Measurement | Setup | Application Method, Soil Nutrient Threshold |
| Fertilizer Measurement | Measurement & Verification | Measurement Verification |

---

## 8. SCHEDULED TASKS & AUTOMATION

### 8.1 Daily Tasks

| Task | Function | Description |
|------|----------|-------------|
| Check Compliance Expiry | `check_compliance_expiry()` | Marks expired compliance records as "Expired" where `valid_until < today()` and status is not already "Expired" |
| Send Application Reminders | `send_application_reminders()` | Creates ToDo for Fertilizer Recommendations with status "Approved" and `modified > 7 days` |

### 8.2 Weekly Tasks (runs every Monday)

| Task | Function | Description |
|------|----------|-------------|
| Generate Waste Summary | `generate_waste_summary()` | Queries submitted Waste Records from the last 7 days. Creates a Notification Log with total organic, inorganic, and overall weight collected |
| Generate Fertilizer Report | `generate_fertilizer_report()` | Queries submitted Fertilizer Applications from the last 7 days. Creates a Notification Log with total quantity applied and number of applications |

### 8.3 Monthly Tasks (runs 1st of month)

| Task | Function | Description |
|------|----------|-------------|
| Generate Nutrient Balance Report | `generate_nutrient_balance_report()` | Queries Nutrient Analysis records from the last 30 days. Creates a Notification Log with total N, P, K gaps across all analyses |

### 8.4 Error Handling
All scheduled tasks have try/except blocks and log errors via `frappe.log_error()` to the Error Log doctype.

---

## 9. SETUP & CONFIGURATION (FIXTURES)

All 7 fixtures are auto-loaded on install (via `hooks.py` `fixtures` array). They are also re-synced on `bench migrate`.

### 9.1 Waste Categories

| Name | Type | Default Disposal Method | Description |
|------|------|------------------------|-------------|
| Organic Waste | Organic | Composting | Biodegradable waste (crop residue, straw, weeds, manure) |
| Inorganic Waste | Inorganic | Recycling | Non-biodegradable materials (bags, containers, plastics) |
| Hazardous Waste | Hazardous | Landfill | Hazardous materials requiring special handling |

### 9.2 Waste Types

| Name | Category | Biodegradable | Recyclable | Hazardous |
|------|----------|:---:|:---:|:---:|
| Crop Residue | Organic Waste | ✅ | ❌ | ❌ |
| Straw | Organic Waste | ✅ | ❌ | ❌ |
| Weeds | Organic Waste | ✅ | ❌ | ❌ |
| Dry Leaves | Organic Waste | ✅ | ❌ | ❌ |
| Fruit & Vegetable Waste | Organic Waste | ✅ | ❌ | ❌ |
| Animal Manure | Organic Waste | ✅ | ❌ | ❌ |
| Empty Fertilizer Bags | Inorganic Waste | ❌ | ✅ | ❌ |
| Pesticide Containers | Inorganic Waste | ❌ | ✅ | ✅ |
| Plastic Mulch Sheets | Inorganic Waste | ❌ | ✅ | ❌ |
| Irrigation Pipes | Inorganic Waste | ❌ | ✅ | ❌ |
| Packaging Materials | Inorganic Waste | ❌ | ✅ | ❌ |

### 9.3 Application Methods

| Method | Efficiency | Description |
|--------|:----------:|-------------|
| Broadcasting | 70% | Evenly spreading over the entire field surface |
| Banding | 85% | Applying in bands near the seed or plant row |
| Foliar Spray | 90% | Applying liquid fertilizer directly to plant leaves |
| Drip Irrigation | 95% | Fertigation through drip irrigation system |
| Side Dressing | 80% | Applying alongside growing plants |

### 9.4 Compost Quality Parameters

| Parameter | Acceptable Range | Unit |
|-----------|:----------------:|:----:|
| Temperature | 40 – 70 | °C |
| Moisture Content | 40 – 60 | % |
| Carbon to Nitrogen Ratio | 20 – 40 | Ratio |
| pH Level | 6.0 – 8.0 | pH |

### 9.5 Crop Nutrient Standards

| Crop | N (kg/ha) | P (kg/ha) | K (kg/ha) |
|------|:---------:|:---------:|:---------:|
| Paddy (Rice) | 120 | 60 | 60 |
| Wheat | 140 | 60 | 50 |
| Cotton | 100 | 50 | 50 |
| Corn (Maize) | 150 | 70 | 80 |
| Sugarcane | 200 | 100 | 120 |
| Groundnut | 30 | 60 | 50 |

### 9.6 Fertilizer Products

| Product | Type | N (%) | P (%) | K (%) |
|---------|:----:|:-----:|:-----:|:-----:|
| Urea (46% N) | Chemical | 46 | 0 | 0 |
| DAP (18-46-0) | Chemical | 18 | 46 | 0 |
| MOP (0-0-60) | Chemical | 0 | 0 | 60 |
| NPK 10-26-26 | Chemical | 10 | 26 | 26 |
| NPK 20-20-0 | Chemical | 20 | 20 | 0 |
| Compost (Farm-made) | Organic | 1.5 | 0.5 | 1.0 |

### 9.7 Soil Nutrient Thresholds

| Nutrient | Low | Medium | High | Unit |
|----------|:---:|:------:|:----:|:----:|
| Nitrogen (N) | < 50 | 50 – 100 | 100 – 200 | kg/ha |
| Phosphorus (P) | < 20 | 20 – 50 | 50 – 100 | kg/ha |
| Potassium (K) | < 100 | 100 – 200 | 200 – 300 | kg/ha |
| pH Level | < 5.5 | 5.5 – 6.5 | 6.5 – 7.5 | pH |
| Organic Matter | < 0.5 | 0.5 – 1.5 | 1.5 – 3.0 | % |

---

## 10. DEMO DATA

The application includes a comprehensive demo data script that creates 14 interconnected records for testing.

### 10.1 Records Created

| # | DocType | Record Name | Links To |
|---|---------|-------------|----------|
| 1 | Land Unit | Demo Farm | — |
| 2 | Waste Record | DEMO-WR-001 | Demo Farm |
| 3 | Composting Batch | DEMO-CB-001 | DEMO-WR-001, Demo Farm |
| 4 | Compost Quality Check | DEMO-CQ-001 | DEMO-CB-001 |
| 5 | Compost Application | DEMO-CA-001 | DEMO-CB-001, Demo Farm |
| 6 | Soil Analysis | DEMO-SA-001 | Demo Farm |
| 7 | Nutrient Analysis | DEMO-NA-001 | DEMO-SA-001, Demo Farm |
| 8 | Fertilizer Recommendation | DEMO-FR-001 | DEMO-NA-001, Demo Farm |
| 9 | Fertilizer Application | DEMO-FA-001 | DEMO-FR-001, Demo Farm |
| 10 | Fertilizer Schedule | DEMO-FS-001 | Demo Farm |
| 11 | Recycling Record | DEMO-RR-001 | DEMO-WR-001 |
| 12 | Disposal Record | DEMO-DR-001 | DEMO-WR-001 |
| 13 | Collection Schedule | DEMO-CS-001 | Demo Farm |
| 14 | Compliance Record | DEMO-CR-001 | DEMO-WR-001 |
| 15 | Measurement Verification | DEMO-MV-001 | Demo Farm |

### 10.2 Run Demo Data

```bash
cd ~/frappe-bench-v15
bench --site your-site.com execute precision_farming.demo.create_demo_data
```

The script is idempotent — it checks if each record already exists and skips duplicates. Records use `DEMO-*` names (not auto-generated naming series) so cross-references resolve correctly on submit.

### 10.3 Demo Data Naming Convention

All demo records use the naming pattern `DEMO-{PREFIX}-{NNN}`:

| DocType | Demo Name |
|---------|-----------|
| Land Unit | Demo Farm |
| Waste Record | DEMO-WR-001 |
| Composting Batch | DEMO-CB-001 |
| Compost Quality Check | DEMO-CQ-001 |
| Compost Application | DEMO-CA-001 |
| Soil Analysis | DEMO-SA-001 |
| Nutrient Analysis | DEMO-NA-001 |
| Fertilizer Recommendation | DEMO-FR-001 |
| Fertilizer Application | DEMO-FA-001 |
| Fertilizer Schedule | DEMO-FS-001 |
| Recycling Record | DEMO-RR-001 |
| Disposal Record | DEMO-DR-001 |
| Collection Schedule | DEMO-CS-001 |
| Compliance Record | DEMO-CR-001 |
| Measurement Verification | DEMO-MV-001 |

---

## 11. FIX UTILITIES

The application includes a `fix_workspace.py` utility with three fix functions to resolve common server-side issues.

### 11.1 Fix Workspace (Restore all 3 workflow sections)

If the workspace shows only Fertilizer Management (missing Waste Management and Inorganic Waste sections):

```bash
cd ~/frappe-bench-v15
bench --site your-site.com execute precision_farming.fix_workspace.fix
bench --site your-site.com clear-cache
bench restart
```

This restores the workspace `content` field with all 3 workflow sections, 8 cards, and ensures `is_public=1`, `is_hidden=0`.

### 11.2 Create Land Unit (Fix "Could not find Land Unit: Demo Farm" error)

If submitting documents fails with "Could not find Land Unit: Demo Farm":

```bash
cd ~/frappe-bench-v15
bench --site your-site.com execute precision_farming.fix_workspace.create_land_unit
bench --site your-site.com clear-cache
bench restart
```

This checks if Land Unit "Demo Farm" exists, renames it from auto-generated names (like `LU-Demo Farm`) if needed, or creates a new one.

### 11.3 Fix All References (Rename auto-generated names to DEMO-*)

If submitting documents fails with "Could not find [DocType]: DEMO-XXX":

```bash
cd ~/frappe-bench-v15
bench --site your-site.com execute precision_farming.fix_workspace.fix_all_references
bench --site your-site.com clear-cache
bench restart
```

The demo data script may have created records with auto-generated names (e.g., `FR-2026-00001`) while link fields reference `DEMO-FR-001`. This utility renames all records so cross-references resolve correctly on submit.

### 11.4 All Fixes in Sequence (New Installation)

For a fresh site with demo data issues, run in order:

```bash
# 1. Fix workspace layout
bench --site your-site.com execute precision_farming.fix_workspace.fix

# 2. Fix Land Unit name
bench --site your-site.com execute precision_farming.fix_workspace.create_land_unit

# 3. Fix all demo record names
bench --site your-site.com execute precision_farming.fix_workspace.fix_all_references

# 4. Clear cache and restart
bench --site your-site.com clear-cache
bench restart
```

---

## 12. TROUBLESHOOTING

### 12.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| App not found during install | App not in apps.txt | `echo "precision_farming" >> sites/apps.txt` |
| Module not found error | Module name mismatch | Ensure `modules.txt` = "Precision Farming" |
| Workspace shows only Fertilizer section | Content field corrupted on server | Run `bench execute precision_farming.fix_workspace.fix` |
| "Could not find Land Unit: Demo Farm" on submit | Land Unit name mismatch | Run `bench execute precision_farming.fix_workspace.create_land_unit` |
| "Could not find [DocType]: DEMO-XXX" on submit | Auto-generated name vs DEMO-* name | Run `bench execute precision_farming.fix_workspace.fix_all_references` |
| Workspace not showing in module list | Private workspace | Set `"is_public": 1` in the workspace JSON, run `bench migrate` then `bench clear-cache` |
| DocTypes not created during migrate | Developer Mode is off | Enable with `bench --site site set-config developer_mode 1` then re-run `bench migrate` |
| Workspace Public checkbox greyed out | Expected for standard workspaces | Edit `precision_farming.json` directly — set `"is_public": 1` |
| Scheduled tasks not running | Scheduler disabled | Enable with `bench --site site scheduler enable` |
| Role permission issues | Roles not created | Run `bench console` then `frappe.get_doc("Precision Farming", "install").after_install()` |
| Fixture data not loading | Fixtures not synced | Run `bench --site site migrate` |

### 12.2 Force Sync DocTypes (if missing)
```bash
bench --site your-site.com console
```
```python
from frappe.model.sync import sync_for
sync_for("precision_farming")
frappe.db.commit()
exit()
```

### 12.3 Force Sync Workspace (if workspace changes not appearing)
```bash
bench --site your-site.com console
```
```python
from frappe.modules.import_file import import_file_by_path
import_file_by_path(frappe.get_app_path('precision_farming','workspace','precision_farming','precision_farming.json'), force=True)
frappe.db.commit()
exit()
```

Then:
```bash
bench --site your-site.com clear-cache
bench restart
```

### 12.4 Full Re-install (Last Resort)
```bash
bench --site your-site.com uninstall-app precision_farming
bench --site your-site.com install-app precision_farming
bench --site your-site.com migrate
bench --site your-site.com clear-cache
```

### 12.5 Clear Cache
```bash
bench --site your-site.com clear-cache
bench restart
```

---

## 13. APPENDIX

### A. Role Permissions

| Role | Waste Mgmt | Fertilizer | Compliance | Setup | Submit/Amend |
|------|:-----------:|:----------:|:----------:|:-----:|:------------:|
| Agriculture Manager | Full Access | Full Access | Full Access | Full Access | ✅ |
| Agriculture User | Create, Read, Write | Create, Read, Write | Read | Read | ❌ |
| System Manager | Full Access | Full Access | Full Access | Full Access | ✅ |

> **Note:** Agriculture User cannot submit or amend submittable DocTypes (Waste Record, Composting Batch, Compost Application, Compost Quality Check, Soil Analysis, Fertilizer Recommendation, Fertilizer Application).

### B. DocType Field Reference

#### Waste Record
| Field | Type | Required | Read-only |
|-------|:----:|:--------:|:---------:|
| Land Unit | Link → Land Unit | ✅ | ❌ |
| Collection Date | Date | ✅ | ❌ |
| Location | Small Text | ❌ | ❌ |
| Waste Items | Table → Waste Record Item | ✅ | ❌ |
| Total Organic Weight (kg) | Float | ❌ | ✅ |
| Total Inorganic Weight (kg) | Float | ❌ | ✅ |
| Total Weight (kg) | Float | ❌ | ✅ |
| Classification Status | Select | ❌ | ✅ |
| Waste Category Type | Select (Organic/Inorganic/Mixed) | ❌ | ✅ |
| Composting Batch | Link → Composting Batch | ❌ | ✅ |
| Recycling Record | Link → Recycling Record | ❌ | ✅ |
| Disposal Record | Link → Disposal Record | ❌ | ✅ |

#### Composting Batch
| Field | Type | Required | Read-only |
|-------|:----:|:--------:|:---------:|
| Source Waste Record | Link → Waste Record | ❌ | ❌ |
| Land Unit | Link → Land Unit | ❌ | ❌ |
| Start Date | Date | ✅ | ❌ |
| Status | Select (Active/Turning/Curing/Ready/Approved/Rejected) | ✅ | ❌ |
| Composting Method | Select (Aerobic/Anaerobic/Vermicomposting/Windrow) | ❌ | ❌ |
| Total Input (kg) | Float | ❌ | ✅ |
| Ingredients | Table → Compost Ingredient | ❌ | ❌ |
| Turning Events | Table → Compost Turning Event | ❌ | ❌ |
| Quality Check Passed | Check | ❌ | ✅ |
| Output Quantity (kg) | Float | ❌ | ❌ |
| Final Quality Rating | Select (Excellent/Good/Average/Poor) | ❌ | ❌ |
| Compost Quality Check | Link → Compost Quality Check | ❌ | ✅ |

#### Fertilizer Recommendation
| Field | Type | Required | Read-only |
|-------|:----:|:--------:|:---------:|
| Land Unit | Link → Land Unit | ✅ | ❌ |
| Nutrient Analysis | Link → Nutrient Analysis | ✅ | ❌ |
| Area (hectare) | Float | ❌ | ✅ |
| Recommended Products | Table → Recommended Product | ❌ | ❌ |
| Total N/P/K to Apply (kg) | Float | ❌ | ✅ |
| Estimated Cost | Currency | ❌ | ✅ |
| Recommendation Date | Date | ✅ | ❌ |
| Status | Select (Draft/Approved/Applied/Cancelled) | ✅ | ❌ |
| Approved By | Link → User | ❌ | ✅ |

#### Measurement Verification
| Field | Type | Required | Read-only |
|-------|:----:|:--------:|:---------:|
| Land Unit | Link → Land Unit | ✅ | ❌ |
| Verification Date | Date | ✅ | ❌ |
| Expected Quantity (kg) | Float | ✅ | ❌ |
| Actual Quantity (kg) | Float | ❌ | ❌ |
| Deviation (%) | Percent | ❌ | ✅ |
| Status | Select (Pending/Verified/Needs Adjustment) | ❌ | ❌ |

### C. Related Documents
- Frappe Framework Documentation: https://frappeframework.com/docs
- ERPNext Agriculture Module: https://docs.erpnext.com/docs/user/manual/en/agriculture

### D. Repository
- **Repository:** https://github.com/Sudhakar1110/Precision_Farming.git
- **Maintainer:** Precision Farming Solutions
- **Contact:** admin@precisionfarming.com

---

*End of SOP Document*
