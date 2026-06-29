import json

from openai import APIError

from ai.client import client
from ai.prompts import SYSTEM_PROMPT


class NLU:

    def understand(self, message: str):

        try:

            response = client.responses.create(

                model="gpt-5.5",

                input=[

                    {
                        "role":"system",
                        "content":SYSTEM_PROMPT
                    },

                    {
                        "role":"user",
                        "content":message
                    }

                ]

            )

            text = response.output_text.strip()

            return json.loads(text)

        except json.JSONDecodeError:

            raise Exception("GPT가 올바른 JSON을 반환하지 않았습니다.")

        except APIError as e:

            raise Exception(f"OpenAI 오류: {e}")