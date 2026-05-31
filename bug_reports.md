# Bug Reports: Execution Results

**Overview:** This document contains the execution results and defect reports discovered during the manual testing phase. 

---

### BUG-001 | System Displays Old Matches and Allows Betting on Past Events
* **Severity:** Critical
* **Reproduction Steps:**
    1. Navigate to the application.
    2. Scroll through the "Upcoming Football Matches" list and locate matches with "PAST" dates prior to the current system date.
    3. Select an odds button for one of these past matches.
    4. Enter a valid stake in the Bet Slip and click "Place Bet".
* **Expected vs Actual Result:**
    * *Expected:* The system must restrict the event type to "Upcoming/Pre-match events only." Past matches should be entirely filtered out by the backend API and never displayed on the UI.
    * *Actual:* The backend API successfully returns old matches (expired events) (e.g., from April 2026). The UI displays them, and the system allows users to successfully place wagers on these concluded events.
* **Business Impact:** This introduces a catastrophic financial vulnerability known as "past-posting." If users can place bets on matches that have already finished, this is an illegal practice in sports betting. 
* **Evidence:** 
    * Screenshot reference: `Screenshots/TC-001-01.jpg`
    * **Root Cause Analysis:** The backend `GET /api/matches` endpoint lacks a time-based query filter. It is serving the entire database of matches regardless of the `kickoffDate` relative to the current server date.

**API Response Snippet (`GET /api/matches`):**
```json
[
    {
        "id": "eredivisie-ajax-feyenoord-2026-04-16",
        "competition": "Eredivisie",
        "kickoffDate": "2026-04-16",
        "homeTeam": "Ajax",
        "awayTeam": "Feyenoord",
        "odds": {
            "home": 2.15,
            "draw": 3.45,
            "away": 3.15
        }
    }
]
```
---

### BUG-002 | Success Receipt Displays Incorrect Potential Payout (UI Data Binding Failure)
* **Severity:** Critical
* **Reproduction Steps:**
    1. Navigate to the application and select a valid match outcome (e.g., Draw, Odds: 3.40).
    2. Enter a Stake of `10.00` in the Bet Slip.
    3. Verify the Bet Slip calculates the potential payout correctly (`34.00`).
    4. Click "Place Bet" and wait for the Success Receipt modal.
    5. Compare the modal's Payout value against the Bet Slip and the Network API response.
* **Expected vs Actual Result:**
    * *Expected:* The Success Receipt modal must dynamically display the correct payout calculation (Stake * Odds = `34.00`), matching both the Bet Slip and the backend API response.
    * *Actual:* The UI completely ignores the API payload and displays a static, incorrect value (e.g., `20.00`) regardless of the actual stake or odds.
* **Business Impact:** This severely damages customer trust. Handing a user an incorrect official receipt will immediately trigger a lot of support tickets, cause them to abandon the platform, and expose the company to legal disputes.
* **Evidence:** * Screenshot reference: `Screenshots/TC-001-03.jpg`
    * **Root Cause Analysis:** The backend is functioning perfectly, proving this is strictly a frontend data-binding issue. The captured `POST /api/place-bet` response clearly returns the correct `"payout": 34`:

```json
{
    "message": "Bet placed successfully",
    "matchId": "premier-league-arsenal-chelsea-2026-06-01",
    "selection": "DRAW",
    "stake": 10,
    "odds": 3.4,
    "payout": 34,
    "balance": 110,
    "currency": "USD"
}
```
---

### BUG-003 | User Balance Fails to Update After Successful Bet (UI State Sync Issue)
* **Severity:** High
* **Reproduction Steps:**
    1. Note the current user balance in the header and bet slip (e.g., `120.00`).
    2. Successfully place a bet with a valid stake (e.g., `10.00`).
    3. Close the Success Receipt modal.
    4. Observe the balance displayed in the top header and the empty bet slip.
    5. Manually refresh the browser page and observe the balance again.
* **Expected vs Actual Result:**
    * *Expected:* The UI should instantly update to reflect the newly deducted balance (`110.00`) as soon as the bet is placed, without requiring a manual page refresh.
    * *Actual:* The UI displays the stale balance (`120.00`) until the user forces a browser reload.
* **Business Impact:** Displaying stale funds creates a highly frustrating user experience. A user might believe they have enough money for another bet, only to be hit with an "Insufficient balance" error when they try to place it. This makes the platform feel broken and unreliable.
* **Evidence:** 
    * Screenshot reference: `Screenshots/TC-001-03.jpg`
    * **Root Cause Analysis:** The `POST /api/place-bet` API successfully processes the deduction and returns the correct new balance (`"balance": 110`). The frontend is failing to update (re-render) the new balance.

**API Response Snippet:**
```json
{
    "message": "Bet placed successfully",
    "matchId": "premier-league-arsenal-chelsea-2026-06-01",
    "selection": "DRAW",
    "stake": 10,
    "odds": 3.4,
    "payout": 34,
    "balance": 110,
    "currency": "USD"
}
```

---

### BUG-004 | Match Team Order Reversed on Success Receipt Modal
* **Severity:** High
* **Reproduction Steps:**
    1. View the upcoming match list and observe a match with distinct Home and Away teams (e.g., Home: Arsenal, Away: Chelsea).
    2. Select an outcome and enter a valid stake in the Bet Slip.
    3. Click "Place Bet" and wait for the Success Receipt modal.
    4. Observe the team order displayed under the "MATCH" header on the receipt.
* **Expected vs Actual Result:**
    * *Expected:* The receipt must strictly preserve the original Home vs Away team order displayed on the match list and defined by the domain convention (e.g., "Arsenal vs Chelsea").
    * *Actual:* The receipt modal incorrectly reverses the team names, displaying the Away team first (e.g., "Chelsea vs Arsenal").
