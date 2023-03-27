import requests

#%% OData API URLs
base_url = "https://ghoapi.azureedge.net/api"
indicator_url = "https://ghoapi.azureedge.net/api/Indicator"

indicator_response = requests.get(indicator_url)

indicator_json = indicator_response.json()
print("The dimensions of the raw data list is:",len(indicator_json))
print("The raw data's type is:",type(indicator_json))

print('\nThe raw data elements are identified by:')
count = 1
for value in indicator_json:
    print(count, value)
    count += 1

print("\nThe number of available indicators is:",len(indicator_json['value']))

print("\nA single indicators raw data is shown below")
# print(indicator_json['@odata.context'])
# print(type(indicator_json['value']))
print(indicator_json['value'][0])
print("The data type here is:",type(indicator_json['value'][0]))

print('\nThis raw data can be pulled out into key and value elements as:')
for keys in indicator_json['value'][0]:
    print(keys,": ", indicator_json['value'][0][keys])
