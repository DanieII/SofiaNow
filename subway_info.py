import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By


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


def test(direction, station, line):
    result = BeautifulSoup(
        requests.get(f"https://schedules.sofiatraffic.bg/metro/{line}#sign/{direction}/{station}").content,
        "html.parser"
    )
    print(result.find("span", {"id": "schedule_10757_direction_4424_current_sign_name"}))
    times_information = result.find("div", {"class": "schedule_times"}).find("tbody").find_all("td")
    times = {}

    for time in times_information:
        times[time["data-cell"]] = time.text.split()

    return times


def get_station_schedule(direction, station, line):
    global driver
    if not driver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
    url = f"https://schedules.sofiatraffic.bg/metro/{line}#sign/{direction}/{station}"
    driver.get(url)
    element = driver.find_element(By.CLASS_NAME, "schedule_times").find_element(By.TAG_NAME, "tbody")
    div_element = driver.find_element(By.CLASS_NAME, "schedule_times")
    tbody_element = div_element.find_elements(By.TAG_NAME, "td")
    [print(x.text.strip()) for x in tbody_element]
    print("\n" * 10)
    driver.refresh()


def close_driver():
    global driver
    driver.close()
    driver = None


class WebDriver:

    def __init__(self):
        self.driver: webdriver.Chrome = None
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.url = "https://schedules.sofiatraffic.bg/metro/"

    @staticmethod
    def merge_link(base, *args):
        line, *rest = args
        fragment = ""
        if rest:
            fragment = "#direction/" + "/".join(rest)
        return base + line + fragment

    @staticmethod
    def get_soup(url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        return soup

    def get_directions(self, line):
        soup = self.get_soup(self.merge_link(self.url, line))
        directions_information = soup.find("ul", {"class": "schedule_view_direction_tabs"}).find_all("li")
        directions = {}
        link_pattern = r"(.*)\/([0-9]+)"

        for information in directions_information:
            current_direction = information.find("a")
            direction_id = re.match(link_pattern, current_direction["href"]).group(2)
            directions[current_direction.find("span").text] = direction_id

        return directions

    def get_stations(self, line, direction):
        self.driver = webdriver.Chrome(options=self.options)
        url = self.merge_link(self.url, line, direction)
        self.driver.get(url)
        stations_information = self.driver.find_element(By.CLASS_NAME, "schedule_direction_sign_wrapper").find_elements(
            By.TAG_NAME, "li")
        pattern = r"(.*)#([0-9]+)"
        stations = {}

        for station in stations_information:
            station_id = re.match(pattern,
                                  station.find_element(By.CLASS_NAME, "stop_link").get_attribute("href")).group(2)
            station_name = station.find_element(By.CLASS_NAME, "stop_change").get_attribute("text")
            stations[station_name] = station_id

        self.driver.close()
        return stations
