def break_word(stuff):
    """This function will break up words for us."""
    words = stuff.split(' ')
    return words


def sort_word(stuff):
    """Sorts the words."""
    return sorted(stuff)

words = break_word("This function will break up words for us.")
print(words)


print(sort_word("This function will break up words for us"))