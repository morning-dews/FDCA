import numpy as np
from scipy.stats import pearsonr
from analysishelper.accessData import accessData
from stockhelper.getstockcode import ReadQuotes
from tqdm import tqdm
from typing import Tuple


class pearsonH():
    def __init__(self) -> None:
        self.all_quotes = ReadQuotes()
        self.search_index_name, self.search_index_quote = self.build_index()
        self.accessData = accessData()

    def PearsonSimple(self) -> Tuple[np, np]:
        test_length = 100
        length = len(self.all_quotes)
        pearson_result = [[0 for _ in range(length)] for _ in range(length)]
        pearson_p_value = [[0 for _ in range(length)] for _ in range(length)]
        for i in tqdm(range(test_length)):
            data_i = self.accessData.getdata(self.all_quotes[i]['Symbol'])
            if data_i.size == 0:
                continue
            for j in range(i+1, test_length):
                data_j = self.accessData.getdata(self.all_quotes[j]['Symbol'])
                if data_j.size == 0:
                    continue
                if data_i.size == data_j.size:
                    pearson_result[i][j], pearson_p_value[i][j] \
                        = pearsonr(data_i, data_j)

        temp_res, temp_p = np.array(pearson_result), np.array(pearson_p_value)
        # pdb.set_trace()
        return temp_res + np.transpose(temp_res), temp_p + np.transpose(temp_p)

    def PearsonDelay(self, start: int = 235, delay: int = 8,
                     window: int = 500) -> Tuple[np, np]:
        test_length = 100
        length = len(self.all_quotes)
        pearson_result = [[-1000 for _ in range(length)]
                          for _ in range(length)]
        pearson_p_value = [[-1000 for _ in range(length)]
                           for _ in range(length)]

        for i in tqdm(range(test_length)):
            data_i = self.accessData.getdata(self.all_quotes[i]['Symbol'])
            if data_i.size == 0:
                continue
            for j in range(test_length):
                data_j = self.accessData.getdata(self.all_quotes[j]['Symbol'])
                if data_i.size == 0:
                    continue
                if i == j:
                    continue
                # pdb.set_trace()
                x, y = data_i[start:start+window], \
                    data_j[start + delay:start + delay + window]
                if x.size == y.size:
                    pearson_result[i][j], pearson_p_value[i][j] \
                        = pearsonr(x, y)

        return np.array(pearson_result), np.array(pearson_p_value)

    # helper functions
    def build_index(self) -> Tuple[dict, dict]:
        count = 0
        name_index = {}
        quote_index = {}
        for quote in self.all_quotes:
            name_index[quote['Name']] = count
            quote_index[quote['Symbol']] = count
            count += 1

        return name_index, quote_index

    def getIndexUsingName(self, name: str) -> int:
        return self.search_index_name[name] \
            if name in self.search_index_name else -1

    def getIndexUsingQuote(self, Companycode: str) -> int:
        return self.search_index_quote[Companycode] \
            if Companycode in self.search_index_quote else -1

    def getNameUsingIndex(self, index: int) -> str:
        return self.all_quotes[index]['Name']
