__author__ = 'Caleb'

import json
import requests
import datetime

def find_roundtrip_flights(search_start_date, return_date, starting_airport, destination_airport, max_price, solutions, api_key):
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
    headers = {'content-type': 'application/json'}
    params = {
        "request": {
            "slice": [
                {
                    "origin": starting_airport,
                    "destination": destination_airport,
                    "date": str(search_start_date)
                },
                #{
                #    "origin": destination_airport,
                #    "destination": starting_airport,
                #    "date": str(return_date)
                #}
            ],
            "passengers": {
                "adultCount": 1
            },
            "maxPrice": "USD" + str(max_price),
            "solutions": solutions,
            "refundable": False
        }
    }
    response = requests.post(url, data=json.dumps(params), headers=headers)
    return response.json()

api_key = ""
flights = []
start_search = datetime.date(2017, 6, 7)
end_search = datetime.date(2017,  6, 10)
return_date = datetime.date(2017, 6, 17)
days = (end_search - start_search).days
for i in range(days + 1):
  data = find_roundtrip_flights(start_search + datetime.timedelta(days=i), return_date, "CMH", "NRT", 2000, 50, api_key)
  for m in range(50):
      try:
          price = data['trips']['tripOption'][m]['saleTotal'].replace("USD", "")
          departure_time = data['trips']['tripOption'][m]['slice'][0]['segment'][0]['leg'][0]['departureTime']
          flights.append([float(price), str(departure_time)])
      except KeyError:
          continue
      except IndexError:
          continue
sorted(flights, key=lambda x: x[0])
for flight in flights:
    print(str(flight[0]) + "  " + str(flight[1]))