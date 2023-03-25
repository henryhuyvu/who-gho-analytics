import requests

#%% OData API URLs
base_url = "https://ghoapi.azureedge.net/api"
indicator_url = "https://ghoapi.azureedge.net/api/Indicator"

indicator_response = requests.get(indicator_url)

indicator_json = indicator_response.json()
print(len(indicator_json))
print(type(indicator_json))

print('\n')
for value in indicator_json:
    print(value)
# print(indicator_json['@odata.context'])
# print(type(indicator_json['value']))
print(indicator_json['value'][0])
print(type(indicator_json['value'][0]))
print(len(indicator_json['value'][0]))

print('\n')
for keys in indicator_json['value'][0]:
    print(keys,": ", indicator_json['value'][0][keys])
# print(type(indicator_json['value'][0]))
# print(indicator_json)