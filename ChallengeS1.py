#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 07:45:06 2019

@author: blackhawk
"""

#Data Incubator challenge Section1

#Section 1: The New York City Fire Department keeps a log of detailed 
#information on incidents handled by FDNY units. In this challenge we will work 
#with a dataset that contains a record of incidents handled by FDNY units from
# 2013-2017. Download the FDNY data set. Also take a look at the dataset 
#landing page and find descriptions of column names here.




#Importing Libraries
import numpy as np
import pandas as pd


#Reading the data set in using Pandas
dataSet = pd.read_csv("Incidents_Responded_to_by_Fire_Companies.csv")


#Section1
#Q1
#What proportion of FDNY responses in this dataset correspond to the most 
#common type of incident?

#Using value count to see each values frequencies 
Incident_frequency = dataSet["INCIDENT_TYPE_DESC"].value_counts()

#checking to see whether or not there is NA values in this column
dataSet["INCIDENT_TYPE_DESC"].isna().sum()
list(dataSet.columns.values)

#Since there is no NA value in the column the proportion of most common type
#is the one with max frequency divided by sum of overal frequency.
SumIncident = int
SumIncident = dataSet["INCIDENT_TYPE_DESC"].value_counts().sum()

MaxFreq = int
MaxFreq = dataSet["INCIDENT_TYPE_DESC"].value_counts().max()

#Since there is not much performance difference between numpy divide and
#regular divide we used regular Python division

S1Q1 = float
S1Q1 = MaxFreq / SumIncident
print(S1Q1)


#Q2
#What is the ratio of the average number of units that arrive to a scene of
#an incident classified as '111 - Building fire' to the number that arrive 
#for '651 - Smoke scare, odor of smoke'?


avgOs111 = np.float64
avgOs651 = np.float64
S1Q2 = np.float64
avgOs111 = dataSet.loc[dataSet["INCIDENT_TYPE_DESC"]== "111 - Building fire", 
            ["UNITS_ONSCENE"]].mean()

avgOs651 = dataSet.loc[dataSet["INCIDENT_TYPE_DESC"]== 
                       "651 - Smoke scare, odor of smoke",
                       ["UNITS_ONSCENE"]].mean()
S1Q2 = np.float64
S1Q2 = avgOs111 / avgOs651
print(S1Q2)


#Q3
#How many times more likely is an incident in Staten Island a false call 
#compared to in Manhattan? The answer should be the ratio of Staten Island 
#false call rate to Manhattan false call rate. A false call is an incident 
#for which 'INCIDENT_TYPE_DESC' is '710 - Malicious, mischievous false call,
# other'.


#Ans: Since false call rate for each 
# SIFcall = false call rate(Staten Islan)/overall calls
# MtFcall = false call rate(Manhattan)/overall calls
# So for the ratio we only need 
#false call rate(Staten Islan)/ false call rate(Manhattan)

#Frequency of each location

loc_Frequency = dataSet["BOROUGH_DESC"].value_counts()


MtFcall, SIFcall = int

dataSet[(dataSet["BOROUGH_DESC"]=="1 - Manhattan") &
                  (dataSet["INCIDENT_TYPE_DESC"] == 
                  "710 - Malicious, mischievous false call, other")].count()
                  
MtFcall = len(dataSet[(dataSet["BOROUGH_DESC"]=="1 - Manhattan") &
                  (dataSet["INCIDENT_TYPE_DESC"] == 
                  "710 - Malicious, mischievous false call, other")])
SIFcall = len(dataSet[(dataSet["BOROUGH_DESC"]=="3 - Staten Island") &
                  (dataSet["INCIDENT_TYPE_DESC"] == 
                  "710 - Malicious, mischievous false call, other")])

S1Q3 = float
S1Q3 = SIFcall / MtFcall
print(S1Q3)

#Q4
#Check the distribution of the number of minutes it takes between the time a 
#'111 - Building fire' incident has been logged into the Computer Aided 
#Dispatch system and the time at which the first unit arrives on scene.
# What is the third quartile of that distribution. Note: the number of minutes
# can be fractional (ie, do not round).



#taking Incident time and arrival time and converting them from object type to
#date type 

ArrivalTime = dataSet.loc[dataSet["INCIDENT_TYPE_DESC"]== "111 - Building fire", 
            ["ARRIVAL_DATE_TIME"]]

IncidentTime = dataSet.loc[dataSet["INCIDENT_TYPE_DESC"]
            == "111 - Building fire", ["INCIDENT_DATE_TIME"]]

ArrivalTime = ArrivalTime.apply(pd.to_datetime)

IncidentTime = IncidentTime.apply(pd.to_datetime)



responsetime = ArrivalTime.values - IncidentTime.values
responsetime = responsetime.astype("timedelta64[s]")
responsetime = responsetime.astype("float64")
responsetime = responsetime / 60.0
 
#Calculating 3rd quartile in the distribution
 
S1Q4 = np.percentile(responsetime, 75)


#Q5
#We can use the FDNY dataset to investigate at what time of the day people cook 
#most. Compute what proportion of all incidents are cooking fires for every hour 
#of the day by normalizing the number of cooking fires in a given hour by the 
#total number of incidents that occured in that hour. Find the hour of the day 
#that has the highest proportion of cooking fires and submit that proportion of 
#cooking fires. A cooking fire is an incident for which 'INCIDENT_TYPE_DESC' is 
#'113 - Cooking fire, confined to container'. Note: round incident times down.
#For example, if an incident occured at 22:55 it occured in hour 22.

#Converting object types to datatime types
dataSet["INCIDENT_DATE_TIME"] = dataSet["INCIDENT_DATE_TIME"].apply(
        pd.to_datetime)

#Taking hour of the day for each incident
dataSet["INCIDENT_HOUR"] = dataSet["INCIDENT_DATE_TIME"].dt.hour 




dataSet[" Incident_Frequency_Hour"] = dataSet.groupby("INCIDENT_HOUR")["INCIDENT_HOUR"].transform("count")



dataSet["Cook_Incident_Frequency_Hour"] = np.where( 
        (dataSet["INCIDENT_TYPE_DESC"] ==  "113 - Cooking fire, confined to container"),
        dataSet.groupby(["INCIDENT_TYPE_DESC", "INCIDENT_HOUR"])["INCIDENT_HOUR"].transform("count"),
         0)

#Crossvalidating results
InFreqHour = dataSet["INCIDENT_HOUR"].value_counts()
cook_incident_by_hour = dataSet.loc[dataSet["INCIDENT_TYPE_DESC"]== 
                       "113 - Cooking fire, confined to container",
                       ["INCIDENT_HOUR"]]
CookIncidentFreq = cook_incident_by_hour["INCIDENT_HOUR"].value_counts()



dataSet["Cooking_Norm_By_Hour"] = np.where( 
        (dataSet["INCIDENT_TYPE_DESC"] ==  "113 - Cooking fire, confined to container"),
        dataSet["Cook_Incident_Frequency_Hour"].values /
        dataSet[" Incident_Frequency_Hour"].values,
         0)


S1Q5 = dataSet.loc[dataSet["Cooking_Norm_By_Hour"].max()]




#Q6
#What is the coefficient of determination (R squared) between the number of 
#residents at each zip code and the number of inicidents whose type is 
#classified as '111 - Building fire' at each of those zip codes. Note: 
#The 2010 US Census population by zip code dataset should be downloaded 
#from here. You will need to use both the FDNY responses and the US 
#Census dataset. Ignore zip codes that do not appear in the census table.

ZipCodeData = pd.read_csv("2010+Census+Population+By+Zipcode+(ZCTA).csv")

dataSet["111_Incident_per_Zipcode"] = np.where( 
        (dataSet["INCIDENT_TYPE_DESC"] ==  "111 - Building fire"),
        dataSet.groupby(["INCIDENT_TYPE_DESC", "ZIP_CODE"])["ZIP_CODE"].transform("count"),
         0)

#CrossValidating our prevous data for overall count of 111 incident in each
#ZipCode

BuildindFireZipecde = dataSet.loc[dataSet["INCIDENT_TYPE_DESC"]== 
                       "111 - Building fire",
                       ["ZIP_CODE"]]
BuildindFireZipecde["Frequency"] = BuildindFireZipecde.groupby(
        ["ZIP_CODE"])["ZIP_CODE"].transform("count")

#CrossValidation was correct

# making sure that all the zipcodes in the zipe code database in unique
ZipCodeData["Zip Code ZCTA"].nunique()
duplicates = ZipCodeData[ZipCodeData.duplicated(["Zip Code ZCTA"], keep =False)]

#In the dataSet we have 33091 rows but we have 32989 unique zip code which
#means we have 206 duplicate which by the look on the list of duplicates 
# in most of them the last one is the biggest number of people in that  zip codes so we drop 
#the duplicates and only keeping the last one

ZipCodeData = ZipCodeData.drop_duplicates(["Zip Code ZCTA"], keep="last")

#dropping duplicates in buildinfzip and then
#Vlookup from buildingFireZip code data frame to Zipcode dataset
BuildindFireZipecde["ZIP_CODE"] = BuildindFireZipecde["ZIP_CODE"].astype(np.int64)
BuildindFireZipecde = BuildindFireZipecde.drop_duplicates(["ZIP_CODE"], keep ="first")

duplicates2 = BuildindFireZipecde[BuildindFireZipecde.duplicated(keep = False)]

ZipCodeData["BFire_Per_Zip"] = ZipCodeData["Zip Code ZCTA"].map(
        BuildindFireZipecde.set_index("ZIP_CODE")["Frequency"])

BuildindFireZipecde["Population_per_zip"]= BuildindFireZipecde["ZIP_CODE"].map(
        ZipCodeData.set_index("Zip Code ZCTA")["2010 Census Population"])

#Taking out NA values
BuildindFireZipecde = BuildindFireZipecde.dropna()


test = BuildindFireZipecde["Population_per_zip"].corr(
        BuildindFireZipecde["Frequency"])
test = test**2
        
S1Q6 = np.float64
S1Q6 = (np.corrcoef(BuildindFireZipecde["Frequency"], 
                    BuildindFireZipecde["Population_per_zip"])[0,1])**2
print(S1Q6)







#Q5
#For this question, only consider incidents that have information about 
#whether a CO detector was present or not. We are interested in how many
#times more likely it is that an incident is long when no CO detector 
#is present compared to when a CO detector is present. For events with CO 
#detector and for those without one, compute the proportion of incidents 
#that lasted 20-30, 30-40, 40-50, 50-60, and 60-70 minutes (both interval 
#boundary values included) by dividing the number of incidents in each time 
#interval with the total number of incidents. For each bin, compute the ratio 
#of the 'CO detector absent' frequency to the 'CO detector present' frequency.
#Perform a linear regression of this ratio to the mid-point of the bins. From 
#this, what is the predicted ratio for events lasting 39 minutes?

dataSetCo = dataSet.copy(deep = True)
dataSetCo = dataSetCo.dropna(axis = 0, subset = ["CO_DETECTOR_PRESENT_DESC"])

#Checking to see whether or not is ther any missing data in duration ?

dataSetCo["TOTAL_INCIDENT_DURATION"].isna().sum()

#After removing NAN in the CO Presence column we have 29675 rows of data
dataSetCo["TOTAL_INCIDENT_DURATION"] = dataSetCo["TOTAL_INCIDENT_DURATION"].astype(np.int64)
dataSetCo["TOTAL_INCIDENT_DURATION"] = dataSetCo[
        "TOTAL_INCIDENT_DURATION"]/60
        
dataSetCo["TOTAL_INCIDENT_DURATION"].max() - dataSetCo["TOTAL_INCIDENT_DURATION"].min()

#Since the question mentioned that both intervals included we have problem 
#on duration = 30 & 40, duration 50 and 60 min because there is no data have
#no problem and we have 11 rows for 30 and 5 rows for 40 which compared to all
#of our data which has CO information (29675 rows) is nearly 0%
# so our been will be 30.01 -40.00 and 40.01 - 50.00 
dataSetCo["TOTAL_INCIDENT_DURATION"].min()
dataSetCo["TOTAL_INCIDENT_DURATION"].max()


bins = pd.IntervalIndex.from_tuples([(0,19.99), (20,30), (30.01,40),
                                     (40.01,50), (50,60), (60, 12800)],
 closed = "both", dtype="interval[float64]")
dataSetCo["Duration_intervals"] =pd.cut(dataSetCo["TOTAL_INCIDENT_DURATION"],
         bins)

#Number of each incident in each bin based on the presence of the CO                                    

dataSetCo["Total_inc_per_Bin"] = dataSetCo.groupby(
        ["Duration_intervals"])["Duration_intervals"].transform("count")
dataSetCo["Total_inc_per_Bin"] = dataSetCo["Total_inc_per_Bin"].astype(np.float64)

dataSetCo["CoPresence"]  = dataSetCo.groupby([ "CO_DETECTOR_PRESENT_DESC" ,
                        "Duration_intervals"])[
"Duration_intervals"].transform("count")



dataSetCo["COYes"] = np.where(dataSetCo["CO_DETECTOR_PRESENT_DESC"]=="Yes",
        dataSetCo.groupby([ "CO_DETECTOR_PRESENT_DESC" ,
                        "Duration_intervals"])["Duration_intervals"].transform("count"),
 0) 
dataSetCo["COYes"] = dataSetCo["COYes"].astype(np.float64)




dataSetCo["CONo"] = np.where(dataSetCo["CO_DETECTOR_PRESENT_DESC"]=="No",
        dataSetCo.groupby([ "CO_DETECTOR_PRESENT_DESC" ,
                        "Duration_intervals"])["Duration_intervals"].transform("count"),
 0)

dataSetCo["CONo"] = dataSetCo["CONo"].astype(np.float64)

dataSetCo["BinsMidpoint"] = [(a.left+a.right)/2 for a in dataSetCo["Duration_intervals"]]

BinsCOYes = dataSetCo[["BinsMidpoint","COYes", "Total_inc_per_Bin"]].copy(deep = True)
BinsCONo  = dataSetCo[["BinsMidpoint","CONo"]].copy(deep = True)


BinsCOYes = BinsCOYes[BinsCOYes["COYes"] != 0]
BinsCONo  = BinsCONo[BinsCONo["CONo"] != 0]


BinsCOYes = BinsCOYes.drop_duplicates()
BinsCONo  = BinsCONo.drop_duplicates()



BinsRatio = pd.merge(BinsCOYes, BinsCONo, on = "BinsMidpoint")
BinsRatio["BinsYRatio"] = BinsRatio["COYes"].div(BinsRatio["Total_inc_per_Bin"])
BinsRatio["BinsNRatio"] = BinsRatio["CONo"].div(BinsRatio["Total_inc_per_Bin"])
BinsRatio["AbstoPresFreq"] = BinsRatio["BinsNRatio"] / BinsRatio["BinsYRatio"]


RegressionData = pd.DataFrame(index = [0,1,2,3,4,5], columns=["X", "Y"])

RegressionData["X"] = BinsRatio["BinsMidpoint"].copy(deep=True)
RegressionData["Y"] = BinsRatio["AbstoPresFreq"].copy(deep =True)

X = RegressionData.iloc[:,:-1]
Y = RegressionData.iloc[:,1]

X.reshape(1,-1)

from sklearn.linear_model import LinearRegression
regression = LinearRegression()
regression.fit(X,Y)


prediction = regression.predict([39])



#S1Q8
#Calculate the chi-square test statistic for testing whether an incident 
#is more likely to last longer than 60 minutes when CO detector is not
#present. Again only consider incidents that have information about whether 
#a CO detector was present or not.

#creating a value to whether an incident is more than 60 mins or not 
dataSetCo["Morethan60min"] =np.where(dataSetCo["TOTAL_INCIDENT_DURATION"] > 60, 
         "YES", "NO")

from scipy.stats import chi2_contingency

chi2Data = pd.DataFrame()
chi2Data["COPresent"] = dataSetCo["CO_DETECTOR_PRESENT_DESC"].copy(deep=True)
chi2Data["Morethan60min"] = dataSetCo["Morethan60min"].copy(deep=True)

chi2Data["COPresent"] =np.where(chi2Data["COPresent"]=="Yes", 1,0 )
chi2Data["Morethan60min"] = np.where(chi2Data["Morethan60min"] == "YES",1,0)




def chi_square_CO_60min(data, cat1 ,cat2):
    groupsizes = data.groupby([cat1, cat2]).size()
    ctsum = groupsizes.unstack(cat1)
    return(chi2_contingency(ctsum.fillna(0)))
    


chi2, p, dof, expected = chi_square_CO_60min(chi2Data,"COPresent", "Morethan60min")
print(p)