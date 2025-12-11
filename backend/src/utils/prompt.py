prompt = ""


def get_prompt(prompt_md: str = "./readme.md") -> str:
    global prompt

    if prompt == "":
        with open(file=prompt_md, mode="r", encoding="utf-8") as f:
            prompt = f.read()

    return prompt
