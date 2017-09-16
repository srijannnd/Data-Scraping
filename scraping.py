import requests
from bs4 import BeautifulSoup
import json

tour_dict = {}
tour_links = []
tour_title = []
tour_info = []

# Getting All tour Links######

url = "http://www.trodly.com/"
source_code = requests.get(url)
plain_text = source_code.content
soup = BeautifulSoup(plain_text, "lxml")
titles = soup.findAll('div', {'class':  'activity_bottom_title act_bot_title_home'})
for title in titles:
    title = title.findAll('a')
    for t in title:
        t = t.get('href')
        t = 'http://www.trodly.com' + t
        tour_links.append(t)
# --------------------------------------------

# Getting everything from tour links
for url in tour_links:
    get_url = requests.get(url)

    # Titles/headings

    get_text = get_url.text
    soup = BeautifulSoup(get_text, "html.parser")
    heading = soup.select('h1')[0].text.strip()
    tour_title.append(heading)
# ---------------------------------------------

    # Price

    price = soup.findAll('div', {'class': 'booking-block-header'})
    for p in price:
        p = p.find('b').text.strip()

# --------------------------------------------

    # Info
    info = soup.findAll('div', {'class':  'activity-detail-block col-md-3 col-sm-4 col-xs-6'})
    x = {'start-point': None, 'grade': None, 'duration': None, 'finish-point': None, 'group-size': None,
         'trip-code': None, 'language': None, 'experience-type': None, 'price': None}
    info_title = soup.findAll('div', {'class':  'activity-detail-block col-md-3 col-sm-4 col-xs-6'})
    info_main = soup.findAll('div', {'class':  'activity-detail-block col-md-3 col-sm-4 col-xs-6'})
    info1 = [None for i in range(len(info))]
    info_main1 = [None for i in range(len(info))]
    info_title1 = [None for i in range(len(info))]

    for i in range(len(info)):
        info_title1[i] = info_title[i].find('span').text.strip()
        info_main1[i] = info_main[i].find('b').text.strip()
        if info_title1[i] == 'Duration':
            x['duration'] = info_main1[i]
        elif info_title1[i] == 'Start Point':
            x['start-point'] = info_main1[i]
        elif info_title1[i] == 'Finish Point':
            x['finish-point'] = info_main1[i]
        elif info_title1[i] == 'Experience Type':
            x['experience-type'] = info_main1[i]
        elif info_title1[i] == 'Trip Code':
            x['trip-code'] = info_main1[i]
        elif info_title1[i] == 'Group Size':
            x['group-size'] = info_main1[i]
        elif info_title1[i] == 'Language':
            x['language'] = info_main1[i]
        elif info_title1[i] == 'Grade':
            x['grade'] = info_main1[i]

    # adding price to tour_info list

    x['price'] = p
    tour_info.append(x)

# making tour_dict by adding tour_title as key and tour_info as value
for i in range(len(tour_links)):
    tour_dict.update({tour_title[i]: {'info': tour_info[i]}})

# saving tour_dict as json file
with open('result.json', 'w') as fp:
    json.dump(tour_dict, fp)
