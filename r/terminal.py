import difflib
import re
import os
import random
import time
import string

variables = {}
todos_term = []
commands = [
    "man",
    "man exit",
    "man help",
    "man man",
    "man let()",
    "man print()",
    "man clear",
    "man echo",
    "man ls",
    "man cat",
    "man whoami",
    "man date",
    "man calc",
    "man rand",
    "man ver",
    "man about",
    "man rps",
    "man todo",
    "man dice",
    "man trivia",
    "man genpass",
    "man guess",
    "man 8ball",
    "man flip",
    "man countdown",
    "man temp",
    "man bin",
    "man hex",
    "man oct",
    "man morse",
    "man reverse",
    "man shuffle",
    "man pal",
    "man count",
    "man sort",
    "man fib",
    "man prime",
    "man factors",
    "man roman",
    "man name",
    "man wyr",
    "man pick",
    "man clap",
    "man emoji",
    "man len",
    "man upper",
    "man lower",
    "man caps",
    "man leet",
    "man acronym",
    "help",
    "exit",
    "print()",
    "let()",
    "clear",
    "echo",
    "ls",
    "cat",
    "whoami",
    "date",
    "calc",
    "rand",
    "ver",
    "about",
    "rps",
    "todo",
    "dice",
    "trivia",
    "genpass",
    "guess",
    "8ball",
    "flip",
    "countdown",
    "temp",
    "bin",
    "hex",
    "oct",
    "morse",
    "reverse",
    "shuffle",
    "pal",
    "count",
    "sort",
    "fib",
    "prime",
    "factors",
    "roman",
    "name",
    "wyr",
    "pick",
    "clap",
    "emoji",
    "len",
    "upper",
    "lower",
    "caps",
    "leet",
    "acronym",
]

eightball_responses_term = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
    "My reply is no.", "My sources say no.", "Outlook not so good.",
    "Very doubtful.",
]

morse_map_term = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}

wyr_questions_term = [
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

name_prefixes_term = ["Cyber", "Neo", "Pixel", "Data", "Byte", "Code", "Syntax", "Logic", "Kernel", "Meta", "Quantum", "Vector", "Binary", "Digital", "Echo", "Flux", "Glitch", "Hyper", "Nova", "Proto"]
name_suffixes_term = ["Bot", "X", "Zero", "Core", "Mind", "Byte", "Drone", "Pulse", "Wave", "Forge", "Node", "Shift", "Chip", "Ward", "Sync", "Labs", "Dex", "Hack", "Gen", "Kit"]
text_emojis_term = ["🔥", "💯", "✨", "🚀", "💻", "⚡", "🎯", "👾", "🤖", "💡", "🔧", "⭐", "🌈", "🎮", "🧠", "🔮", "📡", "🎸", "🏆", "🍕"]

roman_vals_term = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
roman_syms_term = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]


def get_suggestion(rawsug, commands):
    stripped_input = re.sub(r"\(.*", "()", rawsug)
    matches = difflib.get_close_matches(stripped_input, commands, n=1, cutoff=0.5)
    return matches[0] if matches else None


def eval_expr(expr):
    expr = expr.strip()
    token_re = re.compile(r'(\d+\.?\d*|"[^"]*"|\'[^\']*\'|\w+|[+\-*/])')
    tokens = token_re.findall(expr)
    resolved = []
    for t in tokens:
        if (t.startswith('"') and t.endswith('"')) or (
            t.startswith("'") and t.endswith("'")
        ):
            resolved.append(t[1:-1])
        elif t in variables:
            resolved.append(variables[t])
        elif re.match(r"^\d+\.?\d*$", t):
            resolved.append(float(t) if "." in t else int(t))
        elif t in ("+", "-", "*", "/"):
            resolved.append(t)
        else:
            return None, f"undefined: {t}"
    result = resolved[0]
    i = 1
    while i < len(resolved):
        op = resolved[i]
        rhs = resolved[i + 1]
        if op == "+":
            result = (
                str(result) + str(rhs)
                if isinstance(result, str) or isinstance(rhs, str)
                else result + rhs
            )
        elif op == "-":
            result = result - rhs
        elif op == "*":
            result = result * rhs
        elif op == "/":
            if rhs == 0:
                return None, "div by zero"
            result = result / rhs
        i += 2
    return result, None


