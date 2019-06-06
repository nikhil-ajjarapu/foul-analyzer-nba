from bs4 import BeautifulSoup
import requests

def getAllPlays(year, team):

    #access team schedule
    schedule_url = "https://www.basketball-reference.com/teams/" + team + "/" + str(year) + "_games.html"
    schedule_soup = BeautifulSoup(requests.get(schedule_url).text, "html.parser")
    table = schedule_soup.find_all("td", attrs={"data-stat":"box_score_text"})

    #get all urls to every play-by-play log for each game in season
    boxscore_urls = []
    for elem in table:
        elems = elem.a.get('href').split('/')
        temp_url = "https://www.basketball-reference.com/" + elems[1] + "/pbp/" + elems[2]
        boxscore_urls.append(temp_url)

    #get all plays
    play_strings = []
    for (count, url) in enumerate(boxscore_urls):
        url_soup = BeautifulSoup(requests.get(url).text, "html.parser")
        try:
            play_table = url_soup.find_all("table", attrs={"data-cols-to-freeze":"1"})[0]
        except:
            continue
        temp_strings = [elem.text for elem in play_table.find_all('td')]
        for temp_string in temp_strings:
            if temp_string != '\xa0' and any(c.isalpha() for c in temp_string):
                play_strings.append(temp_string)
        play_strings.append("END OF GAME")
        print("Analyzed game #" + str(count + 1) + "...")
        #if count == 0:
            #break
    return play_strings
