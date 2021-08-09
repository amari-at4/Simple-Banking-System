word_1 = input()
word_2 = input()

# How many letters does the longest word contain?
len_word_1 = len(word_1)
len_word_2 = len(word_2)

if len_word_1 >= len_word_2:
    print(str(len_word_1))
else:
    print(str(len_word_2))
