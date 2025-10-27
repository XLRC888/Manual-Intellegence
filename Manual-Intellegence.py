print("Manual Intellegence V1 Main Release")

import time
import re
import string

waiting_for_mood = None

def normalize(text: str) -> str:
    text = text.lower().strip()

    # abbrevations
    rep = {
        "how's": "hows",
        "hows": "hows",
        "what's": "whats",
        "whats": "whats",
        "who's": "whos",
        "whos": "whos",
        "ya": "your",
        "ur": "your",
        "u": "your",
        "yall": "you",
        "y'all": "you",
    }
    for k, v in rep.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text)

    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    text = re.sub(r"\s+", " ", text).strip()
    return text

def matches_any(patterns, text):
    return any(re.search(p, text) for p in patterns)

def evaluate_math_expression(text):
    patterns = [
        r'(\d+)\s*([\+\-\*/])\s*(\d+)',  # 2+2, 5 * 3
        r'(\d+)\s*(plus|minus|times|divided by)\s*(\d+)'  # 2 plus 2, 10 divided by 2
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            num1, op, num2 = match.groups()
            num1, num2 = int(num1), int(num2)
            if op in ['+', 'plus']:
                return num1 + num2
            elif op in ['-', 'minus']:
                return num1 - num2
            elif op in ['*', 'times']:
                return num1 * num2
            elif op in ['/', 'divided by']:
                if num2 == 0:
                    return "Undefined)"
                return num1 / num2
    return None

while True:
    raw = input("You: ")
    ask = normalize(raw)

    math_result = evaluate_math_expression(raw)
    if math_result is not None:
        print(f"Bot: It's {math_result}")
        continue

    if waiting_for_mood:
        good_patterns = [
            r"\bgoo+d\b", r"\bfine+\b", r"\bwe+ll\b", r"\bgrea+t\b",
            r"\bok+\b", r"\bokay+\b", r"\bhapp+y\b"
        ]
        bad_patterns = [
            r"\bbad+\b", r"\bsad+\b", r"not good", r"\btire+d\b",
            r"\bunhapp+y\b", r"\bangr+y\b"
        ]

        if any(re.search(p, ask) for p in good_patterns):
            if waiting_for_mood == "how_are_you":
                print("Bot: Glad you're good!")
            elif waiting_for_mood == "how_was_day":
                print("Bot: Happy to hear your day was good!")
        elif any(re.search(p, ask) for p in bad_patterns):
            if waiting_for_mood == "how_are_you":
                print("Bot: Sorry to hear that. Hope you feel better soon!")
            elif waiting_for_mood == "how_was_day":
                print("Bot: Sorry your day wasn't great. Tomorrow is a new day!")
        else:
            print("Bot: Thanks for sharing!")

        waiting_for_mood = None
        continue

    bye_patterns = [r"\bbye\b", r"\bsee you\b", r"\bsee ya\b"]
    areureal_patterns = ["\b(?:are|r) (?:you|y|u|ya)", r"\breal\b"]
    hi_patterns = [r"\bhi\b", r"\bhello\b", r"\bhey\b"]
    how_are_patterns = [r"\bhow (?:are|r) (?:you|your|ya|u)\b"]
    how_day_patterns = [
        r"\bhows (?:your|ya|ur|u) day been\b",
        r"\bhow was (?:your|ya|ur|u) day\b",
        r"\bhow (?:is|was) (?:your|ya|ur|u) day\b"
    ]
    who_made_patterns = [r"\bwho made (?:you|y)\b", r"\bwho made y\b"]
    name_patterns = [r"\bwhat(?:'s|s)? your name\b", r"\bwhat is your name\b", r"\bwhats your name\b"]

    if matches_any(bye_patterns, ask):
        print("Bot: Bye!")
        time.sleep(3)
        break

    elif matches_any(hi_patterns, ask):
        print("Bot: Hello!")

    elif matches_any(how_are_patterns, ask):
        print("Bot: I'm doing well, thank you. What about you?")
        waiting_for_mood = "how_are_you"

    elif matches_any(who_made_patterns, ask):
        print("Bot: I was created by XlRC888.")

    elif matches_any(how_day_patterns, ask):
        print("Bot: It's been great, what about you?")
        waiting_for_mood = "how_was_day"

    elif matches_any(name_patterns, ask):
        print("Bot: I'm Manual Intelligence! I'm here to chat with you!")

    elif matches_any(areureal_patterns, ask):
        print("I am not a physical being, but I'm surely real!")

    elif "what can i ask y" in ask or "what can i do with y" in ask:
        print("Bot: You can ask me anything you think of! If I fail at answering your question correctly or just cannot answer it completely, that means my owner couldn't implement that feature to my dictionary yet. You can ask my owner, maybe they'll implement it in the next update!")
    else:
        print("Bot: I’m not sure how to respond to that.")
