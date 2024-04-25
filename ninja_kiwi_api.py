import urllib
import json
from urllib import request, error


class NinjaKiwiApi:

    def __init__(self, OAK):
        # OAK = Open Access Key, a token unique to a player.
        self.OAK = OAK
        # Endpoint: /btd6/save/:oakID
        self.games_played = None
        self.monkey_money = None
        self.xp = None
        self.rank = None
        self.trophies = None
        self.current_hero = None
        self.highest_round = None
        self.daily_challenges_completed = None

        # Endpoint: /btd6/users/:userID
        self.name = None
        self.fav_monkey = None
        self.avatar = None
        self.followers = None
        self.bloons_popped = None
        self.black_borders = None


    def _download_url(self, url: str) -> dict:
        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print(f'Status code: {e}')
            raise e

        except ConnectionError:
            print("Local internet connection has been lost.")
            raise ConnectionError

        except json.JSONDecodeError:
            print("Invalid JSON formatting from the remote API.")
            raise json.JSONDecodeError

        finally:
            if response is not None:
                response.close()

        return r_obj
    

    def load_data(self):
        pass