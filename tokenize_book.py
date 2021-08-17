# IMPORTANT!!! run these 2 for the first time to download!
# nltk.download('stopwords')
# Terminal: python -m spacy download en_core_web_sm

import matplotlib.pyplot as plt
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy
import re

SIGNS = ['.', ',', ':', ';', '!', '?', '*', '#', '@', '&', '(', ')',
         '[', ']', '{', '}', '"']
BOOK_START = '*** START OF THIS PROJECT GUTENBERG EBOOK'
BOOK_END = 'End of Project Gutenberg'


def clean_gutenberg_book(filename):  # e, f, g
    """
    A function that reads the whole Project Gutenberg book. It cuts off the
    text that is not part of the book it self, and combines the book lines into
     one string, without any line breaks.
    :param filename: A string referring to a text file.
    :return: A string representing the full book, without Project Gutenberg
    formats.
    """
    text = ""
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
            if line == '':
                continue
            text = text + line.replace("\n", " ")
    return text


def read_wordlist_file(filename):  # b, c, d
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
                line = line.lower().replace(sign, '').replace('\n', '') \
                    .replace('  ', ' ').replace('--', ' ').strip()
            if line == '':
                continue
            words = words + line.split(' ')
    return words


def remove_stopwords(words_list):  # c, d
    """
    A function that removes stop words from a list of words.
    :param words_list: a list of strings, representing words.
    :return: a list of strings, without the strings that represent stop words.
    """
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


def book_stemming(words_list):  # d
    """
    A function that takes a list of words, and turns them into their stems
    using an nltk porter stemmer.
    :param words_list: a list of strings, representing words.
    :return: a list of strings, that represent the stems for the words in the
    original list.
    """
    porter = PorterStemmer()
    for i in range(len(words_list)):
        words_list[i] = porter.stem(words_list[i])
    return words_list


def spacy_recursion(words, ind, phrase):  # e
    """
    A function that creates a list of words that together, represent an adj +
    noun phrase, and the index of the last word in the overall list of words.
    :param words: A list of strings, each represents one word.
    :param ind: The index of the last string in the phrase, of the overall list
     of words.
    :param phrase: A list of strings, each represents one word in a phrase.
    :return: A list of words that together, represent an adj +
    noun phrase, and the index of the last word in the overall list of words.
    """
    if words[ind].pos_ != "NOUN" and words[ind].pos_ != "ADJ":
        return phrase, ind
    # case 2 - yes adj
    if words[ind].pos_ == "ADJ":
        phrase.append(words[ind].text)
        return spacy_recursion(words, ind + 1, phrase)
    # case 3 - yes noun
    if words[ind].pos_ == "NOUN":
        phrase.append(words[ind].text)
        return spacy_recursion(words, ind + 1, phrase)


