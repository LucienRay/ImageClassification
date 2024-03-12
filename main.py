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
    f.close()
except ValueError:
    logging.error("The setting.txt has not been set yet.")
    os._exit(0)

map = cv2.imread(PROJECT_DIR+'\\'+mapName)
traversableBlocksList=[os.listdir(PROJECT_DIR+'\\blocks\\traversable\\normal'),os.listdir(PROJECT_DIR+'\\blocks\\traversable\\event')]
untraversableBlocksList=[os.listdir(PROJECT_DIR+'\\blocks\\untraversable\\normal'),os.listdir(PROJECT_DIR+'\\blocks\\untraversable\\event')]
traversableBlocks=[]
untraversableBlocks=[]
blocks=[]
result=[[0 for i in range(map.shape[1]//blockWidth)]for i in range(map.shape[0]//blockLength)]

if map.shape[0]%blockLength!=0 or map.shape[1]%blockWidth!=0:
    logging.error("Map's size is not a multiple of block's size.")
    os._exit(0)

def SimilarityCheck(target,Blocks):
    for i in Blocks:
        try:
            diff=cv2.absdiff(i,target)
            mse=np.mean(diff**2)
            if mse<50:
                return True
        except:
            cv2.imshow("test",target)
            cv2.waitKey(0)
            cv2.imshow(i)
            cv2.waitKey(0)
    return False

def readImage(path,fileArray):
    result=[]
    for i in fileArray:
        result.append(cv2.imread(path+i))
    return result

if len(traversableBlocksList[0]+traversableBlocksList[1]+untraversableBlocksList[0]+untraversableBlocksList[1])!=0:
    with Bar(f'Loading blocks...',max=len(traversableBlocksList[0]+traversableBlocksList[1]+untraversableBlocksList[0]+untraversableBlocksList[1])) as bar:
        traversableBlocks.append(readImage(PROJECT_DIR+'\\blocks\\traversable\\normal\\',traversableBlocksList[0]))
        bar.next(len(traversableBlocksList[0]))
        traversableBlocks.append(readImage(PROJECT_DIR+'\\blocks\\traversable\\event\\',traversableBlocksList[1]))
        bar.next(len(traversableBlocksList[1]))
        untraversableBlocks.append(readImage(PROJECT_DIR+'\\blocks\\untraversable\\normal\\',untraversableBlocksList[0]))
        bar.next(len(untraversableBlocksList[0]))
        untraversableBlocks.append(readImage(PROJECT_DIR+'\\blocks\\untraversable\\event\\',untraversableBlocksList[1]))
        bar.next(len(untraversableBlocksList[1]))
    
with Bar(f'Classification blocks...',max=(map.shape[0]//blockLength)*(map.shape[1]//blockWidth)) as bar:
    for i in range(0,map.shape[0],blockLength):
        for j in range(0,map.shape[1],blockWidth):
            if SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],traversableBlocks[0]):
                result[i//blockLength][j//blockWidth]=0
            elif SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],untraversableBlocks[0]):
                result[i//blockLength][j//blockWidth]=1
            elif SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],traversableBlocks[1]):
                result[i//blockLength][j//blockWidth]=2
            elif SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],untraversableBlocks[1]):
                result[i//blockLength][j//blockWidth]=3
            elif SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],blocks):
                result[i//blockLength][j//blockWidth]=-1
            else:
                blocks.append(map[i:i+blockLength,j:j+blockWidth])
                result[i//blockLength][j//blockWidth]=-1
            bar.next()
            
if len(blocks)!=0:
    for i in range(len(blocks)):
            cv2.imwrite(f"{PROJECT_DIR}\\blocks\\{i}.png",blocks[i])
    logging.info(f'There are {len(blocks)} unknown blocks in {PROJECT_DIR}\\blocks\\ .')
    logging.info('Please rename these blocks and place them in each directory.')

else:
    with Bar(f'Output result...',max=(map.shape[0]//blockLength)*(map.shape[1]//blockWidth)) as bar:
        lines=[]
        for i in result:
            temp=str(i[0])
            bar.next()
            for j in i[1:]:
                temp+=","+str(j)
                bar.next()
            temp+='\n'
            lines.append(temp)

        path = PROJECT_DIR+'\\result.txt'
        f = open(path, 'w')
        f.writelines(lines)
        f.close()