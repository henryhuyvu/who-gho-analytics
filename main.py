import requests

base_url = "https://ghoapi.azureedge.net/api"
indicator_url = "https://ghoapi.azureedge.net/api/Indicator"

indicators = requests.get(indicator_url)

indicators_json = indicators.json()
print(len(indicators_json))
print(type(indicators_json))
for value in indicators_json:
    print(value)
print(indicators_json['@odata.context'])
print(type(indicators_json['value']))
# print(indicators_json)