import json
import os
from prompt import GamePrompt
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