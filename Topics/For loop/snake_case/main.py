lower_camel_case_word = input()

snake_case_word = ""
is_first_letter = True
for letter in lower_camel_case_word:
    lower_letter = letter.lower()
    if is_first_letter or lower_letter == letter:
        snake_case_word += lower_letter
        is_first_letter = False
    else:
        snake_case_word += "_" + lower_letter

print(snake_case_word)
