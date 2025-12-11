from os import getenv
from openai import OpenAI
from cozepy import (
    COZE_CN_BASE_URL,
    Coze,
    TokenAuth,
    Message,
    ChatEventType,
)
from typing import Dict, Any
from .utils import get_prompt
from json import loads
from .constants import REQUIRED_PROBLEM_FIELDS, DEFAULT_PROBLEM

prompt = get_prompt()

# ByteDance Coze
coze_api_token = getenv("COZE_API_TOKEN")
coze_bot_id = getenv("COZE_BOT_ID")
coze_user_id = getenv("COZE_USER_ID")

if coze_api_token is None:
    raise ValueError("COZE_API_TOKEN is None")
coze_client = Coze(auth=TokenAuth(token=coze_api_token), base_url=COZE_CN_BASE_URL)

# Aliyun
aliyun_api_key = getenv("ALIYUN_API_KEY")
aliyun_base_url = getenv("ALIYUN_BASE_URL")
aliyun_model = getenv("ALIYUN_MODEL", "deepseek-r1")

if aliyun_api_key is None or aliyun_base_url is None:
    raise ValueError("ALIYUN_API_KEY or ALIYUN_BASE_URL is None")

aliyun_client = OpenAI(
    api_key=aliyun_api_key,
    base_url=aliyun_base_url,
)


def get_message_content(level: str) -> str:
    return f"Please generate a programming problem with a difficulty level of {level}"


def check_problem_fields(problem: Dict[str, Any]) -> bool:
    for field in REQUIRED_PROBLEM_FIELDS:
        if field not in problem:
            return False
    return True


def generate_problem_by_coze(level: str) -> Dict[str, Any]:
    try:
        if coze_bot_id is None or coze_user_id is None:
            raise ValueError("COZE_BOT_ID, or COZE_USER_ID is None")

        content = prompt + get_message_content(level)
        md_str = ""
        problem = DEFAULT_PROBLEM

        for event in coze_client.chat.stream(
            auto_save_history=False,
            bot_id=coze_bot_id,
            user_id=coze_user_id,
            additional_messages=[
                Message.build_user_question_text(
                    content,
                    # meta_data={"level": level}
                ),
            ],
            # custom_variables={"level": level},
            # meta_data={"level": level},
            # parameters={"level": level},
        ):
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                if event.message is not None:
                    md_str += event.message.content

            if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                # Problem
                json_str = md_str.removeprefix("```json\n").removesuffix("```").strip()
                problem = loads(json_str)
                if not check_problem_fields(problem):
                    raise ValueError("check_problem_fields(problem) == False")

                # Token count
                if event.chat is not None and event.chat.usage is not None:
                    print("\nToken count:", event.chat.usage.token_count)
                break

        return problem

    except Exception as e:
        print(e)
        return DEFAULT_PROBLEM


def generate_problem_by_aliyun(level: str) -> Dict[str, Any]:
    try:
        problem = DEFAULT_PROBLEM
        completion = aliyun_client.chat.completions.create(
            model=aliyun_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": prompt + get_message_content(level)},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            extra_body={"enable_thinking": False},
        )
        json_str = completion.choices[0].message.content
        if json_str is None:
            raise ValueError("json_str is None")

        problem = loads(json_str)
        if not check_problem_fields(problem):
            raise ValueError("check_problem_fields(problem) == False")

        return problem

    except Exception as e:
        print(e)
        return DEFAULT_PROBLEM


if __name__ == "__main__":
    """
    Usage:
        cd ./backend && python -m src.generate
    """
    problem_by_coze = generate_problem_by_coze(level="easy")
    print("Problem by Coze:", problem_by_coze)

    problem_by_aliyun = generate_problem_by_aliyun(level="easy")
    print("Problem by Aliyun:", problem_by_aliyun)
