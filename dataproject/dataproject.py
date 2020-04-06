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

#DATACLEANING#

#We use pydst to use an API to Denmark's statistics
Dst = pydst.Dst(lang='en')
Dst.get_subjects() #Used to see list of different datasets. 
tables = Dst.get_tables(subjects=['16']) #We choose the main dataset for "Money and credit markets".
tables[tables.id == 'MPK49'] #We choose the subdataset for "Pension funds".
vars = Dst.get_variables(table_id='MPK49')

#To find the variables we need, we inspect the table that we have imported:
vars.values


#Analyze each variable and look at all given information in the dataset. 
vars = Dst.get_variables(table_id='MPK49')
for id in ['AKTPAS','TID','TYPE','INDHOLD']:
    print(id)
    values = Vars.loc[vars.id == id,['values']].values[0,0]
    for value in values:      
        print(f' id = {value["id"]}, text = {value["text"]}')


#After picking out values, we can get our data:
Data = Dst.get_data(table_id = 'MPK49', variables={'AKTPAS':['5180','5190','5200'], 'TID':['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016',], 'TYPE':['*']})
Data.rename(columns={'AKTPAS':'Assets & Liabilities','TID':'Year','TYPE':'Type','INDHOLD':'Amount'},inplace=True)

Index = Data.set_index('Year')
Sort = Index[['Type','Assets & Liabilities','Amount']]

Working = Sort[Sort['Assets & Liabilities']=='Number of working members'].sort_values(['Year','Type']).rename(columns={'Assets & Liabilities':'Currently working', 'Amount':'Average pension funds for currently working'})
Retired = Sort[Sort['Assets & Liabilities']=='Number of retired members'].sort_values(['Year','Type']).rename(columns={'Assets & Liabilities':'Currently retired', 'Amount':'Average pension funds for currently retired'})

Retired_notype_noyear = Retired[['Currently retired', 'Average pension funds for currently retired']]

#Concatenate the two tables:
Concatenated_table = pd.concat([Working, Retired_notype_noyear], axis=1)



#Removing the gender nicer look.
Final_table = Concatenated_table[['Type','Average pension funds for currently working','Average pension funds for currently retired']]
Final_table = Final_table.dropna(axis=0)


Final_table['Gap in pension sum'] = Final_table['Average pension funds for currently working'].astype(float) - Final_table['Average pension funds for currently retired'].astype(float)
Final_table['Difference in pension sum (Pct)'] = ((Final_table['Average pension funds for currently working'].astype(float)/Final_table['Average pension funds for currently retired'].astype(float))-1)*100

Final_table.reset_index(inplace = True)

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2016,1,1)

Final_table = pandas_datareader.data.DataReader('Type','Average pension funds for currently working','Average pension funds for currently retired', start, end))





