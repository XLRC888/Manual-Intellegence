# the fake terminal (out of boredom)
import difflib
import re

variables = {}
commands = ["man", "man exit", "man help", "man man", "man let()", "man print()", "help", "exit", "print()", "let()", "clear"]

def get_suggestion(rawsug, commands):
    stripped_input = re.sub(r'\(.*', '()', rawsug)
    matches = difflib.get_close_matches(stripped_input, commands, n=1, cutoff=0.5)
    return matches[0] if matches else None

def run_terminal():
    while True:
        rawcmd = input(">> ").strip()
        if rawcmd in ["", " "]:
            continue
        elif rawcmd in ["help", "help "]:
            print('-> Welcome to the oNx terminal V0.02!\n  The available commands are:\n    exit : Exits to the main chatbot.\n    help : Displays this text.\n    clear : Clears the terminal.\n    man (Usage: man [COMMAND]) : Shows the manual for a specific command.\n    print() : Prints either a variable (without double quotation marks) or a text (with double quotation marks).\n    let() = value : Defines a variable.')
        elif rawcmd == "exit":
            break
        elif rawcmd == "man":
            print("Improper usage of command 'man'. Correct usage:\n  man [COMMAND]")
        elif rawcmd == "man help":
            print("Displays the available commands in the oNx terminal and the terminal's version.\n  Usage: 'help'")
        elif rawcmd == "man exit":
            print("Exits to the main chatbot.\n  Usage: 'exit'")
        elif rawcmd == "man man":
            print("Shows the manual/usage for a specific command.\n  Usage: 'man [COMMAND]'")
        elif rawcmd == "man clear":
            print("Clears the terminal screen.\n  Usage: 'clear'")
        elif rawcmd == "man let()":
            print('Defines a variable to a value.\n  Usage:\n    let(varname) = varvalue\n  Examples:\n    let(eggcount) = 5\n    let(hw) = "Hello World!"\n  Information:\n    If you define a variable using another variable (e.g. let(a) = b), a gets b`s value at that moment. If you change b later, a won`t update automatically, and you`ll need to define a again.')
        elif rawcmd == "man print()":
            print('Prints a variable/text.\n  Usage:\n    print(varname)\n  Examples:\n    print(eggcount)\n    print("Hello World!")')
        elif rawcmd == "clear":
            print("\033[2J\033[H", end="", flush=True)
        elif rawcmd.startswith('print("') or rawcmd.startswith("print('"):
            printraw = rawcmd[7:-2]
            print(printraw)
            
        elif rawcmd.startswith('let('):
            match = re.match(r"let\((\w+)\)\s*=\s*(.+)", rawcmd)
            if match:
                varname = match.group(1)
                varvalue = match.group(2).strip()
                if (varvalue.startswith('"') and varvalue.endswith('"')) or \
                    (varvalue.startswith("'") and varvalue.endswith("'")):
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
                                print(f"Undefined variable '{varvalue}'")
                                continue
                variables[varname] = varvalue
                print(f"Successfully set {varname} = {variables[varname]}")
            else:
                suggestion = get_suggestion(rawcmd, commands)
                if suggestion and suggestion != rawcmd:
                    print(f"Unknown command '{rawcmd}'. Did you mean '{suggestion}'?")
                else:
                    print("Improper usage of command 'let'. Correct usage:\n  let(varname) = value")

        elif rawcmd.startswith('print('):
            match = re.match(r"print\((\w+)\)$", rawcmd)
            if match:
                varname = match.group(1)
                if varname in variables:
                    print(variables[varname])
                else:
                    print(f"Undefined variable '{varname}'")
            else:
                suggestion = get_suggestion(rawcmd, commands)
                if suggestion:
                    print(f"Unknown command '{rawcmd}'. Did you mean '{suggestion}'?")
                else:
                    print("Invalid syntax. Usage: print(varname)")
                    
        else:
            suggestion = get_suggestion(rawcmd, commands)
            if suggestion:
                print(f"Unknown command '{rawcmd}'. Did you mean '{suggestion}'?")
            else:
                print("Unknown command. See the available commands at 'help'.")