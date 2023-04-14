import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

all_stations = json.loads(requests.get("https://routes.sofiatraffic.bg/resources/stops-bg.json").text)
subway_stations = list(filter(lambda x: "метро" in x["n"].lower(), all_stations))
direction_ids_for_server = {
    "M1-M2": "8451",
    "M3": "10757"
}


def get_directions(line):
    soup = BeautifulSoup(requests.get(f"https://schedules.sofiatraffic.bg/metro/{line}").content, "html.parser")
    directions_information = soup.find("ul", {"class": "schedule_view_direction_tabs"}).find_all("li")
    directions = {}
    link_pattern = r"(.*)\/([0-9]+)"

    for information in directions_information:
        current_direction = information.find("a")
        direction_id = re.match(link_pattern, current_direction["href"]).group(2)
        directions[current_direction.find("span").text] = direction_id

    return directions


def get_stations_with_times(line, direction):
    stations = {}
    # used = [{'y': 42.70209, 'n': 'МЕТРОСТАНЦИЯ ХАДЖИ ДИМИТЪР', 'm': 1, 'x': 23.351575, 'c': '3309'}, {'y': 42.697181, 'n': 'МЕТРОСТАНЦИЯ ТЕАТРАЛНА', 'm': 1, 'x': 23.346866, 'c': '3311'}, {'y': 42.69055, 'n': 'МЕТРОСТАНЦИЯ ОРЛОВ МОСТ', 'm': 1, 'x': 23.33622, 'c': '3315'}, {'y': 42.688237, 'n': 'МЕТРОСТАНЦИЯ СВ. ПАТРИАРХ ЕВТИМИЙ', 'm': 1, 'x': 23.327664, 'c': '3317'}, {'y': 42.689121, 'n': 'МЕТРОСТАНЦИЯ НДК 2', 'm': 1, 'x': 23.318026, 'c': '3319'}, {'y': 42.686537, 'n': 'МЕТРОСТАНЦИЯ МЕДИЦИНСКИ УНИВЕРСИТЕТ', 'm': 1, 'x': 23.30932, 'c': '3321'}, {'y': 42.679241, 'n': 'МЕТРОСТАНЦИЯ БУЛ. БЪЛГАРИЯ', 'm': 1, 'x': 23.300988, 'c': '3323'}, {'y': 42.679228, 'n': 'МЕТРОСТАНЦИЯ ЦАР БОРИС III / КРАСНО СЕЛО', 'm': 1, 'x': 23.284366, 'c': '3327'}, {'y': 42.682777, 'n': 'МЕТРОСТАНЦИЯ ОВЧА КУПЕЛ', 'm': 1, 'x': 23.270943, 'c': '3329'}, {'y': 42.683968, 'n': 'МЕТРОСТАНЦИЯ МИЗИЯ / НБУ', 'm': 1, 'x': 23.257033, 'c': '3331'}, {'y': 42.684747, 'n': 'МЕТРОСТАНЦИЯ ОВЧА КУПЕЛ II', 'm': 1, 'x': 23.247822, 'c': '3333'}, {'y': 42.684117, 'n': 'МЕТРОСТАНЦИЯ ГОРНА БАНЯ', 'm': 1, 'x': 23.242672, 'c': '3335'}]
    # subway_stations[60:]
    for s in subway_stations[60:]:
        res = requests.get(
            f"https://schedules.sofiatraffic.bg/server/html/schedule_load/{direction_ids_for_server[line]}/{direction}/{s['c']}")
        soup = BeautifulSoup(res.content, "html.parser")
        if soup.text:
            all_arrivals = soup.find("div", {"class": "schedule_times"}).find_all("td")
            current_hour = str(datetime.now().hour)
            current_cell = next(filter(lambda x: x["data-cell"] == current_hour, all_arrivals))
            next_cell = current_cell.next_sibling.next_sibling
            stations[s["n"]] = {
                current_cell["data-cell"]: [t.text for t in current_cell.find_all("a")],
                next_cell["data-cell"]: [t.text for t in next_cell.find_all("a")]
            }
    print(stations)


get_stations_with_times("M3", "4425")
