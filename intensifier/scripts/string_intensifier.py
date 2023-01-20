import sys
from string import ascii_lowercase, digits

string = sys.argv[1]

new_word = ''
for letter in string:
    letter_lowered = letter.lower()
    if letter_lowered in ascii_lowercase or letter in  digits:
        new_word += f':{letter_lowered}-intensifies:'
    elif letter == ' ':
        new_word += f'   '
    else:
        new_word += f'{letter}'
print(new_word)