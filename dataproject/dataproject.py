#Installing programs in Anaconda Promt. 
#(1): pip install pandas-datareader
#(2): pip install git+https://github.com/elben10/pydst

#Importing used packages.
import numpy as np
import pandas as pd
import pandas_datareader # install in (1).
import pydst # install in (2).
import matplotlib.pyplot as plt

#DATACLEANING#

#We use pydst to use an API to Denmark's statistics
Dst = pydst.Dst(lang='en')
Dst.get_subjects() #Used to see list of different datasets. 
tables = Dst.get_tables(subjects=['16']) #We choose the main dataset for "Money and credit markets".
tables[tables.id == 'MPK49'] #We choose the subdataset for "Pension funds".
Vars = Dst.get_variables(table_id='MPK49')

#To find the variables we need, we inspect the table that we have imported:
Vars.values



#After picking out values, we can get our data:
Data = Dst.get_data(table_id = 'MPK49', variables={'AKTPAS':['5180','5190','5200'], 'TID':['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016',], 'TYPE':['*']})
Data.rename(columns={'AKTPAS':'Assets & Liabilities','TID':'Year','TYPE':'Type','INDHOLD':'Amount'},inplace=True)

Index = Data.set_index('Year')
Sort = Index[['Type','Assets & Liabilities','Amount']]

Working = Sort[Sort['Assets & Liabilities']=='Number of working members'].sort_values(['Year','Type']).rename(columns={'Assets & Liabilities':'Currently working', 'Amount':'Average pension funds for currently working'})
Retired = Sort[Sort['Assets & Liabilities']=='Number of retired members'].sort_values(['Year','Type']).rename(columns={'Assets & Liabilities':'Currently retired', 'Amount':'Average pension funds for currently retired'})


Retired_notype = Retired[['Currently retired', 'Average pension funds for currently retired']]

#Concatenate the two tables:
Concatenated_table = pd.concat([Working, Retired_notype], axis=1)
Concatenated_table


#Removing the gender nicer look.
Final_table = Concatenated_table[['Type','Average pension funds for currently working','Average pension funds for currently retired']]
Final_table = Final_table.dropna(axis=0)
Final_table

Final_table['Gap in pension sum'] = Final_table['Average pension funds for currently working'].astype(float) - Final_table['Average pension funds for currently retired'].astype(float)
Final_table['Difference in pension sum (Pct)'] = ((Final_table['Average pension funds for currently working'].astype(float)/Final_table['Average pension funds for currently retired'].astype(float))-1)*100
Final_table


#We now wish to create a individual table for each province, and do it like this:
#We start by finding the unique values in the table AKA all the provinces
unik = Final_table.unique()

#Making an empty dictionary which will contain our unique values with their seperate table later
d = {}

#Filling the empty dictionary
for i in unik:
    d.update( {i : Final_table.loc[i]})


#We can now plot the difference between men and women in a graph like this:
def Difference(Gruppe):
    #Simply plotting the difference against years to see the evolution
    plt.plot(d[Gruppe]['Type'],d[Gruppe]['Difference in pension sum (Pct)'])
    plt.xlabel('Type')
    plt.ylabel('Difference in pension sum (Pct)')
    plt.title('Test')
    plt.axis([2000,2016],0,100000)
    plt.grid(True)
    return plt.show()


