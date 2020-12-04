import json
import requests
from uk_covid19 import Cov19API
from flask import Markup

"""This module fetches all the info from the APIs
and builds usable text for the HTML and tts"""

#Config.json fetcher.
def config_fetcher(info):
    """This varible will return info asssociated
    with its arguments"""
    with open('config.json') as json_file:
        data = json.load(json_file)
        new_info = data[str(info)]
    return new_info

def covid_fetch():
    """This function fetches the data from the COVID API as a dictionary"""
    #Sets the structure of the data retrieved from the API
    cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeathsByDeathDate": "newDeathsByDeathDate",
    "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }
    #Sets the filter for the API using config.json
    covid_nation = ['areaType=nation']
    nation = 'areaName=' + str(config_fetcher("covid_region"))
    covid_nation.append(nation)

    #Gets API latest data
    covid_api = Cov19API(
                filters = covid_nation,
                structure = cases_and_deaths,
                )
    #Gets data in form of dictionary
    covid_json = covid_api.get_json()
    #Gets timestamp for last update
    covid_timestamp = covid_api.last_update
    #Assign data to variables
    covid_data = covid_json['data'] #This formats the data as a list, while I want a dictionary, hence the next line.
    return covid_data

def covid_handle(covid_data):
    """This function creates global varibales containing COVID
    data from today and yesterday in order to create daily briefings"""
    global areaName, newCasesToday, cumCasesToday, newCasesYesterday, cumDeathsYesterday, newDeathsYesterday
    #Create dictionary for all COVID data from today
    covid_today = covid_data[0]
    #Create dictionary for all COVID data from yesterday
    covid_yesterday = covid_data[1]
    #Assigns the data to the variables
    areaName = covid_today['areaName']
    newCasesToday = covid_today['newCasesByPublishDate']
    cumCasesToday = covid_today['cumCasesByPublishDate']
    newCasesYesterday = covid_yesterday['newCasesByPublishDate']
    cumDeathsYesterday = covid_yesterday['cumDeathsByDeathDate']
    newDeathsYesterday = covid_yesterday['newDeathsByDeathDate']
    return

def covid_daily():
    """This function creates the daily COVID breifing based
    on the varibles from the function covid_handle"""
    #Fetches data from API and creates global varibles
    covid_handle(covid_fetch())
    #Creates a daily breifing using varibles
    covid_daily_news = (f"The number of new cases in {areaName} \
today is: {newCasesToday}. Bringing the \
cumulative number of cases to: {cumCasesToday}. \nThe number of deaths yesterday were {newDeathsYesterday}, \
leaving the cummulative number of deaths in {areaName} at {cumDeathsYesterday}.")
    return covid_daily_news

def covid_emergency():
    """This function creates an emergency breifing based
    on data comparaisons between varibles from covid_handle"""
    #Fetches data from API and creates global varibles
    covid_handle(covid_fetch())
    #Creates emergency breifing only if new cases are higher today than yesterday
    if int(newCasesYesterday) <= int(newCasesToday):
        difference = int(newCasesToday) - int(newCasesYesterday)
        covid_emergency_news = (f"The number of new COVID-19 cases today in {areaName} \
today was higher than yesterday by {difference}. The cumulative death toll as \
of yesterday is: {cumDeathsYesterday}.")
        return covid_emergency_news
    else:
        return None

def weather_fetch(city, weather_key):
    """This function fetches the data from the weather"""
    #Allows for customizable API key and weather location.
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    city = str(city)
    key = str("&appid=" + weather_key + "&units=metric")
    complete_url = base_url + city + key
    #Gets API with requests and convert to .json
    weather_api = requests.get(complete_url)
    weather_json = weather_api.json()
    return weather_json

def weather_handle(weather_json):
    """This function creates global varibales containing weather
    data from today in order to create daily briefings"""
    #Sets all the variables to global space to be used later.
    global weather_description, current_temp, feels_like, min_temp, max_temp
    #Handles data from API and assigns data to variables.
    weather_weather = weather_json['weather']
    weather_weather = weather_weather[0] #Fixes formatting issue.
    weather_main = weather_json['main']
    weather_description = weather_weather['description']
    current_temp = weather_main['temp']
    feels_like = weather_main['feels_like']
    min_temp = weather_main['temp_min']
    max_temp = weather_main['temp_max']
    return

