import urllib.request as urllib
import json
import time
import chardet


class getStockValue():

    def __init__(self) -> None:
        self.url = 'http://money.finance.sina.com.cn/quotes' + \
            '_service/api/json_v2.php/CN_MarketData.getKLineData?symbol='
        self.url_realtime = 'http://hq.sinajs.cn/list='

    def formUrl(self, symbol: str, scale: int = 5, datalen: int = 2048) -> str:
        # The maximum returned data length is fixed
        # which means shrink the scale would let us get earlier data.
        return self.url + symbol + '&scale=' + str(scale) \
            + '&ma=1&datalen=' + str(datalen)

    def getHistoryData(self, Companycode: str, scale: int = 5,
                       datalen: int = 2048) -> json:
        urlt = self.formUrl(Companycode, scale=scale, datalen=datalen)
        flag = True
        while flag:
            try:
                flag = False
                response = urllib.urlopen(urlt)
                raw_html = response.read()
            except IOError:
                flag = True
                print('API is blocked by Sina, \
                    thus the system is sleeping.... Please wait!')
                time.sleep(60 * 30)  # sleep 30 minutes

        raw_html = str(raw_html, "utf-8")
        data = json.loads(raw_html, object_hook=self.as_float)

        return data

    def getRealTimeData(self, Companycode: str) -> list:

        url_r = self.url_realtime + Companycode
        flag = True
        while flag:
            try:
                flag = False
                response = urllib.urlopen(url_r)
                raw_html = response.read()
            except IOError:
                flag = True
                print('API is blocked by Sina, \
                    thus the system is sleeping.... Please wait!')
                time.sleep(60 * 30)  # sleep 30 minutes

        encoding = chardet.detect(raw_html)["encoding"]
        raw_html = str(raw_html, encoding)[21:-3]
        data = raw_html.split(',')

        return data

    def as_float(self, obj: dict) -> dict:

        if "open" in obj:
            obj["open"] = float(obj["open"])
        if "high" in obj:
            obj["high"] = float(obj["high"])
        if "low" in obj:
            obj["low"] = float(obj["low"])
        if "close" in obj:
            obj["close"] = float(obj["close"])
        if "volume" in obj:
            obj["volume"] = float(obj["volume"])

        return obj


# read_stock = getStockValue()
# data = read_stock.getHistoryData('sz000001')
