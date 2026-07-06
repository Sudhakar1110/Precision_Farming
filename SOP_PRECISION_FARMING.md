# STANDARD OPERATING PROCEDURE (SOP)
## Precision Farming — Waste Management & Fertilizer Measurement System

**App Name:** Precision Farming  
**Version:** 0.0.1  
**Module:** Precision Farming  
**Domain:** Agriculture  
**Last Updated:** July 5, 2026

---

## TABLE OF CONTENTS

1. [Application Overview](#1-application-overview)
2. [System Architecture](#2-system-architecture)
3. [Getting Started](#3-getting-started)
4. [Feature 1: Agriculture Waste Management](#4-feature-1-agriculture-waste-management)
5. [Feature 2: Fertilizer Measurement](#5-feature-2-fertilizer-measurement)
6. [Quality Control & Compliance](#6-quality-control--compliance)
7. [Workspace Navigation](#7-workspace-navigation)
8. [Scheduled Tasks & Automation](#8-scheduled-tasks--automation)
9. [Setup & Configuration](#9-setup--configuration)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. APPLICATION OVERVIEW

### 1.1 Purpose
Precision Farming is a Frappe/ERPNext application designed for managing agricultural waste and fertilizer measurement. It provides a complete digital workflow for:

- **Agriculture Waste Management** — tracking waste collection, composting, recycling, and disposal
- **Fertilizer Measurement & Management** — soil analysis, nutrient gap calculation, fertilizer recommendation, and application tracking

### 1.2 Key Features
- 30 DocTypes across 2 dedicated modules for complete waste and fertilizer lifecycle management
- Automated compliance expiry checks
- Weekly waste summary and fertilizer reports
- Monthly nutrient balance reports
- Application reminders for pending fertilizer tasks
- Role-based access (Agriculture Manager, Agriculture User)

---

## 2. SYSTEM ARCHITECTURE

### 2.1 Technology Stack
- **Framework:** Frappe v15 / ERPNext v15
- **Database:** MariaDB
- **Python:** 3.11+
- **Automated Tasks:** Frappe Scheduler (daily, weekly, monthly)

### 2.2 DocType Structure

| # | DocType Name | Type | Belongs To |
|---|-------------|------|------------|
### 2.2 DocType Structure

| # | DocType Name | Type | Belongs To |
|---|-------------|------|------------|
| 1 | Waste Record | Document | Waste Collection |
| 2 | Waste Category | Setup Master | Waste Collection |
| 3 | Waste Type | Setup Master | Waste Collection |
| 4 | Waste Record Item | Child Table | Waste Record |
| 5 | Composting Batch | Document | Composting |
| 6 | Compost Ingredient | Child Table | Composting Batch |
| 7 | Compost Turning Event | Child Table | Composting Batch |
| 8 | Compost Application | Document | Composting |
| 9 | Compost Quality Check | Document | Composting |
| 10 | Quality Check Result | Child Table | Compost Quality Check |
| 11 | Compost Quality Parameter | Setup Master | Composting |
| 12 | Collection Schedule | Document | Disposal & Recycling |
| 13 | Recycling Record | Document | Disposal & Recycling |
| 14 | Disposal Record | Document | Disposal & Recycling |
| 15 | Compliance Record | Document | Compliance |
| 16 | Soil Analysis | Document | Soil & Nutrient Analysis |
| 17 | Soil Analysis Result | Child Table | Soil Analysis |
| 18 | Nutrient Analysis | Document | Soil & Nutrient Analysis |
| 19 | Nutrient Gap | Child Table | Nutrient Analysis |
| 20 | Crop Nutrient Standard | Setup Master | Soil & Nutrient Analysis |
| 21 | Fertilizer Recommendation | Document | Fertilizer Planning |
| 22 | Recommended Product | Child Table | Fertilizer Recommendation |
| 23 | Fertilizer Application | Document | Fertilizer Planning |
| 24 | Fertilizer Application Item | Child Table | Fertilizer Application |
| 25 | Fertilizer Schedule | Document | Fertilizer Planning |
| 26 | Fertilizer Schedule Item | Child Table | Fertilizer Schedule |
| 27 | Fertilizer Product | Setup Master | Fertilizer Planning |
| 28 | Application Method | Setup Master | Setup |
| 29 | Soil Nutrient Threshold | Setup Master | Setup |
| 30 | Measurement Verification | Document | Measurement & Verification |

---

## 3. GETTING STARTED

### 3.1 Installation
```bash
# From the bench directory
bench get-app https://github.com/Sudhakar1110/Precision_Farming.git
bench --site your-site.com install-app precision_farming
bench --site your-site.com migrate
```

### 3.2 Role Setup
Two roles are automatically created on install:
1. **Agriculture Manager** — Full access to all waste and fertilizer operations
2. **Agriculture User** — Can create and edit records, restricted to Agriculture domain

### 3.3 Initial Configuration
Before using the application, configure these masters:
1. **Waste Categories** — Define organic and inorganic waste types
2. **Waste Types** — Specify individual waste materials
3. **Application Methods** — Set fertilizer application techniques
4. **Compost Quality Parameters** — Define quality testing metrics
5. **Crop Nutrient Standards** — Set NPK requirements per crop type
6. **Fertilizer Products** — Register available fertilizer products
7. **Soil Nutrient Thresholds** — Define acceptable soil nutrient levels

---

## 4. FEATURE 1: AGRICULTURE WASTE MANAGEMENT

### 4.1 Workflow Overview
```
Waste Collection → Segregation → Composting/Recycling/Disposal → Field Application
```

### 4.2 Step-by-Step Process

#### Step 1: Waste Collection (Waste Record)
1. Navigate to **Agriculture Waste Management > Waste Collection**
2. Click **+ Add Waste Record**
3. Enter collection date, source location, and waste origin
4. Add waste items with categories and weight
5. Submit the record

**Fields:** Collection Date, Location, Organic Weight, Inorganic Weight, Total Weight, Collection Status (Active/Done)

#### Step 2: Composting (Composting Batch)
1. Navigate to **Agriculture Waste Management > Composting**
2. Click **+ New Composting Batch**
3. Reference the Waste Record
4. Add compost ingredients (green and brown materials)
5. Track turning events over time
6. Mark batch as completed when ready

**Fields:** Batch ID, Start Date, End Date, Status (Active/Completed), Ingredients, Turning Events

#### Step 3: Compost Quality Check
1. From the Composting card, open **Compost Quality Check**
2. Create a new quality check record
3. Reference the Composting Batch
4. Add quality check results for each parameter (pH, moisture, NPK content, etc.)
5. Review and submit

#### Step 4: Disposal & Recycling
For waste that cannot be composted:
1. **Recycling Record** — Track recyclable materials
2. **Disposal Record** — Track waste sent to landfill or incineration
3. **Collection Schedule** — Plan regular waste collection schedules

#### Step 5: Compost Application (Field Use)
1. Navigate to **Compost Application**
2. Reference the completed Composting Batch
3. Select the target land unit / field
4. Enter application quantity and method
5. Submit

### 4.3 Automated Tasks
- **Daily:** Expired compliance records are auto-marked as "Expired"
- **Weekly:** A waste summary notification is generated showing total organic and inorganic waste collected

---

## 5. FEATURE 2: FERTILIZER MEASUREMENT & MANAGEMENT

### 5.1 Workflow Overview
```
Soil Testing → Nutrient Analysis → Fertilizer Recommendation → Fertilizer Application → Measurement Verification
```

### 5.2 Step-by-Step Process

#### Step 1: Soil Analysis
1. Navigate to **Fertilizer Measurement & Management > Soil & Nutrient Analysis**
2. Click **+ New Soil Analysis**
3. Enter land unit / field details
4. Add soil test results (N, P, K, pH, organic matter, etc.)
5. Submit

**Fields:** Land Unit, Analysis Date, Lab Reference, N/P/K Levels, pH, Organic Matter, Recommendation

#### Step 2: Nutrient Analysis
1. From the same section, create a **Nutrient Analysis**
2. Reference the Soil Analysis
3. System auto-calculates nutrient gaps by comparing soil test results against Crop Nutrient Standards
4. Review the NPK gap analysis
5. Submit

**Key Feature:** Nutrient Gap automatically calculates the difference between current soil nutrients and crop requirements.

#### Step 3: Fertilizer Recommendation
1. Navigate to **Fertilizer Planning**
2. Click **+ New Fertilizer Recommendation**
3. Reference the Nutrient Analysis
4. System suggests recommended products based on NPK gaps
5. Add recommended products with quantities
6. Submit for approval

**Fields:** Land Unit, Recommendation Date, Status (Draft/Approved/Completed), Recommended Products, Total NPK Requirement

#### Step 4: Fertilizer Application
1. From Fertilizer Planning, click **+ New Fertilizer Application**
2. Reference the approved Fertilizer Recommendation
3. Select Application Method (Broadcasting, Banding, Foliar Spray, Drip Irrigation, Side Dressing)
4. Add fertilizer items and quantities applied
5. Record application date and operator details
6. Submit

#### Step 5: Fertilizer Schedule (Planning)
1. Create a **Fertilizer Schedule** for planned applications
2. Add schedule items with dates, products, and quantities
3. Track upcoming applications

#### Step 6: Measurement Verification
1. Navigate to **Measurement & Verification**
2. Create verification records for application accuracy
3. Record actual vs planned measurements
4. Submit for quality assurance

### 5.3 Automated Tasks
- **Daily:** Reminders created for pending fertilizer recommendations (older than 7 days)
- **Weekly:** Fertilizer usage report generated
- **Monthly:** Nutrient balance report showing total NPK gap across all analyses

---

## 6. QUALITY CONTROL & COMPLIANCE

### 6.1 Compliance Records
- Track regulatory compliance for waste management and fertilizer usage
- Set validity periods for permits and certifications
- System auto-expires records when validity period ends
- Status values: Active, Expired, Renewed

### 6.2 Measurement Verification
- Record field measurements for fertilizer application accuracy
- Verify application quantities against recommendations
- Maintain audit trail for regulatory reporting

---

## 7. WORKSPACE NAVIGATION

### 7.1 Home Workspace Layout
The Precision Farming workspace is organized into two main sections:

```
┌─────────────────────────────────────────────────────┐
│                QUICK ACTIONS                        │
│  [+Waste]  [+Compost]  [+Soil]  [+Fert] [+Apply]  │
├─────────────────────────────────────────────────────┤
│           AGRICULTURE WASTE MANAGEMENT              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐│
│  │  Waste   │  │Composting│  │Disposal  │  │Comply││
│  │Collection│  │          │  │& Recycling│  │Record││
│  └──────────┘  └──────────┘  └──────────┘  └──────┘│
├─────────────────────────────────────────────────────┤
│              FERTILIZER MEASUREMENT                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐│
│  │Soil &    │  │Fertilizer│  │  Setup   │  │ Meas ││
│  │Nutrient  │  │Planning  │  │          │  │ Verify││
│  └──────────┘  └──────────┘  └──────────┘  └──────┘│
└─────────────────────────────────────────────────────┘
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

| Section | Card | Accessible DocTypes |
|---------|------|-------------------|
| Agriculture Waste Management | Waste Collection | Waste Record, Waste Category, Waste Type |
| Agriculture Waste Management | Composting | Composting Batch, Compost Application, Compost Quality Check, Compost Quality Parameter |
| Agriculture Waste Management | Disposal & Recycling | Collection Schedule, Recycling Record, Disposal Record |
| Agriculture Waste Management | Compliance & Records | Compliance Record |
| Fertilizer Measurement | Soil & Nutrient Analysis | Soil Analysis, Nutrient Analysis, Crop Nutrient Standard |
| Fertilizer Measurement | Fertilizer Planning | Fertilizer Recommendation, Fertilizer Application, Fertilizer Schedule, Fertilizer Product |
| Fertilizer Measurement | Setup | Application Method, Soil Nutrient Threshold |
| Fertilizer Measurement | Measurement & Verification | Measurement Verification |

### 7.4 Fixtures (Auto-loaded on Install)
The following are loaded automatically as fixtures:
- Waste Category
- Waste Type
- Application Method
- Compost Quality Parameter
- Crop Nutrient Standard
- Fertilizer Product
- Soil Nutrient Threshold

The Precision Farming Workspace is auto-discovered by Frappe v15 from the standard workspace directory (`precision_farming/workspace/precision_farming/precision_farming.json`).

---

## 8. SCHEDULED TASKS & AUTOMATION

### 8.1 Daily Tasks (runs every day)
| Task | Function | Description |
|------|----------|-------------|
| Check Compliance Expiry | `check_compliance_expiry()` | Marks expired compliance records as "Expired" |
| Send Application Reminders | `send_application_reminders()` | Creates ToDo for recommendations pending > 7 days |

### 8.2 Weekly Tasks (runs every Monday)
| Task | Function | Description |
|------|----------|-------------|
| Generate Waste Summary | `generate_waste_summary()` | Creates notification with weekly waste collection totals |
| Generate Fertilizer Report | `generate_fertilizer_report()` | Creates notification with weekly fertilizer application totals |

### 8.3 Monthly Tasks (runs 1st of month)
| Task | Function | Description |
|------|----------|-------------|
| Generate Nutrient Balance Report | `generate_nutrient_balance_report()` | Creates notification with monthly NPK gap analysis |

---

## 9. SETUP & CONFIGURATION

### 9.1 Master Data to Configure

#### Waste Category
- Define categories like: Organic, Inorganic, Hazardous, Recyclable
- Used in: Waste Record

#### Waste Type
- Define types like: Food Waste, Crop Residue, Plastic, Paper, Metal
- Used in: Waste Record Items

#### Application Method
| Method | Efficiency | Description |
|--------|-----------|-------------|
| Broadcasting | 70% | Spreading over entire field |
| Banding | 85% | Applying near seed/plant row |
| Foliar Spray | 90% | Spraying on plant leaves |
| Drip Irrigation | 95% | Fertigation through drip system |
| Side Dressing | 80% | Applying alongside growing plants |

#### Compost Quality Parameter
- Define parameters: pH, Moisture, Carbon:Nitrogen Ratio, NPK Content, Temperature
- Used in: Compost Quality Check

#### Crop Nutrient Standard
- Define per crop: N/P/K requirements, soil pH preference
- Used in: Nutrient Analysis (for gap calculation)

#### Fertilizer Product
- Register products with NPK composition, brand, supplier
- Used in: Fertilizer Recommendation

#### Soil Nutrient Threshold
- Set acceptable ranges for soil nutrients
- Used in: Soil Analysis evaluation

### 9.2 Fixtures (Auto-loaded on Install)
The following are loaded automatically as fixtures:
- Waste Category
- Waste Type
- Application Method
- Compost Quality Parameter
- Crop Nutrient Standard
- Fertilizer Product
- Soil Nutrient Threshold

The Precision Farming Workspace is auto-discovered by Frappe v15 from the workspace directory and is NOT a fixture entry. To modify workspace settings, edit the JSON file directly.

---

## 10. TROUBLESHOOTING

### 10.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| App not found during install | App not in apps.txt | `echo "precision_farming" >> sites/apps.txt` |
| Module not found error | Module name mismatch | Ensure modules.txt = "Precision Farming" |
| Workspace not showing in module list | Private workspace | Set `"is_public": 1` in the workspace JSON, run `bench --site site import-fixtures` then `bench --site site migrate` |
| Workspace not showing changes | Fixtures not synced | Run `bench --site site migrate` |
| Scheduled tasks not running | Scheduler disabled | Enable with `bench --site site scheduler enable` |
| Role permission issues | Roles not created | Run `bench console` then `frappe.get_doc("Precision Farming", "install").after_install()` |

### 10.2 Force Sync Workspace
```python
# In bench console
import frappe
from frappe.utils.fixtures import sync_fixtures
sync_fixtures("precision_farming")
```

### 10.3 Clear Cache
```bash
bench --site your-site.com clear-cache
bench --site your-site.com migrate
```

---

## APPENDIX

### A. Role Permissions

| Role | Waste Mgmt | Fertilizer | Compliance | Setup |
|------|-----------|------------|------------|-------|
| Agriculture Manager | Full Access | Full Access | Full Access | Full Access |
| Agriculture User | Create, Read, Write | Create, Read, Write | Read | Read |
| System Manager | Full Access | Full Access | Full Access | Full Access |

### B. Related Documents
- Frappe Framework Documentation: https://frappeframework.com/docs
- ERPNext Agriculture Module: https://docs.erpnext.com/docs/user/manual/en/agriculture

---

*End of SOP Document*

**Maintainer:** Precision Farming Solutions  
**Contact:** admin@precisionfarming.com  
**Repository:** https://github.com/Sudhakar1110/Precision_Farming.git
