print("Manual Intellegence V1.2")

# for anyone reading this, remember: "if it works, dont touch it"

import math
import random
import time
import re
import string

waiting_for_mood = None

def normalize(text: str) -> str:
    text = text.lower().strip()

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

    text = text.translate(str.maketrans("", "", string.punctuation))

    text = re.sub(r"\s+", " ", text).strip()
    return text

def matches_any(patterns, text):
    return any(re.search(p, text) for p in patterns)

def evaluate_math_expression(text):
    s = text.lower()
    s = s.replace('divided by', '/').replace('plus', '+').replace('minus', '-').replace('times', '*')
    s = re.sub(r'\bx\b', '*', s)
    s = s.replace(',', ' ')

    s = re.sub(r'[^0-9\.\+\-\*\/\(\) ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()

    if not re.search(r'\d', s) or not re.search(r'[\+\-\*\/]', s):
        return None

    import ast

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op = node.op
            if isinstance(op, ast.Add):
                return left + right
            if isinstance(op, ast.Sub):
                return left - right
            if isinstance(op, ast.Mult):
                return left * right
            if isinstance(op, ast.Div):
                return left / right
            raise ValueError("Unsupported operator")
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.UAdd):
                return +_eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -_eval(node.operand)
            raise ValueError("Unsupported unary operator")
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Non-numeric constant")
        if node.__class__.__name__ == 'Num':
            val = getattr(node, 'n', None)
            if isinstance(val, (int, float)):
                return val
            raise ValueError("Non-numeric constant")
        raise ValueError("Unsupported expression")

    try:
        node = ast.parse(s, mode='eval')
        result = _eval(node)
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result
    except ZeroDivisionError:
        return "Undefined)"
    except Exception:
        return None

while True:
    raw = input("You: ")
    ask = normalize(raw)

    math_result = evaluate_math_expression(raw)
    if math_result is not None:
        print(f"Bot: It's {math_result}")
        continue

    if waiting_for_mood:
        good_patterns = "good", "great", "fine", "well", "happy", "awesome", "fantastic", "excellent", "amazing", "cool"
        bad_patterns = "bad", "sad", "not good", "terrible", "awful", "horrible", "unhappy", "depressed", "angry", "upset"
        
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

    bye_patterns = "bye", "see y", "goodbye", "exit", "quit", "farewell"
    areureal_patterns = "are you real", "are yu real", "are u real", "are ya real"
    hi_patterns = "hello", "hey", "helo"
    how_are_patterns = "how are you", "how r you", "how are u", "how r u", "how is you", "how is u"
    how_day_patterns = "hows your day been", "how was your day", "how is your day", "hows ya day been", "how was ya day", "how is ya day", "hows ur day been", "how was ur day", "how is ur day", "hows u day been", "how was u day", "how is u day"
    who_made_patterns = "who made y", "whos your owner", "who's your owner", "whos yo owner", "who's yo owner", "whos ya owner", "who's ya owner"
    name_patterns = "whats your name", "what is your name", "what's your name", "who are you", "introduce yourself", "who r y", "who r u", "whats yo name"
    joke_patterns = "tell me a joke", "make me laugh", "joke"
    joke_answers = (
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the math book look sad? Because it had too many problems!",
        "Why did the computer show up at work late? It had a hard drive!",
        "Why don't programmers like nature? Too many bugs.",
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "How do you organize a space party? You planet.",
        "Why was the broom late? It swept in!",
        "Why did the chicken join a band? Because it had the drumsticks!",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why did the coffee file a police report? It got mugged.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "How does a penguin build its house? Igloos it together.",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
        "What do you call a factory that makes okay products? A satisfactory.",
        "Why did the cookie go to the hospital? Because it felt crummy.",
        "Why did the picture go to jail? Because it was framed.",
        "How do you make holy water? You boil the hell out of it.",
        "Why did the computer get cold? It left its Windows open.",
        "Why was the math lecture so long? The professor kept going off on a tangent.",
        "Why did the physics teacher break up with the biology teacher? There was no chemistry.",
        "How many programmers does it take to change a light bulb? None — that's a hardware problem."
    )
    if matches_any(bye_patterns, ask):
        print("Bot: Bye!")
        time.sleep(3)
        break

    elif matches_any(hi_patterns, ask):
        print("Bot: Hello!")
    elif raw.lower() == "hi":
        print("Bot: Hello!")

    elif matches_any(how_are_patterns, ask):
        print("Bot: I'm doing well, thank you. What about you?")
        waiting_for_mood = "how_are_you"

    elif matches_any(who_made_patterns, ask) or "who made y" in ask:
        print("Bot: I was created by XlRC888.")

    elif matches_any(how_day_patterns, ask):
        print("Bot: It's been great, what about you?")
        waiting_for_mood = "how_was_day"

    elif matches_any(name_patterns, ask):
        print("Bot: I'm Manual Intelligence! I'm here to chat with you!")

    elif "time is it" in ask or "current time" in ask or "what's the time" in ask or "whats the time" in ask or "what is the time" in ask:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Bot: The current time is {current_time}")

    elif "date is it" in ask or "current date" in ask or "what's the date" in ask or "whats the date" in ask or "what is the date" in ask:
        current_date = time.strftime("%Y-%m-%d", time.localtime())
        print(f"Bot: The current date is {current_date}")

    elif matches_any(areureal_patterns, ask):
        print("I am not a physical being, but I'm surely real!")

    elif "what can i ask y" in ask or "what can i do with y" in ask or "what can i do w y" in ask:
        print("Bot: You can ask me anything you think of! If I fail at answering your question correctly or just cannot answer it completely, that means my owner couldn't implement that feature to my dictionary yet. You can ask my owner, maybe they'll implement it in the next update!")

    elif "thank you" in ask or "thanks" in ask:
        print("Bot: You're welcome!")

    elif matches_any(joke_patterns, ask):
        print("Bot: " + random.choice(joke_answers))

    elif "lol" in ask or "lmao" in ask or "haha" in ask or "hehe" in ask:
        print("Bot: Glad you found that funny!")

    else:
        print("Bot: I’m not sure how to respond to that.")