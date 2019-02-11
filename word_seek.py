import sys, os


def preset(words):
    new_set = set()
    while words:
        line = words.pop()
        wd_in_line = line.strip().split(',')
        for wd in wd_in_line:
            new_set.add(wd.strip())
    print('words count: ', len(new_set))
    return new_set


def main(argv):
    if len(argv) > 2:
        in_main = argv[1]
        in_cnt = argv[2]
        out_ = 'cnt.md'
        print('reading ..')
        f_in_main = open(in_main, 'r')
        f_in_main.seek(0)
        main_ctnt = f_in_main.readlines()
        words = preset(main_ctnt)
        f_in_cnt = open(in_cnt, 'r')
        f_in_cnt.seek(0)
        url = f_in_cnt.readline().strip()
        cnt_ctnt = f_in_cnt.read()
        print('read')
        if out_ not in os.listdir('.'):
            open('cnt.md', 'a').close()
        inside = []
        print('counting ..')
        c = 1
        for wd in words:
            print('checking: %d/%d' % (c, len(words)))
            c += 1
            if wd in cnt_ctnt:
                inside.append(wd)
        f_out = open('cnt.md', 'a')
        f_out.write('[link](' + url + ')\n' + str(inside)[1: -1].replace(',', '').replace('\'', '') + '\n\n')
        f_out.close()
        print('finished, begin to check')
        checkin(words)


def checkin(words):
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


if __name__ == '__main__':
    main(sys.argv)
