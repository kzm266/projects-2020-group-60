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
Data = Dst.get_data(table_id = 'MPK49', variables={'AKTPAS':['5180','5190','5200'], 'TID':['*'], 'TYPE':['*']})
Data.rename(columns={'AKTPAS':'Assets & liabilities','TID':'Year','TYPE':'Type','INDHOLD':'Amount'},inplace=True)
Data.set_index('Assets & liabilities')
Data

#Renaming our variabel. 
al='assets/liabilities'


#Changing the index to Municipality:
Index = Data.set_index('AKTPAS')

#Picking out the neccesary variables:
#Sortet = New_index[['TID','KOEN','INDHOLD']].rename(columns={'KOEN':'Gender', 'TID':'Year', 'INDHOLD':'disposable income'})

#Making a table for employed and retired:
Employed = Index[Index['AKTPAS']=='5190'].sort_values(['AKTPAS','Tid']).rename(columns={al:'pension_employed'})
Retired = Index[Index['AKTPAS']=='5190'].sort_values(['AKTPAS','Tid']).rename(columns={al:'pension_retired'})

#We don't want year to appear twice when we concat:
Retired_no_year = Retired[['AKTPAS', 'retired']]

#Concatenate the two tables:
Concatenated_table = pd.concat([Employed, Retired_no_year], axis=1)

#Removing the gender nicer look:
Final_table = Concatenated_table[['Tid','pension_employed','pension_retired']]

#DATACLEANING COMPLETE#

#APPLYING METHODS#

#Creates a function with provides the difference between the genders in %:
def Diff_pct(x):
    """Gives the procentual difference between the status"""
    return round((x['pension_employed']/x['pension_retired']-1)*100, 2) #Use round command to get an outcome in percentages with precise decimals. 

#Applying the function to the end of the table:
Final_table['Difference in pct between employed and retired pension']=Final_table.apply(Diff_pct, axis=1)

#We now wish to create a individual table for each province, and do it like this:
#We start by finding the unique values in the table AKA all the provinces
unik = Final_table.index.unique()

#Making an empty dictionary which will contain our unique values with their seperate table later
d = {}

#Filling the empty dictionary
for i in unik:
    d.update( {i : Final_table.loc[i]})

#We can now plot the difference between men and women in a graph like this:
def Difference(assets):
    #Simply plotting the difference against years to see the evolution
    plt.plot(d[al]['Tid'],d[al]['Difference in pct between employed and retired pension'])
    plt.xlabel('Year')
    plt.ylabel('Difference in pct between employed and retired pension')
    plt.title(f'Difference in pension for {str(al)}')
    plt.axis([])
    plt.grid(True)
    return plt.show()

#To compare the genders visually, we create two normal distributions:
def normal(z):
    
    #Making subplots to be shown in the same figure:
    plt.subplot(2,1,1)
    
    #Creating the normal distribution for the employed:
    s = np.random.normal(d[al]['pension_employed'].mean(), d[al]['pension_retired'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    
    #Plotting the distribution:
    plt.plot(bins, 1/(d[al]['pension_employed'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-d[al]['pension_retired'].mean())**2 / (2 * d[al]['pension_employed'].std()**2)), linewidth = 4)
    
    #Some formal stuff
    plt.title(f'Employed in {str(al)}')
    plt.xlabel('Pension')
    plt.axis([])
    
    #The other subplot:
    plt.subplot(2,1,2)
    
    #Creating the normal distribution for the women:
    s = np.random.normal(d[al]['pension_retired'].mean(), d[al]['pension_employed'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
   
   #Plotting the distribution:
    plt.plot(bins, 1/(d[al]['pension_retired'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-d[al]['pension_employed'].mean())**2 / (2 * d[al]['pension_retired'].std()**2)), linewidth = 4)
    
    #Formal figure stuff again
    plt.title(f'Retired in {str(al)}')
    plt.xlabel('Pension')
    plt.axis([0,300000,0,0.000011])
    plt.subplots_adjust(top=2, bottom=0, left=0, right=1, hspace=0.2)
       
    return plt.show(), print('For employed, the mean is ','{0:.0f}'.format(d[al]['pension_employed'].mean()), 'and the standard deviation is ','{0:.0f}'.format(d[al]['pension_employed'].std())), print('For retired, the mean is ','{0:.0f}'.format(d[al]['pension_retired'].mean()), 'and the standard deviation is ','{0:.0f}'.format(d[al]['pension_retired'].std()))

#Graph that shows the change in disposable income over the years
def change():
    plt.plot(d[al]['Tid'], d[al]['pension_employed'], label = 'Employed')
    plt.plot(d[al]['Tid'], d[al]['pension_retired'], label = 'Retired')
    plt.ylabel('Pension')
    plt.gca().legend(('Employed', 'Retired'))
    plt.title(f'{str(al)}')
    return Difference

#test