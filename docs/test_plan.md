# Test Plan: Single Bet Placement Feature

**Overview:** This document outlines 5 prioritized manual test scenarios for the Single Bet Placement feature. The scenarios are selected to demonstrate coverage across happy paths, boundary conditions, negative validation, and API-layer security.

---

### TC-001 | Happy Path: Successful Single Bet Placement
*   **Priority:** Critical
*   **Risk Rationale:** This validates the core transactional engine of the application. If a user cannot successfully place a valid bet and have their balance properly deducted, the business suffers an immediate total failure in revenue generation.
*   **Steps:**
    1. Navigate to the application URL with a valid user-id = `candidate-PR1EPAagsI`.
    2. Note the current available balance displayed in the header.
    3. From the Match List, select an outcome (e.g., Draw / 'X') for an upcoming match.
    4. In the Bet Slip, enter a valid stake amount (e.g., `10`).
    5. Verify the "Total Stake" and "Potential Payout" calculations update correctly on the slip.
    6. Click the "Place Bet" button.
    7. Observe the button transition to the "Placing..." loading state.
    8. Upon the appearance of the Success Receipt modal, verify all displayed data (Match, Stake, Odds, Payout).
    9. Click the primary "Close" action on the modal.
*   **Expected Result:**
    *   The Success Receipt modal displays the correct, un-altered match details, stake, odds, and mathematically correct potential payout (Stake * Odds).
    *   Closing the receipt returns the user to the main flow, clearing the active selection in the bet slip.
    *   The user's available balance (in both the header and bet slip) is immediately deducted by the exact stake amount.

---

### TC-002 | Boundary Value: Minimum and Maximum Stake Limits
* **Priority:** High
* **Risk Rationale:** This ensures the system strictly follows the business rules defining the acceptable wager range (€1.00 to €100.00).
* **Steps:**
    1. Navigate to the application URL with a valid user-id (`candidate-PR1EPAagsI`).
    2. From the Match List, select an outcome for an upcoming match.
    3. In the Bet Slip, enter a stake of `0.99` (just below the minimum boundary).
    4. Observe the inline UI validation and the state of the "Place Bet" button.
    5. Change the stake to `1.00` (the minimum valid boundary) and verify the button state.
    6. Change the stake to `100.00` (the maximum valid boundary) and verify the button state.
    7. Change the stake to `100.01` (just above the maximum boundary) and observe the UI validation.
* **Expected Result:**
    * When the stake is `0.99`, the UI immediately triggers an inline validation error displaying "Minimum stake is €1.00", and the "Place Bet" button dynamically disables.
    * When the stake is `1.00` or `100.00`, the system accepts the input as valid, no errors are displayed, and the "Place Bet" button remains enabled.
    * When the stake is `100.01`, the UI immediately triggers an inline validation error displaying "Maximum stake is €100.00", and the "Place Bet" button dynamically disables.

---

### TC-003 | Business Logic (Negative): Insufficient Balance
* **Priority:** Critical
* **Risk Rationale:** Prevents user from placing a bet that exceeds his balance. Allowing bets without sufficient balance is a massive financial and regulatory violation for the platform.
* **Steps:**
    1. Navigate to the application and note the user's current available balance in the header (e.g., €20.00).
    2. From the Match List, select an outcome for an upcoming match to open the Bet Slip.
    3. In the Bet Slip, enter a stake amount that is greater than the current available balance (e.g., `22.00`).
    4. Observe the inline UI validation error message.
    5. Check the  state of the "Place Bet" button.
* **Expected Result:**
    * The UI immediately detects that the entered stake exceeds the available balance.
    * An inline error message "Insufficient balance" is displayed below the stake input field.
    * The "Place Bet" button is dynamically disabled, preventing the user from submitting the invalid amount.

---

### TC-004 | API Validation (Negative): Missing Authentication Context on Protected Endpoints
* **Priority:** High
* **Risk Rationale:** Verifies the security of the backend API gateway. If the `x-user-id` header is missing or unenforced on protected routes, malicious actors could leak user data or forge unauthorized transactions.
* **Steps:**
    1. Open the provided API documentation (Swagger UI).
    2. Construct a `GET` request to `/api/balance` and intentionally omit the `x-user-id` header. Execute the request.
    3. Construct a `POST` request to `/api/place-bet` with a valid JSON payload, but intentionally omit the `x-user-id` header. Execute the request.
    4. Observe the response status code and body for both requests.
* **Expected Result:**
    * The backend API gateway strictly rejects both requests.
    * The system returns exactly a `401` status code for both the GET and POST endpoints with details `Error: response status is 401`, ensuring no data is leaked and no bets are processed.
    * The response body returns the explicit error message: `{"error": "Missing user-id in header"}`.

---

### TC-005 | API Business Logic (Negative): Maximum Stake Limit Bypass
* **Priority:** Critical
* **Risk Rationale:** The UI restricts bets over €100.00, but malicious actors can easily bypass the frontend and send payloads directly to the API. If the backend does not independently enforce the maximum stake limit, the business is exposed to unacceptable financial liability.
* **Steps:**
    1. Open the provided API documentation (Swagger UI).
    2. Construct a `POST` request to `/api/place-bet`.
    3. Include a valid `x-user-id` header (`candidate-PR1EPAagsI`).
    4. In the JSON body, pass a valid `matchId` and `selection`, but intentionally set the `stake` to `1000` (well above the business rule limit).
    5. Execute the request and observe the server response.
* **Expected Result:**
    * The backend API strictly enforces the €100.00 maximum stake rule independently of the UI.
    * The system strictly rejects the request, returning a `422 Unprocessable Entity` HTTP status code.
    * The response body contains the exact error schema: `{"error": "invalid_stake_max", "message": "Stake must be at most 100.00."}`.

---

### TC-006 | API Business Logic (Negative): Insufficient Balance Bypass
* **Priority:** Critical
* **Risk Rationale:**  Malicious actors can bypass the frontend. If the backend does not enforce available balance check before placing bet and deducting funds, users can place bets with infinite credit, causing catastrophic financial losses.
* **Steps:**
    1. Open the provided API documentation (Swagger UI).
    2. Execute a `GET` request to `/api/balance` with a valid `x-user-id` to note the current available balance (e.g., €20.00).
    3. Construct a `POST` request to `/api/place-bet` with the same `x-user-id` header.
    4. In the JSON body, pass a valid `matchId` and `selection`, but intentionally set the `stake` higher than the available balance (e.g., `50`).
    5. Execute the request and observe the server response.
* **Expected Result:**
    * The backend API strictly enforces a ledger check independently of the UI.
    * The system rejects the request, returning a `422 Unprocessable Entity` or `400 Bad Request` status code indicating insufficient funds.
    * The user's balance remains unchanged.

---