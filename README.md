How to Use
===

### **step.1取得專案**  
```
git clone git@github.com:ray930227/ImageClassification.git
```
- 請確保專案路徑不包含中文
---
### **step.2安裝套件**
```
pip install -r pip-req.txt 
```
---
<id=3> ### **step.3初始化程式碼**

```
python init.py
```

---
<id=4> ### **step.4設定**

將地圖放進專案目裡，之後更改setting.txt裡的設定

---
### **step.5執行第一次**
```
python main.py
```
---
### **step.6命名未知方塊圖片**

檢查專案目錄中blocks資料夾底下是否有unknown圖片

有的話重新命名，並放入對應的資料夾

沒有的話直接跳下一步

- 請確保blocks資料夾底下的三個資料夾裡有圖片，否則可能會分析錯誤
---
### **step.7執行第二次**
```
python main.py
```
---

結果會顯示在result.txt裡，每隔以逗號隔開，0代表可穿越，1代表不可穿越，2代表事件

之後如果要分析新的地圖，可直接重[第4步](#4)開始

如果要分析不同遊戲得地圖，可直接重[第3步](#3)開始



