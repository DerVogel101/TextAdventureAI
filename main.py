# Author: DerVogel101
# Version: 1.1.0
# Last Modified: 31.08.2023
# Description: A simple text adventure game with an AI as the game master.
# GitHub: https://github.com/DerVogel101/TextAdventureAI

import sys
sys.path.insert(1, './lib')

import openai
import os
import json
import locale
from dotenv import load_dotenv
from filecontrol import FileControl
from prompt import GamePrompt
from mbar import mbar_construct
from game_excaptions import TerminalLengthException, Continue
from border import Border
from terminal_len import get_column_length, get_line_length
from line_del import del_last_line, clear_terminal
from BColors import BColors


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
