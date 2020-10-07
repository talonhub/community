import time

from talon import clip, Module, Context, actions

mod = Module()


@mod.action_class
class Actions:
    def word_neck(index: int):
        """select the following word or the index'th word"""
        word_neck(int(index))

    def word_prev(index: int):
        """select the previous word or the index'th word"""
        word_prev(int(index))

    def small_word_neck(index: int):
        """select the following word or the index'th word"""
        small_word_neck(int(index))

    def small_word_prev(index: int):
        """select the previous word or the index'th word"""
        small_word_prev(int(index))

    def big_word_neck(index: int):
        """select the following word or the index'th word"""
        big_word_neck(int(index))

    def big_word_prev(index: int):
        """select the previous word or the index'th word"""
        big_word_prev(int(index))


alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789_"


def small_word_neck(index):
    return word_neck(index, valid_characters=set(alphanumeric) - set("_"))


def small_word_prev(index):
    return word_prev(index, valid_characters=set(alphanumeric) - set("_"))


def big_word_neck(index):
    return word_neck(index, valid_characters=set(alphanumeric) | set("/\\-_.>=<"))


def big_word_prev(index):
    return word_prev(index, valid_characters=set(alphanumeric) | set("/\\-_.>=<"))


def stop_selection(cursor_position):
    assert cursor_position in ("left", "right")

    with clip.capture() as s:
        actions.edit.extend_right()
        time.sleep(0.25)
        actions.edit.copy()
    current_highlight = s.get()
    actions.edit.extend_left()

    if len(current_highlight) > 1:
        if cursor_position == "left":
            actions.edit.left()
        elif cursor_position == "right":
            actions.edit.right()


def word_neck(word_index, valid_characters=alphanumeric):
    with clip.revert():
        stop_selection("right")

        actions.edit.extend_line_end()
        time.sleep(0.25)
        actions.edit.copy()
        actions.edit.left()
        time.sleep(0.25)
        text_right = clip.get().lower()

    print(text_right)
    print(word_index, type(word_index))

    is_word = [character in valid_characters for character in text_right]
    word_count = 1
    i = 0
    while i < (len(is_word) - 1) and not is_word[i]:
        i += 1

    # print("a start", i)

    while i < (len(is_word) - 1) and word_count < word_index:
        # print(i, is_word[i], word_count, word_index)
        if not is_word[i] and is_word[i + 1]:
            word_count += 1
        i += 1
    # warning: this is a hack, sorry
    # print("i", i)
    if i == 1 and is_word[0]:
        i = 0
    start_position = i
    # print(text_right[start_position:])
    while i < len(is_word) and is_word[i]:
        i += 1
    end_position = i

    # print(start_position, end_position)
    # cursor over to the found word
    for i in range(0, start_position):
        actions.edit.right()
    # now select the word
    for i in range(0, end_position - start_position):
        actions.edit.extend_right()


def word_prev(word_index, valid_characters=alphanumeric):
    with clip.revert():
        stop_selection("left")

        actions.edit.extend_line_start()
        time.sleep(0.25)
        actions.edit.copy()
        actions.edit.right()
        time.sleep(0.25)
        text_right = clip.get().lower()

    text_right = list(reversed(text_right))

    is_word = [character in valid_characters for character in text_right]
    word_count = 1
    i = 0
    while i < (len(is_word) - 1) and not is_word[i]:
        i += 1

    while i < (len(is_word) - 1) and word_count < word_index:
        # print(i, is_word[i], word_count, word_index)
        if not is_word[i] and is_word[i + 1]:
            word_count += 1
        i += 1
    start_position = i
    # print(text_right[start_position:])
    while i < len(is_word) and is_word[i]:
        i += 1
    end_position = i

    # print(start_position, end_position, text_right[start_position:end_position])
    # cursor over to the found word
    for i in range(0, start_position):
        actions.edit.left()
    # now select the word
    for i in range(0, end_position - start_position):
        actions.edit.extend_left()
