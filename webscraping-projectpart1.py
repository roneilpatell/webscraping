from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from twilio.rest import Client
import keys
twilio_client = Client(keys.accountSID, keys.authToken)

url = 'https://crypto.com/price'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')
print(soup.title.text)

twilio_number = "+18449612956"
my_cellphone = "+18323898387"

rows_crypto = soup.findAll('tr')

for cryptos in range(1, 6):
    td_crypto = rows_crypto[cryptos].findAll('td')

    currency= td_crypto[2].text.strip()
    print(f'Name: {currency}')

    price = td_crypto[3]
    price_elements_crypto = price.findAll('p')
    current_price = price_elements_crypto[0].text.strip('$').replace(',', '') if price_elements_crypto else 'N/A'
    print(f'Current Price: {current_price}')

    change_crypto = td_crypto[4].text
    print(f'% change in the last 24 hrs: {change_crypto}')

    price_diff = float(current_price) * (1 + (float(change_crypto.strip('%').strip('+')) / 100))
    print(f'Corresponding price (based on % change): {price_diff:.3f}')

    if currency.lower() == 'ethereum' and float(current_price) > 2000:
        message_crypto = "Notice: Ethereum value is above $2,000"
        message_crypto = twilio_client.messages.create(to=my_cellphone, from_=twilio_number, body=message_crypto)

