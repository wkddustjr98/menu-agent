from datetime import datetime, timedelta

from config import CAMPUSES, CAFETERIAS, MEALS
from models.dto import ParsedQuery


class RuleParser:

    def parse(self, text: str, session: dict | None = None):

        if session is None:
            session = {}

        original = text.strip()
        lower = original.lower()

        raw_campus = self._find_campus(lower)
        raw_cafeteria = self._find_cafeteria(lower)
        raw_meal = self._find_meal(lower)
        raw_date = self._find_date(lower)

        if raw_cafeteria and raw_campus is None:
            raw_campus = self._campus_from_cafeteria(raw_cafeteria)

        has_new_menu_info = (
            raw_campus is not None
            or raw_cafeteria is not None
            or raw_meal is not None
            or self._contains_date(lower)
        )

        if has_new_menu_info:
            intent = "menu"
        elif self._is_recommend_or_question(lower):
            intent = "recommend" if "menus" not in session else "followup"
        elif "menus" in session:
            intent = "followup"
        else:
            intent = "menu"

        last_query = session.get("query", {})

        campus = raw_campus or last_query.get("campus")
        cafeteria = raw_cafeteria or last_query.get("cafeteria_seq")
        meal = raw_meal or last_query.get("meal_type") or "LN"
        ymd = raw_date or last_query.get("ymd") or self._today()

        return ParsedQuery(
            intent=intent,
            campus=campus,
            cafeteria_seq=cafeteria,
            meal_type=meal,
            ymd=ymd,
            original_text=original
        )

    def _find_campus(self, text):

        for name, code in CAMPUSES.items():
            if name.lower() in text:
                return code

        return None

    def _find_cafeteria(self, text):

        for _, info in CAFETERIAS.items():
            for alias in info["aliases"]:
                if alias.lower() in text:
                    return info["seq"]

        return None

    def _campus_from_cafeteria(self, seq):

        for _, info in CAFETERIAS.items():
            if info["seq"] == seq:
                return info["campus"]

        return None

    def _find_meal(self, text):

        for name, code in MEALS.items():
            if name in text:
                return code

        return None

    def _find_date(self, text):

        d = datetime.now()

        if "내일" in text:
            d += timedelta(days=1)
            return d.strftime("%Y%m%d")

        if "모레" in text:
            d += timedelta(days=2)
            return d.strftime("%Y%m%d")

        if "오늘" in text:
            return d.strftime("%Y%m%d")

        return None

    def _today(self):

        return datetime.now().strftime("%Y%m%d")

    def _contains_date(self, text):

        return any(k in text for k in ["오늘", "내일", "모레"])

    def _is_recommend_or_question(self, text):

        keywords = [
            "추천",
            "추천해",
            "추천해줘",
            "뭐먹",
            "뭐 먹",
            "먹을까",
            "먹지",
            "골라",
            "맛있는",
            "칼로리",
            "낮아",
            "높아",
            "제일",
            "가장",
            "국물",
            "매운",
            "든든",
            "다이어트",
            "평점",
            "별점",
            "어때",
            "뭐가",
            "무엇",
            "왜",
            "비교"
        ]

        return any(k in text for k in keywords)