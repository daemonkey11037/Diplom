import re
from colorama import Fore, Style

def passcheck(password):
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&\)\(\}\{\]\[\.\,])[A-Za-z\d@$!%*#?&\)\(\}\{\]\[\.\,]{8,}$"

    if re.search(regex, password):
        print(Fore.LIGHTGREEN_EX + "Cool!" + Style.RESET_ALL)
        return True

    else:
        print(Fore.LIGHTRED_EX + 'Bad!' + Style.RESET_ALL)
        return False