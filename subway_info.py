import requests
from bs4 import BeautifulSoup
import re


def get_line_soup(line):
    html = requests.get(f"https://schedules.sofiatraffic.bg/metro/{line}")
    soup = BeautifulSoup(html.content, "html.parser")
    return soup


def get_directions(line):
    soup = get_line_soup(line)
    directions_information = soup.find("ul", {"class": "schedule_view_direction_tabs"}).find_all("li")
    directions = {}
    link_pattern = r"(.*)\/([0-9]+)"

    for information in directions_information:
        current_direction = information.find("a")
        direction_id = re.match(link_pattern, current_direction["href"]).group(2)
        directions[current_direction.find("span").text] = direction_id

    return directions


def get_stations(line):
    soup = get_line_soup(line)
    stations_information = soup.find("div", {"class": "schedule_direction_sign_wrapper"}).find("ul").find_all("li")
    stations = {}

    for i in stations_information:
        station_id, *station_name = i.text.split()
        stations[" ".join(station_name)] = station_id

    return stations


def get_station_schedule(direction, station, line):
    result = BeautifulSoup(
        requests.get(f"https://schedules.sofiatraffic.bg/metro/{line}#sign/{direction}/{station}").content, "html.parser"
    )
    times_information = result.find("div", {"class": "schedule_times"}).find("tbody").find_all("td")
    times = {}

    for time in times_information:
        times[time["data-cell"]] = time.text.split()

    return times
