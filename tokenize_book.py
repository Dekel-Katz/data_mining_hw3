# IMPORTANT!!! run these 2 for the first time to download!
# nltk.download('stopwords')

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


def cut_de_bullshit(filename):
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


def visualize_doc_ranks(tokens_dict):
    tokens = [key for key in tokens_dict.keys()]
    ranks = list(range(1, len(tokens_dict)+1))
    frequencies = [math.log(value, 2) for value in
                   tokens_dict.values()]
    plt.title("words ranks and frequencies in 'around the wold in 80 days'")
    plt.plot(ranks, frequencies)
    plt.xlabel('Ranks')
    plt.ylabel('Frequencies')
    plt.show()


def spacy_extract_adj_plus_noun(words):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(words)
    phrase_list = []
    inner_ind = -1
    for ind in range(len(doc)):
        if ind > inner_ind:
            if doc[ind].pos_ == "NOUN" or doc[ind].pos_ == "ADJ":
                phrase, inner_ind = spacy_recurrsion(doc, ind, [])
                if len(phrase) > 1:
                    phrase_list.append(" ".join(phrase).lower())
        else:
            continue
    return phrase_list

def spacy_recurrsion(words, ind, phrase):
    if words[ind].pos_ != "NOUN" and words[ind].pos_ != "ADJ":
        return phrase, ind
    # case 2 - yes adj
    if words[ind].pos_ == "ADJ":
        phrase.append(words[ind].text)
        return spacy_recurrsion(words, ind + 1, phrase)
    # case 3 - yes noun
    if words[ind].pos_ == "NOUN":
        phrase.append(words[ind].text)
        return spacy_recurrsion(words, ind + 1, phrase)
    
    
def top_20_phrases(spacy_tokenized):
    top_20 = {}
    counter = 0
    for key, val in spacy_tokenized.items():
        if counter == 20:
            return top_20
        top_20[key] = val
        counter +=1

######################### G #########################
def create_word_cloud_words(words):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(words)
    word_cloud_string = ""
    for word in doc:
        if word.pos_ == "PROPN" and word.text not in SIGNS:
            word_cloud_string = word_cloud_string + word.text + " "
    return word_cloud_string
######################### G #########################

######################### H #########################
def find_consecutive_words(words):
    consecutive_phrases = []
    consecutive_words = re.findall(r"\b([A-Za-z]+)\s\1\b", words.lower())
    for word in consecutive_words:
        consecutive_phrases.append(word + " " + word)
    return consecutive_phrases
######################### H #########################


if __name__ == '__main__':
    text_file = 'around_the_world_in_eighty_days.txt'
    clean_text = cut_de_bullshit(text_file)
    words = read_wordlist_file(text_file)
    # no_stops_list = remove_stopwords(words)
    # stemm_list = book_stemming(no_stops_list)
    # stemmed_d = create_token_dict(stemm_list)
    # spacy_phrases = spacy_extract_adj_plus_noun(clean_text)
    # tokenized_spacy = create_token_dict(spacy_phrases)
    # visualize_doc_ranks(top_20_phrases(tokenized_spacy))
    # test = "google. Sweet peanut butter cookies. Peanut butter jelly " \
    #        "sandwich. John is sitting in the oval office."
    # visualize_doc_ranks(stemmed_d)
    # d = create_token_dict(words)
    # d_no_stops = create_token_dict(no_stops_list)
    # visualize_doc_ranks(d)
    # visualize_doc_ranks(d_no_stops)
    # ordered from here down:

    ######################### G #########################
    cloud_propn_lst = create_word_cloud_words(clean_text)
    ######################### H #########################
    print(find_consecutive_words(clean_text))
