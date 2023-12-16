import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def convert_scraping(url):
    rec = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(rec.text, 'lxml')
    get_div = soup.find('div', class_='tab-box__MainTabContainer-sc-28io75-0 cuMybr')
    get_main = get_div.find('main', class_='tab-box__ContentContainer-sc-28io75-3 joNDZm')
    get_amount_and_from_currency = get_main.find('p', class_='result__ConvertedText-sc-1bsijpp-0 gpvgZe').text
    get_result = get_main.find('p', class_='result__BigRate-sc-1bsijpp-1 dPdXSB').text
    data_dict = {}
    data_dict['amount_and_from'] = get_amount_and_from_currency
    data_dict['result_convert']  = get_result
    return data_dict

