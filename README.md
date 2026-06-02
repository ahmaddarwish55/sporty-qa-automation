# SportyGroup QA Automation Framework

## Overview
This repository contains the completed take-home assignment for the Hybrid QA Engineer position at SportyGroup. It provides a comprehensive quality assurance solution, combining detailed manual test documentation (test plans, bug reports) with a robust, scalable automated testing framework built in Python.

The automation suite focuses on the critical revenue-generating paths, utilizing a hybrid architecture that tests both the UI (Selenium) and the Backend Ledger (API) to ensure complete transactional integrity.

## Technology Stack
* **Language:** Python 3.8+
* **Framework:** Pytest
* **UI Automation:** Selenium WebDriver (Page Object Model)
* **API Automation:** Python `requests` (API Object Model)
* **Data Handling:** JSON (Data-Driven Testing)

## Directory Structure
```text
SPORTY-QA-AUTOMATION/
├── api/
│   └── client.py                  # API Object Model for backend 
├── data/
│   └── test_data.json             # Centralized test data for 
├── docs/
│   ├── bug_reports.md             # Detailed defect logs from manual 
│   ├── test_plan.md               # Prioritized manual test  
│   └── strategy.md                # Prioritized manual test 
├── pages/
│   ├── base_page.py               # Foundational POM with generic 
│   └── main_betting_page.py       # Page-specific locators and 
├── tests/
│   ├── conftest.py                # Pytest fixtures (Driver setup, API client, Data loading)
│   ├── test_001_ui_e2e.py         # UI End-to-End Test (Happy Path + Soft Assertions)
│   └── test_006_api_validation.py # API Security Test (Ledger Exploit Validation)
├── config.py                      # Global configuration 
├── requirements.txt               # Python package dependencies
└── README.md                      # Setup and execution guide
```

## Prerequisites
To run this framework locally, ensure you have the following installed:
1. **Python 3.8 or higher**
2. **Google Chrome browser** (The framework uses the default Chrome WebDriver)
3. **Git** (for cloning the repository)

## Local Setup Instructions

1. **Clone the repository and navigate to the project root:**
```bash
   gh repo clone ahmaddarwish55/sporty-qa-automation
   cd SPORTY-QA-AUTOMATION
   ```

2. **Create and activate a virtual environment:**
   * **Windows:**
```bash
     python -m venv venv
     venv\Scripts\activate
```
   * **macOS/Linux:**
```bash
     python3 -m venv venv
     source venv/bin/activate
```

3. **Install the required dependencies:**
```bash
   pip install -r requirements.txt
```

## Test Execution Guide

The framework is configured to run tests dynamically. Test results and custom logging will be printed directly to the terminal.

**Run the entire test suite (API followed by UI):**
```bash
python -m pytest tests/ -v -s
```

**Run ONLY the API security test (TC-006):**
```bash
python -m pytest tests/test_006_api_validation.py -v -s
```

**Run ONLY the UI End-to-End test (TC-001):**
```bash
python -m pytest tests/test_001_ui_e2e.py -v -s
```

## ⚠️ Important Note on Test Results & Soft Assertions
When executing the UI test (`test_001_ui_e2e.py`), you will notice that the test **PASSES with Warnings**. 

This is an intentional architectural design known as **Soft Assertions**. The framework is engineered to separate *Critical Transaction Blockers* from *Non-Blocking Cosmetic Defects*:
* **Hard Assertions:** If the core transactional engine fails (e.g., the input box is broken, or the backend rejects the bet), the test will explicitly **FAIL** and halt the CI/CD pipeline.
* **Soft Assertions:** If the bet is successfully placed, but the UI contains data-binding bugs (e.g., reversed team names, incorrect payout math, stale balance rendering), the test allows the transaction to complete. It then aggregates these frontend bugs and emits them as **Pytest Warnings**. This proves the revenue engine works while still aggressively logging UI defects for the development team. (See `docs/bug_reports.md` for full details on these logged defects).