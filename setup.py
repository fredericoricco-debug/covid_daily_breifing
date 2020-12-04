import json

'''This module allows the user to set up the program with ease'''

print("Welcome User! \n This setup.py program allows you to configure the main and API_fetch modules with ease.")

covid_region = input('You can get COVID-19 data from all the British Isles. \n Input your country of choice here, it should be formatted like this: \n \n example: England \n example: Wales \n \n')

weather_city = input('You can get weather data from any city in England. \n Input your city of choice here, it should be formatted like this: \n \n example: Exeter \n \n')

news_region = input('You can get news data from all over the world. \n Input your country of choice here, it should be formatted like as a country code: \n \n United States Example: us \n Great Britain Example: gb \n \n')

weather_key = input('Input your weather API key as discussed in readme.txt. \n \n')

news_key = input('Input your news API key as discussed in readme.txt. \n \n')

voice = input('Finally, would you like a male or female text-to-speech voice? \n Input 0 for male and 1 for female: \n \n')

new_dict = {}
new_dict['covid_region'] = covid_region
new_dict['weather_city'] = weather_city
new_dict['news_region'] = news_region
new_dict['weather_key'] = weather_key
new_dict['news_key'] = news_key
new_dict['voice'] = voice
with open("config.json", "w") as f:
    json.dump(new_dict, f)
