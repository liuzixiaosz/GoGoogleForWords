import sys, os
import go_google
import time
import threading

MAX_SIZE = 12

def concatfile(files):
    pass

def splitfile(filename, num):
    fr = open(filename, 'r')
    ctnt = fr.readlines()
    fr.close()
    length = len(ctnt)
    seg = int(length / num)
    names = []
    for i in range(0, num - 1):
        new_name = str(time.time())
        names.append(new_name)
        f = open('%s' % new_name, 'w')
        f.writelines(ctnt[i * seg: (i + 1) * seg])
    new_name = str(time.time())
    names.append(new_name)
    f = open('%s' % new_name, 'w')
    f.writelines(ctnt[(num - 1) * seg: length])
    return names


def main(argv):
    if len(argv) < 2:
        sys.stderr.write('must be more than 1 parameter\n')
    if len(argv) == 3:
        seperation_num = min(MAX_SIZE, int(argv[2]))
    else:
        seperation_num = 1
    new_files = splitfile(argv[1], seperation_num)
    new_argvs = []
    for n in new_files:
        new_argvs.append(['go_google.py', n])
    # pool = multiprocessing.Pool(seperation_num)
    #
    # pool.map(go_google.main, new_argvs)
    for i in range(0, seperation_num):
        t = threading.Thread(target=go_google.main, args=(new_argvs[i],))
        t.start()
    concatfile(new_files)
    for n in new_files:
        os.remove(n)


if __name__ == '__main__':
    main(sys.argv)
