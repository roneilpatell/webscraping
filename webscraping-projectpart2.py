from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

tags = []
diction = {}
quotes = {}
quote_len = {}
num = 1

for values in range(10):
    url = f'http://quotes.toscrape.com/page/{str(num)}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = Request(url, headers=headers)
    webpage = urlopen(request).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    sums = 0

    for new_quotes in range(10):
        raw_quotes = soup.findAll("span", attrs={"class": "text"})
        rawquotes_text = raw_quotes[sums].text
        next_quote = raw_quotes[sums].text.replace('.', '').replace(',', '').replace(u"\u201C", "").replace(u"\u201D", "")

        author_data = soup.findAll("small", attrs={"class": "author"})
        author = author_data[sums].text

        tags = soup.findAll("div", attrs={"class": "tags"})
        new_tag = tags[sums].text.replace("Tags:", "")
        tags.extend(new_tag.split())
        
        quote_len[rawquotes_text] = [len(rawquotes_text)]
        sums += 1

        if author in quotes:
            quotes[author].append(next_quote)
        else:
            quotes[author] = [next_quote]

for item_tags in tags:
    if item_tags in diction:
        diction[item_tags] += 1
    else:
        diction[item_tags] = 1

maximum_count = max(diction.values())
highest_tag = [word for word, count in diction.items() if count == maximum_count]
total_quote = {author: len(quotes) for author, quotes in quotes.items()}
most_quote = max(total_quote, key=total_quote.get)
least_quote = min(total_quote, key=total_quote.get)
total_length = sum(length[0] for length in quote_len.values())
count_quotes = len(quote_len)
average_length = round(total_length / count_quotes)
longest_quote = max(quote_len, key=lambda quote: quote_len[quote][0])
shortest_quote = min(quote_len, key=lambda quote: quote_len[quote][0])

print(f'\n--AUTHORS--')
for a_name, b_value in total_quote.items():
    print(f'\nAuthor: {a_name}')
    print(f'Quote Count: {b_value}')

print(f'\nThe author(s) with most amount of quotes:\n{most_quote}')
print(f'\nThe authors(s) with the least amount of quotes:')

for author_name in least_quote:
    print(author_name)

print(f'\n--QUOTES--')
print(f'\nAverage Quote Length:\n{average_length}')
print(f'\nLongest Quote:\n{longest_quote}')
print(f'\nShortest Quote:\n{shortest_quote}')

print(f'\n--TAGS--')
print(f'\nThe most popular tag is:\n{(str(highest_tag[0])).title()}')
print(f'\nNumber of total tags used:\n{len(tags)}\n')

authors_data_frame = sorted(total_quote.items(), key=lambda x_value: x_value[1], reverse=True)[:10]
authors_frame = pd.DataFrame(authors_data_frame, columns=['Authors', 'Totals of Quotes'])
top_tags_frame = sorted(diction.items(), key=lambda x_value: x_value[1], reverse=True)[:10]
top_tags_data_frame = pd.DataFrame(top_tags_frame, columns=['Tags', 'Popularity'])

authors_graph = px.bar(authors_frame, x='Author', y='Number of Quotes', title='Top 10 Authors and Their Corresponding Number of Quotes')
authors_graph.update_layout(xaxis_title='Author', yaxis_title='Number of Quotes')
authors_graph.show()

tags_graph = px.bar(top_tags_data_frame, x='Tag', y='Popularity', title='Top 10 Tags Based on Popularity')
tags_graph.update_layout(xaxis_title='Tag', yaxis_title='Popularity')
tags_graph.show()
