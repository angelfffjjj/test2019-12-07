#準備資料
import json
file=open("data.txt", mode="r", encoding="utf-8")
data=json.load(file)
file.close()
#每更新一次 按ctrl+c 就可以重新跑出位置 再打python 檔名.py
# 安裝flask (在TERMINAL打) pip still flask
from flask import * # 載入 flask 模組
app=Flask("My Website") # 建立一個網站應用程式物件

#網站的網址:http://主機名稱/路徑?參數名稱=資料&參出名稱=資料&........  (主機>下面打的程式)
#例如:https://test2019-11-30.herokuapp.com//
#如果打http://127.0.0.1:5000/jdosfkolja 會跑出404 因為沒連到主機
@app.route("/") # 指定對應的網址路徑
def home(): # 對應的處理函
    return render_template("home.html") # 回應給前端的訊息
    #在原本的資料夾中 新增一個資料夾 "templates"
    #在HTML中 用"!+Tab"可以跑出上面的東西<!DOCTYPE html>

#例如:https://test2019-11-30.herokuapp.com/test.php?keyword=關鍵字
@app.route("/test.php") # 指定對應的網址路徑
def test(): # 對應的處理函式
    #取得網址列上的參數:requst.args.get(參數名稱,預設值)
    keyword=request.args.get("keyword", None)
    if keyword==None:
        return redirect("/")#如果使用者沒打後面的部分(test.php?keyword=關鍵字) 則導向路徑首頁/
    else:
        if keyword in data: # 回應給前端的訊息
            return render_template("result.html", result=data[keyword])
        else:
            return render_template("result.html", result="沒有翻譯")

#建立負責處理LINE 訊息的網址
#例如：https://test2019-11-30.herokuapp.com/linebot
#找圖片的網址:
#https://test2019-11-30.herokuapp.com/static/images/檔案名稱
#https://test2019-11-30.herokuapp.com/static/images/big.jpg
#https://test2019-11-30.herokuapp.com/static/images/small.jpg
import json #解讀JSON 格式的套件
import urllib.request #發送連線的套件
@app.route("/linebot", methods = ["GET", "POST"])
def linebot():
        #取得 LINE 傳遞過來的資料
        content=request.json #取得整包資訊
        event=content["events"][0] #發生的事件(使用者傳遞訊息、使用者加入好友等等等)
        eventType=event["type"] #事件的型態
        replyToken=event["replyToken"] #回應這個訊息，需要的鑰匙(token)
        text=event["message"]["text"] #取得使用者真正傳遞的訊息文字
        #準備為應給使用者

        if "圖片" in text:
            message={
                "type":"image",
                "originalContentUrl": "https://test2019-11-30.herokuapp.com/static/images/big.jpg", #原始圖片的網址
                "previewImageUrl":"https://test2019-11-30.herokuapp.com/static/images/small.jpg" #預覽圖片的網址
            }

        else:    
            if text=="哈囉":
                replyText="哈囉你好嗎 衷心感謝 珍重再見"
            elif "哈哈" in text:
                replyText="是在哈囉"
            elif "雨量" in text:
                #抓取雨量的資料
                url="http://117.56.59.17/OpenData/API/Rain/Get?stationNo=&loginId=open_rain&dataKey=85452C1D"
                response=urllib.request.urlopen(url)
                response=response.read().decode("utf-8")
                weather=json.loads(response)
                #準備回應
                replyText="雨量觀測資料："
                stations=weather["data"]
                #確認使用者想找的地區
                areas=["文山","大安","中正","中山","松山","信義","南港","內湖","萬華","士林","北投"]
                area=None #記錄使用者的搜尋目標
                for a in areas:
                    if a in text:
                        area=a
                        break
                #根據使用者想找的地區，給資料
                if area==None:
                    replyText+="沒有資料"
                else:
                    for station in stations:
                        if area in station["stationName"]:
                            replyText+="\n"+station["stationName"]+":"+str(station["rain"])+" 公厘"
            else:
                replyText="不知道啦~"
            message={"type":"text", "text":replyText} #單一回應訊息
        #整包回應 : 可以包含很多訊息
        body={
            "replyToken":replyToken,
            "messages":[message]
        }
        # 處理網路連線LINE
        # 準備連線的細節：網址、標頭、資料
        req=urllib.request.Request("https://api.line.me/v2/bot/message/reply", headers={
            "Content-Type":"application/json",
            "Authorization":"Bearer "+"foDTzhEg+4ZjeuSO44b4zbXv0gerVY28M4rBLLxr2sBDHi4gqG4h3kHTd5COeFlqEsr0df71o22lxyTRstOTM/4vbLRgPyNh4n6FvKKN4u3IChHnKxCr3PxowIFLLIg5G6OdSyv7KKR0SXQgKkyUugdB04t89/1O/w1cDnyilFU="  #Messaging API的最後面 > Channel access token
        }, data=json.dumps(body).encode("utf8"))
        # 搋連線
        response=urllib.request.urlopen(req)
        #取得回應
        response=response.read().decode("utf-8")
        print(resonese)
        return "ok"

if __name__=="__main__": # 如果以主程式執行，立即啟動伺服器
    app.run() # 啟動伺服器
#建立一個 "runtime.txt" 告訴它 Python的版本
#建立一個 "requirements.txt"
#建立一個 "Procfile" 用綠色獨角獸(gunucorn)打開app
#TWEMINAL 會出現一個網址 複製貼上GOOGLE裡面 就可以出現一個網站