from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

tags = []
diction = {}
quotes = {}
quote_len = {}
value = 1

for values in range(10):
    url = f'http://quotes.toscrape.com/page/{str(value)}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = Request(url, headers=headers)
    webpage = urlopen(request).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    counter = 0

    for new_quotes in range(10):
        # Quotes
        quote_raw = soup.findAll("span", attrs={"class": "text"})
        quote_raw_text = quote_raw[counter].text
        new_quote = quote_raw[counter].text.replace('.', '').replace(',', '').replace(u"\u201C", "").replace(u"\u201D", "")

        # Authors
        author_raw = soup.findAll("small", attrs={"class": "author"})
        author = author_raw[counter].text

        # Tags
        tag = soup.findAll("div", attrs={"class": "tags"})
        new_tag = tag[counter].text.replace("Tags:", "")
        tags.extend(new_tag.split())

        # Find quote length and put in dictionary
        quote_len[quote_raw_text] = [len(quote_raw_text)]

        counter += 1

        if author in quotes:
            quotes[author].append(new_quote)
        else:
            quotes[author] = [new_quote]

for tag_item in tags:
    if tag_item in diction:
        diction[tag_item] += 1
    else:
        diction[tag_item] = 1

max_count = max(diction.values())
most_popular_tag = [word for word, count in diction.items() if count == max_count]
quote_count = {author: len(quotes) for author, quotes in quotes.items()}
most_quotes_author = max(quote_count, key=quote_count.get)
least_quotes_author = min(quote_count, key=quote_count.get)
total_length = sum(length[0] for length in quote_len.values())
num_quotes = len(quote_len)
average_length = round(total_length / num_quotes)
longest_quote = max(quote_len, key=lambda quote: quote_len[quote][0])
shortest_quote = min(quote_len, key=lambda quote: quote_len[quote][0])

print(f'\n--AUTHOR STATISTICS--')
for k_name, v_value in quote_count.items():
    print(f'\nAuthor: {k_name}')
    print(f'Quote Count: {v_value}')

print(f'\nThe author(s) with most amount of quotes:\n{most_quotes_author}')
print(f'\nThe authors(s) with the least amount of quotes:')

for author_name in least_quotes_author:
    print(author_name)

print(f'\n--QUOTE ANALYSIS--')
print(f'\nAverage Quote Length:\n{average_length}')
print(f'\nLongest Quote:\n{longest_quote}')
print(f'\nShortest Quote:\n{shortest_quote}')

print(f'\n--TAG ANALYSIS--')
print(f'\nThe most popular tag is:\n{(str(most_popular_tag[0])).title()}')
print(f'\nNumber of total tags used:\n{len(tags)}\n')

authors_data_frame = sorted(quote_count.items(), key=lambda x_value: x_value[1], reverse=True)[:10]
authors_frame = pd.DataFrame(authors_data_frame, columns=['Author', 'Number of Quotes'])
top_tags_frame = sorted(diction.items(), key=lambda x_value: x_value[1], reverse=True)[:10]
top_tags_data_frame = pd.DataFrame(top_tags_frame, columns=['Tag', 'Popularity'])

author_graph = px.bar(authors_frame, x='Author', y='Number of Quotes', title='Top 10 Authors and Their Corresponding Number of Quotes')
author_graph.update_layout(xaxis_title='Author', yaxis_title='Number of Quotes')
author_graph.show()

tag_graph = px.bar(top_tags_data_frame, x='Tag', y='Popularity', title='Top 10 Tags Based on Popularity')
tag_graph.update_layout(xaxis_title='Tag', yaxis_title='Popularity')
tag_graph.show()