def spacy_extract_adj_plus_noun(words):  # e
    """
    A function that creates a list of strings, each representing an adj + noun
    phrase.
    :param words: A string representing a text.
    :return: A list of strings.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(words)
    phrase_list = []
    inner_ind = -1
    for ind in range(len(doc)):
        if ind > inner_ind:
            if doc[ind].pos_ == "ADJ":
                phrase, inner_ind = spacy_recursion(doc, ind, [])
                if len(phrase) > 1:
                    phrase_list.append(" ".join(phrase).lower())
        else:
            continue
    return phrase_list


def create_token_dict(words_list):  # b, c, d, e
    """
    A function that counts the performances for each phrase/word (string) on a
    list, and puts them into a dictionary that shows the phrases count, from
    the most frequent to the least.
    :param words_list: A list of strings.
    :return: A dictionary of phrase, count pairs from the highest count to the
    lowest.
    """
    tokens_dict = {}
    for word in words_list:
        if word in tokens_dict:
            tokens_dict[word] += 1
        else:
            tokens_dict[word] = 1
    sorted_token_dict = dict(sorted(tokens_dict.items(), key=lambda kv: kv[1],
                                    reverse=True))
    return sorted_token_dict


def top_20_phrases(spacy_tokenized):  # e
    """
    A function that takes a sorted dict of tokens, and sums it into only 20
    most highly ranked tokens.
    :param spacy_tokenized: A dictionary of token-performances count key-value
    pairs.
    :return: A dictionary of 20 phrase-counts key-value pairs.
    """
    top_20 = {}
    counter = 0
    for key, val in spacy_tokenized.items():
        if counter == 20:
            return top_20
        top_20[key] = val
        counter += 1


def visualize_doc_ranks(tokens_dict, title):  # b, c, d, e
    """
    Initiate a plot to present tokens frequencies, on a logarithmic scale
    graph.
    :param tokens_dict: A dictionary of token-performances count key-value
    pairs.
    :param title: A string for the graph's title.
    :return: None
    """
    tokens = [key for key in tokens_dict.keys()]
    ranks = list(range(1, len(tokens_dict) + 1))
    log_ranks = [math.log(rank, 2) for rank in ranks]
    frequencies = [math.log(value, 2) for value in
                   tokens_dict.values()]
    plt.title(title)
    plt.plot(log_ranks, frequencies)
    plt.xlabel('Log Ranks')
    plt.ylabel('Log Frequencies')
    plt.show()


def top_20_ranked(tokens_dict):  # b, c, d, e
    """
    A function that creates a list of the top 20 ranked keys in a dictionary,
    by their value.
    :param tokens_dict: A dictionary of token-performances count key-value
    pairs.
    :return: A list of 20 strings.
    """
    cont = 0
    top_20 = []
    for key in tokens_dict.keys():
        if cont >= 20:
            return top_20
        top_20.append(key)
        cont += 1


def create_word_cloud_words(words):  # g
    """
    This function creates a string of pronouns from the chosen book, to use in
    the online word cloud generator.
    :param words: The original book text, as a string.
    :return: A string of pronouns.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(words)
    word_cloud_string = ""
    for word in doc:
        if word.pos_ == "PROPN" and word.text not in SIGNS:
            word_cloud_string = word_cloud_string + word.text + " "
    return word_cloud_string


def find_consecutive_words(words):  # h
    """
    A function that finds consecutive words in a book, by using regex.
    :param words: The original book text, as a string.
    :return: A list of all the consecutive words found, as strings.
    """
    consecutive_phrases = []
    consecutive_words = re.findall(r"\b([A-Za-z]+)([.!?\\-]{1,2}\s"
                                   r"?|\s)\1\b", words.lower())
    for word in consecutive_words:
        consecutive_phrases.append(word[0] + word[1] + word[0])
    return set(consecutive_phrases)


if __name__ == '__main__':
    text_file = 'around_the_world_in_eighty_days.txt'
    # b
    title_all = "Words ranks and frequencies in 'Around the World in 80 Days'"
    all_words = read_wordlist_file(text_file)
    all_words_dict = create_token_dict(all_words)
    top_20_all = top_20_ranked(all_words_dict)
    visualize_doc_ranks(all_words_dict, title_all)
    print(top_20_all)
    # c
    title_no_stops = "Words ranks and frequencies in 'Around the World in 80 " \
                     "Days'\n(without stop words) "
    words_no_stops = remove_stopwords(all_words)
    no_stops_tokens_dict = create_token_dict(words_no_stops)
    top_20_no_stops = top_20_ranked(no_stops_tokens_dict)
    visualize_doc_ranks(no_stops_tokens_dict, title_no_stops)
    print(top_20_no_stops)
    # d
    title_no_stops_stemmed = "Stems ranks and frequencies in 'Around the " \
                             "World in 80 Days'\n(without stop words) "
    no_stops_stems = book_stemming(words_no_stops)
    stems_no_stops_tokens_dict = create_token_dict(no_stops_stems)
    top_20_no_stops_stemmed = top_20_ranked(stems_no_stops_tokens_dict)
    visualize_doc_ranks(stems_no_stops_tokens_dict, title_no_stops_stemmed)
    print(top_20_no_stops_stemmed)
    # e
    title_phrases = "Adj + Noun phrases ranks and frequencies in\n'Around " \
                    "the World in 80 Days' "
    clean_text = clean_gutenberg_book(text_file)
    adj_noun_phrases_lst = spacy_extract_adj_plus_noun(clean_text)
    adj_noun_phrases_dict = create_token_dict(adj_noun_phrases_lst)
    top_20_adj_noun_phrases_dict = top_20_phrases(adj_noun_phrases_dict)
    visualize_doc_ranks(top_20_adj_noun_phrases_dict, title_phrases)
    print(list(top_20_adj_noun_phrases_dict.keys()))
    # g
    cloud_propn_lst = create_word_cloud_words(clean_text)  # The function that
    # create the pronouns string for the online word cloud generator.
    # h
    print(find_consecutive_words(clean_text))
