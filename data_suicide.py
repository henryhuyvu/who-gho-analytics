#%% Imports

import requests
import json
import pandas as pd

#%% URLs

# Base WHO GHO API URL
baseURL = "https://ghoapi.azureedge.net/api/"

# Topical URLs
linkURL_Suicide = 'MH_12'

# Request data
fullURL_Suicide = baseURL + linkURL_Suicide
urlRequest_Suicide = requests.get(fullURL_Suicide)
contents_Suicide = urlRequest_Suicide.text

#%% Working with data

json_Suicide = json.loads(contents_Suicide)

# Find OData keys
jsonKeys = []
for i in range(len(list(json_Suicide))):
    jsonKeys.append(list(json_Suicide)[i])

# Assign JSON data to dataframe
data_suicide = json_Suicide[jsonKeys[1]]
dataFrame_Suicide = pd.DataFrame(data_suicide)


# View data
print(dataFrame_Suicide,'\n')

columns = list(dataFrame_Suicide.columns)

# Show unique entries under each column in the data set
# print(f"There are {len(columns)} columns under the names: {str(columns)} \n")
# for keys in columns:
#     print(f"For the [{keys}] column, the count for each key is: \n {dataFrame_Suicide[keys].unique()} \n")

#%% Modify column names

# Dropping unnecessary columns
cleanDataFrame_Suicide = dataFrame_Suicide.drop(columns=["Id","IndicatorCode","TimeDimType","Dim1Type","Dim2Type","Dim2","Dim3Type","Dim3","DataSourceDimType","DataSourceDim","Comments","TimeDimensionBegin","TimeDimensionEnd","Date","TimeDimensionValue"])
print(cleanDataFrame_Suicide)

# Updating column names
cleanDataFrame_Suicide = cleanDataFrame_Suicide.rename(columns={"Dim1":"Sex"})
print(cleanDataFrame_Suicide)
