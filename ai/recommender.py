import json

from ai.client import client


class Recommender:

    def chat(
        self,
        user_message: str,
        menus: list,
        history: list | None = None
    ):

        if history is None:
            history = []

        menu_text = json.dumps(
            menus,
            ensure_ascii=False,
            indent=2
        )

        messages = [
            {
                "role": "system",
                "content": f"""
너는 SK하이닉스 사내식당 메뉴 추천 AI이다.

반드시 아래 제공된 메뉴 목록 안에서만 답변한다.

====================
오늘 메뉴
====================
{menu_text}

규칙:
1. 없는 메뉴를 절대 만들지 않는다.
2. 메뉴 이름은 제공된 이름 그대로 사용한다.
3. 사용자가 추천을 요청하면 1~2개 메뉴를 추천하고 이유를 설명한다.
4. 사용자가 칼로리, 평점, 반찬, 국물, 매운맛 등을 물으면 메뉴 데이터 안에서만 판단한다.
5. 이전 대화 문맥을 참고하되, 메뉴 목록 밖의 음식은 말하지 않는다.
6. 답변은 한국어로 자연스럽고 짧게 한다.
7. 마지막에 가능하면 "추천 메뉴: 메뉴명" 형식으로 정리한다.
"""
            }
        ]

        messages.extend(history)

        messages.append({
            "role": "user",
            "content": user_message
        })

        response = client.responses.create(
            model="gpt-5",
            input=messages
        )

        answer = response.output_text.strip()

        history.append({
            "role": "user",
            "content": user_message
        })

        history.append({
            "role": "assistant",
            "content": answer
        })

        if len(history) > 10:
            history[:] = history[-10:]

        return answer