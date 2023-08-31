from game_excaptions import TerminalLengthException


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
