# Author: DerVogel101
# Version: 1.1.0
# Last Modified: 31.08.2023
# Description: A simple text adventure game with an AI as the game master.
# GitHub: https://github.com/DerVogel101/TextAdventureAI


import openai
import os
import json
import locale
import subprocess
from dotenv import load_dotenv


class GamePrompt:
    """
    A class to edit multiline strings for AI prompts.
    """
    def __init__(self, prompt=""):
        """
        :param prompt: The prompt to be edited (Optional).
        """
        self.prompt = prompt

    def add_from_string(self, prompt: str):
        """
        Adds a new line to the prompt.
        :param prompt: The string to be added to the prompt.
        :return: None
        """
        self.prompt = self.prompt + "\n" + prompt

    def set_from_string(self, prompt: str):
        """
        Sets the prompt to a new string.
        :param prompt: The string to be set as the prompt.
        :return: None
        """
        self.prompt = prompt

    def add_from_list(self, prompt_list: list[str]):
        """
        Adds multiple lines to the prompt.
        :param prompt_list: The list of strings to be added to the prompt.
        :return: None
        """
        self.prompt = self.prompt + "\n" + "\n".join(prompt_list)

    def set_from_list(self, prompt_list: list[str]):
        """
        Sets the prompt to a new list of strings.
        :param prompt_list: The list of strings to be set as the prompt.
        :return: None
        """
        self.prompt = "\n".join(prompt_list)

    def pop(self, line: int):
        """
        Removes a line from the prompt and returns it.
        :param line: number of the line to be popped.
        :return: popped line.
        """
        prompt_list = self.prompt.splitlines()
        poped_line = prompt_list.pop(line)
        self.prompt = "\n".join(prompt_list)
        return poped_line

    def remove_lines(self, lines: iter):
        """
        Removes multiple lines from the prompt.
        :param lines: lines to be removed.
        :return: None
        """
        prompt_list = self.prompt.splitlines()
        prompt_dict = {}
        for lnum, line in enumerate(prompt_list):
            prompt_dict[lnum] = line
        for lnum in lines:
            prompt_dict.pop(lnum)
        sorted_keys = sorted(prompt_dict)
        prompt_list = []
        for key in sorted_keys:
            prompt_list.append(prompt_dict[key])
        self.prompt = "\n".join(prompt_list)

    def edit_line(self, line: int, new_line: str):
        """
        Edits a line in the prompt.
        :param line: Line to be edited.
        :param new_line: The new line.
        :return: None
        """
        prompt_list = self.prompt.splitlines()
        prompt_list[line] = new_line
        self.prompt = "\n".join(prompt_list)

    def line_string(self):
        """
        Returns the prompt as a string with Line numbers in front of the string 1:,2:,3:.
        :return: The Prompt as a string
        """
        prompt_list = self.prompt.splitlines()

        for lnum, line in enumerate(prompt_list):
            prompt_list[lnum] = f"{lnum}: {line}"

        return "\n".join(prompt_list)

    def list_string_break(self, break_len: int, display_line_number: bool = True):
        """
        Provides a list of strings with a maximum length of break_len.\n
        The line is broken at the last space before the break_len if there is a space.
        :param break_len: The maximum length of the strings, the Value gets subtracted by 4.
        :param display_line_number: If the line number should be displayed.
        :return: The list of strings.
        """
        break_len -= 4
        list_string_break_output = []

        if display_line_number:
            prompt_list = self.line_string().splitlines()
        else:
            prompt_list = self.prompt.splitlines()

        def break_line(line: str):
            if (llen := len(line)) > break_len:
                for index, char in enumerate(reversed(line)):
                    if llen - index <= break_len and char == " ":
                        list_string_break_output.append(line[:llen - index])
                        if llen - index < llen:
                            break_line(line[llen - index + 0:])
                        break
                else:
                    list_string_break_output.append(line[:break_len])
                    break_line(line[break_len + 0:])
            else:
                list_string_break_output.append(line)
        for line in prompt_list:
            break_line(line)

        return list_string_break_output

    def __str__(self):
        """
        Returns the prompt as a string.
        :return: The prompt as a string.
        """
        return self.prompt

    def __iter__(self):
        """
        Returns the prompt as an iterator.
        :return: The prompt as an iterator.
        """
        return iter(self.prompt.splitlines())

    def __getitem__(self, index):
        """
        Returns the line at the index.
        :param index: The index of the line.
        :return: The line at the index.
        """
        return self.prompt.splitlines()[index]

    def __len__(self):
        """
        Returns the number of lines in the prompt.
        :return: Length of the prompt.
        """
        return len(self.prompt.splitlines())


