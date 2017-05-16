# import libraries
import json
import urllib2
from bs4 import BeautifulSoup

base_link = "http://www.publicwhip.org.uk/"

# specify the url
list_of_mps_page = 'https://web.archive.org/web/20161019053339/http://www.publicwhip.org.uk/mps.php'
page = urllib2.urlopen(list_of_mps_page)
soup = BeautifulSoup(page, 'html.parser')
table = soup.find('table', attrs={'class': 'mps'})
test = table.text.strip() # strip() is used to remove starting and trailing

counter = 0
mps = []
for row in table.findAll('tr'):
    if 'headings' not in row.attrs['class']:
        mp = []
        mp_link = base_link + row.find('a').attrs['href']
        mp_name = row.findAll('td')[0].text
        mp_party = row.findAll('td')[2].text

        mp_policy_table = []
        policy_page_request = urllib2.Request('http://www.publicwhip.org.uk/mp.php?mpn=Diane_Abbott&mpc=Hackney_North_and_Stoke_Newington&house=commons', headers={'User-Agent' : "Magic Browser"})
        policy_page = urllib2.urlopen(policy_page_request)
        policy_page_dom = BeautifulSoup(policy_page, 'html.parser')
        policy_table_node = policy_page_dom.find('table', attrs={'class': 'mps'})
        
        for row in policy_table_node.findAll('tr'):
            mp_policy_table_row = []
            if 'headings' not in row.attrs['class']:
                mp_policy_table_row.append(row.findAll('td')[1].text)
                mp_policy_table_row.append(row.findAll('td')[0].text)
                mp_policy_table.append(mp_policy_table_row)

        mp.append(mp_link)
        mp.append(mp_name)
        mp.append(mp_party)
        mp.append(mp_policy_table)
        mps.append(mp)
        counter = counter + 1
        print counter 
        print mp_name

with open('data.txt', 'w') as outfile:
    json.dump(mps, outfile)
