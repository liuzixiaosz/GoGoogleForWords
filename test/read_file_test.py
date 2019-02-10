from go_google_from_file import treat_graph
from go_google_from_file import treat_turplist


def main():
    fr1 = open('test_words_index.txt', 'w')
    fr2 = open('test_graph.txt', 'w')
    test1 = [('hello', 1), ('world', 2), ('good', 3)]
    test2 = [[True, True, False], [True, False, False], [False, False, True]]
    fr1.writelines(str(test1))
    fr2.writelines(str(test2))
    fr1.close(); fr2.close()
    fr1 = open('test_words_index.txt', 'r')
    fr2 = open('test_graph.txt', 'r')
    a1 = fr1.readlines()[0]
    a2 = fr2.readlines()[0]
    wds_idx_tup_list = treat_turplist(a1)
    grouped_wds_graph = treat_graph(a2)
    print(str(wds_idx_tup_list))
    print(str(grouped_wds_graph))


if __name__ == '__main__':
    main()
