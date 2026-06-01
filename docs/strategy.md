# Strategy & Recommendations

## 1. Automation Selection Strategy
The automated test suite was intentionally curated to maximize Return on Investment (ROI) while minimizing execution time and framework bloat. I selected the following two tests to demonstrate coverage across different architectural layers:

* **TC-001 (UI End-to-End Happy Path):** This is the core revenue engine of the business. If a user cannot successfully place a bet, the platform fails its primary objective. Automating this flow ensures that the critical path (frontend rendering -> user input -> API communication -> state update -> receipt rendering) is completely functional. Furthermore, by utilizing "Soft Assertions," this automated test can successfully validate the business transaction while simultaneously logging non-blocking frontend cosmetic defects (e.g., BUG-002, BUG-004).
* **TC-006 (API Insufficient Balance Bypass):** UI validations are inherently insecure and easily bypassed by malicious actors using tools like Postman. I chose to automate this backend scenario because it protects against a catastrophic financial exploit. By automating at the API layer, we get a lightning-fast, highly reliable security check that ensures the backend ledger independently validates funds before processing a transaction.

---

## 2. Manual-Only Rationale
To respect the time-boxed nature of this assignment and adhere to the "Test Pyramid," certain scenarios were intentionally left out of the heavy E2E UI automation suite:

* **UI Boundary Validations (TC-002 & TC-003):** Testing frontend boundary limits (e.g., €0.99 vs. €1.00) via Selenium is an anti-pattern. These are typically static validations (HTML attributes or React state) that are better suited for lightning-fast Unit or Component tests (e.g., Jest or React Testing Library). Pushing these to E2E makes the suite slow and brittle.
* **Secondary API Rules (TC-004 & TC-005):** While easily automatable using the established `SportyApiClient`, they were excluded to avoid over-engineering the take-home assignment. TC-006 was chosen as the singular API representative to prove the framework's capability to test backend security without bloating the repository.
* **Visual/Temporal Edge Cases (BUG-001):** Validating that "past matches" do not appear on the UI is highly dependent on server time and dynamic database states. Until a proper test-data-seeding mechanism is built, this is safer to verify manually or via an isolated API integration test.

---

## 3. Recommendations for Scaling
If this project were to scale into a production environment, I recommend the following architectural upgrades:

* **CI/CD Integration with Pytest Warnings:** The current framework is designed to emit `UserWarnings` for non-blocking UI defects while officially passing the test. This should be integrated into a CI/CD pipeline (e.g., GitHub Actions). API tests should run on every Pull Request (Failing Fast), while the UI suite runs on Staging deployments, allowing deployments to proceed while logging frontend bugs to Jira.
* **Test Data Management (Database Seeding):** Currently, tests rely on a static `candidate-ID` and assume a predictable starting balance. At scale, the framework needs a dedicated teardown/setup mechanism (e.g., a backend `/api/test-reset` endpoint) to inject specific user balances and match states before execution. This ensures test idempotency and prevents data collision when running in parallel.
* **Headless Execution & Cross-Browser Grid:** The `conftest.py` should be parameterized to allow running tests in `--headless` mode for faster CI execution, and integrated with Selenium Grid or BrowserStack to ensure compatibility across Safari, Firefox, and mobile viewports.
* **Test Management & Stakeholder Visibility (Jira Xray Integration):** To provide high-level stakeholders with clear, real-time visibility into platform health, the automation framework should be integrated with a test management tool like Xray in Jira. By linking the Pytest automated scripts directly to Jira test cases (using decorators/markers) and automatically pushing execution results (e.g., via JUnit XML) directly to the repository, product managers and engineering leads gain a centralized, dynamic dashboard of test coverage and release readiness directly alongside project requirements.