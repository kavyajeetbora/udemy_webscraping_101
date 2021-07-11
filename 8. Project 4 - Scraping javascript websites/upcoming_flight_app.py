# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 12:03:55 2021

@author: KVBA
"""
import requests
from lxml import html
import re
import click

@click.command()
@click.option("--flight_number", default="DLH1034", help = "Please enter a valid fligt number.\nfor example: --flight number = 'DLH1034'")
def upcoming_flights(flight_number):

    script = '''
        headers = {
            ["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
          }
          splash:set_custom_headers(headers)
          splash.private_mode_enabled = false
          splash.images_enabled = false
          assert(splash:go(args.url))
          splash:wait(1)

          return {
            html = splash:html()
          }
    '''

    print(flight_number)
    response = requests.post(url="http://localhost:8050/run", json = {
            "lua_source": script,
            "url": "https://flightaware.com/live/flight/"+flight_number
        })

    tree = html.fromstring(response.content)
    upcoming_flights = tree.xpath("//div[contains(@data-type, 'upcoming')]")

    if len(upcoming_flights)>0:
        ## for cleaning the text
        def clean_text(text):
            return re.sub("\\\\[n|t]","",str(text))

        def extract_time(time_txt):
            return re.findall("\d{2}:\d{2}", str(time_txt))[0]

        flights = []

        for flight in upcoming_flights:
            date = flight.xpath(".//div[1]/span/em/text()")[1]
            dep_time = flight.xpath(".//div[2]/div/div/span/em/span/text()")[0]
            arr_time = flight.xpath(".//div[3]/div/div/span/em/span/text()")[0]
            dep_airport = flight.xpath(".//div[2]/div/div/span[2]/text()")[0]
            arr_airport = flight.xpath(".//div[3]/div/div/span[2]/text()")[0]
            aircraft = flight.xpath(".//div[4]/span/text()")[0]
            duration = flight.xpath(".//div[5]/em/text()")[0]

            data = {
                "date": str(date),
                "dep_time": extract_time(dep_time),
                "arr_time": extract_time(arr_time),
                "dep_airport": clean_text(dep_airport).strip(),
                "arr_airport": clean_text(arr_airport).strip(),
                "aircraft": str(aircraft),
                "duration": clean_text(duration)
            }

            flights.append(data)

        click.echo(flights)
        return flights
    else:
        click.echo("There were no upcoming flights found for flight number: %s" % flight_number)
        return None


if __name__ == "__main__":
    print(upcoming_flights())


''' Output

> python upcoming_flight_app.py
DLH1034
[{'date': '13-Jul-2021', 'dep_time': '12:25', 'arr_time': '13:40', 'dep_airport': "Frankfurt Int'l -", 'arr_airport': 'Charles de Gaulle/Roissy -', 'aircraft': 'A320', 'duration': '1h 15m'}, {'date': '12-Jul-2021', 'dep_time': '12:25', 'arr_time': '13:40', 'dep_airport': "Frankfurt Int'l -", 'arr_airport': 'Charles de Gaulle/Roissy -', 'aircraft': 'A321', 'duration': '1h 15m'}]

> python upcoming_flight_app.py --flight_number=HOP1319
HOP1319
There were no upcoming flights found for flight number: HOP1319

'''
