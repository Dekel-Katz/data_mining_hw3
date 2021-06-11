import matplotlib.pyplot as plt
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

SIGNS = ['.', ',', ':', ';', '!', '?', '*', '#', '@', '&', '(', ')',
         '[', ']', '{', '}', '"']
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
                line = line.lower().replace(sign, '').replace('\n', '')\
                    .replace('  ', ' ').replace('--', ' ').strip()
            if line == '':
                continue
            words = words + line.split(' ')
    return words


def create_token_dict(words_list):
    tokens_dict = {}
    for word in words_list:
        if word in tokens_dict:
            tokens_dict[word] += 1
        else:
            tokens_dict[word] = 1
    sorted_token_dict = dict(sorted(tokens_dict.items(), key=lambda kv: kv[1],
                                    reverse=True))
    return sorted_token_dict


def remove_stopwords(words_list):
    stop_words = stopwords.words('english')
    words_without_stops = []
    for word in words_list:
        word_parts = word.split("'")
        for part in word_parts:
            if part == '':
                continue
            elif part not in stop_words:
                words_without_stops.append(part)
    return words_without_stops


def book_stemming(words_list):
    porter = PorterStemmer()
    for i in range(len(words_list)):
        words_list[i] = porter.stem(words_list[i])
    return words_list


def visualize_doc_ranks(tokens_dict, all_words_count):
    tokens = [key for key in tokens_dict.keys()]
    ranks = list(range(1, len(tokens_dict)+1))
    frequencies = [math.log(value / all_words_count, 2) for value in
                   tokens_dict.values()]
    plt.title("words ranks and frequencies in 'around the wold in 80 days'")
    plt.plot(ranks, frequencies)
    plt.xlabel('Ranks')
    plt.ylabel('Frequencies')
    plt.show()


def extract_adj_plus_noun(words):
    adjective = ['JJ', 'JJS', 'JJR']
    noun = ['NN', 'NNS', 'NNP', 'NNPS']
    word_types = nltk.pos_tag(words)
    phrase_list = []
    for index in range(len(word_types)):
        if word_types[index][1] in adjective:
            if word_types[index+1][1] in noun:
                phrase = word_types[index][0] + ' ' + word_types[index+1][0]
                adj_index = index - 1
                adj_list = []
                while True:
                    if word_types[adj_index][1] in adjective:
                        adj_list.append(word_types[adj_index][0])
                        adj_index -= 1
                        if adj_index < 0:
                            break
                    else:
                        break
                for adj in adj_list[0::-1]:
                    phrase = adj + ' ' + phrase
                noun_list = []
                noun_index = index + 1
                while True:
                    if word_types[noun_index][1] in noun:
                        noun_list.append(word_types[noun_index][0])
                        noun_index += 1
                        if noun_index == len(word_types):
                            break
                    else:
                        break
                for no in noun_list[1:]:
                    phrase = phrase + ' ' + no
                phrase_list.append(phrase)
    return phrase_list


def recurse_pos_adj_and_noun(words, phrase_lst, phrase):
    adjective = ['JJ', 'JJS', 'JJR']
    noun = ['NN', 'NNS', 'NNP', 'NNPS']
    word_types = nltk.pos_tag(words)
    phrase = []
    while len(words) > 0:
        if word_types[0][1] not in adjective and word_types[0][1] not in noun:
            if len(phrase) > 2:
                phrase = ' '.join(phrase)
                print(phrase)
                phrase_lst.append(phrase)
            phrase_lst = recurse_pos_adj_and_noun(words[1:], phrase_lst, [])
        if word_types[0][1] in adjective:
            phrase.append(word_types[0][0])
            phrase_lst = recurse_pos_adj_and_noun(words[1:], phrase_lst, phrase)
        if word_types[0][1] in noun:
            phrase.append(word_types[0][0])
    return phrase_lst


if __name__ == '__main__':
    text_file = 'around_the_world_in_eighty_days.txt'
    words = read_wordlist_file(text_file)
    print(extract_adj_plus_noun(words))
    # print(len(create_token_dict(words)))
    no_stops_list = remove_stopwords(words)
    stemm_list = book_stemming(no_stops_list)
    stemmed_d = create_token_dict(stemm_list)
    visualize_doc_ranks(stemmed_d, len(stemm_list))
    # d = create_token_dict(words)
    # d_no_stops = create_token_dict(no_stops_list)
    # visualize_doc_ranks(d, len(words))
    # visualize_doc_ranks(d_no_stops, len(no_stops_list))


