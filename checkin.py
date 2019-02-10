import sys
from word_seek import preset

if __name__ == '__main__':
    f_wds = open(sys.argv[1]); f_wds.seek(0)
    words = preset(f_wds.readlines())
    list_words = list(words)
    f = open('cnt.md', 'r')
    f.seek(0)
    lines = f.readlines()
    for line in lines:
        if 'http' in line:
            continue
        elif line == '\n':
            continue
        else:
            check_wds = line.strip().split(' ')
            for w in check_wds:
                if w in list_words:
                    list_words.remove(w)
    print('remain: %d' % len(list_words))
    print(str(list_words))
