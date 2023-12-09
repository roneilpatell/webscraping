from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from twilio.rest import Client

url_crypto = 'https://crypto.com/price'
headers_crypto = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req_crypto = Request(url_crypto, headers=headers_crypto)
webpage_crypto = urlopen(req_crypto).read()
soup_crypto = BeautifulSoup(webpage_crypto, 'html.parser')
print(soup_crypto.title.text)

import keys
twilio_client = Client(keys.accountSID, keys.authToken)

twilio_number = "+18449612956"
my_cellphone = "+18323898387"

rows_crypto = soup_crypto.findAll('tr')

for idx in range(1, 6):
    td_crypto = rows_crypto[idx].findAll('td')

    # name of the currency
    currency_name = td_crypto[2].text.strip()
    print(f'Name: {currency_name}')

    # current price
    raw_price_crypto = td_crypto[3]
    price_elements_crypto = raw_price_crypto.findAll('p')
    current_price_crypto = price_elements_crypto[0].text.strip('$').replace(',', '') if price_elements_crypto else 'N/A'
    print(f'Current Price: {current_price_crypto}')

    #% change in the last 24 hrs
    change_crypto = td_crypto[4].text
    print(f'% change in the last 24 hrs: {change_crypto}')

    # corresponding price based on % change
    change_price_crypto = float(current_price_crypto) * (1 + (float(change_crypto.strip('%').strip('+')) / 100))
    print(f'Corresponding price (based on % change): {change_price_crypto:.3f}')

    if currency_name.lower() == 'ethereum' and float(current_price_crypto) > 2000:
        message_crypto = "Notice: Ethereum value is above $2,000"
        message_crypto = twilio_client.messages.create(to=my_cellphone, from_=twilio_number, body=message_crypto)

    print()
    print()
