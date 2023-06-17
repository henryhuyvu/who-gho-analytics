#%% Imports

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

#%% URLs

# Base WHO GHO API URL
baseURL = "https://ghoapi.azureedge.net/api/"

# Topical URLs
linkURL_Suicide = 'MH_12'

# Request data
fullURL_Suicide = baseURL + linkURL_Suicide
urlRequest_Suicide = requests.get(fullURL_Suicide)
contents_Suicide = urlRequest_Suicide.text

#%% Data Manipulation

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

# Dropping unnecessary columns and updating column names
cleanDataFrame_Suicide = dataFrame_Suicide.drop(columns=["Id","IndicatorCode","TimeDimType","Dim1Type","Dim2Type","Dim2","Dim3Type","Dim3","DataSourceDimType","DataSourceDim","Comments","TimeDimensionBegin","TimeDimensionEnd","Date","TimeDimensionValue"])
cleanDataFrame_Suicide = cleanDataFrame_Suicide.rename(columns={"Dim1":"Sex", "TimeDim":"Year"})
print(cleanDataFrame_Suicide)

#%% Prepping data for plotting
spatialWorldBank = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'WORLDBANKINCOMEGROUP']['SpatialDim'].unique())
spatialRegions = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'REGION']['SpatialDim'].unique())
spatialCountries = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'COUNTRY']['SpatialDim'].unique())


# Male and Female comparisons 
# Dataframe for AFG Males
print(cleanDataFrame_Suicide.loc[
    (cleanDataFrame_Suicide['SpatialDim'] == spatialCountries[0]) &
    (cleanDataFrame_Suicide['Sex'] == "MLE")
    ].sort_values(by=["Year"]))

# Dataframe for AFG Females
print(cleanDataFrame_Suicide.loc[
    (cleanDataFrame_Suicide['SpatialDim'] == spatialCountries[0]) &
    (cleanDataFrame_Suicide['Sex'] == "FMLE")
    ].sort_values(by=["Year"]))


# Global comparisons
# Dataframe for AFG Mixed Sex

MixedSex_AFG = cleanDataFrame_Suicide.loc[
    (cleanDataFrame_Suicide['SpatialDim'] == spatialCountries[0]) &
    (cleanDataFrame_Suicide['Sex'] == "BTSX")
    ].sort_values(by=["Year"])

ax = MixedSex_AFG.plot(y="NumericValue",x="Year")

MixedSex_2 = cleanDataFrame_Suicide.loc[
    (cleanDataFrame_Suicide['SpatialDim'] == spatialCountries[1]) &
    (cleanDataFrame_Suicide['Sex'] == "BTSX")
    ].sort_values(by=["Year"])

MixedSex_2.plot(ax=ax, y="NumericValue",x="Year")

plt.legend(spatialCountries[:2])
plt.show()

# print(cleanDataFrame_Suicide.loc[
#     (cleanDataFrame_Suicide['SpatialDim'] == spatialCountries[0]) &
#     (cleanDataFrame_Suicide['Sex'] == "BTSX")
#     ].sort_values(by=["Year"]))

# cleanDataFrame_Suicide.loc[
#     (cleanDataFrame_Suicide['SpatialDim'] == spatialCountries[0]) &
#     (cleanDataFrame_Suicide['Sex'] == "BTSX")
#     ].sort_values(by=["Year"]).plot(y="NumericValue",x="Year")

# cleanDataFrame_Suicide.loc[
#     (cleanDataFrame_Suicide['SpatialDim'] == spatialCountries[0]) &
#     (cleanDataFrame_Suicide['Sex'] == "BTSX")
#     ].plot.scatter(y="NumericValue",x="Year")
# # cleanDataFrame_Suicide.plot(y="NumericValue",x="Year","ro")
# # plt.plot(x,y,'ro')
# plt.show()