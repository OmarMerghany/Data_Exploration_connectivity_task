#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
import seaborn as sns
import sys

warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# Loading Data

# In[2]:


df_data = pd.read_csv('connectivity_task.csv')


# In[3]:


df_data.head()


# In[4]:


df_data.info()


# * Number of null values

# In[5]:


nan_values = len(df_data) - df_data.count()
print(nan_values)


# # Data Cleaning

# * Drop rows with nan values at event_time & event_type

# In[6]:


print('number of rows that have nan in event_time column: ', len(df_data[df_data['event_time'].isnull()]))
rows_with_nan_eventime = df_data[df_data['event_time'].isnull()]
# drop rows with nan values in event_time
df_data = df_data[df_data['event_time'].notna()]
print('number of rows without nan in event_time',len(df_data))


# * Convert event_time from string to pandas datetime

# In[7]:


df_data["event_time"]= pd.to_datetime(df_data["event_time"],  format= "%Y-%m-%d %H:%M:%S") 


# * set event_time to be the index

# In[8]:


df_data.set_index('event_time', inplace=True)


# In[9]:


df_data.head()


# In[10]:


df_data['asset_type'].unique() 


# In[11]:


df_data.describe(include='all')


# In[12]:


df_data.describe(include = ['O'])


# # Data Visualization

# In[13]:


event_type_distribution = df_data.groupby('event_type').size()
print(event_type_distribution)
labels = ["Connected", "Disconnected"]
fig1, (ax1,ax2) = plt.subplots(1,2,figsize=(10,10))
ax1.title.set_text('event_type_distribution')
ax1.pie(event_type_distribution, labels=labels, autopct='%1.1f%%')

organisations_distribution = df_data.groupby('organisation_name').size()
labels2 = df_data['organisation_name'].unique()
ax2.title.set_text('organisations_distribution')
ax2.pie(organisations_distribution, labels=labels2, autopct='%1.1f%%')


# ### Show time window of the data

# In[14]:


start_date = df_data.index.min()
end_date = df_data.index.max()
difference_of_date = end_date - start_date
print('the time window of the data is: ', difference_of_date)
print('First record starts at:', start_date)
print('Last record ends at: ', end_date)


# # Deep dive into the Data

# In[15]:


# Split data by organisation_name
orgs = df_data['organisation_name'].unique()
plt.figure(figsize=(15, 3))
colors = ['b', 'c', 'y', 'm', 'r']

for organisation in orgs:    
    org_data = df_data.loc[df_data['organisation_name']==organisation]
    places_within_org = org_data['place_name'].unique()
    print('*******************************************************************************************************************')
    print('Organisation name is: ', organisation)
    print(org_data.describe(include = ['O']))
    
    org_distribution = org_data.groupby('place_name').size()
    labels2 = places_within_org
    if(organisation == 'Taylor, Flores and Douglas'):
        fig1, ax2 = plt.subplots(figsize=(15,20))
    else:
        fig1, ax2 = plt.subplots(figsize=(15,5))
    plc_titles = 'Places within Organisation:' + organisation
    ax2.title.set_text(plc_titles)
    ax2.pie(org_distribution, labels=labels2, autopct='%1.1f%%')
    
    for place in places_within_org:
        print('---------------------------------------------------------------------------------')
        print('\nplace: ', place)
        plc_data = org_data.loc[org_data['place_name']==place]
        asset_names_within_place = plc_data['asset_name'].unique()
        
        plc_distribution = plc_data.groupby('asset_name').size()
        labels2 = asset_names_within_place
        
        fig1, ax2 = plt.subplots(figsize=(15,5))
        asset_titles = 'asset_names within Place:' + place
        ax2.title.set_text(asset_titles)
        ax2.pie(plc_distribution, labels=labels2, autopct='%1.1f%%')
        
#         print('number of asset_name within_place is :',len(asset_names_within_place))
        print('asset_names_within_place: ', asset_names_within_place)
        plt.figure(figsize=(15, 3))
        asset_types_within_place = plc_data['asset_type'].unique()
        asset_names_within_place = plc_data['asset_name'].unique()
#         module_id__within_place = plc_data.groupby('module_id').size()
        module_id__within_place = plc_data['module_id'].unique()
        print('asset_types_within_place: ', asset_types_within_place)
        print('module_id__within_place: ', module_id__within_place)
        for asset_name in asset_names_within_place:
            asset_data = plc_data.loc[plc_data['asset_name']==asset_name]
            asset_data['event_type'] = asset_data['event_type'].replace(['Connected','Disconnected'],[1,0])
            
            graph_title = 'Organisation name is: '+ str(organisation)+', place: '+str(place) + ' with asset_name: '                    + str(asset_names_within_place) + ' and asset_types: '+ str(asset_types_within_place)
            plt.title(graph_title)
            asset_types_within_asset_name = asset_data['asset_type'].unique()
            for asset_type in asset_types_within_asset_name:
                asset_type_data = asset_data.loc[asset_data['asset_type']==asset_type]
                if(asset_type == 8):
                    clr = 'b'
                elif(asset_type == 5):
                    clr = 'r'
                else:
                    clr = 'y'
                plt.scatter(asset_type_data.index, asset_type_data['event_type'], color=clr)
                plt.legend(asset_types_within_place)


# # Conclusion

# 1. The data represents 3 Organisations 
# 2. Each Organisation has unique places
# 3. Each place within single Organisation contains one or more asset_name and one or more asset_type
