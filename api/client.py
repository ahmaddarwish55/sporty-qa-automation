import requests

class SportyApiClient:
    """
    API Object Model for the Sporty Betting Backend.
    Handles all raw HTTP requests and returns response objects.
    """
    def __init__(self, base_url="https://qae-assignment-tau.vercel.app", user_id="candidate-PR1EPAagsI"):
        self.base_url = f"{base_url}/api"
        self.headers = {
            "x-user-id": user_id,
            "Content-Type": "application/json"
        }

    def get_balance(self):
        """Fetches the user's current balance."""
        url = f"{self.base_url}/balance"
        return requests.get(url, headers=self.headers)

    def place_bet(self, match_id, selection, stake):
        """Attempts to place a bet."""
        url = f"{self.base_url}/place-bet"
        payload = {
            "matchId": match_id,
            "selection": selection,
            "stake": stake
        }
        return requests.post(url, json=payload, headers=self.headers)