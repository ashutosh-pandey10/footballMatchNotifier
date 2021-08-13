import requests, urllib
from constants import TEAM_ID
from config import *
import datetime, time
import notify2


def get_team_id(team_name):
    return TEAM_ID[team_name]


def _generate_url(action, query_params=None):
    """
    Generates a URL for the given action, with optional query parameters
    that can be used to filter the response.
    """
    if query_params:
        query_params = urllib.parse.urlencode(query_params)
        action = f"{action}?{query_params}"
        

    url = urllib.parse.urljoin(api_url, action)

    return url

def get_fixtures(team, dateFrom=None, dateTo=None, status=None, venue=None, limit=None):
    """
    Returns a json of the fixtures for a team.
    """
    query_params = {}
    if dateFrom:
        query_params['dateFrom'] = dateFrom
    if dateTo:
        query_params['dateTo'] = dateTo
    if status:
        query_params['status'] = status
    else:
        query_params['status'] = 'SCHEDULED'            
    if venue:
        query_params['venue'] = venue
    if limit :
        query_params['limit'] = limit  
        
    url = _generate_url(f"teams/{team}/matches", query_params)
    fixtures = requests.get(url, headers=headers).json()
    
    return fixtures

#time.sleep(30)

# Setup various variables. 
api_url = 'http://api.football-data.org/v2/'
headers = {"X-Auth-Token": api_key}
team_id = get_team_id(team_name)

# Desktop Notifier
notify2.init("Football Fixtures")

while True:
    current_date = datetime.date.today() 
    next_date = current_date + datetime.timedelta(days=timeframe)

    fixtures = get_fixtures(team_id, current_date, next_date)
    
    i=0
    while(i<len(fixtures["matches"])):
        matches = ""
        # print(fixtures["matches"][i]["homeTeam"]["name"]+"(Home)" + " vs " + fixtures["matches"][i]["awayTeam"]["name"]+"(Away)")
        title = fixtures["matches"][i]["homeTeam"]["name"]+"(Home)" + " vs " + fixtures["matches"][i]["awayTeam"]["name"]+"(Away)\n"
        
        # print(fixtures["matches"][i]["competition"]["name"]+", "+fixtures["matches"][i]["competition"]["area"]["name"])
        matches = matches + fixtures["matches"][i]["competition"]["name"]+", "+fixtures["matches"][i]["competition"]["area"]["name"]+"\n"

        # print("Date(yyyy-mm-dd) : " + fixtures["matches"][i]["utcDate"])
        matches = matches+"Date: " + fixtures["matches"][i]["utcDate"]+"\n\n"
        # print()
        i+=1

        # Send the notification/s.
        n=notify2.Notification(title, matches, icon = "/home/mouse10/football-api/real.png")
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.set_timeout(1000) 
        n.show()
        time.sleep(1)

    if(len(fixtures["matches"])==0):
        message_alert = "No upcoming fixtures in the next {} days. ;(".format(timeframe)
        n=notify2.Notification(message_alert, '', icon = "/home/mouse10/football-api/real.png")
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.set_timeout(1000) 
        n.show()
        time.sleep(1)
    
    time.sleep(86400)