def weather_daily():
    """This function creates the daily weather breifing based
    on the varibles from the function weather_handle"""
    #Fetches data from API and creates global varibles.
    weather_handle(weather_fetch(config_fetcher('weather_city'), config_fetcher('weather_key')))
    #Creates a message that changes based on the temperature.
    if int(current_temp) <= 15:
        variable_message = "You better grab a coat!"
    #Searches for r'ain' in weather_description, without capilization.
    elif 'ain' in weather_description:
        variable_message = "Pick your favourite umbrella. You deserve it!"
    else:
        variable_message = "I'd probably wear a t-shirt if I were you..."
    #Creates a daily breifing using varibles.
    weather_daily_text = (f"It's {current_temp}°C right now, but it feels \
more like {feels_like}°C. \nThe warmest it'll be is {max_temp}°C, and the coldest \
it'll be is {min_temp}°C. One could describe the weather as {weather_description}.\
\n{variable_message}")
    return weather_daily_text

def weather_emergency():
    """This function checks for a weather emergency by
    searching for weather terms in variables and creates
    a message based on the weather."""
    #Fetches data from API and creates global varibles.
    weather_handle(weather_fetch(config_fetcher('weather_city'), config_fetcher('weather_key')))
    #Creates a message that changes based on the temperature.
    storm_matches = ['hunder', 'ightning', 'trong wind', 'torm']
    snow_matches = ['snow', 'Snow']
    rain_matches = ['ain', 'rizzle', 'recip']
    if any(x in weather_description for x in storm_matches):
        weather_emergency_text = "There's a storm out there! Be careful."
        return weather_emergency_text
    elif any(x in weather_description for x in snow_matches):
        weather_emergency_text = "Let it snow! Look outside."
        return weather_emergency_text
    elif any(x in weather_description for x in rain_matches):
        weather_emergency_text = "You'll get wet if you go out today..."
        return weather_emergency_text
    else:
        return None

def news_fetch(region,news_key):
    """This function fetches the data from the news"""
    #Allows for customizable API key and weather location.
    url = (f"http://newsapi.org/v2/top-headlines?country={region}&apiKey={news_key}")
    #Gets API with requests and convert to .json
    news_api = requests.get(url)
    news_json = news_api.json()
    return news_json

def news_handle(news_json):
    """This function creates global variables containing news
    data from today in order to create daily breifings"""
    #Sets all the variables to global space to be used later.
    global title_1, title_2, author_1, author_2, source_1, source_2, url_1_final, url_2_final
    #Handles data from API and assigns data to variables.
    news_data = news_json['articles']
    article_1 = news_data[0]
    article_2 = news_data[1]
    title_1 = article_1['title']
    author_1 = article_1['author']
    source_1 = article_1['source']['name']
    url_1 = article_1['url']
    url_1_final = '<a href="{}">Read More</a>'.format(url_1)
    title_2 = article_2['title']
    author_2 = article_2['author']
    source_2 = article_2['source']['name']
    url_2 = article_2['url']
    url_2_final = '<a href="{}">Read More</a>'.format(url_2)
    return

def news_daily():
    """This function creates the daily news breifing based
    on the varibles from the function news_handle"""
    #Fetches data from API and creates global varibles.
    news_handle(news_fetch(config_fetcher('news_region'), config_fetcher('news_key')))
    #Creates a daily breifing using varibles
    news_daily_news = Markup((f"The top headline for today is entitled: {title_1}, and was \
written by {author_1}. It was written for {source_1} and can be found here: {url_1_final}. \
\nHere is a second headline, entitled: {title_2}, written by {author_2}. \
It was written for {source_2} and can be found here {url_2_final}."))
    return news_daily_news

def news_speech():
    """This function creates a readable news briefing for tts"""
    #Fetches data from API and creates global varibles.
    news_handle(news_fetch(config_fetcher('news_region'), config_fetcher('news_key')))
    #Creates a daily breifing using varibles
    news_daily_news = Markup((f"The top headline for today is entitled: {title_1}, and was \
written by {author_1}. Here is a second headline, entitled: {title_2}, written by {author_2}."))
    return news_daily_news

def news_emergency():
    """This function checks for a news emergency by
    searching for breaking news."""
    #Fetches data from API and creates global varibles.
    news_handle(news_fetch(config_fetcher('news_region'), config_fetcher('news_key')))
    #Creates a message or not.
    if 'reaking news' in title_1:
        news_emergency_text = Markup((f"Breaking News! {title_1} \n Click to continue reading: {url_1_final}"))
        return news_emergency_text
    elif 'reaking news' in title_2:
        news_emergency_text = Markup((f"Breaking News! {title_2} \n Click to continue reading: {url_2_final}"))
        return news_emergency_text
    elif 'russels' in title_1:
        news_emergency_text = Markup((f"Breaking News! {title_1} \n Click to continue reading: {url_1_final}"))
        return news_emergency_text
    else:
        return None
