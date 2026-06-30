from uuid import uuid4

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

        # 서버 메모리에 실제 대화 상태 저장
        self.store = {}

    def _get_sid(self, session: dict):
        if "sid" not in session:
            session["sid"] = str(uuid4())

        return session["sid"]

    def _get_state(self, sid: str):
        if sid not in self.store:
            self.store[sid] = {
                "query": {},
                "menus": [],
                "history": []
            }

        return self.store[sid]

    async def process(self, message: str, session: dict):

        sid = self._get_sid(session)
        state = self._get_state(sid)

        parsed = self.parser.parse(message, state)

        print("SID:", sid)
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

            # 쿠키 session에는 sid만 저장하고,
            # 실제 menus/history는 서버 메모리에 저장
            self.store[sid] = {
                "query": query,
                "menus": menus,
                "history": []
            }

            print("NEW QUERY:", query)
            print("NEW MENUS:", [m.get("main") for m in menus])

            return {
                "type": "menu",
                "query": query,
                "menus": menus
            }

        # ==================================================
        # 2. 추천 / 후속 질문
        # ==================================================
        if parsed.intent in ["recommend", "followup"]:

            state = self._get_state(sid)

            menus = state.get("menus", [])
            query = state.get("query", {})
            history = state.get("history", [])

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

            state["history"] = history

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