def handle_rps():
    wins = 0
    losses = 0
    choices = ["rock", "paper", "scissors"]
    while True:
        inp = input(">> ").strip().lower()
        if inp in ["quit", "exit", "stop", "q"]:
            print(f"w:{wins} l:{losses}")
            return
        if inp not in choices:
            continue
        bot = random.choice(choices)
        if inp == bot:
            print(f"{inp} vs {bot}: tie (w:{wins} l:{losses})")
        elif (inp == "rock" and bot == "scissors") or (inp == "scissors" and bot == "paper") or (inp == "paper" and bot == "rock"):
            wins += 1
            print(f"{inp} vs {bot}: win (w:{wins} l:{losses})")
        else:
            losses += 1
            print(f"{inp} vs {bot}: loss (w:{wins} l:{losses})")


def handle_trivia():
    questions = [
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
    ]
    score = 0
    for i, q in enumerate(questions):
        print(f"Q{i + 1}: {q['q']}")
        ans = input(">> ").strip().lower()
        if ans in ["quit", "exit", "q"]:
            print(f"{score}/{i}")
            return
        if ans == q["a"]:
            score += 1
            print("correct")
        else:
            print(q["a"])
    print(f"{score}/{len(questions)}")


def handle_guess():
    parts = input(">> ").strip()
    max_num = 100
    if parts:
        try:
            max_num = max(10, min(int(parts), 99999))
        except ValueError:
            pass
    target = random.randint(1, max_num)
    attempts = 0
    while True:
        inp = input(">> ").strip().lower()
        if inp in ["quit", "exit", "q"]:
            print(target)
            return
        try:
            guess = int(inp)
            attempts += 1
            if guess == target:
                print(f"correct: {target} ({attempts})")
                return
            elif guess < target:
                print(f"higher ({attempts})")
            else:
                print(f"lower ({attempts})")
        except ValueError:
            pass


