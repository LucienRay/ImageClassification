import cv2
import numpy as np
import os
import logging
from progress.bar import Bar

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
PROJECT_DIR=os.path.dirname(os.path.abspath(__file__))

f=open(PROJECT_DIR+'\\setting.txt','r')
setting=f.readlines()
mapName=setting[0].split('=')[1].strip()
blockLength=int(setting[1].split('=')[1].strip())
blockWidth=int(setting[2].split('=')[1].strip())
f.close()


map = cv2.imread(PROJECT_DIR+'\\'+mapName)
traversableBlocksList=os.listdir(PROJECT_DIR+'\\blocks\\traversable')
untraversableBlocksList = os.listdir(PROJECT_DIR+'\\blocks\\untraversable')
eventBlocksList=os.listdir(PROJECT_DIR+'\\blocks\\event')
traversableBlocks=[]
untraversableBlocks=[]
eventBlocks=[]
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

if len(traversableBlocksList+untraversableBlocksList+eventBlocksList)!=0:
    with Bar(f'Loading blocks...',max=len(traversableBlocksList+untraversableBlocksList+eventBlocksList)) as bar:
        for i in traversableBlocksList:
            traversableBlocks.append(cv2.imread(PROJECT_DIR+'\\blocks\\traversable\\'+i))
            bar.next()

        for i in untraversableBlocksList:
            untraversableBlocks.append(cv2.imread(PROJECT_DIR+'\\blocks\\untraversable\\'+i))
            bar.next()

        for i in eventBlocksList:
            eventBlocks.append(cv2.imread(PROJECT_DIR+'\\blocks\\event\\'+i))
            bar.next()
    
with Bar(f'Classification blocks...',max=(map.shape[0]//blockLength)*(map.shape[1]//blockWidth)) as bar:
    for i in range(0,map.shape[0],blockLength):
        for j in range(0,map.shape[1],blockWidth):
            if SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],traversableBlocks):
                result[i//blockLength][j//blockWidth]=0
            elif SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],untraversableBlocks):
                result[i//blockLength][j//blockWidth]=1
            elif SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],eventBlocks):
                result[i//blockLength][j//blockWidth]=2
            elif SimilarityCheck(map[i:i+blockLength,j:j+blockWidth],blocks):
                result[i//blockLength][j//blockWidth]=-1
            else:
                blocks.append(map[i:i+blockLength,j:j+blockWidth])
                result[i//blockLength][j//blockWidth]=-1
            bar.next()
            
if len(blocks)!=0:
    for i in range(len(blocks)):
            cv2.imwrite(f"C:\CODE\ImageClassification\\blocks\\{i}.png",blocks[i])
    logging.info(f'There are {len(blocks)} unknown blocks in {PROJECT_DIR}+\\blocks\\ .')
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

        path = 'C:\CODE\ImageClassification\\result.txt'
        f = open(path, 'w')
        f.writelines(lines)
        f.close()