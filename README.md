# ImageClassification

How to Use
===

**step.1取得專案**  
```
git clone git@github.com:ray930227/ImageClassification.git
```
- 請確保專案路徑不包含中文

**step.2安裝套件**
```
pip install -r pip-req.txt 
```

**step.3執行第一次**
```
python main.py
```

**step.4命名未知方塊圖片**

將專案目錄中blocks資料夾底下的unknown圖片重新命名，並放入對應的資料夾

**step.5執行第二次**
```
python main.py
```

結果會顯示在result.txt裡，每隔以逗號隔開，0代表可穿越，1代表不可穿越，2代表事件
