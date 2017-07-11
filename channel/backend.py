import simplejson as json
import wikipedia
from bs4 import BeautifulSoup
import urllib3
import re
import codecs

from channel.models import Season, Series, Video, Channel

def get_all_data(show_title, year=0):

    http = urllib3.PoolManager()

    api_url = "http://netflixroulette.net/api/api.php?"
    title = show_title
    title = title.replace(" ", "%20")
    url = "%stitle=%s&year=%d" % (api_url, title, year)
    response = http.request('GET', url)
    payload = json.loads(response.data)
    if 'error' not in payload:
        return payload
    else:
        return 'Unable to locate data'

def find_wiki_url(title):

    query_text = 'List of %s episodes' % (title)

    query = wikipedia.search(query_text)

    print(query)

    for i in query:

        if i == query_text:

            page_title = i

            print(page_title)

            try:

                page = wikipedia.page(page_title)

                page_url = page.url

                print(page_url)

                return page_url

            except:

                print("can't find page url")

        else:

            return None

def get_season_list(url):

    span_list = []

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    soup = BeautifulSoup(response.data)

    page_h3s = soup.find_all('h3')

    i = 0

    for item in page_h3s:

        span_info = str(item.span)

        if "Season" in span_info:

            i = i + 1

            season_number = i

            season_id = item.span.get('id')

            span_list.append([season_number,season_id])

    return span_list

def get_episode_list(url, season_list):

    episode_list = []

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    soup = BeautifulSoup(response.data)

    for season in season_list:
        season_id = str(season[1])
        season_span = soup.find(id=season_id)

        season_num = season[0]

        season_table = season_span.find_next('table')

        episodes = season_table.find_all('tr')

        for episode in episodes[1:]:

                series_episode_number = episode.find_next("th").get_text()
                season_episode_number = episode.find_next("td")
                episode_name = season_episode_number.find_next("td").get_text()

                episode_list.append([season_num, series_episode_number, episode_name])

    return episode_list

def get_netflix_show_data(show_id):

    url = "https://www.netflix.com/title/%s" % (show_id)

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    soup = BeautifulSoup(response.data,"html.parser")

    title = soup.find('h1',class_="show-title").text
    descrip = soup.find('p',class_="synopsis").text

    return [title,descrip]

def get_netflix_episodes(show_id):

    url = "https://www.netflix.com/title/%s" % (show_id)

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    soup = BeautifulSoup(response.data,"html.parser")

    scripts = soup.find_all('script')

    raw_text_list = []

    for script in scripts:

        script_text = str(script)

        if "window.netflix = window.netflix || {} ;         netflix.reactContext =" in script_text:

            pattern = r'"episodeId".*?"artwork"'
            regex = re.compile(pattern, re.IGNORECASE)

            i = 0

            for match in regex.finditer(script_text):

                match_item = match.group()
                patt2 = r',"artwork"'
                match_clean2 = re.sub(patt2 , '}',match_item)

                if i == 0:

                    match_clean2 = '{' + match_clean2

                else:

                    i+= 1

                clean_text = codecs.getdecoder("unicode_escape")(match_clean2)[0]

                raw_text_list.append(clean_text)

    return raw_text_list

def get_netflix_ep_data(json_item):


    j = json.loads(json_item)

    episodeTitle = j['title']
    episodeNum = j['episodeNum']
    episodeId = j['episodeId']
    episodeDescription = j['synopsis']
    seasonName = j['seasonInfo']['seasonName']
    seasonNum = j['seasonInfo']['num']
    seasonId = j['seasonInfo']['seasonId']
    seasonDescription = j['seasonInfo']['synopsis']

    try:
        year = j['year']
    except:
        year = None
    try:
        runtime = j['runtime']
    except:
        runtime = None

    return [episodeTitle, episodeId, episodeNum, episodeDescription, year, runtime, seasonName, seasonNum, seasonId, seasonDescription]
