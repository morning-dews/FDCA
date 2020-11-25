import requests
import json
import timeit
import io
import os
import pdb
export_path = './tmp/'

def load_all_quote_symbol():
    print("load_all_quote_symbol start..." + "\n")
    start = timeit.default_timer()
    all_quotes = []
    all_quotes_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'
    try:
        count = 1
        while (count < 1000):
            para_val = '[["hq","hs_a","",0,' + str(count) + ',500]]'
            r_params = {'__s': para_val}
            r = requests.get(all_quotes_url, params=r_params)
            if(len(r.json()[0]['items']) == 0):
                break
            for item in r.json()[0]['items']:
                quote = {}
                code = item[0]
                name = item[2]
                ## convert quote code
                if(code.find('sh') > -1):
                    # code = code[2:] + '.SS'
                ## convert quote code end
                    quote['Symbol'] = code
                    quote['Name'] = name
                    all_quotes.append(quote)
            count += 1
    except Exception as e:
        print("Error: Failed to load all stock symbol..." + "\n")
        print(e)
    print("load_all_quote_symbol end... time cost: " +
            str(round(timeit.default_timer() - start)) + "s" + "\n")
    print("total " + str(len(all_quotes)) + " quotes are loaded..." + "\n")
    return all_quotes


def ReadQuotes(file_name='stockQuotes'):
    # start = timeit.default_timer()
    file_path = export_path + '/' + file_name + '.json'
    if os.path.exists(file_path):
        f = open(file_path, 'r')
        data_string = f.read()
        if len(data_string) > 0:
            return json.loads(data_string)
        
    all_quotes = load_all_quote_symbol()

    if not os.path.exists(export_path):
        os.makedirs(export_path)
    if(all_quotes is None or len(all_quotes) == 0):
        print("no data to export...\n")
    
    f = open(file_path, 'w')

    json.dump(all_quotes, f, ensure_ascii=False)
    return all_quotes



if __name__ == '__main__':
    data = ReadQuotes()