class FileControl:
    """
    A class to control the needed files.
    """
    def __init__(self, prompt_path: str, save_path: str):
        """
        :param prompt_path: The path to the prompt files.
        :param prompt_path: The path to Prompts.
        :param save_path: The path to Saves.
        """
        self.prompt_path = prompt_path
        self.save_path = save_path

    def save_prompt(self, prompt: GamePrompt, filename: str):
        """
        Saves a prompt to a json file.
        :param prompt: The prompt to be saved.
        :param filename: The filename to save the prompt to.
        :return: None
        """
        with open(os.path.join(self.prompt_path, filename + ".json"), "w") as file:
            json.dump(str(prompt), file)

    def save_state(self, conversation: list[dict], message_history: list[str], filename: str):
        """
        Saves the conversation and history to json files\n
        the files end with _conv.json and _hist.json.
        :param conversation: The conversation to be saved.
        :param message_history: The history to be saved.
        :param filename: The filename to save the conversation and history to.
        :return: None
        """
        with open(os.path.join(self.save_path, filename + "_conv.json"), "w") as file:
            json.dump(conversation, file)
        with open(os.path.join(self.save_path, filename + "_hist.json"), "w") as file:
            json.dump(message_history, file)

    def load_prompt(self, filename: str):
        """
        Loads a prompt from a json file.
        :param filename: The filename to load the prompt from.
        :return: The prompt as a string.
        """
        with open(os.path.join(self.prompt_path, filename + ".json"), "r") as file:
            return json.load(file)

    def load_state(self, filename: str) -> tuple[list[dict], list[str]]:
        """
        Loads the conversation and history from json save files\n
        the files end with _conv.json and _hist.json.
        :param filename: The filename to load the conversation and history from.
        :return: The conversation and history as a tuple.
        """
        with open(os.path.join(self.save_path, filename + "_conv.json"), "r") as file:
            output_conv: list[dict] = json.load(file)
        with open(os.path.join(self.save_path, filename + "_hist.json"), "r") as file:
            output_hist: list[str] = json.load(file)
        return output_conv, output_hist


