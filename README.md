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
### **step.3初始化程式碼**

```
python init.py
```

---
### **step.4設定**

將地圖放進專案目錄裡，之後更改setting.txt裡的設定

此時若已有切割好的方塊圖片可以先放入blocks資料夾裡

---
### **step.5執行第一次**
```
python main.py
```
---
### **step.6命名未知方塊圖片**

檢查專案目錄中blocks資料夾底下是否有unknown圖片

有的話重新命名(可略過)

沒有的話直接跳下一步

- 請確保圖片有放入正確的資料夾裡，否則可能會分析錯誤
---
### **step.7執行第二次**
```
python main.py
```
---

結果會顯示在result.txt裡，每格以setting.txt裡的interval隔開

之後如果要分析新的地圖，可直接重第4步開始

如果要分析不同遊戲得地圖，可直接重第3步開始
