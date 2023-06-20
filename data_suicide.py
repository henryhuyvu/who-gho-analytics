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
columns = list(dataFrame_Suicide.columns)
print(columns)

# Dropping unnecessary columns and updating column names
cleanDataFrame_Suicide = dataFrame_Suicide.drop(columns=["Id","IndicatorCode","TimeDimType","Dim1Type","Dim2Type","Dim2","Dim3Type","Dim3","DataSourceDimType","DataSourceDim","Comments","TimeDimensionBegin","TimeDimensionEnd","Date","TimeDimensionValue"])
cleanDataFrame_Suicide = cleanDataFrame_Suicide.rename(columns={"Dim1":"Sex", "TimeDim":"Year"})
print(cleanDataFrame_Suicide)

#%% Prepping data for plotting
spatialWorldBank = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'WORLDBANKINCOMEGROUP']['SpatialDim'].unique())
spatialRegions = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'REGION']['SpatialDim'].unique())
spatialCountries = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'COUNTRY']['SpatialDim'].unique())

def extractCountryData(countryCode,sex):    
    countryData.append(cleanDataFrame_Suicide.loc[
        (cleanDataFrame_Suicide['SpatialDim'] == countryCode) & 
        (cleanDataFrame_Suicide['Sex'] == sex)
        ].sort_values(by=["Year"]))
    
def extractRegionData(countryCode,sex):    
    regionData.append(cleanDataFrame_Suicide.loc[
        (cleanDataFrame_Suicide['SpatialDim'] == countryCode) & 
        (cleanDataFrame_Suicide['Sex'] == sex)
        ].sort_values(by=["Year"]))
    

#%% Country Data
countryData = []
for i in range(len(spatialCountries)):
    extractCountryData(spatialCountries[i],"BTSX")

# Plot all the data
for i in range(len(spatialCountries)):
    if i == 0:
        ax = countryData[i].plot(y="NumericValue",x="Year")
    else:
        countryData[i].plot(ax=ax,y="NumericValue",x="Year")

# plt.title("Age-standardized suicide rates by Country")
# plt.xlabel("Year")
# plt.ylabel("Suicide rate per 100,000 population")
# plt.xlim([2000,2019])
# plt.legend(spatialCountries, bbox_to_anchor=(1, 1.), loc='best', prop={'size': 4}, ncol=4)
# plt.show(block=False)

# Looking at the highest rates amongst all of the countries
print(round(countryData[1].iloc[-1,-3], 1))

print(countryData[1])
print(spatialCountries)
valueColumnIndex = -3
latestDataRowIndex = -1
recentSuicideRates = []
for i in range(len(countryData)):
    recentSuicideRates.append({f"{spatialCountries[i]}":f"{round(countryData[i].iloc[latestDataRowIndex,valueColumnIndex], 1)}"})
print(type(recentSuicideRates))
print(len(recentSuicideRates))
print(recentSuicideRates[0])
print(max(recentSuicideRates,key=recentSuicideRates.get))
# print(spatialCountries[i],": ",round(countryData[i].iloc[latestDataRowIndex,valueColumnIndex], 1))

#%% Regional Data 
# regionData = []
# for i in range(len(spatialRegions)):
#     extractRegionData(spatialRegions[i],"BTSX")

# # Plot all the data
# for i in range(len(spatialRegions)):
#     if i == 0:
#         ax = regionData[i].plot(y="NumericValue",x="Year")
#     else:
#         regionData[i].plot(ax=ax,y="NumericValue",x="Year")

# plt.title("Age-standardized suicide rates by Region")
# plt.xlabel("Year")
# plt.ylabel("Suicide rate per 100,000 population")
# plt.xlim([2000,2019])
# plt.legend(spatialRegions, bbox_to_anchor=(1, 1.), loc='best', prop={'size': 8}, ncol=4)
# plt.show()
