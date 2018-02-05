import re

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

from binance.client import Client

client = Client("", "")


def binance(bin_id):
    # 币安价格
    return float(client.get_symbol_ticker(symbol=bin_id)['price'])


def otc(otc_id):
    # otcbtc价格
    print(otc_id)
    r = requests.get(url='https://otcbtc.com/sell_offers?currency=' + otc_id + '&fiat_currency=cny&payment_type=all')
    soup = BeautifulSoup(r.text, "html5lib")
    t = soup.find_all(name='span', class_='recent-average-price')[0].contents[0]
    otc_price = float("".join(re.findall("[0-9.]", t)))
    p = soup.find_all(name='span', class_='live-count')[0].contents[0]
    p_num = "".join(re.findall("[0-9]", p))
    print('otc价格:', otc_price, '--在线人数:' + p_num)
    return otc_price


def coincola(pay_type, crypto_currency):
    # coincola价格
    headers = {
        'accept-language': 'zh-HK',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36',
    }
    r = requests.get(url='https://www.coincola.com/' + pay_type + '/' + crypto_currency + '?country_code=CN',
                     headers=headers)
    soup = BeautifulSoup(r.text, 'html5lib')
    tds = soup.find_all(name='td', class_='td-price')
    prices = []
    for td in tds:
        prices.append(float("".join(re.findall('[0-9.]', td.contents[0]))))

    return DataFrame(prices).mean()[0]


def coinw():
    # 币赢价格
    eth = requests.post(' https://www.coinw.com/appApi.html?action=market&symbol=14').json()['buy']
    eos = requests.post(' https://www.coinw.com/appApi.html?action=market&symbol=29').json()['buy']
    return 'coinw:', {'eth': eth, 'eos': eos}


def localcoin():
    # LocalCoin价格
    r = requests.get('https://localbitcoins.com/zh-cn/buy-bitcoins-online/cny/')
    soup = BeautifulSoup(r.text, 'html5lib')
    strs = soup.find_all(name='div', id='result-count')[0].contents[-2]
    num = int("".join(re.findall('[0-9]', strs.string)))
    tds = soup.find_all(name='td', class_='column-price')
    prices = []
    for td in tds:
        prices.append(float("".join(re.findall('[0-9.]', td.contents[0]))))
    return {'prices:': DataFrame(prices).mean()[0], '人数': num}
