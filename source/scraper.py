from calendar import week
import requests
import lxml.html
import os
from datetime import datetime
import unicodedata

import csv_test as manage_csv

def log_in_txt(data):
    file = './activity_log.txt'
    if os.path.isfile(file):
        with open(file, 'a', encoding='UTF8') as file:
            file.write(data + '\n')
    else:
        with open(file, 'w', encoding='UTF8') as file:            
            file.write(data + '\n')

def get_json_page(page_num: int):
    url = 'https://disfrutemosba.com/api/search'

    payload = "{\"type_of_experiences\":[],\"kind_of_places\":[],\"min_price\":0,\"max_price\":3200,\"only_free\":1,\"dates\":[],\"moments\":[],\"districts\":[],\"only\":\"\",\"page\":" + str(page_num) + "}"
    headers = {'Content-Type':'application/json',
           'sec-ch-ua':'".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
           'Accept':'application/json, text/plain, */*',
           'sec-ch-ua-mobile':'?0',
           'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
           'sec-ch-ua-platform':'"Linux"'}

    response = requests.request("POST",url, headers=headers,data = payload)

    return response.json()

def get_places(page):
    dictionary_places = {}

    for place in page['kind_of_places']:
       dictionary_places[place['id']] = place['name']

    return dictionary_places

def get_dates(url):
    #to do caso donde tengan diferentes horarios por dia, como hacemos?
    #to do si no tiene horarios que valor ponemos? Eso capaz pasa en lugares como plazas donde son 24/7?
    #para mi si no tiene horario va vacio y listo
    response = requests.request("GET",url)
    formatting_response = lxml.html.fromstring(response.text)
    day_arr = []
    time_arr = []
    days = formatting_response.xpath("//ul[contains(@class,'howtoget')]/h4/following-sibling::li")

    for day in days:
        week_day = day.xpath(".//p[1]/text()")[0]
        day_time = day.xpath(".//p[2]/text()")[0]
        day_arr.append(week_day)
        time_arr.append(day_time)

    if not day_arr:
        day_arr = "NULL"
    else:
        day_arr_final = []
        for i in day_arr:
            day_arr_final.append(strip_accents(i))
        day_arr = set(day_arr_final)

    if not time_arr: 
        time_arr = "NULL"
    else:
        time_arr = set(time_arr)

    return day_arr,time_arr

def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def strip_accents(texto):
   return ''.join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn')


def get_activity(page, places):
    #ver que hacemos aca vio
    for activity in page['activities']['items']:
        activity_id = activity['id']
        print("Actividad con id: " + str(activity_id))
        log_in_txt("Actividad con id: " + str(activity_id))
        activty_name = strip_accents(activity['activity']['name'])
        activity_url = "https://disfrutemosba.buenosaires.gob.ar/lugares/" + activity['activity']['slug']
        dates = get_dates(activity_url)
        activity_date = dates[0]
        activity_times = dates[1]
        try:
            activity_place = strip_accents(places[int(activity['activity']['kind_of_place_id'])])
        except:
            try:
                activity_place = strip_accents(places[int(activity['activity']['places'][0]['kind_of_place_id'])])
            except:
                activity_place = "NULL"

        try:
            activity_district = strip_accents(activity['activity']['district']['name'])
        except:
            activity_district = "NULL"

        try:
            activity_address = strip_accents(activity['activity']['address'])
        except:
            activity_address = "NULL"

        activity_description = "NULL"
        for modules in activity['activity']['modules']:
            if modules['type'] == 'Paragraph':
                activity_description = strip_accents(remove_html_tags(modules['metadata'][0]['value']))
        #escribir en csv
        data_arr = [activity_id,activty_name,activity_url,activity_date,activity_times,activity_place,activity_district,activity_address,activity_description]
        manage_csv.write_csv(data_arr)

def push_csv_result():
    last_csv_path = manage_csv.get_last_csv()
    os.system("cd ../data; git add "+last_csv_path +"; git commit -m 'subo ultimo archivo csv generado' "+last_csv_path+";git push origin develop;")
    

def scrap_activities():
    print("Current date: " + str(datetime.now()))
    log_in_txt("Current date: " + str(datetime.now()) )
    print("Script currently in page: 1")
    log_in_txt("Script currently in page: 1")
    page = get_json_page(1)
    places = get_places(page)
    get_activity(page, places)
    lastPageNum = int(page['activities']['pagination']['last_page'])
    
    for pageNum in range(lastPageNum + 1):
        if pageNum > 1:
            print("Script currently in page: "+ str(pageNum))
            log_in_txt("Script currently in page: "+ str(pageNum))
            page = get_json_page(pageNum)
            get_activity(page, places)

    print("Finished")
    log_in_txt("Finished")

    push_csv_result()

scrap_activities()