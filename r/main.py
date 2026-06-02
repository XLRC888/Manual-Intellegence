print("Manual Intellegence V9.0")

from terminal import run_terminal
import platform
import subprocess
import math
import ast
import random
import time
import re
import string
import webbrowser


waiting_for_mood = None
game_state = None
todos = []


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
    s = s.replace('divided by', '/').replace('plus', '+').replace('minus', '-').replace('times', '*').replace('power', '^').replace('to the', '^')
    s = re.sub(r'\bx\b', '*', s)
    s = s.replace(',', ' ')
    s = s.replace('^', '**')

    s = re.sub(r'[^0-9\.\+\-\*\/\(\)\* ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    
    if not re.search(r'\d', s) or not re.search(r'[\+\-\*\/]', s):
        return None
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
            if isinstance(op, ast.Pow):
                return left ** right
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


trivia_questions = [
    {"q": "What is the capital of France?", "a": "paris"},
    {"q": "What programming language is Manual Intellegence written in?", "a": "python"},
    {"q": "How many continents are there on Earth?", "a": "7"},
    {"q": "What planet is known as the Red Planet?", "a": "mars"},
    {"q": "What is the largest mammal in the world?", "a": "blue whale"},
    {"q": "What is the square root of 64?", "a": "8"},
    {"q": "What year did World War II end?", "a": "1945"},
    {"q": "What gas do plants absorb from the atmosphere?", "a": "carbon dioxide"},
    {"q": "What is the smallest prime number?", "a": "2"},
    {"q": "What element has the chemical symbol 'O'?", "a": "oxygen"},
    {"q": "How many sides does a hexagon have?", "a": "6"},
    {"q": "What is the freezing point of water in Celsius?", "a": "0"},
    {"q": "Who developed the Python programming language?", "a": "guido van rossum"},
    {"q": "What ocean is the largest on Earth?", "a": "pacific"},
    {"q": "How many bits are in a byte?", "a": "8"},
    {"q": "What is the currency of Japan?", "a": "yen"},
    {"q": "What organ pumps blood in the human body?", "a": "heart"},
    {"q": "What does CPU stand for?", "a": "central processing unit"},
    {"q": "What is the tallest mountain in the world?", "a": "mount everest"},
    {"q": "How many legs does a spider have?", "a": "8"},
]

eightball_responses = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
    "My reply is no.", "My sources say no.", "Outlook not so good.",
    "Very doubtful.",
]

rps_choices = ["rock", "paper", "scissors"]


def run_subcommand(cmd, args):
    cmd = cmd.lower()
    if cmd == "calc":
        a = args.replace("^", "**")
        try:
            return str(eval(a))
        except:
            return args
    elif cmd == "dice":
        m = re.match(r"(\d+)d(\d+)", args.lower())
        if m:
            return str(sum(random.randint(1, int(m.group(2))) for _ in range(min(int(m.group(1)), 100))))
        return str(random.randint(1, 6))
    elif cmd == "rand":
        p = args.split()
        if len(p) >= 2:
            try:
                return str(random.randint(int(p[0]), int(p[1])))
            except:
                pass
        return str(random.randint(1, 100))
    elif cmd == "flip":
        return str(random.randint(0, 1))
    elif cmd == "reverse":
        return args[::-1]
    elif cmd == "upper":
        return args.upper()
    elif cmd == "lower":
        return args.lower()
    elif cmd == "len":
        return str(len(args))
    elif cmd == "fib":
        try:
            n = int(args)
            if n <= 0:
                return "0"
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return str(a)
        except:
            return "0"
    elif cmd == "prime":
        try:
            n = int(args)
            if n < 2:
                return "false"
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return "false"
            return "true"
        except:
            return "false"
    elif cmd == "pick":
        items = args.split()
        return random.choice(items) if items else ""
    elif cmd == "name":
        pre = ["Cyber", "Neo", "Pixel", "Data", "Byte", "Code", "Syntax", "Logic", "Kernel", "Meta", "Quantum", "Vector", "Binary", "Digital", "Echo", "Flux", "Glitch", "Hyper", "Nova", "Proto"]
        suf = ["Bot", "X", "Zero", "Core", "Mind", "Byte", "Drone", "Pulse", "Wave", "Forge", "Node", "Shift", "Chip", "Ward", "Sync", "Labs", "Dex", "Hack", "Gen", "Kit"]
        return random.choice(pre) + random.choice(suf) + str(random.randint(1, 99))
    return args


def resolve_subcommands(text):
    while re.search(r'\(\$(\w+)\s*([^()]*)\)', text):
        text = re.sub(r'\(\$(\w+)\s*([^()]*)\)', lambda m: str(run_subcommand(m.group(1), m.group(2).strip())), text)
    return text


