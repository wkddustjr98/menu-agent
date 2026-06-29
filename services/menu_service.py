from api.menu_api import MenuAPI
from ai.parser import RuleParser
from ai.recommender import Recommender
from services.formatter import Formatter


class MenuService:

    def __init__(self):
        self.parser = RuleParser()
        self.api = MenuAPI()
        self.formatter = Formatter()
        self.recommender = Recommender()

    async def process(self, message: str, session: dict):

        parsed = self.parser.parse(message, session)

        print("PARSED:", parsed)

        # ==================================================
        # 1. 메뉴 조회
        # ==================================================
        if parsed.intent == "menu":

            if parsed.campus is None:
                return {
                    "type": "ask",
                    "question": "어느 캠퍼스인가요?\n(이천 / 청주 / 분당)"
                }

            if parsed.cafeteria_seq is None:
                return {
                    "type": "ask",
                    "question": "어느 식당인가요?"
                }

            if parsed.meal_type is None:
                parsed.meal_type = "LN"

            if parsed.ymd is None:
                raise Exception("날짜 정보를 찾을 수 없습니다.")

            query = {
                "campus": parsed.campus,
                "cafeteria_seq": parsed.cafeteria_seq,
                "meal_type": parsed.meal_type,
                "ymd": parsed.ymd
            }

            raw_menus = self.api.get_menu(
                campus=query["campus"],
                cafeteriaSeq=query["cafeteria_seq"],
                mealType=query["meal_type"],
                ymd=query["ymd"]
            )

            menus = self.formatter.format(raw_menus)

            # 핵심:
            # session을 완전히 새 조회 결과로 덮어쓴다.
            session.clear()
            session["query"] = query
            session["menus"] = menus
            session["history"] = []

            print("NEW QUERY:", session["query"])
            print("NEW MENUS:", [m.get("main") for m in session["menus"]])

            return {
                "type": "menu",
                "query": session["query"],
                "menus": session["menus"]
            }

        # ==================================================
        # 2. 추천 / 후속 질문
        # ==================================================
        if parsed.intent in ["recommend", "followup"]:

            menus = session.get("menus", [])
            query = session.get("query", {})
            history = session.get("history", [])

            if not menus:
                return {
                    "type": "ask",
                    "question": "먼저 메뉴를 조회해주세요.\n예: 이천 SKY 점심"
                }

            print("ASK AI QUERY:", query)
            print("ASK AI WITH MENUS:", [m.get("main") for m in menus])

            answer = self.recommender.chat(
                user_message=message,
                menus=menus,
                history=history
            )

            session["history"] = history

            return {
                "type": "recommend",
                "recommendation": answer,
                "menus": menus,
                "query": query
            }

        return {
            "type": "ask",
            "question": "무슨 말씀인지 이해하지 못했습니다."
        }