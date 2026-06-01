import pytest
from pages.main_betting_page import MainBettingPage

def test_successful_bet_placement(driver, test_data, app_config):
    """
    Test Case: TC-001 / BUG-002 / BUG-003 / BUG-004
    A dynamic, data-driven E2E test validating core transactional math.
    """
    page = MainBettingPage(driver)
    
    print("\nStep 1: Navigating to the application...")
    # Dynamic URL injection
    full_url = f"{app_config['base_url']}/?user-id={app_config['user_id']}"
    page.navigate(full_url)
    
    # FIX 2: Wait for API to resolve initial balance
    page.pause()
    initial_balance_text = page.get_current_balance()
    initial_balance = page.extract_number(initial_balance_text)
    print(f"Initial Balance: €{initial_balance}")
    
    print("\nStep 2: Selecting match dynamically from test_data.json...")
    match_data = test_data["matches"]["upcoming_valid_match"]
    page.select_match_outcome(match_id=match_data["id"], selection=test_data["selections"]["draw"])
    
    print("Step 3: Entering stake...")
    stake_amount = 10.0
    page.enter_stake(stake_amount)
    
    # FIX 3: Strict mathematical assertion, not just string inclusion
    totals = page.get_bet_slip_totals()
    ui_stake = page.extract_number(totals["stake"])
    assert ui_stake == stake_amount, f"UI Input Failure: Expected €{stake_amount}, got €{ui_stake}"
    
    print("Step 4: Placing the bet and awaiting backend processing...")
    page.click_place_bet()
    
    # FIX 4: Explicit wait for the receipt modal to render
    page.wait_for_receipt_modal()
    
    print("\nStep 5: Validating the Success Receipt Data dynamically...")
    receipt = page.get_receipt_details()
    
    # FIX 5: Dynamic mathematical calculation of Expected Payout
    ui_odds = float(receipt["odds"])
    actual_ui_payout = page.extract_number(receipt["payout"])
    expected_payout = round(stake_amount * ui_odds, 2)
    
    assert actual_ui_payout == expected_payout, \
        f"BUG-002 (UI Data Binding Failure): Math error! {stake_amount} * {ui_odds} should be {expected_payout}. UI displayed {actual_ui_payout}"

    # FIX 6: Dynamic match name reconstruction
    expected_match_name = f"{match_data['home_team']} vs {match_data['away_team']}"
    assert receipt["match"] == expected_match_name, \
        f"BUG-004 (Team Order Reversed): Expected '{expected_match_name}', got '{receipt['match']}'!"

    print("\nStep 6: Closing modal and verifying balance deduction...")
    page.close_receipt()
    page.pause()
    
    # FIX 7: Dynamic mathematical assertion of the new balance
    final_balance_text = page.get_current_balance()
    final_balance = page.extract_number(final_balance_text)
    
    expected_final_balance = round(initial_balance - stake_amount, 2)
    assert final_balance == expected_final_balance, \
        f"BUG-003 (UI State Sync): Balance failed to deduct correctly! Expected €{expected_final_balance}, got €{final_balance}!"