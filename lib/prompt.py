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