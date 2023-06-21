#%%
import csv

# Relative path to country code file
relative_path = "country-codes-and-names.csv"

codesAndNames = []
with open(relative_path, 'r') as file:
    csvreader = csv.reader(file, delimiter='_')
    for row in csvreader:
        codesAndNames.append(row)

def listToDict(list):
    keyValuePairs = {codesAndNames[i][0]: codesAndNames[i][1] for i in range(len(codesAndNames))}
    return keyValuePairs

countryCodes = {}
for i in range(len(codesAndNames)):
    countryCodes.update({f"{str(list(listToDict(codesAndNames))[i])}":str(codesAndNames[i][1])})

testArray = ['AFG','JPN','CAD','KOR','PRK']

print(countryCodes)
print(len(countryCodes))
print(type(countryCodes))
print(list(countryCodes)[0])
# codeToName = {}
# for i in range(len(testArray)):
