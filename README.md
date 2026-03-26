# Medical Test Records Management System

A command-line based system for managing patients' medical test records.  
The system supports record management, advanced filtering, abnormal result detection, reporting, and CSV import/export.

Implemented using **Python (main version)** and **Shell Scripting (secondary version)**.

---

## Overview

This project simulates a simplified medical records system where patient test data can be stored, updated, filtered, and analyzed.

The system focuses on:

- Data validation
- Structured data storage
- Query-like filtering
- Analytical reporting

---

## Features

### Medical Record Management

- Add new test records for patients
- Update existing test results
- Delete test records
- Prevent duplicate test entries (same test & date)

---

### Advanced Filtering

- Filter by **Patient ID**
- Filter by **Test Name**
- Filter by **Date Range**
- Filter by **Test Status** (Pending, Completed, Reviewed)
- Filter **Abnormal Test Results**
- Filter by **Turnaround Time**

---

### Abnormal Test Detection

- Detects abnormal values based on:
  - Minimum & maximum ranges
  - Only minimum or only maximum thresholds

---

### Reporting & Analytics

- Generate summary reports:
  - Minimum test value
  - Maximum test value
  - Average test value
- Turnaround time statistics (min, max, average)

---

### Input Validation

- Patient ID (7-digit numeric)
- Date format (`YYYY-MM-DD HH:MM`)
- Numeric test values
- Controlled status input

---

## Technologies Used

- Python
- Shell Scripting
- File Handling
- Object-Oriented Programming
- Data Structures (lists, dictionaries)

---

## How to Run

### Python Version

```bash
cd python
python medical_system.py
```

### Shell Version

```bash
cd shell
bash medical_system.sh
```

---

## Required Input File Formats

The file structure differs slightly between the Python and Shell versions.

---

### Python Version

#### `medicalRecord.txt`

Each line represents a single medical test record.

```
1300500: RBC, 2024-03-01 05:20, 13.5, mg/dL, completed, 2024-03-01 05:30
1300511: LDL, 2024-03-02 07:30, 110, mg/dL, pending
1300520: systole, 2024-03-04 04:40, 150, mm Hg, pending
```

**Fields:**

* Patient ID: 7-digit integer
* Test name: string
* Test date and time: `YYYY-MM-DD HH:MM`
* Numeric result value
* Unit
* Status: `Pending`, `Completed`, or `Reviewed`
* Result date and time: included **only if** the status is `Completed`

**Rules:**

* Patient ID must be exactly 7 digits
* Keep the punctuation and separators exactly as shown
* Result date and time should appear only for completed tests

#### `medicalTest.txt`

This file stores the test metadata, including the normal range and nominal turnaround time.

```
Name: Hemoglobin (Hgb); Range: > 13.8, < 17.2; Unit: g/dL, 00-03-04
Name: Blood Glucose Test (BGT); Range: > 70, < 99; Unit: mg/dL, 00-12-06
Name: LDL Cholesterol Low-Density Lipoprotein (LDL); Range: < 100; Unit: mg/dL, 00-17-06
Name: Systolic Blood Pressure (systole); Range: < 120; Unit: mm Hg, 00-08-04
Name: Diastolic Blood Pressure (diastole); Range: < 80; Unit: mm Hg, 00-10-00
```

**Fields:**

* Name
* Range
* Unit
* Nominal turnaround time in `DD-hh-mm` format

**Rules:**

* Keep the punctuation exactly as shown, because the program parses this file directly

---

### Shell Version

#### `medicalRecord.txt`

```
1300500: RBC, 2024-03, 13.5, mg/dL, completed
1300511: LDL, 2024-03, 110, mg/dL, pending
```

**Fields:**

* Patient ID: 7-digit integer
* Test name: string
* Test date: `YYYY-MM`
* Result value
* Unit
* Status

**Rules:**

* Patient ID must be exactly 7 digits
* Keep the separators exactly as shown
* No result date/time is stored in the Shell version

#### `medicalTest.txt`

This file stores only the test metadata needed by the Shell version.

```
Name: Hemoglobin (Hgb); Range: > 13.8, < 17.2; Unit: g/dL
Name: Blood Glucose Test (BGT); Range: > 70, < 99; Unit: mg/dL
Name: LDL Cholesterol Low-Density Lipoprotein (LDL); Range: < 100; Unit: mg/dL
Name: Systolic Blood Pressure (systole); Range: < 120; Unit: mm Hg
Name: Diastolic Blood Pressure (diastole); Range: < 80; Unit: mm Hg
```

**Fields:**

* Name
* Range
* Unit

---

The second file named `medicalTest.txt` stores the clinic test definitions. For the **Python version**, it includes the test name, normal range, unit, and nominal turnaround time. For the **Shell version**, it includes only the test name, normal range, and unit.


## Documentation

A detailed testing report is included:

**System_Testing_Report.pdf**

It contains:

- Test scenarios
- Example outputs
- System behavior validation

---

## Design Highlights

- Patients stored in a **dictionary structure**
- Each patient contains a list of test records
- Separation between:
  - Test metadata (ranges, units)
  - Patient records
- Supports both:
  - File-based persistence
  - In-memory processing
---
