from pymongo import MongoClient
from stockhelper.getData import getStockValue
from stockhelper.getstockcode import ReadQuotes
import pytz
import pandas as pd
import pdb
import datetime
import time



class updateDatabase():
    def __init__(self):

        self.all_quotes = ReadQuotes()
        self.read_stock = getStockValue()
        self.sleep_time = 5
        self.connection = MongoClient(host='localhost', port=27017)
        self.database = self.connection['StockData']
        # pdb.set_trace()

    def check_collection(self, Companycode):

        if Companycode in self.database.list_collection_names():
            data_t = self.database[Companycode]
            return data_t.count() != 0

        return False


    def InsertAll(self, Companycode):
        data_all = self.read_stock.getHistoryData(Companycode)

        collection_t = self.database[Companycode]
        collection_t.insert_many(data_all)
        

    def updateANew(self, Companycode):
        # pdb.set_trace()
        tz = pytz.timezone('Asia/Shanghai')
        query = {'day': {'$gt': datetime.datetime.now(
            tz=tz) - datetime.timedelta(days=3)}}

        arg = [
            {'$match': query},
            {'$group': {
                '_id': 1,
                'day':'$day'
            }},
            {'$sort': {'day': 1}},
        ]
        # latest_record_time = self.database[Companycode].aggregate(arg)
        latest_record = self.database[Companycode].find({}).sort([('day', -1)]).limit(1)
        latest_record_time = latest_record[0]['day']
        now = datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        
        days = pd.bdate_range(latest_record_time, now, freq='b')
        lens = max(len(days),1) * 4 * 12
        data_specific = self.read_stock.getHistoryData(
            Companycode, datalen=lens)
        data_specific.sort(key=lambda x:x["day"])
        data_new = []
        for data in data_specific:
            if data['day'] > latest_record_time:
                data_new.append(data)

        if data_new:
            self.database[Companycode].insert_many(data_new)
        
        # pdb.set_trace()


    def updateAllDatabase(self):
        # pdb.set_trace()
        # count = 0
        for quote in self.all_quotes:
            # count += 1
            # if count > 100:
            #     count = 0
            #     time.sleep(self.sleep_time)
            time.sleep(self.sleep_time)
            
            if self.check_collection(quote['Symbol']):
                self.updateANew(quote['Symbol'])
                print(quote['Symbol'] + '\'s updating is finished!')
            else:
                self.InsertAll(quote['Symbol'])
                print(quote['Symbol'] + '\'s inserting is finished!')

    def updateADatabase(self, Companycode):
        # pdb.set_trace()
        
        if self.check_collection(Companycode):
            time.sleep(self.sleep_time)
            self.updateANew(Companycode)
            print(Companycode + '\'s updating is finished!')
        else:
            time.sleep(self.sleep_time)
            self.InsertAll(Companycode)
            print(Companycode + '\'s inserting is finished!')

    

        



