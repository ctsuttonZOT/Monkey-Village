import urllib
import json
from urllib import request, error


class NinjaKiwiApi:

    def __init__(self, OAK):
        # OAK = Open Access Key, a token unique to a player.
        self.OAK = OAK

        # Endpoint: /btd6/save/:oakID
        self.monkey_money = None
        self.current_hero = None

        # Endpoint: /btd6/users/:userID
        self.name = None
        self.rank = None
        self.fav_monkey = None
        self.avatar_url = None
        self.followers = None
        self.bloons_popped = None
        self.games_played = None
        self.highest_round = None
        self.fav_hero = None
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
    
    def split_monkey_name(self, name:str) -> str:
        res = ''
        for i in name:
            if i.isupper():
                res += "*" + i
            else:
                res += i
        if res != name:
            name = res.split("*")
            name = ' '.join(name[1:])
        return name
    

    def load_data(self) -> None:
        url_userID = f"https://data.ninjakiwi.com/btd6/users/{self.OAK}"
        url_oakID = f"https://data.ninjakiwi.com/btd6/save/{self.OAK}"

        r_obj1 = self._download_url(url_userID)
        r_obj2 = self._download_url(url_oakID)

        self.name = r_obj1["body"]["displayName"]
        self.rank = r_obj1["body"]["rank"]
        self.fav_monkey = self.split_monkey_name(r_obj1["body"]["mostExperiencedMonkey"])
        self.avatar_url = r_obj1["body"]["avatarURL"]
        self.followers = r_obj1["body"]["followers"]
        self.bloons_popped = r_obj1["body"]["bloonsPopped"]["bloonsPopped"]
        self.highest_round = r_obj1["body"]["gameplay"]["highestRound"]
        fav_hero_name = [key for key in r_obj1["body"]["heroesPlaced"] if r_obj1["body"]["heroesPlaced"][key] == max(r_obj1["body"]["heroesPlaced"].values())]
        self.fav_hero = self.split_monkey_name(fav_hero_name[0])
        self.black_borders = r_obj1["body"]["_medalsSinglePlayer"]["CHIMPS-BLACK"]

        self.monkey_money = r_obj2["body"]["monkeyMoney"]
        self.current_hero = self.split_monkey_name(r_obj2["body"]["primaryHero"])
    
    def valid_oak_check(self) -> bool:
        test_url = f"https://data.ninjakiwi.com/btd6/users/{self.OAK}"
        r_obj = self._download_url(test_url)

        # If error is null, oak is valid
        if r_obj["error"]:
            return False
        return True
