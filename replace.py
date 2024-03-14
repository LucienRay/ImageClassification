import os
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
PROJECT_DIR=os.path.dirname(os.path.abspath(__file__))

try:
    f=open(PROJECT_DIR+'\\setting.txt','r')
    setting=f.readlines()
    interval=setting[4].split('=')[1].strip("\"\n")
    f.close()
except ValueError:
    logging.error("The setting.txt has not been set yet.")
    sys.exit()

try:
    if len(sys.argv)<3:
        logging.error("need at least two argument")
    else:
        f = open(os.path.join(PROJECT_DIR, 'result.txt'), 'r+')
        lines=f.readlines()
        for i in sys.argv[1:-1]:
            lines=[sys.argv[-1].join(line.split(i)) for line in lines]
        f.close()
        os.remove(PROJECT_DIR + '\\result.txt')
        f = open(PROJECT_DIR + '\\result.txt', 'w')
        f.writelines(lines)
        f.close()

except FileNotFoundError:
    logging.error("result.txt not find")
    sys.exit()
