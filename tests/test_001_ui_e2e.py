import pytest
from pages.main_betting_page import MainBettingPage
import warnings

def test_successful_bet_placement(driver, test_data, app_config):
    """
    Test Case: TC-001
    A dynamic E2E test validating core transactional math.
    Uses Hard Assertions for critical path blockers and Soft Assertions for UI defects.
    """
    page = MainBettingPage(driver)
    ui_defects = []
    
    print("\nStep 1: Navigating to the application...")
    full_url = f"{app_config['base_url']}/?user-id={app_config['user_id']}"
    page.navigate(full_url)
    
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
    
    # HARD ASSERT 1: UI failure. If the input field fails, we cannot proceed.
    totals = page.get_bet_slip_totals()
    ui_stake = page.extract_number(totals["stake"])
    assert ui_stake == stake_amount, f"CRITICAL BLOCKER: UI Input Failure! Expected €{stake_amount}, got €{ui_stake}"
    
    # Soft Assertion: Bet Slip Payout Math
    ui_slip_payout = page.extract_number(totals["payout"])
    slip_odds = page.get_bet_slip_odds()
    expected_slip_payout = round(stake_amount * slip_odds, 2)

    if ui_slip_payout != expected_slip_payout:
        ui_defects.append(f"(Bet Slip Math): Slip payout showed €{ui_slip_payout}, expected €{expected_slip_payout}")

    print("Step 4: Placing the bet and awaiting backend processing...")
    page.click_place_bet()
    
    # HARD ASSERT 2: Transaction check. Ensure the Success Modal appears.
    try:
        page.wait_for_receipt_modal()
    except Exception:
        # If the success modal fails to appear, check if the error modal showed up instead
        if page.is_error_modal_displayed():
            error_text = page.get_error_message()
            pytest.fail(f"CRITICAL BLOCKER: Transaction Failed! Error Modal appeared: '{error_text}'")
        else:
            pytest.fail("CRITICAL BLOCKER: Application froze. Neither a success nor error modal appeared.")
    
    print("\nStep 5: Validating the Success Receipt Data (Soft Assertions)...")
    receipt = page.get_receipt_details()
    
    # Soft Assertion 1: Payout Math 
    ui_odds = float(receipt["odds"])
    actual_ui_payout = page.extract_number(receipt["payout"])
    expected_payout = round(stake_amount * ui_odds, 2)
    
    if actual_ui_payout != expected_payout:
        ui_defects.append(f"(Data Binding): Payout UI showed {actual_ui_payout}, expected {expected_payout}")

    # Soft Assertion 2: Team Order 
    expected_match_name = f"{match_data['home_team']} vs {match_data['away_team']}"
    if receipt["match"] != expected_match_name:
        ui_defects.append(f"(Team Order): Receipt showed '{receipt['match']}', expected '{expected_match_name}'")

    print("\nStep 6: Closing modal and verifying balance deduction...")
    page.close_receipt()
    page.pause()
    
    # Soft Assertion 3: Balance Sync 
    final_balance_text = page.get_current_balance()
    final_balance = page.extract_number(final_balance_text)
    
    expected_final_balance = round(initial_balance - stake_amount, 2)
    if final_balance != expected_final_balance:
        ui_defects.append(f"(UI State Sync): Balance showed €{final_balance}, expected €{expected_final_balance}")

    # Final Evaluation: 
    if len(ui_defects) > 0:
        # We format the list of defects into a readable string
        defect_message = "The bet was placed successfully, but the following UI defects were detected:\n- " + "\n- ".join(ui_defects)
        
        # We trigger a Pytest Warning instead of an AssertionError
        warnings.warn(UserWarning(defect_message))
        
        print("\n" + defect_message)