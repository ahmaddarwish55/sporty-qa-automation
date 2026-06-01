from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class MainBettingPage(BasePage):
    """
    Page Object for the main Sporty betting dashboard, Bet Slip, and Success Modal.
    """
    
    # --- LOCATORS ---
    # Header
    HEADER_BALANCE = (By.ID, "header-balance")
    
    # Bet Slip
    STAKE_INPUT = (By.ID, "bet-slip-stake-input")
    TOTAL_STAKE = (By.ID, "bet-slip-total-stake")
    POTENTIAL_PAYOUT = (By.ID, "bet-slip-potential-payout")
    PLACE_BET_BUTTON = (By.ID, "bet-slip-place-bet")
    
    # Success Modal
    MODAL_MATCH = (By.ID, "modal-success-match")
    MODAL_STAKE = (By.ID, "modal-success-stake")
    MODAL_ODDS = (By.ID, "modal-success-odds")
    MODAL_PAYOUT = (By.ID, "modal-success-payout")
    MODAL_CLOSE_BTN = (By.ID, "modal-success-close")

    def __init__(self, driver):
        super().__init__(driver)

    # --- ACTIONS ---
    
    def get_current_balance(self):
        """Fetches the user's balance string from the top header."""
        return self.get_text(self.HEADER_BALANCE)

    def select_match_outcome(self, match_id, selection):
        """Dynamically locates and clicks the correct odds button."""
        button_id = f"odds-{match_id}-{selection.lower()}"
        dynamic_locator = (By.ID, button_id)
        
        element = self.find(dynamic_locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.click(dynamic_locator)

    def enter_stake(self, amount):
        """Types the bet amount into the Bet Slip."""
        self.type_text(self.STAKE_INPUT, str(amount))

    def get_bet_slip_totals(self):
        """Retrieves the Total Stake and Potential Payout from the slip."""
        return {
            "stake": self.get_text(self.TOTAL_STAKE),
            "payout": self.get_text(self.POTENTIAL_PAYOUT)
        }

    def click_place_bet(self):
        """Clicks the final Place Bet button."""
        self.click(self.PLACE_BET_BUTTON)
        
    def get_receipt_details(self):
        """Extracts the data from the Success Modal."""
        return {
            "match": self.get_text(self.MODAL_MATCH),
            "stake": self.get_text(self.MODAL_STAKE),
            "odds": self.get_text(self.MODAL_ODDS),
            "payout": self.get_text(self.MODAL_PAYOUT)
        }
        
    def close_receipt(self):
        """Clicks the primary Close button on the modal."""
        self.click(self.MODAL_CLOSE_BTN)

    def wait_for_receipt_modal(self):
        """Explicitly waits for the Success Modal to appear on screen."""
        # This stays here because self.MODAL_MATCH is unique to this page!
        self.find(self.MODAL_MATCH)    