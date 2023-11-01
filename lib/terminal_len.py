import subprocess
import os


def get_column_length(loc: str) -> str | None:
    """Returns the length of the terminal in columns\n
    :param loc: The language to be used"""

    if os.name == "nt":
        match loc:
            case loc.startswith("de"):
                mode_con_out = subprocess.check_output("mode con|findstr Spalten", shell=True)
                terminal_column_length = mode_con_out.split()[1].decode("utf-8")
            case loc.startswith("en"):
                mode_con_out = subprocess.check_output("mode con|findstr Columns", shell=True)
                terminal_column_length = mode_con_out.split()[1].decode("utf-8")
            case _:
                terminal_column_length = None
    else:
        terminal_column_length = os.get_terminal_size().columns

    return terminal_column_length


def get_line_length(loc: str) -> str | None:
    """Returns the length of the terminal in lines\n
    :param loc: The language to be used"""

    if os.name == "nt":
        match loc:
            case loc.startswith("de"):
                mode_con_out = subprocess.check_output("mode con|findstr Zeilen", shell=True)
                terminal_line_length = mode_con_out.split()[1].decode("utf-8")
            case loc.startswith("en"):
                mode_con_out = subprocess.check_output("mode con|findstr Lines", shell=True)
                terminal_line_length = mode_con_out.split()[1].decode("utf-8")
            case _:
                terminal_line_length = None
    else:
        terminal_line_length = os.get_terminal_size().lines

    return terminal_line_length
