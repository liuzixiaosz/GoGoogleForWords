#!/usr/bin/env python3
# -*- Coding: utf-8 -*-


import sys, os
import time

import bs4, requests
import random
import googlesearch


def preset(words):
    new_set = set()
    while words:
        line = words.pop()
        wd_in_line = line.strip().split(',')
        for wd in wd_in_line:
            new_set.add(wd.strip())
    print('words count: ', len(new_set))
    return new_set


def read_input(argv):
    if len(argv) == 1:
        print('input all words to match, ctrl-D to continue')
        return sys.stdin.readlines()
    elif len(argv) > 1:
        words_path = argv[1]
        print('reading %s ...' % words_path)
        fr = open(words_path, 'r')
        fr.seek(0)
        raw_words = fr.readlines()
        fr.close()
        return raw_words


def create_list_bin_graph(length):
    g = []
    for i in range(0, length):
        g.append([False] * length)
    return g


def group_by_synonyms(words):
    length = len(words)
    my_graph = create_list_bin_graph(length)
    words_list = list(words)

    for idx in range(0, length):
        wd = words_list[idx]
        try:
            synonyms = search_synonyms(wd)
            for syn in synonyms:
                if syn in words:
                    nxt_idx = words_list.index(syn)
                    my_graph[nxt_idx][idx] = True
                    my_graph[idx][nxt_idx] = True
        except Exception:
            sys.stderr.write(str(Exception) + 'Problems occur when searching for ' + wd)
            time.sleep(3)
            try:
                synonyms = search_synonyms(wd)
                for syn in synonyms:
                    if syn in words:
                        nxt_idx = words_list.index(syn)
                        my_graph[nxt_idx][idx] = True
                        my_graph[idx][nxt_idx] = True
            except Exception:
                pass

    for idx in range(0, length):
        wd = words_list[idx]
        words_list[idx] = (wd, idx)

    return words_list, my_graph


def search_synonyms(word):
    print('searching synonyms of: ' + word)
    syn_search_url = 'https://www.dictionary.com/browse/' + word
    css_class = 'css-1an5ojz e15p0a5t0'

    def grab_syn(sp):
        syn = set()
        try:
            syn_words = sp.find(class_=css_class).contents[1:]
            for ele in syn_words:
                if type(ele) is not bs4.NavigableString:
                    wd = str(ele.text).strip()
                    syn.add(wd)
                    sys.stdout.write(wd + ' ')
            print()
        except AttributeError:
            sys.stderr.write('error occurs for this word')
            time.sleep(5)
            try:
                syn_words = sp.find(class_=css_class).contents[1:]
                for ele in syn_words:
                    if type(ele) is not bs4.NavigableString:
                        wd = str(ele.text).strip()
                        syn.add(wd)
                        sys.stdout.write(wd + ' ')
                print()
            except Exception:
                pass
        return syn

    r = requests.get(url=syn_search_url)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    if soup:
        return grab_syn(soup)
    else:
        print('error occurs, retrying...')
        time.sleep(5)
        return search_synonyms(word)


def googleit(tup_list, sorted_tup_list, graph):
    length = len(tup_list)
    wd_list = [tup[0] for tup in tup_list]
    web_dict = {}

    def treat_search(wd2search, stop):
        phrase = str(wd2search)[1: -1].replace(',', '')
        score = 0
        inc = []
        u = ''
        for this_url in googlesearch.search(phrase, stop=stop):
            try:
                r = requests.get(url=this_url)
            except Exception:
                time.sleep(3)
                try:
                    r = requests.get(url=this_url)
                except Exception:
                    # sys.stderr.write('error with %s \n' % this_url)
                    continue
            this_score = 0
            soup = bs4.BeautifulSoup(r.text, "lxml")
            this_inc = []
            txt = str(soup.text).lower()
            for wd in wd2search:
                if wd in txt:
                    this_score += 1
                this_inc.append(wd)
                if this_score > score:
                    score = this_score
                    inc = this_inc
                    u = this_url
        return inc, u

    for tup in sorted_tup_list:
        to_search = [tup[0]]
        this_idx = tup[1]
        for j in range(0, length):
            if graph[this_idx][j]:
                to_search.append(tup_list[j][0])
        included, url = treat_search(to_search, 3)
        for inc_wd in included:
            wd_list.remove(inc_wd)
        web_dict[url] = included
        print(url + ': ' + str(included))

    while wd_list:
        to_search = []
        for w in wd_list:
            to_search.append(w)
            if len(to_search) > 2:
                included, url = treat_search(to_search, 3)
                for inc_wd in included:
                    wd_list.remove(inc_wd)
                web_dict[url] = included
                print(url + ' :' + str(included))
                to_search = []
        if to_search:
            treat_search(to_search, 3)
            for inc_wd in included:
                wd_list.remove(inc_wd)
            web_dict[url] = included
            print(url + ': ' + str(included))

    return web_dict


def write_web(url_words_dict):
    filename = 'articles.txt'
    print('writing webinfo ...')
    fw = open(filename, 'w')
    for i in range(1, len(url_words_dict)):
        itm = str(url_words_dict.popitem())[1: -1]
        fw.write(itm + '\n')
        fw.flush()
    fw.seek(0)
    fw.close()


def write_syn(tup_list, syn_graph):
    print('writing synonyms_info ...')
    length = len(tup_list)
    wd_list = [tup[0] for tup in tup_list]
    fw1 = open('synonyms_all.md', 'w')
    fw2 = open('synonyms_group.txt', 'w')
    for i in range(0, length):
        this_word = tup_list[i][0]
        group1 = []
        group2 = []
        if this_word in wd_list:
            wd_list.remove(this_word)
            group2.append(this_word)
        for j in range(0, length):
            if syn_graph[i][j]:
                group1.append(tup_list[j][0])
                if tup_list[j][0] in wd_list:
                    group2.append(tup_list[j][0])

        fw1.write('## %s\n ' % this_word)
        fw1.writelines('![%s](#%s) ' % (line, line) for line in group1)
        fw1.write('\n\n')
        fw2.writelines(line + ', ' for line in group2)
        fw2.write('\n\n')
        fw1.flush()
        fw2.flush()
    fw1.close()
    fw2.close()


def sort_by_imp(graph, words_idx_tup_list):
    imp_dict = {}
    length = len(words_idx_tup_list)
    for i in range(0, length):
        imp_dict[words_idx_tup_list[i][0]] = sum(graph[i])
    sorted_words_list = sorted(words_idx_tup_list, key=lambda x: imp_dict.get(x[0]))
    return sorted_words_list, imp_dict


def main(argv):
    print('Started.')
    raw_words = read_input(argv)
    words_set = preset(set(raw_words))
    wds_idx_tup_list, grouped_wds_graph = group_by_synonyms(words_set)
    write_syn(wds_idx_tup_list, grouped_wds_graph)
    sorted_tup_list, freq_dict = sort_by_imp(grouped_wds_graph, wds_idx_tup_list)
    url_words_dict = googleit(wds_idx_tup_list, sorted_tup_list, grouped_wds_graph)
    write_web(url_words_dict)
    print('Ended.')


if __name__ == '__main__':
    main(sys.argv)
