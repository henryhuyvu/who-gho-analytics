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

# Dropping unnecessary columns and updating column names
cleanDataFrame_Suicide = dataFrame_Suicide.drop(columns=["Id","IndicatorCode","TimeDimType","Dim1Type","Dim2Type","Dim2","Dim3Type","Dim3","DataSourceDimType","DataSourceDim","Comments","TimeDimensionBegin","TimeDimensionEnd","Date","TimeDimensionValue"])
cleanDataFrame_Suicide = cleanDataFrame_Suicide.rename(columns={"Dim1":"Sex", "TimeDim":"Year"})

#%% Prepping data for plotting
spatialWorldBank = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'WORLDBANKINCOMEGROUP']['SpatialDim'].unique())
spatialRegions = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'REGION']['SpatialDim'].unique())
spatialCountries = list(cleanDataFrame_Suicide.loc[cleanDataFrame_Suicide['SpatialDimType'] == 'COUNTRY']['SpatialDim'].unique())

def extractDataToArray(countryCode,sex,arrayName):    
    arrayName.append(cleanDataFrame_Suicide.loc[
        (cleanDataFrame_Suicide['SpatialDim'] == countryCode) & 
        (cleanDataFrame_Suicide['Sex'] == sex)
        ].sort_values(by=["Year"]))
    
#%% Regional Data 
regionData = []
for i in range(len(spatialRegions)):
    extractDataToArray(spatialRegions[i],"BTSX",regionData)

# Plot all the data
for i in range(len(spatialRegions)):
    if i == 0:
        ax = regionData[i].plot(y="NumericValue",x="Year")
    else:
        regionData[i].plot(ax=ax,y="NumericValue",x="Year")

plt.title("Age-standardized suicide rates by region")
plt.xlabel("Year")
plt.ylabel("Suicide rate per 100,000 population")
plt.xlim([2000,2019])
plt.legend(spatialRegions, bbox_to_anchor=(1, 1.), loc='best', prop={'size': 8}, ncol=4)
plt.grid()
plt.show(block=False)

#%% Country Data
countryData = []
for i in range(len(spatialCountries)):
    extractDataToArray(spatialCountries[i],"BTSX",countryData)

# Plot all the data
for i in range(len(spatialCountries)):
    if i == 0:
        ax = countryData[i].plot(y="NumericValue",x="Year",legend=None, linewidth=0.8)
    else:
        countryData[i].plot(ax=ax,y="NumericValue",x="Year",legend=None, linewidth=0.8)

plt.title(f"Age-standardized suicide rates for all {len(spatialCountries)} countries")
plt.xlabel("Year")
plt.ylabel("Suicide rate per 100,000 population")
plt.xlim([2000,2019])
# plt.legend(spatialCountries, loc='best', bbox_to_anchor=(1,1), prop={'size': 4}, ncol=4)
plt.locator_params(axis="x", integer=True, tight=True)
plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.grid()
plt.show(block=False)

#%% Highest rates for N countries amongst all countries
valueColumnIndex = -3
latestDataRowIndex = -1
recentSuicideRates = {}
for i in range(len(countryData)):
    recentSuicideRates.update({f"{spatialCountries[i]}":round(countryData[i].iloc[latestDataRowIndex,valueColumnIndex], 3)})

sortedRecentRates = sorted(list(recentSuicideRates.values()))
numberOfTopCountries = 10
topRates = []
topCountries = []
for n in range(numberOfTopCountries):
    topRates.append(sortedRecentRates[-(n+1)])
    topCountries.append(list(recentSuicideRates.keys())[list(recentSuicideRates.values()).index(sortedRecentRates[-(n+1)])])

topCountryData = []
for i in range(numberOfTopCountries):
    extractDataToArray(topCountries[i],"BTSX",topCountryData)

for i in range(numberOfTopCountries):
    if i == 0:
        ax = topCountryData[i].plot(y="NumericValue",x="Year",)
    else:
        topCountryData[i].plot(ax=ax,y="NumericValue",x="Year")

plt.title(f"Change in the {numberOfTopCountries} highest 2019 age-standardized suicide rates")
plt.xlabel("Year")
plt.ylabel("Suicide rate per 100,000 population")
plt.xlim([2000,2019])
plt.legend(topCountries,loc='best', prop={'size': 6}, ncol=4)
plt.grid()
plt.locator_params(axis="x", integer=True, tight=True)
plt.show(block=False)

#%% Lowest rates for N countries amongst all countries


numberOfBottomCountries = 10
bottomRates = []
bottomCountries = []
for n in range(numberOfBottomCountries):
    bottomRates.append(sortedRecentRates[n])
    bottomCountries.append(list(recentSuicideRates.keys())[list(recentSuicideRates.values()).index(sortedRecentRates[n])])

bottomCountryData = []
for i in range(numberOfBottomCountries):
    extractDataToArray(bottomCountries[i],"BTSX",bottomCountryData)

for i in range(numberOfBottomCountries):
    if i == 0:
        ax = bottomCountryData[i].plot(y="NumericValue",x="Year",)
    else:
        bottomCountryData[i].plot(ax=ax,y="NumericValue",x="Year")

plt.title(f"Change in the {numberOfBottomCountries} lowest 2019 age-standardized suicide rates")
plt.xlabel("Year")
plt.ylabel("Suicide rate per 100,000 population")
plt.xlim([2000,2019])
plt.ylim([0,15])
plt.legend(bottomCountries,loc='best', prop={'size': 6}, ncol=4)
plt.grid()
plt.locator_params(axis="x", integer=True, tight=True)
plt.show()
