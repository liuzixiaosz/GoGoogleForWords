#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

import sys
from go_google import sort_by_imp, googleit, write_web


def treat_turplist(lst):
    lst = lst[2: -2]
    new_str = lst.replace('), (', ', ').split(', ')
    new_list = []
    tmp = ''
    for i in range(0, len(new_str)):
        if i % 2 == 0:
            tmp = new_str[i][1: -1]
        else:
            new_list.append((tmp, int(new_str[i])))
    return new_list


def treat_graph(lsts_str):
    lsts_str = lsts_str[2: -2].replace('], [', ', EOL, ') + ', EOL'
    new_graph = []
    new_line = []
    lst = lsts_str.split(', ')
    for ele in lst:
        if ele == 'True':
            new_line.append(True)
        elif ele == 'False':
            new_line.append(False)
        elif ele == 'EOL':
            new_graph.append(new_line)
            new_line = []
    return new_graph


def main(argv):
    fr1 = open('words_index.txt')
    fr2 = open('graph.txt')
    a1 = fr1.readlines()[0]
    a2 = fr2.readlines()[0]
    wds_idx_tup_list = treat_turplist(a1)
    grouped_wds_graph = treat_graph(a2)
    sorted_tup_list, freq_dict = sort_by_imp(grouped_wds_graph, wds_idx_tup_list)
    print('parse finished.')
    url_words_dict = googleit(wds_idx_tup_list, sorted_tup_list, grouped_wds_graph)
    write_web(url_words_dict)


if __name__ == '__main__':
    main(sys.argv)
