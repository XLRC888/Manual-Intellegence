import difflib
import re

variables = {}
commands = [
    "man",
    "man exit",
    "man help",
    "man man",
    "man let()",
    "man print()",
    "help",
    "exit",
    "print()",
    "let()",
    "clear",
]


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
            return None, f"Undefined variable '{t}'"
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
                return None, "Division by zero"
            result = result / rhs
        i += 2
    return result, None


def handle_command(rawcmd):
    if rawcmd in ["", " "]:
        return
    elif rawcmd in ["help", "help "]:
        print(
            "-> Welcome to the oNx terminal V0.03!\n  The available commands are:\n    exit : Exits to the main chatbot.\n    help : Displays this text.\n    clear : Clears the terminal.\n    man (Usage: man [COMMAND]) : Shows the manual for a specific command.\n    print() : Prints a variable, text, or expression (e.g. print(x+y)).\n    let() = value : Defines a variable.\n  Tip: chain commands with &&"
        )
    elif rawcmd == "exit":
        return "exit"
    elif rawcmd == "man":
        print("Improper usage of command 'man'. Correct usage:\n  man [COMMAND]")
    elif rawcmd == "man help":
        print(
            "Displays the available commands in the oNx terminal and the terminal's version.\n  Usage: 'help'"
        )
    elif rawcmd == "man exit":
        print("Exits to the main chatbot.\n  Usage: 'exit'")
    elif rawcmd == "man man":
        print(
            "Shows the manual/usage for a specific command.\n  Usage: 'man [COMMAND]'"
        )
    elif rawcmd == "man clear":
        print("Clears the terminal screen.\n  Usage: 'clear'")
    elif rawcmd == "man let()":
        print(
            'Defines a variable to a value.\n  Usage:\n    let(varname) = varvalue\n  Examples:\n    let(eggcount) = 5\n    let(hw) = "Hello World!"\n  Information:\n    If you define a variable using another variable (e.g. let(a) = b), a gets b`s value at that moment.'
        )
    elif rawcmd == "man print()":
        print(
            'Prints a variable, text, or expression.\n  Usage:\n    print(varname)\n    print("text")\n    print(x+y)\n  Supports +, -, *, / between variables and literals.'
        )
    elif rawcmd == "clear":
        print("\033[2J\033[H", end="", flush=True)
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
                                print(f"Undefined variable '{varvalue}'")
                                return
                            varvalue = result
            variables[varname] = varvalue
            print(f"Successfully set {varname} = {variables[varname]}")
        else:
            suggestion = get_suggestion(rawcmd, commands)
            if suggestion and suggestion != rawcmd:
                print(f"Unknown command '{rawcmd}'. Did you mean '{suggestion}'?")
            else:
                print(
                    "Improper usage of command 'let'. Correct usage:\n  let(varname) = value"
                )
    elif rawcmd.startswith("print("):
        inner = re.match(r"print\((.+)\)$", rawcmd)
        if inner:
            expr = inner.group(1).strip()
            if re.match(r"^\w+$", expr):
                if expr in variables:
                    print(variables[expr])
                else:
                    print(f"Undefined variable '{expr}'")
            else:
                result, err = eval_expr(expr)
                if err:
                    print(f"Error: {err}")
                else:
                    print(result)
        else:
            suggestion = get_suggestion(rawcmd, commands)
            if suggestion:
                print(f"Unknown command '{rawcmd}'. Did you mean '{suggestion}'?")
            else:
                print("Invalid syntax. Usage: print(varname) or print(x+y)")
    else:
        suggestion = get_suggestion(rawcmd, commands)
        if suggestion:
            print(f"Unknown command '{rawcmd}'. Did you mean '{suggestion}'?")
        else:
            print("Unknown command. See the available commands at 'help'.")


def run_terminal():
    while True:
        rawcmd = input(">> ").strip()
        parts = [p.strip() for p in rawcmd.split("&&")]
        for part in parts:
            result = handle_command(part)
            if result == "exit":
                return
