import cv2
import numpy as np
import os
import logging
from progress.bar import Bar

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
PROJECT_DIR=os.path.dirname(os.path.abspath(__file__))

try:
    f=open(PROJECT_DIR+'\\setting.txt','r')
    setting=f.readlines()
    mapName=setting[0].split('=')[1].strip()
    blockLength=int(setting[1].split('=')[1].strip())
    blockWidth=int(setting[2].split('=')[1].strip())
    threshold=int(setting[3].split('=')[1].strip())
    interval=setting[4].split('=')[1].strip("\"\n")
    f.close()
except ValueError:
    logging.error("The setting.txt has not been set yet.")
    os._exit(0)

map = cv2.imread(PROJECT_DIR+'\\'+mapName)
blocks={i:None for i in os.listdir(PROJECT_DIR+'\\blocks')}
unknownBlocks=[]
result=[[0 for i in range(map.shape[1]//blockWidth)]for i in range(map.shape[0]//blockLength)]

if map.shape[0]%blockLength!=0 or map.shape[1]%blockWidth!=0:
    logging.error("Map's size is not a multiple of block's size.")
    os._exit(0)

if len(blocks)!=0:
    with Bar(f'Loading blocks...',max=len(blocks))as bar:
        for i in blocks.keys():
            blocks[i]=cv2.imread(PROJECT_DIR+f'\\blocks\\{i}')
            bar.next()

with Bar(f'Classification blocks...',max=(map.shape[0]//blockLength)*(map.shape[1]//blockWidth)) as bar:
    def SimilarityCheck(target, Blocks):
        for i in range(len(Blocks)):
            diff = cv2.absdiff(Blocks[i], target)
            mse = np.mean(diff ** 2)
            if mse < threshold:
                return True,i
        return False,None

    for i in range(0,map.shape[0],blockLength):
        for j in range(0,map.shape[1],blockWidth):
            knownCheck = SimilarityCheck(map[i:i + blockLength, j:j + blockWidth], list(blocks.values()))
            unknownCheck = SimilarityCheck(map[i:i + blockLength, j:j + blockWidth], unknownBlocks)
            if knownCheck[0]:
                result[i//blockLength][j//blockWidth]=list(blocks.keys())[knownCheck[1]][:-4]
            elif unknownCheck[0]:
                result[i//blockLength][j//blockWidth]="unknown"
            else:
                unknownBlocks.append(map[i:i+blockLength,j:j+blockWidth])
                result[i//blockLength][j//blockWidth]="unknown"
            bar.next()

if len(unknownBlocks)!=0:
    with Bar(f'Save unknownBlocks...', max=(len(unknownBlocks))) as bar:
        for i in range(len(unknownBlocks)):
                cv2.imwrite(f"{PROJECT_DIR}\\blocks\\{i}.png",unknownBlocks[i])
                bar.next()
    logging.info(f'There are {len(unknownBlocks)} unknown blocks in {PROJECT_DIR}\\blocks\\ .')
    logging.info('Please rename these blocks and place them in each directory.')

else:
    with Bar(f'Output result...',max=(map.shape[0]//blockLength)*(map.shape[1]//blockWidth)) as bar:
        lines=[]
        for i in result:
            temp=str(i[0])
            bar.next()
            for j in i[1:]:
                temp+=interval+str(j)
                bar.next()
            temp+='\n'
            lines.append(temp)

        path = PROJECT_DIR+'\\result.txt'
        f = open(path, 'w')
        f.writelines(lines)
        f.close()
