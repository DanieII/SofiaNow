import requests
from bs4 import BeautifulSoup
import re

html = requests.get("https://schedules.sofiatraffic.bg/metro/M3")
soup = BeautifulSoup(html.content, "html.parser")


def get_directions():
    directions_information = soup.find("ul", {"class": "schedule_view_direction_tabs"}).find_all("li")
    directions = {}
    link_pattern = r"(.*)\/([0-9]+)"

    for information in directions_information:
        current_direction = information.find("a")
        direction_id = re.match(link_pattern, current_direction["href"]).group(2)
        directions[current_direction.find("span").text] = direction_id

    return directions


def get_stations():
    stations_information = soup.find("div", {"class": "schedule_direction_sign_wrapper"}).find("ul").find_all("li")
    stations = {}

    for i in stations_information:
        station_id, *station_name = i.text.split()
        stations[" ".join(station_name)] = station_id

    return stations


def get_station_schedule(direction, station):
    result = BeautifulSoup(requests.get(f"https://schedules.sofiatraffic.bg/metro/M3#sign/{direction}/{station}").content, "html.parser")
    times_information = result.find("div", {"class": "schedule_times"}).find("tbody").find_all("td")
    times = {}

    for time in times_information:
        times[time["data-cell"]] = time.text.split()

    return times
