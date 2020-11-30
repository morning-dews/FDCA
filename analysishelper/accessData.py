from pymongo import MongoClient
import numpy as np


class accessData():
    def __init__(self) -> None:
        self.connection = MongoClient(host='localhost', port=27017)
        self.database = self.connection['StockData']

    def getdata(self, Companycode: str, type_: str = 'close') -> np:
        connection_t = self.database[Companycode]
        data = list(connection_t.find({}, {'_id': 0, type_: 1}))

        data_all = []
        for data_t in data:
            data_all.append(data_t[type_])

        return np.array(data_all)
