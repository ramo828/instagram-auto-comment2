from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtGui import QTextCursor
from instagrapi import Client
from instagrapi.exceptions import UnknownError, ClientNotFoundError
import random as rd
from random import randint
import datetime
import time
from controls.database import Database


class Utility:
    def __init__(self, choise = 0):
        self.choise = choise
    
    def randomize(self):
        char = ""
        alpha = "abcdefghjklmnopqrstuvxyzw"
        numeric = "0123456789"
        symbol = "~!@#$%^&*()_+:'"
        if(self.choise == 0):
            rand = rd.randint(0, len(alpha)-1)
            char = alpha[rand]
        elif (self.choise == 1):
            rand = rd.randint(0, len(numeric)-1)
            char = numeric[rand]
        elif (self.choise == 2):
            rand = rd.randint(0, len(symbol)-1)
            char = symbol[rand]
        return char

    def buildRand(self, length):
        ch = ""
        for i in range(length):
            ch = ch + self.randomize()
        return ch
    
   


class autoComment:
    def __init__(self, url="https://www.instagram.com/p/", temp_code=""):
        self.url = url
        self.tempCode = temp_code
        self.medias = []
        self.user_id = ""
        self.cl = Client()
        # call instapi client
       

    def setAccount(self, username, password):
        self.username = username
        self.password = password
        # Login ve sifre
    def connect(self):
        self.cl.login(self.username, self.password)
        self.user_id = self.cl.user_id_from_username(self.page)
        # instagram page
       

    def getMedia(self, commentNo):
        self.medias = self.cl.user_medias(int(self.user_id), 2+commentNo)
        # page media (max=5)
        latest_post = self.medias[commentNo].code
        # latest post code
        self.tempCode = latest_post
        # tamper code
        self.url = self.url
        # instagram post link

    def setPage(self, page):
        self.page = page

    def setComment(self, comment:str, rcount:int, rchoise:int):
        util = Utility(rchoise)
        comment_temp = comment.splitlines()
        length = len(comment_temp)-1
        self.comment = comment_temp[randint(0,length)]+" "+str(util.buildRand(rcount))

        # print(self.comment)

    def send(self, code):
        media_pk = self.cl.media_pk_from_url(self.url+code)
        media_id = self.cl.media_id(media_pk=media_pk)
        print(self.cl.media_info(media_pk=media_pk))
        print(media_id)
        # latest post id
        comment = self.cl.media_comment(media_id, self.comment)
        # comment   

class Worker(QObject):
    flag = True
    log = Signal(str)
    success_counter_signal = Signal(int)
    try_counter_signal = Signal(int)

        
    def stopBot(self, flag):
        self.flag = flag

    def setData(self, san:int, sayfa:str, rcount:int,rchoise:int, yorum:str):
        self.san = san
        self.sayfa = sayfa
        self.rcount = rcount
        self.rchoise = rchoise
        self.yorum = yorum


    def runBot(self):      
        util = Utility()
        d = Database()
        unique = "testData"
        count = 1
        success_counter = 0
        self.log.emit("Çalışıyor...")
        kadi = d.load_data(index=2)
        ksifre = d.load_data(index=3)
      
        util.choise = self.rchoise
        # self.yorum +=str(util.buildRand(self.rcount))
        auto = autoComment()
        if(self.flag!=True):
            self.log.emit("Durduruldu...")
        self.try_counter_signal.emit(str(count))
        while(self.flag):
            an = datetime.datetime.now()
            saat = datetime.datetime.strftime(an, '%X') # Saat
            self.log.emit(f"\n{saat} >> Denetleme süresi: {self.san}")
            time.sleep(self.san)
            if(self.flag != True):
                break
            self.log.emit(f"\n{saat} >> Deneme sayısı: {count}")
            auto.setAccount(username=kadi, password=ksifre)
            auto.setPage(self.sayfa)
            try:
                auto.setComment(comment=self.yorum, rcount=self.rcount, rchoise=self.rchoise)
                auto.connect()
            except UnknownError:
                self.log.emit("\nLütfen instagram bilgilerini kontrol edip doğru girdiyinizden emin olun")
            if(self.flag != True):
                break
            try:
                auto.getMedia(0)
            except (ClientNotFoundError, IndexError):
                self.log.emit("\nSayfa bulunamadı")
            # Bura baxarsan
            if(count < 2):
                unique = auto.tempCode
            count=count+1
            if(unique != auto.tempCode):
                auto.send(auto.tempCode)
                if(self.flag != True):
                    break
                self.log.emit(f"\n{saat} >> Yeni post paylaşıldı və comment yazıldı")
                unique = auto.tempCode
                success_counter+=1
            else:
                if(self.flag != True):
                    break
                self.log.emit(f"\n{saat} >> Yeni paylaşım bulunamadı")
                self.success_counter_signal.emit(success_counter)
                self.try_counter_signal.emit(count)
                continue