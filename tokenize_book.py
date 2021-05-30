SIGNS = ['.', ',', ':', ';', '!', '?', '*', '#', '@', '&', '(', ')',
         '[', ']', '{', '}', '--']
BOOK_START = '*** START OF THIS PROJECT GUTENBERG EBOOK'
BOOK_END = 'End of Project Gutenberg'


def read_wordlist_file(filename):
    """
    Reads the words' list file and returns its insides as a list
    :param filename: The name of the words file
    :return: A list contains the words from the file
    """
    words = []
    with open(filename, 'r') as txt:
        cont = 0
        for line in txt.readlines():
            if cont == 0 and BOOK_START not in line:
                continue
            elif cont == 0 and BOOK_START in line:
                cont = 1
                continue
            if BOOK_END in line:
                break
            if line == '\n':
                continue
            for sign in SIGNS:
                line = line.replace(sign, '').replace('\n', '').strip()
            words = words + line.split(' ')
    return words


print(read_wordlist_file('around_the_world_in_eighty_days.txt'))