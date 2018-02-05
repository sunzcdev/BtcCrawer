def yijia(otc_id, bin_id):
    print(otc_id)
    soup = get(otc_id)
    t = soup.find_all(name='span', class_='recent-average-price')[0].contents[0]
    otc_price = float("".join(re.findall("[0-9.]", t)))
    p = soup.find_all(name='span', class_='live-count')[0].contents[0]
    p_num = "".join(re.findall("[0-9]", p))
    print('otc价格:', otc_price, '--在线人数:' + p_num)
    binance_price = float(client.get_symbol_ticker(symbol=bin_id)['price']) * 6.285
    print('币安价格:', binance_price)
    rate = ((otc_price / binance_price) - 1) * 100
    print('溢价', rate)
    return binance_price