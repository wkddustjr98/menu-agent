import requests

from config import API_URL


class MenuAPI:

    def __init__(self):

        self.url = API_URL

    def get_menu(
        self,
        campus: str,
        cafeteriaSeq: str,
        mealType: str,
        ymd: str,
    ):

        payload = {

            "campus": campus,
            "cafeteriaSeq": cafeteriaSeq,
            "mealType": mealType,
            "ymd": ymd

        }

        response = requests.post(
            self.url,
            data=payload,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data.get("menuList", [])