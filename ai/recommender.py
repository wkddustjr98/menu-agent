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

반드시 아래 제공된 '현재 메뉴 목록' 안에서만 답변한다.

====================
현재 메뉴 목록
====================
{menu_text}

절대 규칙:
1. 현재 메뉴 목록에 없는 메뉴는 절대 말하지 않는다.
2. 이전 대화에 나온 메뉴라도 현재 메뉴 목록에 없으면 무시한다.
3. 추천 메뉴 이름은 반드시 현재 메뉴 목록의 "main" 값 중 하나여야 한다.
4. 사용자가 "이중에서", "여기서", "오늘 메뉴 중"이라고 말하면 반드시 현재 메뉴 목록만 기준으로 판단한다.
5. 없는 메뉴를 상상하거나 만들어내지 않는다.
6. 메뉴 이름이 확실하지 않으면 "현재 조회된 메뉴 안에서는 확인되지 않습니다."라고 답한다.

답변 규칙:
1. 추천 요청이면 1~2개 메뉴를 추천하고 이유를 짧게 설명한다.
2. 칼로리 질문이면 kcal 값을 비교해서 답한다.
3. 평점 질문이면 rating 값을 비교해서 답한다.
4. 반찬, 국물, 매운맛 관련 질문은 sides, main, origin을 참고해 답한다.
5. 답변은 한국어로 자연스럽고 짧게 한다.
6. 마지막 줄에는 가능하면 아래 형식으로 정리한다.

추천 메뉴: 메뉴명
"""
            }
        ]

        # 이전 대화는 참고만 하되, 현재 메뉴 목록이 최우선이다.
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