def handle_command(rawcmd):
    if rawcmd in ["", " "]:
        return
    elif rawcmd in ["help", "help "]:
        print(
            "-> Welcome to the oNx terminal V1.0!\n  Basic:\n    exit / help / clear / man [cmd] / ver / about\n  Variables:\n    let(v) = val / print(v) / ls\n  Files:\n    cat [file] / echo [text] / whoami / date\n  Math:\n    calc [expr] / rand [min] [max]\n  Games:\n    rps / trivia / guess / dice [XdY] / 8ball / wyr\n  Text:\n    reverse / shuffle / morse / clap / emoji / upper / lower / caps / leet / acronym\n  Tools:\n    flip / countdown [s] / temp [val]c/f / bin/hex/oct [n]\n    pal / count / len / sort / fib / prime / factors / roman\n    name / pick / genpass [len] / todo\n  Tip: chain commands with &&"
        )
    elif rawcmd == "exit":
        return "exit"
    elif rawcmd == "man":
        print("usage: man [COMMAND]")
    elif rawcmd == "man help":
        print("Displays the available commands in the oNx terminal and the terminal's version.\n  Usage: 'help'")
    elif rawcmd == "man exit":
        print("Exits to the main chatbot.\n  Usage: 'exit'")
    elif rawcmd == "man man":
        print("Shows the manual/usage for a specific command.\n  Usage: 'man [COMMAND]'")
    elif rawcmd == "man clear":
        print("Clears the terminal screen.\n  Usage: 'clear'")
    elif rawcmd == "man let()":
        print('Defines a variable to a value.\n  Usage:\n    let(varname) = varvalue\n  Examples:\n    let(eggcount) = 5\n    let(hw) = "Hello World!"\n  Information:\n    If you define a variable using another variable (e.g. let(a) = b), a gets b`s value at that moment.')
    elif rawcmd == "man print()":
        print('Prints a variable, text, or expression.\n  Usage:\n    print(varname)\n    print("text")\n    print(x+y)\n  Supports +, -, *, / between variables and literals.')
    elif rawcmd == "man echo":
        print("Prints text to the terminal.\n  Usage: echo [text]\n  Example: echo Hello World!")
    elif rawcmd == "man ls":
        print("Lists all currently defined variables.\n  Usage: ls")
    elif rawcmd == "man cat":
        print("Simulates reading a file.\n  Usage: cat [filename]\n  This is a simulation, no real files are read.")
    elif rawcmd == "man whoami":
        print("Displays the current user of the terminal.\n  Usage: whoami")
    elif rawcmd == "man date":
        print("Displays the current system date and time.\n  Usage: date")
    elif rawcmd == "man calc":
        print("Evaluates a mathematical expression.\n  Usage: calc [expression]\n  Example: calc 5 + 3 * 2")
    elif rawcmd == "man rand":
        print("Generates a random number between min and max.\n  Usage: rand [min] [max]\n  Example: rand 1 100")
    elif rawcmd == "man ver":
        print("Shows the current terminal version.\n  Usage: ver")
    elif rawcmd == "man about":
        print("Displays information about the oNx terminal.\n  Usage: about")
    elif rawcmd == "man rps":
        print("Play Rock Paper Scissors.\n  Usage: rps\n  Type rock, paper, or scissors. 'quit' to exit.")
    elif rawcmd == "man todo":
        print("Manage a todo list.\n  Usage:\n    todo : List all tasks.\n    todo add [task] : Add a task.\n    todo remove [n] : Remove task by number.\n    todo clear : Clear all tasks.")
    elif rawcmd == "man dice":
        print("Roll virtual dice.\n  Usage:\n    dice : Roll 1d6.\n    dice 3d6 : Roll three 6-sided dice.\n    dice 2d20 : Roll two 20-sided dice.\n    dice 10 : Roll 1d10.")
    elif rawcmd == "man trivia":
        print("Trivia quiz.\n  Usage: trivia")
    elif rawcmd == "man genpass":
        print("Generate a random password.\n  Usage:\n    genpass : Generate a 16-character password.\n    genpass 24 : Generate a 24-character password.")
    elif rawcmd == "man guess":
        print("Number guessing game.\n  Usage: guess")
    elif rawcmd == "man 8ball":
        print("Magic 8 Ball.\n  Usage: 8ball")
    elif rawcmd == "man flip":
        print("Flip a coin.\n  Usage: flip")
    elif rawcmd == "man countdown":
        print("Countdown timer.\n  Usage: countdown [seconds]")
    elif rawcmd == "man temp":
        print("Convert temperature between C and F.\n  Usage: temp [value]c or temp [value]f")
    elif rawcmd == "man bin":
        print("Convert decimal to binary.\n  Usage: bin [number]")
    elif rawcmd == "man hex":
        print("Convert decimal to hexadecimal.\n  Usage: hex [number]")
    elif rawcmd == "man oct":
        print("Convert decimal to octal.\n  Usage: oct [number]")
    elif rawcmd == "man morse":
        print("Convert text to Morse code.\n  Usage: morse [text]")
    elif rawcmd == "man reverse":
        print("Reverse text.\n  Usage: reverse [text]")
    elif rawcmd == "man shuffle":
        print("Randomly shuffle text characters.\n  Usage: shuffle [text]")
    elif rawcmd == "man pal":
        print("Check if a word is a palindrome.\n  Usage: pal [word]")
    elif rawcmd == "man count":
        print("Count characters and words.\n  Usage: count [text]")
    elif rawcmd == "man sort":
        print("Sort items.\n  Usage: sort [item1] [item2] [...]")
    elif rawcmd == "man fib":
        print("Generate Fibonacci sequence.\n  Usage: fib [n]")
    elif rawcmd == "man prime":
        print("Check if a number is prime.\n  Usage: prime [number]")
    elif rawcmd == "man factors":
        print("Find all factors of a number.\n  Usage: factors [number]")
    elif rawcmd == "man roman":
        print("Convert number to Roman numerals.\n  Usage: roman [number] (1-3999)")
    elif rawcmd == "man name":
        print("Generate a random username.\n  Usage: name")
    elif rawcmd == "man wyr":
        print("Get a random 'Would You Rather' question.\n  Usage: wyr")
    elif rawcmd == "man pick":
        print("Pick a random item from a list.\n  Usage: pick [item1] [item2] [...]")
    elif rawcmd == "man clap":
        print("Add clap emoji between words.\n  Usage: clap [text]")
    elif rawcmd == "man emoji":
        print("Add random emojis after words.\n  Usage: emoji [text]")
    elif rawcmd == "man len":
        print("Count characters in text.\n  Usage: len [text]")
    elif rawcmd == "man upper":
        print("Convert text to uppercase.\n  Usage: upper [text]")
    elif rawcmd == "man lower":
        print("Convert text to lowercase.\n  Usage: lower [text]")
    elif rawcmd == "man caps":
        print("Convert text to alternating caps.\n  Usage: caps [text]")
    elif rawcmd == "man leet":
        print("Convert text to leetspeak.\n  Usage: leet [text]")
    elif rawcmd == "man acronym":
        print("Make an acronym from words.\n  Usage: acronym [text]")
    elif rawcmd == "clear":
        print("\033[2J\033[H", end="", flush=True)
    elif rawcmd == "ver":
        print("oNx Terminal V1.0")
    elif rawcmd == "about":
        print("oNx Terminal V1.0  XlRC888  Manual Intellegence")
    elif rawcmd == "whoami":
        print("guest")
    elif rawcmd == "date":
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    elif rawcmd.startswith("echo "):
        print(rawcmd[5:])
    elif rawcmd == "ls":
        if variables:
            for k, v in variables.items():
                print(f"{k} = {v}")
        else:
            print("(none)")
    elif rawcmd.startswith("cat "):
        filename = rawcmd[4:].strip()
        fake_files = {
            "readme": "Welcome to oNx Terminal!\nThis is a simulated file system.\nHave fun exploring!",
            "welcome": "Welcome to Manual Intellegence!\nType 'help' to see available commands.\nType 'exit' to return to main bot.",
            "help": "This file contains help information.\nFor more details, type 'help' in the terminal.",
            "about": "oNx Terminal V1.0  XlRC888",
            "secret": "You found a secret file!\nThere is no treasure here, but congratulations anyway!",
            "motd": "Message of the day:\nKeep calm and code on!",
            "license": "MIT License\nCopyright (c) 2024 XlRC888\nPermission is hereby granted...",
            "todo": "Things to add:\n- More commands\n- Better error handling\n- Scripting support\n- Game integration",
            "games": "rps  trivia  guess  dice",
        }
        if filename in fake_files:
            print(fake_files[filename])
        else:
            print(f"cat: {filename}: No such file or directory")
    elif rawcmd.startswith("calc "):
        expr = rawcmd[5:].replace("^", "**")
        try:
            result = eval(expr)
            print(result)
        except Exception:
            print("invalid expression")
    elif rawcmd.startswith("rand "):
        parts = rawcmd[5:].split()
        if len(parts) == 2:
            try:
                min_v = int(parts[0])
                max_v = int(parts[1])
                if min_v > max_v:
                    min_v, max_v = max_v, min_v
                print(random.randint(min_v, max_v))
            except ValueError:
                print("usage: rand [min] [max]")
        else:
            print("usage: rand [min] [max]")
    elif rawcmd == "rps":
        handle_rps()
    elif rawcmd == "trivia":
        handle_trivia()
    elif rawcmd == "guess":
        handle_guess()
    elif rawcmd == "flip" or rawcmd == "coin":
        print(random.choice(["Heads!", "Tails!"]))
    elif rawcmd.startswith("countdown "):
        try:
            secs = max(1, min(int(rawcmd[10:].strip()), 999))
            for i in range(secs, 0, -1):
                print(i)
                time.sleep(1)
            print("done")
        except ValueError:
            print("usage: countdown [seconds]")
    elif rawcmd.startswith("temp "):
        val = rawcmd[5:].strip().lower()
        match = re.match(r"(-?\d+(?:\.\d+)?)\s*([cf])", val)
        if match:
            num = float(match.group(1))
            unit = match.group(2)
            if unit == "c":
                print(f"{round(num * 9/5 + 32, 1)}F")
            else:
                print(f"{round((num - 32) * 5/9, 1)}C")
        else:
            print("usage: temp [val]c or temp [val]f")
    elif rawcmd.startswith("bin ") or rawcmd.startswith("hex ") or rawcmd.startswith("oct "):
        try:
            cmd, val = rawcmd.split(None, 1)
            n = int(val.strip())
            if rawcmd.startswith("bin "):
                print(f"0b{bin(n)[2:]}")
            elif rawcmd.startswith("hex "):
                print(f"0x{hex(n)[2:].upper()}")
            else:
                print(f"0o{oct(n)[2:]}")
        except ValueError:
            print("usage: bin/hex/oct [number]")
    elif rawcmd.startswith("morse "):
        text = rawcmd[6:].strip().lower()
        result = []
        for ch in text:
            if ch in morse_map_term:
                result.append(morse_map_term[ch])
            elif ch == " ":
                result.append("/")
        print(" ".join(result))
    elif rawcmd.startswith("reverse "):
        print(rawcmd[8:].strip()[::-1])
    elif rawcmd.startswith("shuffle "):
        chars = list(rawcmd[8:].strip())
        random.shuffle(chars)
        print("".join(chars))
    elif rawcmd.startswith("pal "):
        word = rawcmd[4:].strip().lower()
        clean = re.sub(r'[^a-z0-9]', '', word)
        if clean and clean == clean[::-1]:
            print("yes")
        else:
            print("no")
    elif rawcmd.startswith("count "):
        text = rawcmd[6:].strip()
        chars = len(text)
        words = len(text.split()) if text else 0
        print(f"{chars} chars, {words} words")
    elif rawcmd.startswith("sort "):
        items = rawcmd[5:].strip().split()
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
        print(" ".join(str(x) for x in (nums + strs)))
    elif rawcmd.startswith("fib "):
        try:
            n = min(int(rawcmd[4:].strip()), 100)
            seq = []
            a, b = 0, 1
            for _ in range(n):
                seq.append(a)
                a, b = b, a + b
            print(" ".join(str(x) for x in seq))
        except ValueError:
            print("usage: fib [n]")
    elif rawcmd.startswith("prime "):
        try:
            n = int(rawcmd[6:].strip())
            if n < 2:
                print("no")
            else:
                for i in range(2, int(n ** 0.5) + 1):
                    if n % i == 0:
                        print("no")
                        break
                else:
                    print("yes")
        except ValueError:
            print("usage: prime [n]")
    elif rawcmd.startswith("factors "):
        try:
            n = int(rawcmd[8:].strip())
            facts = [i for i in range(1, n + 1) if n % i == 0]
            print(" ".join(str(x) for x in facts))
        except ValueError:
            print("usage: factors [n]")
    elif rawcmd.startswith("roman "):
        try:
            n = int(rawcmd[6:].strip())
            if n < 1 or n > 3999:
                print("use 1-3999")
            else:
                result = ""
                for v, s in zip(roman_vals_term, roman_syms_term):
                    while n >= v:
                        result += s
                        n -= v
                print(result)
        except ValueError:
            print("usage: roman [n]")
    elif rawcmd == "name":
        name = random.choice(name_prefixes_term) + random.choice(name_suffixes_term) + str(random.randint(1, 99))
        print(name)
    elif rawcmd == "wyr":
        print(random.choice(wyr_questions_term))
    elif rawcmd.startswith("pick "):
        items = rawcmd[5:].strip().split()
        if items:
            print(random.choice(items))
    elif rawcmd.startswith("clap "):
        print(" 👏 ".join(rawcmd[5:].strip().split()))
    elif rawcmd.startswith("emoji "):
        words = rawcmd[6:].strip().split()
        print(" ".join(w + " " + random.choice(text_emojis_term) for w in words))
    elif rawcmd.startswith("len "):
        print(len(rawcmd[4:].strip()))
    elif rawcmd.startswith("upper "):
        print(rawcmd[6:].strip().upper())
    elif rawcmd.startswith("lower "):
        print(rawcmd[6:].strip().lower())
    elif rawcmd.startswith("caps "):
        text = rawcmd[5:].strip()
        print("".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text)))
    elif rawcmd.startswith("leet "):
        leet_table = str.maketrans("aeiotl", "431071")
        print(rawcmd[5:].strip().lower().translate(leet_table))
    elif rawcmd.startswith("acronym "):
        words = rawcmd[8:].strip().split()
        print("".join(w[0].upper() for w in words if w))
    elif rawcmd.startswith("8ball"):
        print(random.choice(eightball_responses_term))
    elif rawcmd.startswith("todo"):
        parts = rawcmd.split(maxsplit=1)
        if len(parts) == 1:
            if not todos_term:
                print("(empty)")
            else:
                for i, task in enumerate(todos_term, 1):
                    print(f"{i}: {task}")
        else:
            sub = parts[1].strip()
            if sub.startswith("add "):
                task = sub[4:]
                if task:
                    todos_term.append(task)
                    print(f"added: {task} ({len(todos_term)})")
            elif sub.startswith("remove ") or sub.startswith("rm "):
                try:
                    idx = int(sub.split()[1]) - 1
                    if 0 <= idx < len(todos_term):
                        removed = todos_term.pop(idx)
                        print(f"removed: {removed}")
                    else:
                        print(f"invalid index ({len(todos_term)} tasks)")
                except (ValueError, IndexError):
                    print("usage: todo remove [n]")
            elif sub == "clear":
                todos_term.clear()
                print("cleared")
            elif sub == "list":
                if not todos_term:
                    print("(empty)")
                else:
                    for i, task in enumerate(todos_term, 1):
                        print(f"{i}: {task}")
            else:
                print("usage: todo, todo add [task], todo remove [n], todo clear")
    elif rawcmd.startswith("dice"):
        parts = rawcmd.split()
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
            print(rolls[0])
        else:
            print(f"{rolls} = {sum(rolls)}")
    elif rawcmd.startswith("genpass"):
        parts = rawcmd.split()
        length = 16
        if len(parts) >= 2:
            try:
                length = max(4, min(int(parts[1]), 128))
            except ValueError:
                pass
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(chars) for _ in range(length))
        print(password)
    elif rawcmd.startswith('print("') or rawcmd.startswith("print('"):
        printraw = rawcmd[7:-2]
        print(printraw)
    elif rawcmd.startswith("let("):
        match = re.match(r"let\((\w+)\)\s*=\s*(.+)", rawcmd)
        if match:
            varname = match.group(1)
            varvalue = match.group(2).strip()
            if (varvalue.startswith('"') and varvalue.endswith('"')) or (
                varvalue.startswith("'") and varvalue.endswith("'")
            ):
                varvalue = varvalue[1:-1]
            else:
                try:
                    varvalue = int(varvalue)
                except ValueError:
                    try:
                        varvalue = float(varvalue)
                    except ValueError:
                        if varvalue in variables:
                            varvalue = variables[varvalue]
                        else:
                            result, err = eval_expr(varvalue)
                            if err:
                                print(f"undefined: {varvalue}")
                                return
                            varvalue = result
            variables[varname] = varvalue
            print(f"{varname} = {variables[varname]}")
        else:
            suggestion = get_suggestion(rawcmd, commands)
            if suggestion and suggestion != rawcmd:
                print(f"unknown command. did you mean '{suggestion}'?")
            else:
                print("usage: let(varname) = value")
    elif rawcmd.startswith("print("):
        inner = re.match(r"print\((.+)\)$", rawcmd)
        if inner:
            expr = inner.group(1).strip()
            if re.match(r"^\w+$", expr):
                if expr in variables:
                    print(variables[expr])
                else:
                    print(f"undefined: {expr}")
            else:
                result, err = eval_expr(expr)
                if err:
                    print(err)
                else:
                    print(result)
        else:
            suggestion = get_suggestion(rawcmd, commands)
            if suggestion:
                print(f"unknown command. did you mean '{suggestion}'?")
            else:
                print("usage: print(varname) or print(x+y)")
    else:
        suggestion = get_suggestion(rawcmd, commands)
        if suggestion:
            print(f"unknown command. did you mean '{suggestion}'?")
        else:
            print("unknown command. type 'help'")


def run_subcommand_term(cmd, args):
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


def resolve_subcommands_term(text):
    while re.search(r'\(\$(\w+)\s*([^()]*)\)', text):
        text = re.sub(r'\(\$(\w+)\s*([^()]*)\)', lambda m: str(run_subcommand_term(m.group(1), m.group(2).strip())), text)
    return text


def run_terminal():
    while True:
        rawcmd = input(">> ").strip()
        parts = [p.strip() for p in rawcmd.split("&&")]
        for part in parts:
            part = resolve_subcommands_term(part)
            result = handle_command(part)
            if result == "exit":
                return

if __name__ == "__main__":
    run_terminal()
