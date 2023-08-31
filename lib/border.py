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