class BColors:
    """
    A class to color the terminal output.\n
    Using ANSI escape sequences.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def mbar_construct(terminal_column_length: int, menu_bar: list[str], override_len: int = 2, fill: str = "█",
                   ignore_error: bool = False) -> str:
    """
    Constructs a menu bar with the given parameters.\n
    The menu bar is centered in the terminal.
    :param terminal_column_length: Length of the terminal in columns.
    :param menu_bar: The menu bar to be constructed.
    :param override_len: The length of the menu bar to override. Default = 2 (Optional)
    :param fill: The fill character. Default = "█" (Optional)
    :param ignore_error: If the function should ignore the error if the estimated length of the menu bar is greater
                         than the terminal length. Default = False (Optional)
    :return: The constructed menu bar.
    """
    menu_bar_size = {}
    estimated_length = 0
    menu_bar_amount = len(menu_bar)
    for bar_pos, option in enumerate(menu_bar):
        estimated_length += (option_length := len(option) + 2)
        menu_bar_size[bar_pos] = option_length

    if estimated_length > terminal_column_length and not ignore_error:
        raise TerminalLengthException("The estimated length of the menu bar is greater than the terminal length.")

    menu_bar_length_remain = terminal_column_length - estimated_length
    menu_bar_add = menu_bar_length_remain // menu_bar_amount
    menu_bar_add_remain = menu_bar_length_remain % menu_bar_amount

    for bar_pos, option in enumerate(menu_bar):
        fill_length = menu_bar_size[bar_pos] + menu_bar_add
        if (menu_bar_override_len := menu_bar_size[bar_pos] * override_len) < fill_length:
            menu_bar_add_remain += fill_length - menu_bar_override_len
            fill_length = menu_bar_override_len

        menu_bar[bar_pos] = f"{option:{fill}^{fill_length}}"

    menu_bar_output = "".join(menu_bar)

    if menu_bar_add_remain > 0:
        menu_bar_output = menu_bar_output + fill * menu_bar_add_remain

    return menu_bar_output


class Border:
    """
    A class to construct borders around a string.
    """
    def __init__(self, border_up: list[str, str], border_down: list[str, str], border_vert: str,
                 border_horizont: str, column_length: int):
        """
        :param border_up: The left and right corner characters of the upper border.
        :param border_down: The left and right corner characters of the lower border.
        :param border_vert: The vertical border character.
        :param border_horizont: The horizontal border character.
        :param column_length: The column length of the border.
        """
        self.border_up = border_up
        self.border_down = border_down
        self.border_vert = border_vert
        self.border_horizont = border_horizont
        self.column_length = column_length

    def en_up(self, text: str) -> str:
        """Returns a string with the upper border"""
        return f"{self.border_up[0]}{text}{self.border_up[1]}"

    def en_down(self, text: str) -> str:
        """Returns a string with the lower border"""
        return f"{self.border_down[0]}{text}{self.border_down[1]}"

    def en_vert(self, text: str, add_len: int = 0) -> str:
        """
        Returns a string with the vertical border
        :param text: String to be wrapped
        :param add_len: Additional length to be added to the string, usecase: if ANSI escape sequences are used
        :return: String with the vertical border
        """
        return f"{self.border_vert} {text:<{self.column_length - 4 + add_len}} {self.border_vert}"

    def en_horizont(self, text: str, add_len: int = 0) -> str:
        """
        Returns a string with the horizontal border
        :param text: String to be wrapped
        :param add_len: Additional length to be added to the string, usecase: if ANSI escape sequences are used
        :return: String with the horizontal border
        """
        return f"{text:{self.border_horizont}^{self.column_length + add_len}}"

    def en_c_up(self, text: str, add_len: int = 0) -> str:
        """
        Centers the text and returns a string with the upper border and corners
        :param text: String to be wrapped
        :param add_len: Additional length to be added to the string, usecase: if ANSI escape sequences are used
        :return: String with the upper border and corners
        """
        return f"{self.border_up[0]}{text:{self.border_horizont}^{self.column_length - 2 + add_len}}{self.border_up[1]}"

    def en_c_down(self, text: str, add_len: int = 0) -> str:
        """
        Centers the text and returns a string with the lower border and corners
        :param text: String to be wrapped
        :param add_len: Additional length to be added to the string, usecase: if ANSI escape sequences are used
        :return: String with the lower border and corners
        """
        return f"{self.border_down[0]}{text:{self.border_horizont}^{self.column_length - 2 + add_len}}{self.border_down[1]}"

    def en_wrap(self, text_list: list, add_len: dict[int:int] = None) -> str:
        """
        Wraps a list of strings in vertical borders
        :param text_list: List of strings to be wrapped
        :param add_len: Additional length to be added to the line of a string, must be a dict with the line number as key
                        and the additional length as value,
                        usecase: if ANSI escape sequences are used
        :return: String with the vertical borders
        """
        en_wrap_output = []
        for lnum, line in enumerate(text_list):
            if lnum in add_len:
                wr_add_len = add_len[lnum]
            else:
                wr_add_len = 0
            en_wrap_output.append(self.en_vert(line, wr_add_len))

        return "\n".join(en_wrap_output)


def del_last_line(loops: int = 1):
    """Deletes the last line in the terminal
    :param loops: The number of lines to be deleted default = 1"""
    cursor_up = '\x1b[{}A'.format(loops)
    erase_line = '\x1b[2K'
    for _ in range(loops):
        print(cursor_up + erase_line + cursor_up)


def get_line_space(text: str, term_column_length: int, text_space_offset: int = 0) -> int:
    """Returns the number of lines the text needs in the terminal
    :param text: The text to be checked
    :param term_column_length: The length of the terminal in columns
    :param text_space_offset: The offset of the text space default = 0"""
    text_length = len(text) + text_space_offset
    if text_length < term_column_length:
        return 1
    else:
        complete_lines = text_length // term_column_length
        if text_length % term_column_length > 0:
            complete_lines += 1
        return complete_lines


def communicate_with_ai(messages_to_send: list[dict[str, str]], model_name: str) -> dict:
    """Communicates with the ChatGPT API and returns the response.
    :param messages_to_send: The messages to send to the API.
    :param model_name: The name of the model to use.
    :return: The response from the API.
    """

    communicate_with_ai_response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages_to_send
    )

    return communicate_with_ai_response


class TerminalLengthException(Exception):
    pass


class Continue(Exception):
    pass


def get_column_length(loc: str) -> str | None:
    """Returns the length of the terminal in columns\n
    :param loc: The language to be used"""

    if os.name == "nt":
        match loc:
            case "de_DE" | "de_AT" | "de_CH" | "de_LU":
                mode_con_out = subprocess.check_output("mode con|findstr Spalten", shell=True)
                terminal_column_length = mode_con_out.split()[1].decode("utf-8")
            case "en_US" | "en_GB" | "en_CA" | "en_AU":
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
            case "de_DE" | "de_AT" | "de_CH" | "de_LU":
                mode_con_out = subprocess.check_output("mode con|findstr Zeilen", shell=True)
                terminal_line_length = mode_con_out.split()[1].decode("utf-8")
            case "en_US" | "en_GB" | "en_CA" | "en_AU":
                mode_con_out = subprocess.check_output("mode con|findstr Lines", shell=True)
                terminal_line_length = mode_con_out.split()[1].decode("utf-8")
            case _:
                terminal_line_length = None
    else:
        terminal_line_length = os.get_terminal_size().lines

    return terminal_line_length


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


if __name__ == "__main__":
    # Load the API key from the .env file
    load_dotenv()
    openai.api_key = os.getenv("API_KEY")

    # Create the paths to the prompt and save folders
    app_path = os.path.dirname(os.path.abspath(__file__))
    path_folder_prompt = os.path.join(app_path, "prompts")
    path_folder_save = os.path.join(app_path, "saves")
    # Create the FileControl object
    files = FileControl(path_folder_prompt, path_folder_save)

    # Create the folders if they don't exist
    if not os.path.exists(path_folder_prompt):
        os.mkdir(path_folder_prompt)
    if not os.path.exists(path_folder_save):
        os.mkdir(path_folder_save)

    # Get system language
    local = locale.getlocale()
    local_language = local[0]

    # Get column and line length of the terminal
    term_column_length = get_column_length(local_language)
    term_line_length = get_line_length(local_language)
    # Set the column and line length to default values if they are None
    if term_column_length is None:
        term_column_length = 120
    else:
        term_column_length = int(term_column_length)
    if term_line_length is None:
        term_line_length = 30
    else:
        term_line_length = int(term_line_length)

    # Create the default prompt from the default.json file
    system_message = GamePrompt(FileControl.load_prompt(files, "default"))
    print("Loaded default Prompt\n")

    # Create the main menu bar options
    main_menu_bar_options = ["╣ 1. Add a line ╠", "╣ 2. Remove lines ╠", "╣ 3. Edit a line ╠", "╣ 4. Print the prompt ╠",
                             "╣ 5. Load a prompt from a file ╠", "╣ 6. Save the prompt to a file ╠", "╣ 7. Continue ╠"]

    # Create the main menu bar if the terminal is wide enough otherwise ask the user if he wants to continue
    try:
        main_menu_bar = mbar_construct(term_column_length, main_menu_bar_options, override_len=2, fill="═")
    except TerminalLengthException:
        print(BColors.WARNING + "Warning: Your Terminal is not wide enough!\n"
                                "         Do You want to Continue anways or restart the Programm\n"
                                "         with an adjusted window size or font size?\n"
                                "         Y/N  Y for Continue / N for Restart" + BColors.ENDC)
        user_input = input("Your choice: ")
        if user_input in ["Y", "y", "J", "j"]:
            main_menu_bar = mbar_construct(term_column_length, main_menu_bar_options, override_len=2, fill="═",
                                           ignore_error=True)
        else:
            exit(1)

    # Prompt editing menu
    try:  # Ends the loop if the user chooses to continue
        clear_terminal()
        while True:  # Loop for the prompt editing menu
            print("\n" + main_menu_bar)
            user_input = input("Your choice: ")

            while True:  # Breaks the loop if the user input is valid and executed flawlessly
                match user_input:  # Menu options
                    case "1":  # Add a line of text to the prompt
                        clear_terminal()
                        system_message.add_from_string(input("\nEnter the line content you want to add: "))
                        print("\nAdded Line\n", system_message.line_string())
                        break

                    case "2":  # Remove lines from the prompt
                        clear_terminal()
                        lines_remove_usr = input("\nEnter the lines you want to remove: \n"
                                                 "You can enter lines like this: 0, 1, 2 \n")
                        try:
                            lines_to_remove = eval(f"[{lines_remove_usr}]")
                            system_message.remove_lines(lines_to_remove)
                            print("\nRemoved Lines\n", system_message.line_string())
                            break
                        except SyntaxError:
                            print("Invalid input.")
                            continue

                    case "3":  # Edit a line in the prompt
                        clear_terminal()
                        lnum_usr = input("\nEnter the line number you want to edit: ")
                        try:
                            lnum = int(lnum_usr)
                            system_message.edit_line(lnum, input("Enter the new line: "))
                            print("\nEdited Line\n", system_message.line_string())
                            break
                        except ValueError:
                            print("Invalid input.")
                            continue
                        except IndexError:
                            print("Line number out of range.")
                            continue

                    case "4":  # Print the prompt
                        clear_terminal()
                        print("\n", system_message.line_string())
                        break

                    case "5":  # Load a prompt from a file
                        clear_terminal()
                        try:
                            system_message.set_from_string(files.load_prompt(input("\nEnter the filename: ")))
                            print("\nLoaded Prompt\n", system_message.line_string())
                            break
                        except FileNotFoundError:
                            print("File not found.")
                            continue
                        except json.decoder.JSONDecodeError:
                            print("Invalid file.")
                            continue

                    case "6":  # Save the prompt to a file
                        clear_terminal()
                        try:
                            files.save_prompt(system_message, input("\nEnter the filename: "))
                            print("\nSaved Prompt\n", system_message.line_string())
                            break
                        except FileNotFoundError:
                            print("File not found.")
                            continue
                        except json.decoder.JSONDecodeError:
                            print("Invalid file.")
                            continue

                    case "7":  # Continue
                        raise Continue

                    case _:  # Invalid input
                        clear_terminal()
                        print("Invalid input.")
                        break

    except Continue:
        clear_terminal()
        print("\nContinuing...\n")
        pass

    # Loading a save from a file
    print("\nDo you want to load a Save from a file? Y/N")
    user_input = input("Your choice: ")
    history = None
    conversation: list[dict] = []
    while True:
        match user_input:
            case "Y" | "y" | "J" | "j":
                user_load_input = input("\nEnter the filename without the _hist/_conv.json: ")
                try:
                    conversation, history = files.load_state(user_load_input)
                    break
                except FileNotFoundError:
                    print("File not found.")
                    continue
            case "N" | "n":
                break
            case _:
                print("Invalid input.")

    # Set up Border objects and variables
    border: Border = Border(["╔", "╗"], ["╚", "╝"], "║", "═", term_column_length)
    enter_action = "Enter in your Action: "
    # Upper border for User actions in game
    text_you = BColors.HEADER + BColors.BOLD + ' Your Action ' + BColors.ENDC
    text_you = border.en_c_up(text_you, add_len=13)
    # Upper border for AI actions in game
    text_answer = BColors.HEADER + BColors.BOLD + ' Game ' + BColors.ENDC
    text_answer = border.en_c_up(text_answer, add_len=13)
    # Vertical border for empty lines
    empty_vert = border.en_vert(" ")

    # Set up GamePrompt objects and variables for easy conversion
    action_display_class: GamePrompt = GamePrompt()
    action_display: str = ""
    game_display_class: GamePrompt = GamePrompt()
    game_display: str = ""

    # Create the conversation log variables
    conv_log: list[str] = []

    # Print the history if there is any loaded in
    if history is not None:
        for hist_message in history:
            print(hist_message)

    # Conversation loop
    while True:

        # User Action
        if len(conversation) > 0:  # If the Ai has already replied once
            user_input = input(enter_action)
            # Exit the conversation loop if the user enters [EXIT]
            if user_input == "[EXIT]":
                break
            # Calculate the number of line the user entered and delete those lines
            del_last_line(loops=get_line_space(user_input + enter_action, term_column_length))

            # Set the user input as the action display
            action_display_class.set_from_string(user_input)
            # Wrap the action display in vertical borders
            action_display = border.en_wrap(action_display_class.list_string_break
                                            (term_column_length, False), add_len={0: 0})

            # Print the incapsulated action display
            print((conv_log_append := f"{text_you}\n{empty_vert}\n{action_display}\n{empty_vert}\n{border.en_c_down('')}"))

            # Add the user input to the conversation log
            conv_log.append(conv_log_append)
            # Add the user input to the conversation with the API
            conversation.append({"role": "user", "content": user_input})

        # AI Action
        # Create the messages with the Prompt as a basis and the conversation as the messages
        messages = [{"role": "system", "content": str(system_message)}] + conversation
        # Get the response from the API
        response = communicate_with_ai(messages, model_name="gpt-3.5-turbo")

        # If the API answered with a response
        if ai_reply := response["choices"][0]["message"]["content"]:
            # Set the response as the game display
            game_display_class.set_from_string(ai_reply)
            # Wrap the game display in vertical borders
            game_display = border.en_wrap(game_display_class.list_string_break
                                          (term_column_length, False), add_len={0: 0})

            # Print the incapsulated game display
            print((conv_log_append := f"{text_answer}\n{empty_vert}\n{game_display}\n{empty_vert}\n{border.en_c_down('')}"))

            # Add the response to the conversation log
            conv_log.append(conv_log_append)
            # Add the response to the conversation with the API
            conversation.append({"role": "assistant", "content": ai_reply})

        # If the API didn't answer with a response
        else:
            print(BColors.FAIL + BColors.BOLD + "Failed to get a response from the ChatGPT API." + BColors.ENDC)

    # Exit menu bar
    clear_terminal()

    # Create the exit menu bar options
    exit_menu_bar_options = ["╣ 1. Exit ╠", "╣ 2. Save ╠"]
    # Create the exit menu bar
    exit_menu_bar = mbar_construct(term_column_length, exit_menu_bar_options, override_len=2,
                                   fill="═", ignore_error=True)
    # Print the exit menu bar
    print(exit_menu_bar)

    # Exit menu loop
    while True:
        match input("Your choice: "):
            case "1":  # Exit
                exit(0)

            case "2":  # Save
                print("Please enter the filename you want to save to.")
                while True:
                    user_input = input("Your choice: ")

                    try:
                        # Save the conversation and history to json files
                        files.save_state(conversation, conv_log, user_input)

                        # Clear the screen and print the exit menu bar with a success message
                        clear_terminal()
                        print(exit_menu_bar)
                        print(f"Saved to {user_input}_hist.json and {user_input}_conv.json.")
                        break

                    except FileExistsError:
                        print("File already exists.")
                        continue
                    except json.decoder.JSONDecodeError:  # Invalid file contents
                        print("Invalid file.")
                        continue

            case _:  # Invalid input
                print("Invalid input.")
                continue
