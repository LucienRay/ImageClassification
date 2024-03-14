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
    if len(sys.argv)!=3:
        logging.error("need two argument")
    else:
        f = open(os.path.join(PROJECT_DIR, 'result.txt'), 'r+')
        lines=[sys.argv[2].join(i.split(sys.argv[1])) for i in f.readlines()]
        f.seek(0)
        f.writelines(lines)
        f.close()
        os.remove(PROJECT_DIR + '\\result.txt')
        f = open(PROJECT_DIR + '\\result.txt', 'w')
        f.writelines(lines)
        f.close()

except FileNotFoundError:
    logging.error("result.txt not find")
    sys.exit()
