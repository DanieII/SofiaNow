from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

all_stations = requests.get("https://routes.sofiatraffic.bg/resources/stops-bg.json").json()
subway_stations = list(filter(lambda x: "метро" in x["n"].lower(), all_stations))
soup = BeautifulSoup(requests.get("https://schedules.sofiatraffic.bg/metro/M1-M2").content, "html.parser")
active_list = soup.find("ul", {"class": "schedule_active_list_tabs"}).find_all("li")
workday = False
for i, option in enumerate(active_list, 1):
    if "schedule_active_list_active_tab" in option.find("a")["class"]:
        if i == 1:
            workday = True
if workday:
    direction_ids_for_server = {
        "M1-M2": "8451",
        "M3": "10757"
    }
else:
    direction_ids_for_server = {
        "M1-M2": "11349",
        "M3": "10758"
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

    # Roughly where the stations are. May not work if new stations are added in the json file
    # If this happens this block of code should be removed and all stations should be checked with a request(this will be too slow)
    if line == "M1-M2":
        current_subway_stations = subway_stations[len(subway_stations) - 100:len(subway_stations) - 30]

    elif line == "M3":
        current_subway_stations = subway_stations[len(subway_stations) - 30:]

    session = requests.Session()
    for s in current_subway_stations:
        res = session.get(
            f"https://schedules.sofiatraffic.bg/server/html/schedule_load/{direction_ids_for_server[line]}/{direction}/{s['c']}")
        if res.content:
            soup = BeautifulSoup(res.content, "html.parser")

            all_arrivals = soup.find("div", {"class": "schedule_times"}).find_all("td")
            current_hour = str(datetime.now().hour)

            current_cell_hour = f"Няма курсове за {current_hour}"
            current_cell_arrivals = []

            next_cell_hour = f"Няма курсове за {(int(current_hour) + 1) % 24}"
            next_cell_arrivals = []

            if 4 <= int(current_hour) <= 23 or current_hour == "0":
                current_cell = next(filter(lambda x: x["data-cell"] == current_hour, all_arrivals))

                if current_cell.find("a"):
                    current_cell_hour = current_cell["data-cell"]
                    current_cell_arrivals = [t.text for t in current_cell.find_all("a")]

                next_cell = current_cell.next_sibling.next_sibling

                if next_cell:
                    if next_cell.find("a"):
                        next_cell_hour = next_cell["data-cell"]
                        next_cell_arrivals = [t.text for t in next_cell.find_all("a")]

            elif current_hour == "3":
                cell_4_am = next(filter(lambda x: x["data-cell"] == "4", all_arrivals))
                if cell_4_am.find("a"):
                    next_cell_hour = cell_4_am["data-cell"]
                    next_cell_arrivals = [t.text for t in cell_4_am.find_all("a")]

            stations[s["n"]] = {
                current_cell_hour: current_cell_arrivals,
                next_cell_hour: next_cell_arrivals
            }

    session.close()
    return stations
