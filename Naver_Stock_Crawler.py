from bs4 import BeautifulSoup
import urllib.request as req
import json
from urllib.parse import  urlparse
upAndDown = { "상승" : 1, "하락" : -1, None : 1}
"""
{
    "date" : "YYYY.MM.DD" ,
    "closing" : "" ,
    "variation" : "" ,
    "opening" : "" ,
    "highest" : "" ,
    "lowest" : "" ,
    "trading" : ""
}

"""
stocks = []
url = "https://finance.naver.com/item/sise_day.nhn?code=005930&page="
res = req.urlopen(url + str(1))
soup = BeautifulSoup(res, "html.parser")
max_page = int(soup.find(class_ = "pgRR").find('a')['href'].split("=")[2])

for page in range(1, max_page + 1 ):
    res = req.urlopen(url + str(page))
    soup = BeautifulSoup(res, "html.parser")
    soup = soup.find(class_ = "type2")
    for table_Row in soup.find_all("tr")[2:] :
        table_Data = table_Row.find_all("td")
        if len(table_Data) < 7 or len(table_Data[0].text) == 1:
            continue
        temp = str(table_Data[0].text).split(".")

        date = temp[0] + "-" + temp[1] + "-" + temp[2]

        """
        if type(table_Data[2].find('img')) is type(None) :
            weight = 1
        else :
            weight = upAndDown[table_Data[2].find('img')['alt']]
        """
        stocks.append({
            "date": date,
            "closing": int(str(table_Data[1].text.replace(",", ""))),
            "variation": 0,
            "opening": int(str(table_Data[3].text.replace(",", ""))),
            "highest": int(str(table_Data[4].text.replace(",", ""))),
            "lowest": int(str(table_Data[5].text.replace(",", ""))),
            "trading": int(str(table_Data[6].text.replace(",", "")))
        })
    print(str(page) + "/" + str(max_page) + " page Crawling Complete")
print("Crawling Complete")

print("json create")
with open('stockData' + '.json', 'w', encoding='utf-8') as f:
    json.dump(stocks, f, ensure_ascii=False, indent=4)

print("json create Complete")