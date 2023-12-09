from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

tags = []
diction = {}
quotes = {}
len_quotes = {}
val = 1

for values in range(10):
    url = f'http://quotes.toscrape.com/page/{str(val)}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = Request(url, headers=headers)
    webpage = urlopen(request).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    counter = 0

    for values in range(10):
        quote = soup.findAll("span", attrs={"class": "text"})
        quote_text = quote[counter].text
        next_quote = quote[counter].text.replace('.', '').replace(',', '').replace(u"\u201C", "").replace(u"\u201D", "")

        author_data = soup.findAll("small", attrs={"class": "author"})
        author = author_data[counter].text

        tag = soup.findAll("div", attrs={"class": "tags"})
        next_tag = tag[counter].text.replace("Tags:", "")
        tags.extend(next_tag.split())
        len_quotes[quote_text] = [len(quote_text)]
        counter += 1
        if author in quotes:
            quotes[author].append(next_quote)
        else:
            quotes[author] = [next_quote]


for tag in tags:
    if tag in diction:
        diction[tag] += 1
    else:
        diction[tag] = 1

highest_count = max(diction.values())
most_popular_tag = [word for word, count in diction.items() if count == highest_count]
quote_count = {author: len(quotes) for author, quotes in quotes.items()}
most_quotes = max(quote_count, key=quote_count.get)
least_quotes = min(quote_count, key=quote_count.get)
total_length = sum(length[0] for length in len_quotes.values())
num_quotes = len(len_quotes)
avgquot_length = round(total_length / num_quotes)
longest_quote = max(len_quotes, key=lambda quote: len_quotes[quote][0])
shortest_quote = min(len_quotes, key=lambda quote: len_quotes[quote][0])

print(f'\nAUTHORS')
for a_name, q_value in quote_count.items():
    print(f'\nAuthor: {a_name}')
    print(f'Quote Count: {q_value}')
print(f'\nThe author with the most amount of quotes:\n{most_quotes}')
print(f'\nThe authors with the least amount of quotes:')

for author_name in least_quotes:
    print(author_name)

print(f'\nQUOTES')
print(f'\nAverage Quote Length:\n{avgquot_length}')
print(f'\nLongest Quote:\n{longest_quote}')
print(f'\nShortest Quote:\n{shortest_quote}')

print(f'\nTAGS DATA')
print(f'\nThe tag that is most used is:\n{(str(most_popular_tag[0])).title()}')
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