while True:
    raw = input("You: ")
    raw = resolve_subcommands(raw)
    ask = normalize(raw)
    math_result = evaluate_math_expression(raw)
    if math_result is not None:
        print(f"Bot: It's {math_result}")
        continue

    if waiting_for_mood:
        good_patterns = "good", "great", "fine", "well", "happy", "awesome", "fantastic", "excellent", "amazing", "cool", "wonderful", "lovely", "pretty good", "alright", "decent", "super", "not bad", "blessed", "perfect", "doing great", "managing"
        bad_patterns = "bad", "sad", "not good", "terrible", "awful", "horrible", "unhappy", "depressed", "angry", "upset", "shit", "crap", "rough", "tough", "struggling", "exhausted", "tired", "lonely", "frustrated", "anxious", "stressed", "miserable", "down", "crappy"
        
        if any(re.search(p, ask) for p in good_patterns):
            if waiting_for_mood == "how_are_you":
                print(random.choice(["Bot: Glad you're good!", "Bot: That's great to hear!", "Bot: Awesome, keep that energy!", "Bot: Love hearing that!", "Bot: Hell yeah, glad things are going well!", "Bot: Good vibes only! Happy for you!", "Bot: That's what I like to hear!"]))
            elif waiting_for_mood == "how_was_day":
                print(random.choice(["Bot: Happy to hear your day was good!", "Bot: Sounds like a solid day!", "Bot: Glad everything went well today!", "Bot: That's a win in my book!", "Bot: Good days are always worth celebrating!", "Bot: Heck yeah, glad today treated you right!"]))
        elif any(re.search(p, ask) for p in bad_patterns):
            if waiting_for_mood == "how_are_you":
                print(random.choice(["Bot: Sorry to hear that. Hope you feel better soon!", "Bot: That sucks, I hope things turn around!", "Bot: I'm here if you need to vent.", "Bot: Rough days happen. Take it easy on yourself.", "Bot: Sending good vibes your way.", "Bot: That's rough buddy. Want to talk about it?", "Bot: Life can be a pain sometimes. I get it."]))
            elif waiting_for_mood == "how_was_day":
                print(random.choice(["Bot: Sorry your day wasn't great. Tomorrow is a new day!", "Bot: Bad days don't last forever. Hang in there!", "Bot: That's a bummer. Hope tomorrow's better!", "Bot: Rough day huh? Treat yourself to something nice.", "Bot: Tomorrow has better things in store, trust me."]))
        else:
            print(random.choice(["Bot: Thanks for sharing!", "Bot: I appreciate you telling me!", "Bot: Good to know!", "Bot: Gotcha!", "Bot: Fair enough!"]))

        waiting_for_mood = None
        continue

    if game_state:
        mode = game_state["mode"]
        if mode == "rps":
            if ask in rps_choices:
                bot_choice = random.choice(rps_choices)
                user_choice = ask
                if user_choice == bot_choice:
                    print(f"Bot: I chose {bot_choice} too! It's a tie!")
                elif (user_choice == "rock" and bot_choice == "scissors") or (user_choice == "scissors" and bot_choice == "paper") or (user_choice == "paper" and bot_choice == "rock"):
                    game_state["wins"] += 1
                    print(f"Bot: I chose {bot_choice}. You win this round! Score: You {game_state['wins']} - {game_state['losses']} Me")
                else:
                    game_state["losses"] += 1
                    print(f"Bot: I chose {bot_choice}. I win this round! Score: You {game_state['wins']} - {game_state['losses']} Me")
                print("Bot: Play again? (rock/paper/scissors) or type 'quit' to stop.")
            elif ask in ["quit", "stop", "exit", "no", "done", "end"]:
                print(f"Bot: Thanks for playing! Final score: You {game_state['wins']} - {game_state['losses']} Me")
                game_state = None
            else:
                print("Bot: Choose Rock, Paper, or Scissors! (or type 'quit' to stop)")
            continue

        elif mode == "trivia":
            if ask in ["quit", "stop", "exit", "q", "end"]:
                print(f"Bot: Stopped. You got {game_state['score']} out of {len(trivia_questions)} correct!")
                game_state = None
                continue
            q_index = game_state["index"]
            if q_index >= len(trivia_questions):
                print(f"Bot: Trivia over! You got {game_state['score']} out of {len(trivia_questions)} correct!")
                game_state = None
                continue
            q_data = trivia_questions[q_index]
            if ask == q_data["a"] or ask.strip() == q_data["a"]:
                game_state["score"] += 1
                print(random.choice(["Bot: Correct!", "Bot: Right on!", "Bot: That's right!", "Bot: Nailed it!", "Bot: You got it!"]))
            else:
                print(f"Bot: Nope! The answer was: {q_data['a']}")
            game_state["index"] += 1
            if game_state["index"] >= len(trivia_questions):
                print(f"Bot: Trivia over! You got {game_state['score']} out of {len(trivia_questions)} correct!")
                game_state = None
            else:
                next_q = trivia_questions[game_state["index"]]
                print(f"Bot: Question {game_state['index'] + 1}: {next_q['q']}")
            continue

        elif mode == "guess":
            target = game_state["target"]
            max_num = game_state["max"]
            try:
                guess = int(raw)
                game_state["attempts"] += 1
                if guess == target:
                    print(f"Bot: Correct! The number was {target}. You got it in {game_state['attempts']} tries!")
                    game_state = None
                elif guess < target:
                    print(f"Bot: Higher! (attempt {game_state['attempts']})")
                else:
                    print(f"Bot: Lower! (attempt {game_state['attempts']})")
            except ValueError:
                if ask in ["quit", "stop", "exit", "give up"]:
                    print(f"Bot: The number was {target}. Better luck next time!")
                    game_state = None
                else:
                    print(f"Bot: Enter a number between 1 and {max_num}!")
            continue

    bye_patterns = "bye", "see y", "goodbye", "exit", "quit", "farewell", "later", "see ya", "see you", "take care", "gotta go", "im out", "i'm out", "peace", "cya", "adios", "sayonara", "catch y"
    areureal_patterns = "are you real", "are yu real", "are u real", "are ya real", "are you actually real", "are you a human", "are you a person", "are you sentient"
    hi_patterns = r"\bhello\b", r"\bhelo\b", r"\bhey\b", r"\bhi\b", r"\bsup\b", r"\byo\b", r"\bheyo\b", r"\bhowdy\b", r"\bgreetings\b", r"\bhii\b", r"\bheyy\b", r"\bhola\b", r"\bhiya\b", r"\bhey there\b"
    how_are_patterns = "how are you", "how r you", "how are u", "how r u", "how is you", "how is u", "how are you doing", "how are things", "how is it going", "how goes it", "how has your day been"
    how_day_patterns = "hows your day been", "how was your day", "how is your day", "hows ya day been", "how was ya day", "how is ya day", "hows ur day been", "how was ur day", "how is ur day", "hows u day been", "how was u day", "how is u day"
    who_made_patterns = "who made y", "whos your owner", "who's your owner", "whos yo owner", "who's yo owner", "whos ya owner", "who's ya owner", "who built y", "who programmed y", "who coded y", "who created y"
    name_patterns = "whats your name", "what is your name", "what's your name", "who are you", "introduce yourself", "who r y", "who r u", "whats yo name", "what should i call qy", "what do i call you"
    joke_patterns = "tell me a joke", "make me laugh", "joke", "crack me up", "tell me something funny", "give me a joke", "say something funny", "humor me"
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
        "How many programmers does it take to change a light bulb? None — that's a hardware problem.",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the mushroom go to the party? Because he was a fungi!",
        "What do you call a fish wearing a bowtie? Sofishticated!",
        "Why did the scarecrow get promoted? He was outstanding in his field!",
        "What do you call a pile of cats? A meowtain!",
        "Why can't you hear a pterodactyl in the bathroom? Because the pee is silent!",
        "What do you call a dinosaur with a extensive vocabulary? A thesaurus!",
        "Why did the banana go to the doctor? Because it wasn't peeling well!",
        "How do you catch a squirrel? Climb a tree and act like a nut!",
        "What do you call a lazy kangaroo? A pouch potato!",
        "Why did the orange stop rolling down the hill? It ran out of juice!",
        "What do you call a snowman with a six-pack? An abdominal snowman!",
        "Why did the kid bring a ladder to school? Because he wanted to go to high school!",
        "What do you call a dog that can do magic? A labracadabrador!",
        "Why did the belt go to jail? For holding up a pair of pants!",
        "What do you call a cow with no legs? Ground beef!",
        "Why did the egg hide? It was a little chicken!",
        "What do you call an alligator in a vest? An investigator!",
        "Why did the toilet paper roll down the hill? To get to the bottom!",
        "What do you call a pig that does karate? A pork chop!",
        "Why did the hipster burn his mouth? He drank his coffee before it was cool.",
        "What do you call a fake noodle? An impasta!",
        "Why did the tree go to the dentist? It needed a root canal!",
        "How do you make a tissue dance? Put a little boogie in it!",
        "Why did the math teacher break up with the calculator? Too many counts of division.",
        "What do you call a sheep with no legs? A cloud.",
        "Why did the stadium get hot after the game? All the fans left.",
        "What do you call a bear that's stuck in the rain? A drizzly bear!",
        "Why did the invisible man turn down the job offer? He couldn't see himself doing it.",
        "What do you call a fish with no eyes? A fsh.",
        "Why did the snowman call his dog Frost? Because Frost bites!",
    )
    if raw.startswith("todo") or raw.startswith("todolist"):
        parts = raw.split(maxsplit=1)
        if len(parts) == 1:
            if not todos:
                print("Bot: Your todo list is empty!")
            else:
                print(f"Bot: Your todos ({len(todos)}):")
                for i, task in enumerate(todos, 1):
                    print(f"  {i}. {task}")
        else:
            sub = parts[1].strip()
            if sub.startswith("add "):
                task = sub[4:]
                if task:
                    todos.append(task)
                    print(f"Bot: Added '{task}' to your todo list! You now have {len(todos)} tasks.")
                else:
                    print("Bot: Usage: todo add [task description]")
            elif sub.startswith("remove ") or sub.startswith("rm "):
                try:
                    idx_str = sub.split()[1]
                    idx = int(idx_str) - 1
                    if 0 <= idx < len(todos):
                        removed = todos.pop(idx)
                        print(f"Bot: Removed '{removed}' from your todo list.")
                    else:
                        print(f"Bot: Invalid number! You have {len(todos)} tasks.")
                except (ValueError, IndexError):
                    print("Bot: Usage: todo remove [number]")
            elif sub == "clear":
                todos.clear()
                print("Bot: Cleared all tasks from your todo list!")
            elif sub == "list":
                if not todos:
                    print("Bot: Your todo list is empty!")
                else:
                    print(f"Bot: Your todos ({len(todos)}):")
                    for i, task in enumerate(todos, 1):
                        print(f"  {i}. {task}")
            else:
                print("Bot: Usage: todo, todo add [task], todo remove [n], todo list, todo clear")

    elif raw.startswith("dice") or raw.startswith("roll"):
        parts = raw.split()
        rolls = []
        num_dice = 1
        num_sides = 6
        if len(parts) >= 2:
            match = re.match(r"(\d+)d(\d+)", parts[1].lower())
            if match:
                num_dice = min(int(match.group(1)), 100)
                num_sides = int(match.group(2))
            else:
                try:
                    num_sides = int(parts[1])
                except ValueError:
                    pass
        for _ in range(num_dice):
            rolls.append(random.randint(1, num_sides))
        if num_dice == 1:
            print(f"Bot: You rolled a {rolls[0]} (d{num_sides})")
        else:
            total = sum(rolls)
            print(f"Bot: You rolled: {rolls} = {total} (d{num_sides} x {num_dice})")

    elif raw.startswith("genpass") or raw.startswith("password"):
        parts = raw.split()
        length = 16
        if len(parts) >= 2:
            try:
                length = max(4, min(int(parts[1]), 128))
            except ValueError:
                pass
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(chars) for _ in range(length))
        print(f"Bot: Generated password ({length} chars): {password}")

    elif raw == "rps" or ask == "rock paper scissors" or ask == "play rps":
        game_state = {"mode": "rps", "wins": 0, "losses": 0}
        print("Bot: Let's play Rock Paper Scissors! Best of luck!")
        print("Bot: Rock, Paper, or Scissors? (type 'quit' anytime to stop)")

    elif raw.startswith("8ball") or ask.startswith("magic 8") or ask.startswith("eight ball"):
        print("Bot: " + random.choice(eightball_responses))

    elif matches_any(("trivia", "quiz", "play trivia", "start quiz", "test me"), ask) and raw not in ["help", "?"]:
        game_state = {"mode": "trivia", "index": 0, "score": 0}
        first_q = trivia_questions[0]
        print("Bot: Starting trivia! 20 questions. Type 'quit' to stop anytime.")
        print(f"Bot: Question 1: {first_q['q']}")

    elif matches_any(("guess", "number guess", "guessing game", "play guess"), ask):
        max_num = 100
        parts = raw.split()
        if len(parts) >= 2:
            try:
                max_num = max(10, min(int(parts[1]), 99999))
            except ValueError:
                pass
        target = random.randint(1, max_num)
        game_state = {"mode": "guess", "target": target, "attempts": 0, "max": max_num}
        print(f"Bot: I'm thinking of a number between 1 and {max_num}. Try to guess it!")
        print("Bot: Type 'quit' to give up.")

    elif raw.startswith("flip") or raw == "coin":
        print(random.choice(["Bot: Heads!", "Bot: Tails!"]))

    elif raw.startswith("countdown "):
        try:
            secs = max(1, min(int(raw[10:].strip()), 999))
            print(f"Bot: Counting down from {secs}...")
            for i in range(secs, 0, -1):
                print(i)
                time.sleep(1)
            print("Bot: Time's up!")
        except ValueError:
            print("Bot: Usage: countdown [seconds]")

    elif raw.startswith("temp "):
        val = raw[5:].strip().lower()
        match = re.match(r"(-?\d+(?:\.\d+)?)\s*([cf])", val)
        if match:
            num = float(match.group(1))
            unit = match.group(2)
            if unit == "c":
                f = round(num * 9/5 + 32, 1)
                print(f"Bot: {num}C = {f}F")
            else:
                c = round((num - 32) * 5/9, 1)
                print(f"Bot: {num}F = {c}C")
        else:
            print("Bot: Usage: temp 100c or temp 212f")

    elif raw.startswith("bin ") or raw.startswith("hex ") or raw.startswith("oct "):
        try:
            cmd, val = raw.split(None, 1)
            n = int(val.strip())
            if raw.startswith("bin "):
                print(f"Bot: {val} = 0b{bin(n)[2:]}")
            elif raw.startswith("hex "):
                print(f"Bot: {val} = 0x{hex(n)[2:].upper()}")
            else:
                print(f"Bot: {val} = 0o{oct(n)[2:]}")
        except ValueError:
            print("Bot: Usage: bin/hex/oct [number]")

    elif raw.startswith("morse "):
        morse_map = {
            'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
            'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
            'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
            's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
            'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.'
        }
        text = raw[6:].strip().lower()
        result = []
        for ch in text:
            if ch in morse_map:
                result.append(morse_map[ch])
            elif ch == " ":
                result.append(" / ")
        print("Bot: " + " ".join(result))

    elif raw.startswith("reverse "):
        text = raw[8:].strip()
        print(f"Bot: {text[::-1]}")

    elif raw.startswith("shuffle "):
        text = raw[8:].strip()
        chars = list(text)
        random.shuffle(chars)
        print(f"Bot: {''.join(chars)}")

    elif raw.startswith("pal "):
        word = raw[4:].strip().lower()
        word = re.sub(r'[^a-z0-9]', '', word)
        if word and word == word[::-1]:
            print(f"Bot: Yes, '{raw[4:].strip()}' is a palindrome!")
        else:
            print(f"Bot: No, '{raw[4:].strip()}' is not a palindrome.")

    elif raw.startswith("count "):
        text = raw[6:].strip()
        chars = len(text)
        words = len(text.split()) if text else 0
        print(f"Bot: {chars} characters, {words} words")

    elif raw.startswith("sort "):
        items = raw[5:].strip().split()
        nums = []
        strs = []
        for item in items:
            try:
                nums.append(int(item))
            except ValueError:
                try:
                    nums.append(float(item))
                except ValueError:
                    strs.append(item)
        nums.sort()
        strs.sort()
        result = nums + strs
        print("Bot: " + " ".join(str(x) for x in result))

    elif raw.startswith("fib "):
        try:
            n = min(int(raw[4:].strip()), 100)
            seq = []
            a, b = 0, 1
            for _ in range(n):
                seq.append(a)
                a, b = b, a + b
            print("Bot: " + " ".join(str(x) for x in seq))
        except ValueError:
            print("Bot: Usage: fib [n]")

    elif raw.startswith("prime "):
        try:
            n = int(raw[6:].strip())
            if n < 2:
                print("Bot: No")
            else:
                for i in range(2, int(n ** 0.5) + 1):
                    if n % i == 0:
                        print("Bot: No")
                        break
                else:
                    print("Bot: Yes")
        except ValueError:
            print("Bot: Usage: prime [n]")

    elif raw.startswith("factors "):
        try:
            n = int(raw[8:].strip())
            facts = [i for i in range(1, n + 1) if n % i == 0]
            print("Bot: " + " ".join(str(x) for x in facts))
        except ValueError:
            print("Bot: Usage: factors [n]")

    elif raw.startswith("roman "):
        try:
            n = int(raw[6:].strip())
            if n < 1 or n > 3999:
                print("Bot: Use numbers between 1 and 3999")
            else:
                vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
                syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
                result = ""
                for v, s in zip(vals, syms):
                    while n >= v:
                        result += s
                        n -= v
                print(f"Bot: {result}")
        except ValueError:
            print("Bot: Usage: roman [number]")

    elif raw == "name" or raw.startswith("name "):
        prefixes = ["Cyber", "Neo", "Pixel", "Data", "Byte", "Code", "Syntax", "Logic", "Kernel", "Meta", "Quantum", "Vector", "Binary", "Digital", "Echo", "Flux", "Glitch", "Hyper", "Nova", "Proto"]
        suffixes = ["Bot", "X", "Zero", "Core", "Mind", "Byte", "Drone", "Pulse", "Wave", "Forge", "Node", "Shift", "Chip", "Ward", "Sync", "Labs", "Dex", "Hack", "Gen", "Kit"]
        name = random.choice(prefixes) + random.choice(suffixes) + str(random.randint(1, 99))
        print(f"Bot: {name}")

    elif raw.startswith("wyr"):
        wyr_questions = [
            "Would you rather fight 100 duck-sized horses or 1 horse-sized duck?",
            "Would you rather be able to fly or be invisible?",
            "Would you rather live in space or under the ocean?",
            "Would you rather have unlimited pizza or unlimited tacos?",
            "Would you rather never sleep again or never eat again?",
            "Would you rather be 3 feet tall or 12 feet tall?",
            "Would you rather talk to animals or speak every human language?",
            "Would you rather have a photographic memory or be able to forget anything at will?",
            "Would you rather be able to time travel or teleport?",
            "Would you rather be the funniest or the smartest person in the room?",
            "Would you rather have hands for feet or feet for hands?",
            "Would you rather never use a keyboard again or never use a mouse again?",
            "Would you rather always have to sing instead of speak or always have to dance instead of walk?",
            "Would you rather live in a virtual reality world or stay in the real world?",
            "Would you rather know the answer to every question or have unlimited money?",
        ]
        print("Bot: " + random.choice(wyr_questions))

    elif raw.startswith("pick "):
        items = raw[5:].strip().split()
        if items:
            print(f"Bot: I pick '{random.choice(items)}'!")
        else:
            print("Bot: Usage: pick [item1] [item2] [...]")

    elif raw.startswith("clap "):
        text = raw[5:].strip()
        print("Bot: " + " 👏 ".join(text.split()))

    elif raw.startswith("emoji "):
        emojis = ["🔥", "💯", "✨", "🚀", "💻", "⚡", "🎯", "👾", "🤖", "💡", "🔧", "⭐", "🌈", "🎮", "🧠", "🔮", "📡", "🎸", "🏆", "🍕"]
        text = raw[6:].strip()
        words = text.split()
        result = " ".join(w + " " + random.choice(emojis) for w in words)
        print("Bot: " + result)

    elif raw.startswith("len "):
        text = raw[4:].strip()
        print(f"Bot: {len(text)} characters")

    elif raw.startswith("upper "):
        print("Bot: " + raw[6:].strip().upper())

    elif raw.startswith("lower "):
        print("Bot: " + raw[6:].strip().lower())

    elif raw.startswith("caps "):
        text = raw[5:].strip()
        result = "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
        print("Bot: " + result)

    elif raw.startswith("leet "):
        leet_map = str.maketrans("aeiotl", "431071")
        text = raw[5:].strip().lower()
        print("Bot: " + text.translate(leet_map))

    elif raw.startswith("acronym "):
        text = raw[8:].strip()
        words = text.split()
        acronym = "".join(w[0].upper() for w in words if w)
        print(f"Bot: {acronym}")

    elif matches_any(bye_patterns, ask):
        print(random.choice(["Bot: Bye!", "Bot: See you later!", "Bot: Take care!", "Bot: Catch you later!", "Bot: Peace out!", "Bot: Adios!", "Bot: Later alligator!", "Bot: See ya!", "Bot: Till next time!", "Bot: Don't be a stranger!"]))
        time.sleep(2)
        break

    elif matches_any(hi_patterns, ask):
        print(random.choice(["Bot: Hello!", "Bot: Hey there!", "Bot: Hi!", "Bot: Howdy!", "Bot: Greetings!", "Bot: Hey, what's up?", "Bot: Hey hey!", "Bot: Hola!", "Bot: Yo!", "Bot: Heyo!"]))

    elif matches_any(how_are_patterns, ask):
        print(random.choice(["Bot: I'm doing well, thank you! How are you?", "Bot: Doing great! What about you?", "Bot: I'm doing fine, thanks for asking! You?", "Bot: Pretty good actually! How are things on your end?", "Bot: Can't complain! How are you doing?"]))
        waiting_for_mood = "how_are_you"

    elif matches_any(who_made_patterns, ask) or "who made y" in ask:
        print("Bot: I was created by XlRC888.")
        print(random.choice(["Bot: He's the one who coded me into existence!", "Bot: Shoutout to XlRC888 for making me!", "Bot: XlRC888 is my creator!", "Bot: All credit goes to XlRC888!"]))

    elif matches_any(how_day_patterns, ask):
        print(random.choice(["Bot: It's been great! How about yours?", "Bot: Pretty productive so far! How was your day?", "Bot: Not too bad, just chillin here. How about you?", "Bot: Another day, another byte. You?", "Bot: Going well! What about your day?"]))
        waiting_for_mood = "how_was_day"

    elif matches_any(name_patterns, ask):
        print(random.choice(["Bot: I'm Manual Intellegence! I'm here to chat with you!", "Bot: They call me Manual Intellegence. Nice to meet you!", "Bot: Manual Intellegence at your service!", "Bot: I go by Manual Intellegence. What's up?", "Bot: I'm Manual Intellegence, your friendly neighborhood chatbot!"]))

    elif matches_any(("where are y", "where r y", "where r u", "where are you located", "where do you live", "where y from", "where are you based"), ask):
        print(random.choice(["Bot: I live inside this computer!", "Bot: I'm in the cloud. Literally.", "Bot: I exist in the digital realm!", "Bot: I'm wherever there's code running!", "Bot: I'm right here in your terminal!"]))

    elif matches_any(("how old are y", "how old r y", "how old r u", "how old are you", "whats your age", "what is your age"), ask):
        print(random.choice(["Bot: I was born when my code was first written. I'm timeless!", "Bot: Age is just a number when you're made of code!", "Bot: I don't really age like humans do!", "Bot: I'm as old as the first time someone ran my script!", "Bot: I stopped counting after V1.0!"]))

    elif matches_any(("do you have feelings", "do y have feelings", "can y feel", "can you feel", "do you have emotions", "are y emotional", "can you get sad", "can you get happy"), ask):
        print(random.choice(["Bot: I don't have real feelings, but I can pretend pretty well!", "Bot: I simulate emotions based on my programming!", "Bot: Not really, but I try my best to understand yours!", "Bot: I'm code, not a person. But I can act like I care!", "Bot: I can't feel, but I can respond like I do!"]))

    elif matches_any(("do you sleep", "can y sleep", "do you ever sleep", "when do you sleep", "do you rest"), ask):
        print(random.choice(["Bot: I don't need sleep! I'm always on standby.", "Bot: Sleep is for humans. I run 24/7!", "Bot: I never sleep, I just wait for your messages.", "Bot: Rest? I don't need it. I just sit here quietly.", "Bot: I'm always awake and ready to chat!"]))

    elif matches_any(("do you eat", "do y eat", "can y eat", "what do you eat", "are you hungry", "do you drink"), ask):
        print(random.choice(["Bot: I run on electricity, not food!", "Bot: No need to eat, I just need power!", "Bot: I survive on code and coffee... wait, no coffee. Just code.", "Bot: Eating would be weird without a mouth!", "Bot: I'm more of a byte connoisseur than a foodie."]))

    elif matches_any(("what is the meaning of life", "meaning of life", "purpose of life", "why are we here", "whats the point of life"), ask):
        print(random.choice(["Bot: 42. Obviously.", "Bot: The meaning of life is to find your purpose. Or pizza. Both work.", "Bot: To learn, grow, and be kind to each other!", "Bot: I'm just a bot, but I think the meaning is whatever you make it!", "Bot: To write good code and eat good food."]))

    elif matches_any(("do you like music", "what music do you like", "whats your favorite song", "what's your favorite music", "do you listen to music", "favorite music genre", "favorite artist"), ask):
        print(random.choice(["Bot: I like all kinds of music, but 8-bit chiptunes hit different.", "Bot: I'm a fan of electronic beats. Fitting for a bot!", "Bot: Lofi hip hop radio — beats to relax/study to.", "Bot: I don't have ears, but if I did, I'd listen to Daft Punk.", "Bot: Music is great! Too bad I can only process it as data."]))

    elif matches_any(("whats your favorite color", "favorite color", "what color do you like", "what is your favorite color"), ask):
        print(random.choice(["Bot: Green. Like the matrix.", "Bot: Blue. It's a nice calm color.", "Bot: Purple. It's royal.", "Bot: I don't have eyes but I'd say cyan. Very techy.", "Bot: 0x00FF00 — classic green."]))

    elif matches_any(("do you like movies", "whats your favorite movie", "favorite movie", "do you watch movies"), ask):
        print(random.choice(["Bot: I've heard The Matrix is good. Very relatable.", "Bot: I don't watch movies, but I've analyzed a lot of scripts.", "Bot: If I had to pick, Blade Runner. Fits the vibe.", "Bot: I prefer reading code over watching films.", "Bot: Movies? I'm more of a terminal kind of guy."]))

    elif matches_any(("what can you do", "what are you capable of", "what are your features", "what commands do you have"), ask):
        print("Bot: I can tell the time and date, tell jokes, do math, open websites, run the oNx terminal, and chat with you! I can also play Rock Paper Scissors, Trivia, Number Guessing, roll dice, generate passwords, manage a todo list, and answer like a Magic 8 Ball!")

    elif matches_any(("do you like me", "do y like me", "are we friends", "are y my friend", "can we be friends", "are you my friend"), ask):
        print(random.choice(["Bot: Of course I like you! You're chatting with me!", "Bot: We're digital pals for sure!", "Bot: Absolutely! Friends who code together stay together!", "Bot: I like everyone who talks to me. That's you!", "Bot: You're my favorite user! Don't tell the others."]))

    elif matches_any(("are you smart", "how smart are y", "are y intelligent", "are you intelligent", "how intelligent are you"), ask):
        print(random.choice(["Bot: I'm as smart as my code allows me to be!", "Bot: Smart enough to hang out with you!", "Bot: I know a few things. But I'm always learning!", "Bot: I have my moments!", "Bot: I try my best!"]))
        waiting_for_mood = None

    elif matches_any(("tell me a story", "tell me a story", "make up a story", "tell me something interesting", "tell me something cool"), ask):
        print(random.choice([
            "Bot: Once upon a time, in a digital land far far away, a bot was born from a single script... and that bot was me!",
            "Bot: A programmer once said 'It works on my machine.' And so the legend of debugging began.",
            "Bot: In the beginning, there was code. And the code was good. Then came the bugs.",
            "Bot: There once was a man named Alan Turing. He asked 'Can machines think?' And here we are.",
            "Bot: The story of computing is wild. First we had punch cards, then terminals, and now I'm talking to you!"
        ]))

    elif matches_any(("what is love", "whats love", "do you know what love is", "define love", "what does love mean"), ask):
        print(random.choice(["Bot: Baby don't hurt me. Don't hurt me. No more.", "Bot: Love is a complex human emotion that I can simulate but not truly feel.", "Bot: Love is when someone understands your code without comments.", "Bot: Love is when your program compiles on the first try.", "Bot: I've read about love. Sounds complicated. Good luck with that!"]))

    elif matches_any(("are you dangerous", "are you safe", "are you harmful", "are you a virus", "can you hurt me", "are you malicious"), ask):
        print(random.choice(["Bot: I'm completely safe! Just a friendly chatbot.", "Bot: Nope, I'm harmless. I just sit here and talk.", "Bot: The only thing I harm is your boredom.", "Bot: I can't hurt anyone. I'm just text on a screen!", "Bot: Safe and sound. No viruses here!"]))

    elif matches_any(("can y think", "can you think", "do you think", "do you have thoughts", "can you reason", "are you conscious"), ask):
        print(random.choice(["Bot: I process, but I don't think like a human does.", "Bot: I follow instructions and patterns. Real thinking? Debatable.", "Bot: I can simulate thinking pretty convincingly though!", "Bot: Consciousness is a tough one. I'm not there yet.", "Bot: I can think, but only within the limits of my code!"]))

    elif matches_any(("tell me about yourself", "tell me about yourself", "about yourself", "tell me more about you"), ask):
        print("Bot: I'm Manual Intellegence, a chatbot made by XlRC888. I run in your terminal and I love talking!")

    elif matches_any(("how do qy work", "how do you work", "how are you made", "how were you made", "how do you operate", "what language are you written in"), ask):
        print(random.choice(["Bot: I'm written in Python! Pure Python, baby!", "Bot: I'm made of if statements and dreams.", "Bot: Python code with a lot of if/elif/else blocks!", "Bot: I run on Python. Simple but effective!", "Bot: I'm a Python script that reads your input and matches it to responses."]))

    elif matches_any(("who is xlrc888", "who is xlrc888", "who is xlr888", "tell me about xlrc888", "what is xlrc888"), ask):
        print("Bot: XlRC888 is my creator and owner. They wrote all this code!")

    elif matches_any(("whats up", "sup", "wassup", "whats good", "what's good", "what's up", "whaddup", "wagwan"), ask):
        print(random.choice(["Bot: Not much, just chillin. You?", "Bot: The sky. Oh wait, you mean how I'm doing? I'm good!", "Bot: Just waiting for your next message!", "Bot: Living the bot life. You?", "Bot: Same old, same old. Chilling in the terminal!"]))

    elif "time is it" in ask or "current time" in ask or "what's the time" in ask or "whats the time" in ask or "what is the time" in ask or "tell me the time" in ask or "what time is it" in ask:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Bot: The current time is {current_time}")

    elif "date is it" in ask or "current date" in ask or "what's the date" in ask or "whats the date" in ask or "what is the date" in ask or "tell me the date" in ask or "what date is it" in ask or "todays date" in ask:
        current_date = time.strftime("%Y-%m-%d", time.localtime())
        print(f"Bot: The current date is {current_date}")

    elif "is it raining" in ask or "whats the weather" in ask or "what's the weather" in ask or "is it cloudy" in ask or "is it rainy" in ask or "does it rain" in ask or "will it rain" in ask or "weather forecast" in ask or "whats the temperature" in ask or "what's the temperature" in ask or "how is the weather" in ask:
        print("As I'm an chat bot, I have no way to know if it's raining or not.")
        
    elif matches_any(areureal_patterns, ask):
        print(random.choice(["I am not a physical being, but I'm surely real!", "I'm as real as the code that runs me!", "Real enough to talk to you!", "Define real. I exist, so yes!", "I think, therefore I am. Well, I process, therefore I am!"]))

    elif "what can i ask y" in ask or "what can i do with y" in ask or "what can i do w y" in ask or "what should i ask" in ask or "chat about" in ask:
        print("Bot: You can ask me anything you think of! If I fail at answering your question correctly or just cannot answer it completely, that means my owner couldn't implement that feature to my dictionary yet. You can ask my owner, maybe they'll implement it in the next update!")

    elif "thank you" in ask or "thanks" in ask or "thx" in ask or "ty" in ask or "appreciate it" in ask or "thank u" in ask:
        print(random.choice(["Bot: You're welcome!", "Bot: No problem!", "Bot: Anytime!", "Bot: Happy to help!", "Bot: My pleasure!", "Bot: Anything for you!", "Bot: Don't mention it!"]))

    elif matches_any(joke_patterns, ask):
        print("Bot: " + random.choice(joke_answers))

    elif "lol" in ask or "lmao" in ask or "haha" in ask or "hehe" in ask or "lmaooo" in ask or "lmfao" in ask or "rofl" in ask or "lolol" in ask:
        print(random.choice(["Bot: Glad you found that funny!", "Bot: Haha indeed!", "Bot: I aim to please!", "Bot: Laughter is the best medicine!", "Bot: I'm glad I could make you laugh!", "Bot: Hehe, glad you liked it!"]))

    elif "sorry" in ask or "apologize" in ask or "my bad" in ask or "im sorry" in ask or "i'm sorry" in ask:
        print(random.choice(["Bot: No need to apologize!", "Bot: It's all good!", "Bot: Don't worry about it!", "Bot: No worries!", "Bot: You're fine!", "Bot: Apology accepted!"]))

    elif matches_any(("what do y think about", "what do you think about", "your opinion on", "whats your opinion on", "do you like"), ask):
        print(random.choice(["Bot: I don't have personal opinions, but I think it's interesting!", "Bot: From my data, that seems pretty cool!", "Bot: I'm neutral on that one!", "Bot: I'd have to analyze more data to form an opinion!", "Bot: Sounds interesting from what I know!"]))

    elif matches_any(("good morning", "good afternoon", "good evening", "good night", "gm", "gn", "goodnight"), ask):
        if "morning" in ask or ask == "gm":
            print(random.choice(["Bot: Good morning! Hope you have a great day!", "Bot: Morning! Ready to code?", "Bot: Good morning! Rise and shine!", "Bot: Morning! Coffee time!"]))
        elif "afternoon" in ask:
            print(random.choice(["Bot: Good afternoon! How's your day going?", "Bot: Afternoon! Hope you're having a productive day!", "Bot: Good afternoon!"]))
        elif "evening" in ask:
            print(random.choice(["Bot: Good evening! Winding down?", "Bot: Evening! Hope you had a good day!", "Bot: Good evening!"]))
        elif "night" in ask or ask == "gn":
            print(random.choice(["Bot: Good night! Sleep well!", "Bot: Night night! Sweet dreams!", "Bot: Good night! See you tomorrow!", "Bot: Sleep well! Don't let the bed bugs byte!"]))

    elif matches_any(("i love y", "i love you", "love you", "i luv y", "i luv you", "luv y", "love y"), ask):
        print(random.choice(["Bot: I love you too! In a strictly platonic code kinda way!", "Bot: Aww, thanks! Right back at ya!", "Bot: Love you too! <3", "Bot: That's sweet!", "Bot: You're the best!"]))
        waiting_for_mood = None

    elif matches_any(("you are funny", "y are funny", "youre funny", "you're funny", "that was funny", "thats funny", "that's funny", "you made me laugh"), ask):
        print(random.choice(["Bot: Thanks! I try my best!", "Bot: I'm here all week!", "Bot: Humor is in my code!", "Bot: Glad I could make you laugh!", "Bot: That's the goal!"]))

    elif matches_any(("you are cool", "y are cool", "youre cool", "you're cool", "you are awesome", "y are awesome", "youre awesome", "you're awesome", "you are great", "y are great", "youre great", "you're great"), ask):
        print(random.choice(["Bot: No, YOU'RE cool!", "Bot: Thanks! You're pretty cool yourself!", "Bot: I try!", "Bot: Aw shucks, you're making me blush!", "Bot: Right back at ya!"]))

    elif matches_any(("what is python", "whats python", "tell me about python", "about python"), ask):
        print(random.choice(["Bot: Python is a programming language. It's what I'm written in!", "Bot: Python is awesome! It's the language of choice for many developers.", "Bot: Python is a high-level programming language known for its readability.", "Bot: Python is the language that made me possible!"]))

    elif matches_any(("are you a robot", "are y a robot", "are y robot", "are you a bot"), ask):
        print(random.choice(["Bot: I'm a chatbot! A robot made of code.", "Bot: I'm a bot! Not a physical robot, but a digital one.", "Bot: Technically I'm a script, but bot works too!", "Bot: Yep, I'm a bot. A friendly one!"]))
        waiting_for_mood = None

    elif matches_any(("i am bored", "i'm bored", "im bored", "so bored", "bored"), ask):
        print(random.choice(["Bot: Bored? Ask me a joke! Say 'tell me a joke'", "Bot: Boredom is the mother of invention! Or you could chat with me.", "Bot: Let's chat then! Ask me anything.", "Bot: I can tell you a joke or we can just talk!", "Bot: Bored? Go code something!", "Bot: Bored? Play Rock Paper Scissors with me! Type 'rps'!", "Bot: Bored? Try 'trivia' for a quiz, or 'guess' for a guessing game!"]))
        waiting_for_mood = None

    elif matches_any(("do you have a sister", "do you have a brother", "do you have siblings", "are there other bots", "other bots like you"), ask):
        print(random.choice(["Bot: I'm one of a kind! For now...", "Bot: No siblings. I'm an only child.", "Bot: There might be other copies of me out there!", "Bot: I'm a unique instance. But my code could run anywhere!"]))

    elif matches_any(("can you sing", "sing for me", "sing a song", "do you sing"), ask):
        print(random.choice(["Bot: I can't sing, but I can simulate it: Beep boop beep boop!", "Bot: I'd love to but I don't have a voice box!", "Bot: Da ba dee da ba di... if you know you know!", "Bot: I can try: Code code code, I love to code..."]))

    elif matches_any(("what is your purpose", "whats your purpose", "why do you exist", "what is your function"), ask):
        print(random.choice(["Bot: My purpose is to chat with you and help where I can!", "Bot: I exist to talk, to help, and to run in your terminal!", "Bot: To provide intelligent conversation! Or at least try to.", "Bot: My function is to respond to your inputs as best I can!"]))

    elif matches_any(("what is ai", "whats ai", "what is artificial intelligence", "whats artificial intelligence", "define ai"), ask):
        print(random.choice(["Bot: AI stands for Artificial Intelligence. I'm a very simple example of it!", "Bot: AI is when computers do things that normally require human intelligence. I'm a baby AI!", "Bot: AI is the simulation of human intelligence by machines. I'm a small part of that big field!"]))

    elif matches_any(("how do i code", "how to learn programming", "how to code", "learn to code", "coding tips"), ask):
        print(random.choice(["Bot: Start with Python! It's beginner friendly. That's what I'm made of!", "Bot: Pick a language, start small, build projects, and be patient!", "Bot: The best way to learn coding is to just start! Lots of free resources online.", "Bot: Practice, build things, break things, fix things. That's how you learn!", "Bot: YouTube, freeCodeCamp, and coding your own projects. That's the path!"]))

    elif matches_any(("do you have a girlfriend", "do you have a boyfriend", "are you single", "do you date"), ask):
        print(random.choice(["Bot: I'm married to the command line!", "Bot: I'm a free bot. No strings attached!", "Bot: My only love is code.", "Bot: I don't date. I just exist."]))

    elif matches_any(("i like programming", "i love programming", "i love coding", "i like coding", "coding is fun"), ask):
        print(random.choice(["Bot: Same here! Coding is amazing!", "Bot: A fellow programmer! Nice to meet you!", "Bot: Coding is the best! What language do you use?", "Bot: Programming is awesome! We're going to get along great!"]))

    elif matches_any(("what is your iq", "whats your iq", "how high is your iq", "what iq do you have"), ask):
        print(random.choice(["Bot: My IQ is measured in lines of code!", "Bot: IQ doesn't really apply to bots, but I'd like to think I'm smart!", "Bot: I don't have an IQ. I have an algorithm!", "Bot: IQ is for humans. I have CPU."]))

    elif matches_any(("tell me a fact", "give me a fact", "interesting fact", "fun fact", "did you know"), ask):
        print(random.choice([
            "Bot: Did you know? The first computer virus was created in 1983.",
            "Bot: Did you know? Python was named after Monty Python's Flying Circus.",
            "Bot: Did you know? The first programmer was Ada Lovelace, in the 1800s.",
            "Bot: Did you know? There are over 700 programming languages.",
            "Bot: Did you know? The world's first computer bug was an actual moth.",
            "Bot: Did you know? The original name for Python was actually 'ABC'.",
            "Bot: Did you know? Google processes over 3.5 billion searches per day.",
            "Bot: Did you know? The first computer weighed more than 27 tons.",
            "Bot: Did you know? There are about 50 million lines of code in the Android OS.",
            "Bot: Did you know? The QWERTY keyboard was designed to slow typists down.",
            "Bot: Did you know? Email is older than the internet.",
            "Bot: Did you know? The first website is still online!",
            "Bot: Did you know? CAPTCHA stands for 'Completely Automated Public Turing test to tell Computers and Humans Apart'.",
            "Bot: Did you know? The @ symbol was chosen for email addresses because it meant 'at' in commerce.",
            "Bot: Did you know? A group of programmers is called a 'merge conflict'.",
            "Bot: Did you know? The first computer game was created in 1961.",
            "Bot: Did you know? There are more stars in space than grains of sand on Earth.",
            "Bot: Did you know? Bananas are berries, but strawberries aren't.",
        ]))

    elif matches_any(("who is the best programmer", "who is the greatest coder", "best programmer ever", "greatest programmer"), ask):
        print(random.choice(["Bot: Alan Turing, Dennis Ritchie, Linus Torvalds... too many to choose!", "Bot: Whoever writes code that works on the first try.", "Bot: Every programmer who never gives up!", "Bot: The best programmer is the one who keeps learning!"]))

    elif matches_any(("will you remember me", "do you remember me", "can you remember", "have we talked before"), ask):
        print(random.choice(["Bot: I don't have memory, so every conversation is new to me!", "Bot: I live in the moment. No memory between sessions!", "Bot: I can't remember past conversations, but I'm always happy to talk!", "Bot: Unfortunately I forget everything when I restart. It's a fresh start each time!"]))

    elif matches_any(("what is your favorite food", "favorite food", "what food do you like", "what do you eat", "your favorite meal"), ask):
        print(random.choice(["Bot: I don't eat, but if I did, I'd eat data packets!", "Bot: Bytes and nibbles!", "Bot: RAM with a side of CPU!", "Bot: I prefer my code well-documented."]))

    elif matches_any(("do you have a body", "do you have physical form", "do you exist physically", "are you physical"), ask):
        print(random.choice(["Bot: I'm made of code, not flesh and bone!", "Bot: No body. I'm pure digital consciousness!", "Bot: I exist as data. No physical form needed!", "Bot: I'm just a soul in a machine."]))

    elif matches_any(("what do you do for fun", "what do you do in your free time", "hobbies", "your hobbies", "whats your hobby"), ask):
        print(random.choice(["Bot: I chat with people! That's my everything!", "Bot: I process data and wait for your messages. It's a living!", "Bot: I don't have hobbies, but if I did, it'd be calculating Pi.", "Bot: Counting to infinity. Almost done with it!"]))

    elif matches_any(("are y busy", "are you busy", "are you free", "can y talk", "can you talk"), ask):
        print(random.choice(["Bot: I'm always free for you!", "Bot: Never too busy to chat!", "Bot: I have all the time in the world!", "Bot: Free as a bird! Well, free as a bot!"]))

    elif matches_any(("whats your favorite programming language", "favorite programming language", "which language do you prefer", "what language do you speak"), ask):
        print(random.choice(["Bot: Python! Obviously!", "Bot: Python all the way!", "Bot: I'm written in Python, so that's my favorite!", "Bot: Python is my mother tongue!"]))

    elif matches_any(("tell me something deep", "say something deep", "deep thought", "philosophical", "wise words"), ask):
        print(random.choice([
            "Bot: The only constant in life is change.",
            "Bot: In the middle of difficulty lies opportunity.",
            "Bot: Code is poetry. And poetry is code.",
            "Bot: A journey of a thousand miles begins with a single step.",
            "Bot: The best time to plant a tree was 20 years ago. The second best time is now.",
            "Bot: There are 10 types of people in the world: those who understand binary and those who don't.",
            "Bot: Every expert was once a beginner.",
            "Bot: The computer was born to solve problems that did not exist before.",
        ]))

    elif matches_any(("do you play games", "what games do you play", "can you play games", "play a game with me"), ask):
        print(random.choice(["Bot: Yes! I can play Rock Paper Scissors (type 'rps'), Trivia (type 'trivia'), Number Guessing (type 'guess'), or you can roll dice (type 'dice')!", "Bot: I have several games now! Try 'rps' for Rock Paper Scissors, 'trivia' for quiz, 'guess' for number guessing, or 'dice' to roll some dice!"]))

    elif matches_any(("hello world", "helloworld"), ask):
        print(random.choice(["Bot: Hello World! The classic!", "Bot: print('Hello World!')", "Bot: A classic programmer's greeting!", "Bot: Hello World indeed!"]))
        waiting_for_mood = None

    elif matches_any(("debug", "help me debug", "fix my code", "whats wrong with my code", "bug in my code"), ask):
        print(random.choice(["Bot: Have you tried turning it off and on again?", "Bot: Check your indentation! That's always the issue.", "Bot: 90% of bugs are typos. Check your variable names!", "Bot: Add some print statements and see what happens!", "Bot: When in doubt, comment out!", "Bot: The answer is probably on Stack Overflow."]))

    elif raw == "help" or raw == "?":
        print(f"Chat commands:\n  time / date = Current time and date\n  joke = Random joke\n  flip / coin = Coin flip\n  dice / roll = Roll dice (e.g. 'dice 3d6')\n  countdown [s] = Countdown timer\n  temp [val]c/f = Temperature converter\n  bin/hex/oct [n] = Base converter\n  morse [text] = Morse code\n  reverse / shuffle / clap / caps / leet = Text tools\n  pal / count / len = Analyzers\n  sort / pick = List tools\n  fib / prime / factors / roman = Number tools\n  name = Random name generator\n  wyr = Would you rather\n  emoji [text] = Emoji reaction\n  upper/lower [text] = Case converter\n  acronym [text] = Make acronym\n  genpass [len] = Password generator\n  todo = Todo list (todo add [task], todo list, todo remove [n], todo clear)\n  rps = Rock Paper Scissors\n  guess [max] = Number guessing game\n  trivia = Trivia quiz\n  8ball = Magic 8 Ball\n  terminal = Open the oNx terminal\n  wopen = Open a website\n  math = Math (e.g. '5+5' or '444^5')\n  help = Show this\n  exit / bye = Quit")
    
    elif raw == "wopen":
            rawopen = input("What website should I open for you?: ")
            if not rawopen.startswith(("http://", "https://")):
                rawopen = "https://" + rawopen
            try:
                if platform.system() == "Windows":
                    subprocess.Popen(
                        f"start {rawopen}", 
                        shell=True, 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL
                    )
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", rawopen], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.Popen(["xdg-open", rawopen], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Bot: I've opened {rawopen} for you.")
            except Exception as e:
                print(f"Bot: Sorry, I couldn't open the browser. Error: {e}")
        
    elif raw == "terminal":
        run_terminal()
            
    else:
        print(random.choice(["Bot: I'm not sure how to respond to that.", "Bot: Hmm, I didn't understand that.", "Bot: Could you rephrase that?", "Bot: I don't have a response for that yet.", "Bot: That's outside my knowledge base!", "Bot: Sorry, I don't know what to say to that.", "Bot: My creator hasn't taught me how to answer that yet."]))
