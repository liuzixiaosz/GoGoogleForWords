#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

import sys, os
import bs4, requests


def preset(words):
    line = words.pop()
    wd_in_line = line.strip().split(',')
    for wd in wd_in_line:
        words.add(wd.strip())
    return words


def read_input(argv):
    if len(argv) == 1:
        print('input all words to match, ctrl-D to continue')
        return sys.stdin.readlines()
    elif len(argv) > 1:
        words_path = argv[1]
        print('reading %s' % words_path)
        fr = open(words_path, 'r')
        fr.seek(0)
        raw_words = fr.readlines()
        fr.close()
        return raw_words


def group_by_synonyms(words):
    new_graph = [[0] * len(words)] * len(words)
    wd = words.pop()
    synonyms = search_synonyms(wd)

    return new_graph


def search_synonyms(word):
    css1st = 'css-3kshty etbu2a31'
    css2nd = 'css-1ruewre etbu2a31'
    css3rd = 'css-1gk8jl3 etbu2a31'
    syn = {}
    syn_search_url = 'https://www.thesaurus.com/browse/%s?s=t' % word
    r = requests.get(url=syn_search_url)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    s = soup.find(class_='css-1lc0dpe et6tpn80')
    len_syn = len(s.contents)
    for wd_li in s.contents:
        if True: #TODO:
            pass
    # syn{1}



def google_it(words_graph):
    return {'1', 'helloworld'}


def write_file(url_words_dict):
    new_name = 'articles.txt'
    fw = open(new_name, 'w')
    for i in range(1, len(url_words_dict)):
        itm = url_words_dict.popitem()[1: -1]
        fw.write(itm + '\n')
    fw.seek(0)
    fw.close()


def main(argv):
    print('Started.')
    raw_words = read_input(argv)
    words = preset(set(raw_words))

    # format: weighted graph, words to words similarity
    grouped_wds_graph = group_by_synonyms(words)
    url_words_dict = google_it(grouped_wds_graph)
    write_file(url_words_dict)
    print('Ended.')


if __name__ == '__main__':
    main(sys.argv)
