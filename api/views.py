from django.views.generic import View
from .models import Scraper
from .threads import Threads
from django.http import HttpResponse, HttpRequest, JsonResponse, QueryDict
import json
import time
from datetime import datetime

class ScraperAPI(View):


    #Habilitación de threads
    objThreads = Threads()
    objThreads.thread_function() 

    def get(self, *args, **kwargs):
        objThreads = Threads()
        data_scrapers = objThreads.getDataThreads()
        retorno = { 
                    "scrapers": data_scrapers
                  }
        return JsonResponse(retorno)

    def post(self, *args, **kwargs):
        try:
            body_unicode = self.request.body.decode('utf-8')
            body_data = QueryDict(body_unicode)

            date_now = datetime.now()
        
            currency = body_data['currency']
            frequency = body_data['frequency']
            try:
                obj = Scraper.objects.get(currency=currency)
                return JsonResponse({"error": "Scraper it already exists"})
            except:
                b4 = Scraper(currency=currency, frequency=frequency, created_at=date_now)
                b4.save()
                obj = Scraper.objects.get(currency=currency)
                result = {
                            "id": obj.id,
                            "created_at": date_now,
                            "currency": currency,
                            "frequency": frequency
                        }
                objThreads = Threads()
                objThreads.addToThread(obj)
                return JsonResponse(result)
        except:
            return JsonResponse({"error": "Internal error"})

    def put(self, *args, **kwargs):
        try:
            body_unicode = self.request.body.decode('utf-8')
            body_data = QueryDict(body_unicode)
            
            date_now = datetime.now()
        
            id_in = body_data['id']
            frequency = body_data['frequency']
            obj = Scraper.objects.get(id=id_in)
            obj.frequency = frequency
            obj.save()
            objThreads = Threads()
            objThreads.updateObjData(id_in, frequency)
            return JsonResponse({"msg": "Scraper updated"})
        except:
            return JsonResponse({"error": "Internal error"})

    def delete(self, *args, **kwargs):
        try:
            body_unicode = self.request.body.decode('utf-8')
            body_data = QueryDict(body_unicode)
            date_now = datetime.now()
            id_in = body_data['id']
            obj = Scraper.objects.get(id=id_in).delete()
            objThreads = Threads()
            objThreads.deleteObjData(id_in)
            return JsonResponse({"msg": "Scraper deleted"})
        except:
            return JsonResponse({"error": "Internal error"})