* **Business Impact:** user seeing flipped team names on their receipt will panic, thinking they bet on the wrong game. the receipt is simply not legally correct. In sports, who plays at home matters. Issuing a receipt that reverses this gives users a valid excuse to demand refunds and creates a major compliance for the company.
* **Evidence:** 
    * Screenshot (Match List - Correct Order): `Screenshots/TC-001-01.jpg`
    * Screenshot (Receipt - Reversed Order): `Screenshots/TC-001-03.jpg`
    * **Root Cause Analysis:** The backend sends the correct structure. The `GET /api/matches` endpoint separates the `homeTeam` and `awayTeam`. The frontend correctly parses this for the main list, but the Success Receipt modal likely displays these strings in the wrong order (e.g., `awayTeam + " vs " + homeTeam`).

**API Response Snippet (`GET /api/matches`):**
```json
{
    "id": "premier-league-arsenal-chelsea-2026-06-01",
    "competition": "Premier League",
    "kickoffDate": "2026-06-01",
    "homeTeam": "Arsenal",
    "awayTeam": "Chelsea",
    "odds": {
        "home": 2.05,
        "draw": 3.4,
        "away": 3.55
    }
}
```
---

### BUG-005 | Missing Time in Match List, only date is displayed (API/UI Requirement Discrepancy)
* **Severity:** Medium
* **Reproduction Steps:**
    1. Navigate to the main application dashboard.
    2. View the "Upcoming Football Matches" list.
    3. Check the date label displayed directly above any match's team names.
* **Expected vs Actual Result:**
    * *Expected:* the UI must display a "Kickoff date/time label" so users know exactly when the event begins.
    * *Actual:* The UI only displays the date (e.g., "Tomorrow" or "Sun, Jun 07") and completely omits the exact time of the match.
* **Business Impact:** Users need to know exactly when a match starts so they do not miss the cutoff to place their bets. Without a specific time, a user might plan to bet later in the day, only to find the match has already started and betting is locked. This causes immense frustration for the user and directly results in lost revenue for the platform.
* **Evidence:** 
    * Screenshot reference: `Screenshots/TC-001-01.jpg`
    * **Root Cause Analysis:** This is a discrepancy between the product requirements and the API implementation. The frontend UI cannot display the time because the backend API does not provide it. The `GET /api/matches` endpoint strictly returns a `YYYY-MM-DD` date string without any timestamp data.

**API Response Snippet (`GET /api/matches`):**
```json
{
    "id": "premier-league-arsenal-chelsea-2026-06-01",
    "competition": "Premier League",
    "kickoffDate": "2026-06-01",
    "homeTeam": "Arsenal",
    "awayTeam": "Chelsea",
    "odds": {
        "home": 2.05,
        "draw": 3.4,
        "away": 3.55
    }
}
```

----


### BUG-006 | API Returns Incorrect Currency Code (Backend Logic Failure)
* **Severity:** High
* **Reproduction Steps:**
    1. Place a successful bet via the UI.
    2. Inspect the JSON response body in the Network tab.
    3. Locate the `currency` field.
* **Expected vs Actual Result:**
    * *Expected:* the system strictly operates in Euros. The API must return `"currency": "EUR"`.
    * *Actual:* The API returns `"currency": "USD"`. 
* **Business Impact:** While the current UI masks this issue by hardcoding the Euro symbol (€), it will affect other services (such as reporting tools or payment gateways) that record these transactions in the wrong currency. This bug will also create immediate technical issue for future scalability (multi-currency support).
* **Evidence:** 
    * **Root Cause Analysis:** The backend logic is incorrectly sending "USD" in the response payload builder.

**API Response Snippet (`POST /api/place-bet`):**
```json
{
    "message": "Bet placed successfully",
    "matchId": "premier-league-arsenal-chelsea-2026-06-01",
    "selection": "DRAW",
    "stake": 10,
    "odds": 3.4,
    "payout": 34,
    "balance": 110,
    "currency": "USD"
}
```
-------

### BUG-007 | API Allows Wagers Exceeding User Balance (Negative Ledger Exploit)
* **Severity:** Critical
* **Reproduction Steps:**
    1. Ensure the user account has a known low balance (e.g., `€20.00`).
    2. Bypass the UI and send a `POST /api/place-bet` request directly to the backend.
    3. Include a valid `x-user-id` header.
    4. Set the `stake` parameter in the JSON payload to an amount greater than the current balance (e.g., `50`).
    5. Check the API response and verify the updated user balance.
* **Expected vs Actual Result:**
    * *Expected:* The backend must independently verify the ledger and block the transaction, returning an error for insufficient funds.
    * *Actual:* The backend blindly accepts the wager, processing the bet successfully (`200 OK`) and driving the user's balance into negative territory (e.g., `-30`).
* **Business Impact:** This is a catastrophic financial issue. A malicious user can bypass the frontend to place massive wagers with money they do not have. This completely breaks the financial integrity of the platform and exposes the business to unlimited liability.
* **Evidence:** * Screenshot reference: `Screenshots/TC-006-01.jpg`
    * **Root Cause Analysis:** The `POST /api/place-bet` endpoint completely lacks server-side validation against the user's current ledger balance before executing the transaction deduction.

**API Response Snippet (`POST /api/place-bet`):**
```json
{
  "message": "Bet placed successfully",
  "matchId": "premier-league-manutd-chelsea",
  "selection": "HOME",
  "stake": 50,
  "odds": 2.45,
  "payout": 122.5,
  "balance": -30,
  "currency": "USD"
}
```
---
