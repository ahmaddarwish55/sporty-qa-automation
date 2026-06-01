import pytest

def test_insufficient_balance_bypass(api_client, test_data):
    """
    Test Case: TC-006 / BUG-007
    Validates that the API backend independently enforces ledger checks.
    """
    print("\nStep 1: Fetching current user balance...")
    balance_response = api_client.get_balance()
    
    assert balance_response.status_code == 200, "Failed to retrieve initial balance."
    current_balance = balance_response.json().get("balance", 0)
    print(f"Current Balance: €{current_balance}")
    
    print("\nStep 2: Calculating a malicious stake that respects API boundaries...")
    
    # If the user has €100 or more, we physically cannot test this without tripping the Max Stake rule.
    if current_balance >= 100.0:
        pytest.skip(f"Test skipped: Balance (€{current_balance}) is too high to isolate the insufficient funds bug without triggering the €100 max stake rule.")
        
    # Calculate a stake slightly higher than their balance
    malicious_stake = float(current_balance) + 10.0
    
    # CRITICAL FIX 1: Ensure we don't trip the €100 Maximum Stake validation
    if malicious_stake > 100.0:
        malicious_stake = 100.0 
        
    # CRITICAL FIX 2: Ensure we don't trip the €1 Minimum Stake validation (if balance is negative)
    if malicious_stake < 1.0:
        malicious_stake = 1.0
        
    # Round to 2 decimal places to match currency standards
    malicious_stake = round(malicious_stake, 2)
    
    print(f"Sending POST request with malicious stake: €{malicious_stake}...")
    
    bet_response = api_client.place_bet(
        match_id=test_data["matches"]["upcoming_valid_match"]["id"],  
        selection=test_data["selections"]["draw"],
        stake=malicious_stake
    )
    
    print("\nStep 3: Validating backend security response...")
    
    if bet_response.status_code == 200:
        pytest.fail(f"CRITICAL VULNERABILITY: API allowed wager exceeding balance! Response: {bet_response.text}")
    elif bet_response.status_code not in [400, 422]:
        pytest.fail(f"System Error: Expected 400 or 422, but got HTTP {bet_response.status_code}. Response: {bet_response.text}")
        
    print("Success: The API successfully blocked the invalid transaction.")