
with open("ocs_ai_answerer_advanced.py", "r", encoding="utf-8", newline="") as f:
    content = f.read()
nl = "\r\n"

# 4. Comprehension prompt improvements
old = """    @staticmethod
    def _build_completion_prompt(question: str) -> str:
        """构建填空题prompt"""
        return f"""你是一个专业的在线考试答题助手，请严格按照要求回答。

【题目类型】填空题

【题目】
{question}

【回答要求】
1. 给出准确、简洁的答案
2. 如果有多个空，用井号#分隔
3. 不要添加任何解释或额外文字
4. 无法确定时，根据上下文推断最合理的答案

【示例】
如果题目有两个空，答案分别是"北京"和"上海"，则输出：北京#上海

现在请回答上述题目：""""""

new = """    @staticmethod
    def _build_completion_prompt(question: str) -> str:
        """构建填空题prompt"""
        blank_count = len(re.findall(r"_{2,}|（）|\(\)", question)) or 1
        has_letter_opts = bool(re.search(r"[（(][A-Ha-h][）)]", question))
        has_slash_opts = bool(re.search(r"[（(][^）)]+/[^）)]+[）)]", question))
        hints = []
        if blank_count > 1:
            hints.append("题目有 " + str(blank_count) + " 个空，答案用#分隔")
        else:
            hints.append("只填一个答案")
        if has_letter_opts:
            hints.append("括号内有字母选项，从中选择")
        if has_slash_opts:
            hints.append("括号内有选项如（早/晚），从中选择")
        hints.append("多个空用#分隔，无法确定时根据上下文推断，绝不返回空答案")
        hint = "。".join(hints) + "。"
        return f"""你是一个专业的在线考试答题助手，请严格按照要求回答。

【题目类型】填空题

【题目】
{question}

【回答要求】
{hint}

【示例】
如果题目有两个空，答案分别是"北京"和"上海"，则输出：北京#上海

现在请回答上述题目：""""""

if old in content:
    content = content.replace(old, new)
    print("4. Completion prompt updated")
else:
    print("4. Pattern not found")

# 5. Question truncation
old = "def ai_answer(question: str, options: List[str], q_type: str"
new = "MAX_QUESTION_LEN = 2000\n\n\ndef ai_answer(question: str, options: List[str], q_type: str"
content = content.replace(old, new)
old = "    if not question:\n        return None, None, None, \"题目为空\""
new = "    if not question:\n        return None, None, None, \"题目为空\"\n    if len(question) > MAX_QUESTION_LEN:\n        question = question[:MAX_QUESTION_LEN] + \"...\""
content = content.replace(old, new)
print("5. Question truncation added")

with open("ocs_ai_answerer_advanced.py", "w", encoding="utf-8", newline="") as f:
    f.write(content)
print("Done")
