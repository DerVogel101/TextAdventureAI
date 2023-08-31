import os
import subprocess
from BColors import BColors


def del_last_line(loops: int = 1):
    """Deletes the last line in the terminal
    :param loops: The number of lines to be deleted default = 1"""
    cursor_up = '\x1b[{}A'.format(loops)
    erase_line = '\x1b[2K'
    for _ in range(loops):
        print(cursor_up + erase_line + cursor_up)


def clear_terminal(ignore_error: bool = False):
    """Clears the terminal
    :param ignore_error: If the function should ignore the error if the terminal is not supported default = False"""
    operating_system = os.name
    if operating_system == "nt":
        subprocess.run("cls", shell=True)
    elif operating_system == "posix":
        subprocess.run("clear", shell=True)
    else:
        if not ignore_error:
            print(BColors.WARNING + "Warning: Your Terminal is not Supported!\n"
                                    "         Do You want to Continue anway\n"
                                    "         Y/N  Y for Continue / N for Quit" + BColors.ENDC)
            user_input = input("Your choice: ")
            if user_input not in ["Y", "y", "J", "j"]:
                exit(1)