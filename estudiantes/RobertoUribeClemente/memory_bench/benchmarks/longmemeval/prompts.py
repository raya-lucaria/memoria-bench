"""Fixed prompts. The judge templates are copied verbatim from the official
LongMemEval src/evaluation/evaluate_qa.py (xiaowu0162/LongMemEval)."""

READER = (
    "I will give you several history chats between you and a user. Please answer the "
    "question based on the relevant chat history. Answer concisely. If the history does "
    "not contain the answer, say you don't know.\n\n"
    "History Chats:\n\n{history}\n\nCurrent Date: {date}\nQuestion: {question}\nAnswer:"
)


def history(item: dict, session_idx: list[int]) -> str:
    blocks = []
    # Shown in chronological order, as in the official reader setup.
    for n, si in enumerate(sorted(session_idx), 1):
        turns = "\n".join(f"{t['role']}: {t['content']}" for t in item["haystack_sessions"][si])
        blocks.append(f"### Session {n}:\nSession Date: {item['haystack_dates'][si]}\n"
                      f"Session Content:\n{turns}")
    return "\n\n".join(blocks)


_BASE = ("I will give you a question, a correct answer, and a response from a model. Please "
         "answer yes if the response contains the correct answer. Otherwise, answer no. ")
_STEPS = ("If the response is equivalent to the correct answer or contains all the intermediate "
          "steps to get the correct answer, you should also answer yes. If the response only "
          "contains a subset of the information required by the answer, answer no. ")
_TAIL = ("\n\nQuestion: {}\n\nCorrect Answer: {}\n\nModel Response: {}\n\n"
         "Is the model response correct? Answer yes or no only.")


def judge(qtype: str, question: str, answer: str, response: str, abstention: bool) -> str:
    if abstention:
        t = ("I will give you an unanswerable question, an explanation, and a response from a "
             "model. Please answer yes if the model correctly identifies the question as "
             "unanswerable. The model could say that the information is incomplete, or some "
             "other information is given but the asked information is not.\n\nQuestion: {}\n\n"
             "Explanation: {}\n\nModel Response: {}\n\nDoes the model correctly identify the "
             "question as unanswerable? Answer yes or no only.")
    elif qtype in ("single-session-user", "single-session-assistant", "multi-session"):
        t = _BASE + _STEPS + _TAIL
    elif qtype == "temporal-reasoning":
        t = (_BASE + _STEPS + "In addition, do not penalize off-by-one errors for the number of "
             "days. If the question asks for the number of days/weeks/months, etc., and the model "
             "makes off-by-one errors (e.g., predicting 19 days when the answer is 18), the "
             "model's response is still correct. " + _TAIL)
    elif qtype == "knowledge-update":
        t = (_BASE + "If the response contains some previous information along with an updated "
             "answer, the response should be considered as correct as long as the updated answer "
             "is the required answer." + _TAIL)
    elif qtype == "single-session-preference":
        t = ("I will give you a question, a rubric for desired personalized response, and a "
             "response from a model. Please answer yes if the response satisfies the desired "
             "response. Otherwise, answer no. The model does not need to reflect all the points "
             "in the rubric. The response is correct as long as it recalls and utilizes the "
             "user's personal information correctly.\n\nQuestion: {}\n\nRubric: {}\n\nModel "
             "Response: {}\n\nIs the model response correct? Answer yes or no only.")
    else:
        raise ValueError(qtype)
    return t.format(question, answer, response)
