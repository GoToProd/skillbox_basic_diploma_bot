import re


def is_russian_word(word):
    return bool(re.fullmatch(r"[а-яА-ЯёЁ]+", word))
