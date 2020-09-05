from .models import Scraper
import json
import threading
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

class Threads():

    data_scrapers = []
    def createThread(self, id_in, frequency, index):
        time.sleep(frequency)
        try:
            bs = self.getDataCoin()
            data = Scraper.objects.get(id=id_in)
            oneItem = {}
            oneItem['id'] = data.id
            oneItem['created_at'] = str(data.created_at)
            currency = (str(data.currency)).lower()
            oneItem['currency'] = currency
            currency = (str(data.currency)).lower()
            frequency = int(data.frequency)
            oneItem['frequency'] = frequency
            # Obtiene valor
            value = str(bs.find(href="/currencies/"+currency+"/markets/").text)[1:]
            oneItem['value'] = value
            date_now = datetime.now()
            oneItem['value_updated_at'] = date_now
            t = threading.Thread(target=self.createThread,args=[data.id, frequency, index])
            t.start()
            self.data_scrapers[index] = oneItem
            return
        except:
            pass
    
    def addToThread(self, obj):
        bs = self.getDataCoin()
        oneItem = {}
        oneItem['id'] = obj.id
        oneItem['created_at'] = str(obj.created_at)
        currency = (str(obj.currency)).lower()
        oneItem['currency'] = currency
        currency = (str(obj.currency)).lower()
        frequency = int(obj.frequency)
        oneItem['frequency'] = frequency
        # Obtiene valor
        value = str(bs.find(href="/currencies/"+currency+"/markets/").text)[1:]
        oneItem['value'] = value
        date_now = datetime.now()
        oneItem['value_updated_at'] = date_now
        self.data_scrapers.append(oneItem)
        t = threading.Thread(target=self.createThread,args=[obj.id, frequency, len(self.data_scrapers) - 1])
        t.start()

    def getDataThreads(self):
        return self.data_scrapers
        
    def getDataCoin(self):
        url = 'https://coinmarketcap.com/'
        #Se obtiene data de URL
        res = requests.get(url)
        res.encoding = "utf-8"
        bs = BeautifulSoup(res.text, "html.parser")
        return bs

    def updateObjData(self, id_in, frequency):
        count = 0
        for i in self.data_scrapers:
            if str(i['id']) == str(id_in):
                self.data_scrapers[count]['frequency'] = frequency
            count += 1

    def deleteObjData(self, id_in):
        count = 0
        for i in self.data_scrapers:
            if str(i['id']) == str(id_in):
                del self.data_scrapers[count]
            count += 1

    def thread_function(self):
        print (' --- Inicialización de threads ---')
        resultsData = Scraper.objects.all()
        bs = self.getDataCoin()
        count = 0
        for i in resultsData:
            oneItem = {}
            oneItem['id'] = i.id
            oneItem['created_at'] = str(i.created_at)
            currency = (str(i.currency)).lower()
            oneItem['currency'] = currency
            currency = (str(i.currency)).lower()
            frequency = int(i.frequency)
            oneItem['frequency'] = frequency
            # Obtiene valor
            value = str(bs.find(href="/currencies/"+currency+"/markets/").text)[1:]
            oneItem['value'] = value
            date_now = datetime.now()
            oneItem['value_updated_at'] = date_now
            t = threading.Thread(target=self.createThread,args=[i.id, frequency, count])
            t.start()
            self.data_scrapers.append(oneItem)
            count += 1
