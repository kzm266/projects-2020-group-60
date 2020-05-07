#Installing programs in Anaconda Promt. 
#(1): pip install pandas-datareader
#(2): pip install git+https://github.com/elben10/pydst

#Importing used packages.
import numpy as np
import pandas as pd
import pandas_datareader # install in (1).
import pydst # install in (2).
import datetime
import matplotlib.pyplot as plt

###Datacleaning###


##General##

#We use the Python module pydst for assesing the API of Denmark's statistics.
Dst = pydst.Dst(lang='en')

#This data is organized into Tables and Subjects indexed by numbers so we use the following to see the list.
Overview=Dst.get_subjects()

#We choose the main dataset for "Money and credit markets" with subject=16 seen below.
Theme=Dst.get_tables(subjects=['16']) 





##Table[1]##
#Then we choose the subdataset for "Pension funds" with id=MPK49 that is shown below.
Subject_1=Theme[Theme.id == 'MPK49'] 

#Further we can examine the variables in more deepth. 
Vars_1 = Dst.get_variables(table_id = 'MPK49')
Vars_1.values

#Now we are retrieving data from the above mentioned subject and subset we creat an unsorted table. 
Data_1 = Dst.get_data(table_id = 'MPK49', variables={'AKTPAS':['5320'], 'TID':['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016',], 'TYPE':['5410', '5420']})
#Rename the variables of the dataset.
Data_1.rename(columns={'AKTPAS':'Assets & Liabilities','TID':'Year','TYPE':'Type','INDHOLD':'Amount'},inplace=True)

#Change the index of the table to the variables 'Year' for now. 
Index_1 = Data_1.set_index('Year')
#Sort the dataset to get a more clear order in the dataset. 
Sort = Index_1[['Type','Assets & Liabilities','Amount']]

#Now we are creating two datasets from the before mentioned table ('Data') where we sort the data tables for corporet and intersectoral pension funds. 
Corporate = Sort[Sort['Type']=='Corporate pension funds'].sort_values(['Year','Type'])
Corp = pd.DataFrame(Corporate).rename(columns={'Amount': 'Corporate pension funds in mio kr.'})
Corp_Reduc = Corp.drop('Type',axis=1)

Intersectoral = Sort[Sort['Type']=='Intersectoral pension funds '].sort_values(['Year','Type'])
Inter = pd.DataFrame(Intersectoral).rename(columns={'Amount': 'Intersectoral pension funds in mio kr.'})
Inter_Reduc = Inter.drop('Type', axis=1)


#We merge the two datasets into one collective table. 
Pension = pd.concat([Inter_Reduc, Corp_Reduc], axis=1)
Pen_Reduc = Pension.drop('Assets & Liabilities', axis =1)










##Table[2]##
Subject_2=Theme[Theme.id == 'MPK13'] 


#we want to insepect the correlation between the share index and pension funds, we finde the share index in the data base. 
Vars_2 = Dst.get_variables(table_id = 'MPK13')
Vars_2.values


# We will be using the OMXC share index with index = 1995, wich is calculated on a monthly basis.   
Data_2 = Dst.get_data(table_id = 'MPK13', variables={'Type':['10'], 'TID':['*']})

#Rename the variables of the dataset.
Data_2.rename(columns={'TYPE':'Type','TID':'Time','INDHOLD':'Share Index'},inplace=True)




Index_2 = Data_2.set_index('Time')


Shared_Index = pd.DataFrame(Index_2)

# Dropping all variables out of range 2000M01-2016M12
Shared_Index.drop(Shared_Index.loc['1996M01':'1999M12','2017M01':'2020M03'].index, inplace=True)

# Now that we use the same timeline as under the pension data, we want to create a new Year list, where the monnthly share_index is represantet as an yearly avrg.
Year_2000 = Shared_Index['Share Index'].iloc[0:11].mean(axis=0)
Year_2001 = Shared_Index['Share Index'].iloc[12:24].mean(axis=0)
Year_2002 = Shared_Index['Share Index'].iloc[24:36].mean(axis=0)
Year_2003 = Shared_Index['Share Index'].iloc[36:48].mean(axis=0)
Year_2004 = Shared_Index['Share Index'].iloc[48:60].mean(axis=0)
Year_2005 = Shared_Index['Share Index'].iloc[60:72].mean(axis=0)
Year_2006 = Shared_Index['Share Index'].iloc[72:84].mean(axis=0)
Year_2007 = Shared_Index['Share Index'].iloc[84:96].mean(axis=0)
Year_2008 = Shared_Index['Share Index'].iloc[96:108].mean(axis=0)
Year_2009 = Shared_Index['Share Index'].iloc[108:120].mean(axis=0)
Year_2010 = Shared_Index['Share Index'].iloc[120:132].mean(axis=0)
Year_2011 = Shared_Index['Share Index'].iloc[132:144].mean(axis=0)
Year_2012 = Shared_Index['Share Index'].iloc[144:156].mean(axis=0)
Year_2013 = Shared_Index['Share Index'].iloc[156:168].mean(axis=0)
Year_2014 = Shared_Index['Share Index'].iloc[168:180].mean(axis=0)
Year_2015 = Shared_Index['Share Index'].iloc[180:192].mean(axis=0)
Year_2016 = Shared_Index['Share Index'].iloc[192:204].mean(axis=0)

Shared_Index['Share Index'].iloc[192:204]





Shared_Frame = pd.DataFrame({'Yearly average share_index': [Year_2000, Year_2001, Year_2002, Year_2003, Year_2004, Year_2005,
                            Year_2006, Year_2007, Year_2008, Year_2009, Year_2010, Year_2011, Year_2012 , Year_2013, Year_2014, Year_2015, Year_2016]
                            , 'Year': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]})
Shared_Frame




Shared_Frame_Reduc = Shared_Frame.set_index('Year')
Shared_Frame_Reduc


# Merging the to dataframes. 
Collective = pd.concat([Pension, Shared_Frame_Reduc], axis=1)

np.corrcoef(Collective['Intersectoral pension funds in mio kr.'], Collective['Yearly average share_index'])
np.corrcoef(Collective['Corporate pension funds in mio kr.'], Collective['Yearly average share_index'])



















#resseting Index for graphical analysis.
Collective.reset_index(inplace = True)



Collective_Year = Collective['Year']
Collective_IP = Collective['Intersectoral pension funds in mio kr.']
Collective_CP = Collective['Corporate pension funds in mio kr.']
Collective_SI = Collective['Yearly average share_index']

#Creating Figure with 2 y-axis to compare pension funds and yearly share index.
fig,ax = plt.subplots()
ax.plot(Collective_Year, Collective_IP, color='red', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Intersectoral pension funds in mio kr.', color='red')

# using twinx to create second axi.
ax2=ax.twinx()
ax2.plot(Collective_Year, Collective_SI, color = 'blue', marker='o')
ax2.set_ylabel('Yearly average share_index', color='blue')
plt.show()





# Now creating a figure with corporate pension funds, and share_index.
#Creating Figure with 2 y-axis to compare pension funds and yearly share index.
fig,ax = plt.subplots()
ax.plot(Collective_Year, Collective_CP, color='red', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Corporate pension funds in mio kr.', color='red')

# using twinx to create second y_aix.
ax2=ax.twinx()
ax2.plot(Collective_Year, Collective_SI, color = 'blue', marker='o')
ax2.set_ylabel('Yearly average share_index', color='blue')
plt.show()







