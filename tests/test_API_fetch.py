from API_fetch import *

def test_config_fetcher():
    assert config_fetcher('covid_region') != None

#Creates variables for testing.
weather_city = config_fetcher('weather_city')
weather_key = config_fetcher('weather_key')
news_region = config_fetcher('news_region')
news_key = config_fetcher('news_key')

#Test API calls.
def test_weather_fetch():
    assert weather_fetch(weather_city, weather_key) != None

def test_covid_fetch():
    assert covid_fetch() != None

def test_news_fetch():
    assert news_fetch(news_region, news_key) != None

#Tests daily briefings.
def test_covid_daily():
    assert covid_daily() != None

def test_weather_daily():
    assert weather_daily() != None

def test_news_daily():
    assert news_daily() != None

def test_news_speech():
    assert news_speech() != None
