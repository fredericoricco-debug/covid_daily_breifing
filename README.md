# covid_daily_breifing
A flask application that loads data from various APIs and announces them to the user with tts once an alarm runs out. It also displays 'smart notifications' that will appear when something out of the ordinary happens.

Welcome!

This COVID-19 Daily Briefing flask application will let you set
alarms that when reached will display a notification based on user
preferences and will read it aloud.

In order to use this program, the following dependencies must be installed.

- pyttsx3
- flask
- uk_covid19
- requests

Use

console%- pip install 'depency'

to install them.

You will also need two API keys. Visit the following websites to get them, it's free!

- https://newsapi.org/
- https://openweathermap.org/

You can use the config.json file to configure the program to your liking.
Alternatively, you can use the setup.py file to adjust the settings.

You can also test the program using pytest. Use:

console%- pip install pytest

and then:

console%- python -m pytest

to test if the code is still working. If the fetch functions no longer work,
it is because of an API error, meaning your key might be wrong, the API might
be down, or you have run out of free requests to the API.

Run main.py from the folder and enjoy!
(make sure not to refresh the page before the alarm goes off)

