import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

all_stations = json.loads(requests.get("https://routes.sofiatraffic.bg/resources/stops-bg.json").text)
subway_stations = list(filter(lambda x: "метро" in x["n"].lower(), all_stations))
even_day = (datetime.today().weekday() + 1) % 2 == 0
if even_day:
    direction_ids_for_server = {
        "M1-M2": "11349",
        "M3": "10758"
    }
else:
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


def get_stations_with_arrivals(line, direction):
    stations = {}

    if line == "M1-M2":
        if direction == "2666" or direction == "2668":
            line_range = range(77, 147, 2)
        elif direction == "2667" or direction == "2669":
            line_range = range(78, 147, 2)

    elif line == "M3":
        if direction == "4424":
            line_range = range(148, 171, 2)
        elif direction == "4425":
            line_range = range(147, 171, 2)

    current_subway_stations = []
    for station in subway_stations:
        if subway_stations.index(station) in line_range:
            current_subway_stations.append(station)

    for s in current_subway_stations:
        res = requests.get(
            f"https://schedules.sofiatraffic.bg/server/html/schedule_load/{direction_ids_for_server[line]}/{direction}/{s['c']}")
        if res.content:
            soup = BeautifulSoup(res.content, "html.parser")

            all_arrivals = soup.find("div", {"class": "schedule_times"}).find_all("td")
            current_hour = str(datetime.now().hour)

            current_cell = next(filter(lambda x: x["data-cell"] == current_hour, all_arrivals))
            current_cell_hour = current_cell["data-cell"] if current_cell else f"No arrivals for {current_hour}"
            if current_cell:
                current_cell_arrivals = [t.text for t in current_cell.find_all("a")]
            else:
                current_cell_arrivals = []

            next_cell = current_cell.next_sibling.next_sibling
            next_cell_hour = next_cell["data-cell"] if next_cell else f"No arrivals for {int(current_hour) + 1}"
            if next_cell:
                next_cell_arrivals = [t.text for t in next_cell.find_all("a")]
            else:
                next_cell_arrivals = []

            stations[s["n"]] = {
                current_cell_hour: current_cell_arrivals,
                next_cell_hour: next_cell_arrivals
            }

    return stations
