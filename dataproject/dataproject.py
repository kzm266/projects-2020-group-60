#Installing programs in Anaconda Promt. 
#(1): pip install pandas-datareader
#(2): pip install git+https://github.com/elben10/pydst

#Importing used packages.
import numpy as n
import pandas as pd
import pandas_datareader # install in (1).
import pydst # install in (2).
import datetime
import matplotlib.pyplot as plt



###Datacleaning###
#We use the Python module pydst for assesing the API of Denmark's statistics.
Dst = pydst.Dst(lang='en')

#This data is organized into Tables and Subjects indexed by numbers so we use the following to see the list.
Dst.get_subjects()

#We choose the main dataset for "Money and credit markets" with subject=16 seen below.
tables = Dst.get_tables(subjects=['16']) 

#Then we choose the subdataset for "Pension funds" with id=MPK49 that is shown below.
tables[tables.id == 'MPK49'] 

#Further we can examine the variables in more deepth. 
vars = Dst.get_variables(table_id = 'MPK49')
vars.values

#Now we are retrieving data from the above mentioned subject and subset we creat an unsorted table. 
Data = Dst.get_data(table_id = 'MPK49', variables={'AKTPAS':['5180','5190','5200'], 'TID':['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016',], 'TYPE':['*']})
#Rename the variables of the dataset.
Data.rename(columns={'AKTPAS':'Assets & Liabilities','TID':'Year','TYPE':'Type','INDHOLD':'Amount'},inplace=True)

#Change the index of the table to the variables 'Year' for now. 
Index = Data.set_index('Year')
#Sort the dataset to get a more clear order in the dataset. 
Sort = Index[['Type','Assets & Liabilities','Amount']] 

#Now we are creating two datasets from the before mentioned table ('Data') where we sort the data tables for working and retired members. 
Working = Sort[Sort['Assets & Liabilities']=='Number of working members'].sort_values(['Year','Type']).rename(columns={'Assets & Liabilities':'Currently working', 'Amount':'Currently working members'})
Retired = Sort[Sort['Assets & Liabilities']=='Number of retired members'].sort_values(['Year','Type']).rename(columns={'Assets & Liabilities':'Currently retired', 'Amount':'Currently retired members'})

#Thereto we remove the variables 'Year' and 'Type' because when we merge the tables later we dont want duplications of these variables. 
Retired_notype_noyear = Retired[['Currently retired', 'Currently retired members']]

#Merging the two tables for working and retired members together. 
Merge = pd.concat([Working, Retired_notype_noyear], axis=1)

#Combining the necessary variables and tables into one.
Reduced = Merge[['Type','Currently working members','Currently retired members']]
#Removing data where values are missing or isnt existing altogether. 
Reduced = Reduced.dropna(axis=0)

#Adding collums with results of different calculations. 
Reduced['Gap in pension sum'] = Reduced['Currently working members'].astype(float) - Reduced['Currently retired members'].astype(float)
Reduced['Difference in pension sum (Pct)'] = ((Reduced['Currently working members'].astype(float)/Reduced['Currently retired members'].astype(float))-1)*100

#Reseting index for the dataset.
Reduced.reset_index(inplace = True)

#Only keeping data for corporate pension funds as we want a more reduced final dataset.
Complete = Reduced[Reduced['Type'] == "Corporate pension funds"]



###Graph###
#Creating function to creat graphs of our collums. 
def Graph(yaxs):
    Complete.plot(x='Year', y=yaxs ,style='-o')
    plt.xlabel('Year')
    plt.ylabel(yaxs)
    plt.grid(True)
    return plt.show()





