# pip install requests (to be able to get HTML pages and load them into Python)
# pip install bs4 (for beautifulsoup - python tool to parse HTML)


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

import csv

##############FOR MACS THAT HAVE ERRORS LOOK HERE################
## https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/

############## ALTERNATIVELY IF PASSWORD IS AN ISSUE FOR MAC USERS ########################
##  > cd "/Applications/Python 3.6/"
##  > sudo "./Install Certificates.command"




url = 'https://registrar.web.baylor.edu/exams-grading/fall-2023-final-exam-schedule'
# Request in case 404 Forbidden error
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req =  Request(url, headers = headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

tables = soup.findAll('table')

finals_table = tables[1]

tr = finals_table.findAll('tr')

infile = open('myclasses.csv', 'r')

csv_file = csv.reader(infile)

for rec in csv_file:
    myclass = rec[0]
    mytime = rec[2]


    for row in tr:
        td = row.findAll('td')
        if td:
            sch_class = td[0].text
            sch_time = td[1].text
            exam_day = td[2].text
            exam_time = td[3].text
        
            if sch_class == myclass and sch_time == mytime:
                print(myclass, mytime, exam_day, exam_time)