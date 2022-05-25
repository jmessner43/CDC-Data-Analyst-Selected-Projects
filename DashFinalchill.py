#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#load and display the data

df = pd.read_excel(r"C:\Users\JasonMessner\Health Department of Northwest Michigan\CDCF - HDNW - General\Dashboards\Data Sources\HDNW COVID Dashboard 1-11-2022.xlsx")


# In[9]:


df1 = df[['Patient_ID','Patient_Status','INV171', 'Case_Status', 'Case_Disposition', 'Onset_Date', 'Referral_Date', 'Case_Entry_Date','Zip','Sex_at_Birth', 'County', 'Age','Fever','Chills', 'Rigors', 'Muscle_aches__myalgia_', 'Runny_nose__rhinorrhea_', 'Sore_Throat', 'Cough__new_onset_or_worsening', 'Shortness_of_breath__dyspnea_', 'Nausea', 'Vomiting', 'Headaches', 'Abdominal_pain', 'Diarrhea___gt__3_loose_looser', 'Fatigue_Lethargy_Weakness', 'Congestion__Coryza_', 'Encephalopathy_Encephalitis', 'Wheezing', 'Difficulty_Breathing', 'Chest_Pain', 'Loss_of_Taste', 'Loss_of_Smell', 'Evidence_of_Pneumonia', 'Seizure', 'Multi_organ_Dysfunction_Syndr', 'Acute_Respiratory_Distress_Sy', 'Toxic_state__Sepsis_', 'Stroke_Venous_Thromboembolism', 'Multisystem_Inflammatory_Synd',
]]


# In[11]:


from datetime import date, timedelta 
df2 = df1.copy()
end = pd.to_datetime('2000-01-01')
df2['Onset_Date'] = df2['Onset_Date'].fillna(end)
df2['Onset_Date']


# In[12]:


from datetime import date, timedelta 

def renamestat3 (row):
   if  abs(row['Onset_Date'] - row['Referral_Date']) > timedelta(days=90) or row['Onset_Date'] > row['Referral_Date'] or row['Onset_Date'] == row['Referral_Date'] :
        return row['Referral_Date'] 
   if row['Onset_Date'] < row['Referral_Date'] :
      return row['Onset_Date']  

df2['Recovered_Active_Dates'] = df2.apply (lambda row: renamestat3(row), axis=1)


# In[13]:


##Active 

#Time
from datetime import date, timedelta

current_date = date.today().isoformat()
days_before = (date.today()-timedelta(days=145)).isoformat()

df3 = df2.copy()
# create a list of our conditions
conditions = [ (df2['Recovered_Active_Dates'] >= days_before) & (df2['INV171'] != 'Died'), 
   ]

# create a list of the values we want to assign for each condition
values = [1]

# create a new column and use np.select to assign values to it using our lists as arguments
df3['Active'] = np.select(conditions, values)
df4 =df3.copy()


# In[15]:


##Deaths

#Time
from datetime import date, timedelta

current_date = date.today().isoformat()
days_before = (date.today()-timedelta(days=145)).isoformat()

# create a list of our conditions
conditions = [ (df4['INV171'] == 'Died'), 
  (df4['INV171'] != 'Died') ]

# create a list of the values we want to assign for each condition
values = [1,0]

# create a new column and use np.select to assign values to it using our lists as arguments
df4['Dead'] = np.select(conditions, values)


# In[16]:


#Add column indicating whether case is Recovered

#Time
from datetime import date, timedelta

current_date = date.today().isoformat()   
days_before = (date.today()-timedelta(days=145)).isoformat() 

# create a list of our conditions
conditions = [ ( (df4['Recovered_Active_Dates'] < days_before) & (df4['INV171'] != 'Died'))]

# create a list of the values we want to assign for each condition
values = [1]

# create a new column and use np.select to assign values to it using our lists as arguments
df4['Recovered'] = np.select(conditions, values)
df5 =df4.copy()


# In[17]:


#new cases

#Time
from datetime import date, timedelta

current_date = date.today().isoformat()   
days_before = (date.today()-timedelta(days=115)).isoformat() 
df6 = df5.copy()
# create a list of our conditions
conditions = [ (df6['Case_Entry_Date'] == days_before), (df6['Case_Entry_Date'] != days_before)
    ]

# create a list of the values we want to assign for each condition
values = [1, 0]

# create a new column and use np.select to assign values to it using our lists as arguments
df6['new_cases'] = np.select(conditions, values)
df7 = df6.copy()


# In[18]:


#Add column indicating Case for Counting

df8 = df7.copy()
# create a list of our conditions
conditions = [ (df8['Patient_ID'] > 0), (df8['Patient_ID'] < 0)
    ]

# create a list of the values we want to assign for each condition
values = [1, 0]

# create a new column and use np.select to assign values to it using our lists as arguments
df8['Cases'] = np.select(conditions, values)
df9 = df8.copy()


# In[20]:


df10 = df9.copy()
def get_num_people_by_age_category(df10):
    df10["age_group"] = pd.cut(x=df['Age'], bins=[0,9,19,29,39,49,59,69,79,89,99,110],labels=['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99','100+'])
    return df10

# Call function
df10 = get_num_people_by_age_category(df10)


# In[21]:



def get_num_people_by_age_category(df10):
    df10["age_groups"] = pd.cut(x=df['Age'], bins=[0,9,19,29,39,49,59,69,79,89,99,110],labels=[1, 2,3,4,5,6,7,8,9,99,999])
    return df10

# Call function
df10 = get_num_people_by_age_category(df10)


# In[23]:


def renamestat (row):
   if row['Patient_Status'] == 'A' :
      return 'Alive'
   if row['Patient_Status'] == 'D':
      return 'Dead'
 
df10.apply (lambda row: renamestat(row), axis=1)


# In[24]:


df10['Patient_Status'] = df10.apply (lambda row: renamestat(row), axis=1)


# In[26]:


df10['County1'] = df10['County']


# In[27]:


df10['County'] = df10['County'] + ' MI'


# In[28]:


df10['Recovered_Active_Dates'] = pd.to_datetime(df10['Recovered_Active_Dates']).dt.date


# In[29]:


df10['Case_Entry_Date'] = pd.to_datetime(df10['Case_Entry_Date']).dt.date


# In[32]:


def renames (row):
   if row['Case_Disposition'] == 'O' :
      return 'Outpatient'
   if row['Case_Disposition'] == 'I':
      return 'Inpatient'
   if row['Case_Disposition'] == 'D':
      return 'Dead'
   
df10.apply (lambda row: renames(row), axis=1)


# In[33]:


df10['Case_Disposition'] = df10.apply (lambda row: renames(row), axis=1)


# In[34]:


def renamestat (row):
   if row['County1'] == 'Otsego' :
      return '137'
   if row['County1'] == 'Charlevoix':
      return '029'
   if row['County1'] == 'Antrim':
      return '009'
   if row['County1'] == 'Emmet':
      return '047'
df10.apply (lambda row: renamestat(row), axis=1)


# In[35]:


df10['COUNTYFP'] = df10.apply (lambda row: renamestat(row), axis=1)


# In[36]:


df11 = df10[['Patient_ID','Patient_Status','INV171', 'Case_Disposition','Case_Status', 'Onset_Date',
       'Referral_Date', 'Case_Entry_Date', 'Zip', 'Sex_at_Birth', 'County','Age', 'Recovered_Active_Dates', 'Active', 'Recovered', 'new_cases', 'Cases','Dead',
       'age_group', 'age_groups', 'County1','COUNTYFP']]


# In[38]:


df11.to_excel(r'C:\Users\JasonMessner\Health Department of Northwest Michigan\CDCF - HDNW - General\Dashboards\Dashboard Project\Dashboards\DashData41222.xlsx', sheet_name='DashData!', index=False)


# 
# 
# 

# In[40]:


### Symptom Percents Data



dfsymp = df9[[ 'Cases', 'Fever','Chills', 'Rigors', 'Muscle_aches__myalgia_', 'Runny_nose__rhinorrhea_', 'Sore_Throat', 'Cough__new_onset_or_worsening', 'Shortness_of_breath__dyspnea_', 'Nausea', 'Vomiting', 'Headaches', 'Abdominal_pain', 'Diarrhea___gt__3_loose_looser', 'Fatigue_Lethargy_Weakness', 'Congestion__Coryza_', 'Encephalopathy_Encephalitis', 'Wheezing', 'Difficulty_Breathing', 'Chest_Pain', 'Loss_of_Taste', 'Loss_of_Smell', 'Evidence_of_Pneumonia', 'Seizure', 'Multi_organ_Dysfunction_Syndr', 'Acute_Respiratory_Distress_Sy', 'Toxic_state__Sepsis_', 'Stroke_Venous_Thromboembolism', 'Multisystem_Inflammatory_Synd'
]]


# In[42]:


d = {}
for column in dfsymp[[ 'Fever','Chills', 'Rigors', 'Muscle_aches__myalgia_', 'Runny_nose__rhinorrhea_', 'Sore_Throat', 'Cough__new_onset_or_worsening', 'Shortness_of_breath__dyspnea_', 'Nausea', 'Vomiting', 'Headaches', 'Abdominal_pain', 'Diarrhea___gt__3_loose_looser', 'Fatigue_Lethargy_Weakness', 'Congestion__Coryza_', 'Encephalopathy_Encephalitis', 'Wheezing', 'Difficulty_Breathing', 'Chest_Pain', 'Loss_of_Taste', 'Loss_of_Smell', 'Evidence_of_Pneumonia', 'Seizure', 'Multi_organ_Dysfunction_Syndr', 'Acute_Respiratory_Distress_Sy', 'Toxic_state__Sepsis_', 'Stroke_Venous_Thromboembolism', 'Multisystem_Inflammatory_Synd'
]]:
    
    # Select column contents by column  
    # name using [] operator
 
        d[column]= dfsymp.groupby(column)['Cases'].count().reset_index()
        d[column]['Percentage']=100 * d[column]['Cases']  / d[column]['Cases'].sum()


# In[43]:


percents = pd.concat(d.values(), ignore_index=True)


# In[45]:


percentsm = percents.copy()


# In[46]:



for column in percentsm[['Fever','Chills', 'Rigors', 'Muscle_aches__myalgia_', 'Runny_nose__rhinorrhea_', 'Sore_Throat', 'Cough__new_onset_or_worsening', 'Shortness_of_breath__dyspnea_', 'Nausea', 'Vomiting', 'Headaches', 'Abdominal_pain', 'Diarrhea___gt__3_loose_looser', 'Fatigue_Lethargy_Weakness', 'Congestion__Coryza_', 'Encephalopathy_Encephalitis', 'Wheezing', 'Difficulty_Breathing', 'Chest_Pain', 'Loss_of_Taste', 'Loss_of_Smell', 'Evidence_of_Pneumonia', 'Seizure', 'Multi_organ_Dysfunction_Syndr', 'Acute_Respiratory_Distress_Sy', 'Toxic_state__Sepsis_', 'Stroke_Venous_Thromboembolism', 'Multisystem_Inflammatory_Synd'
]]:
    
    # Select column contents by column  
    # name using [] operator
      
    percentsm[column] = column + '_' + percentsm[column]


# In[47]:



for column in percentsm[['Fever','Chills', 'Rigors', 'Muscle_aches__myalgia_', 'Runny_nose__rhinorrhea_', 'Sore_Throat', 'Cough__new_onset_or_worsening', 'Shortness_of_breath__dyspnea_', 'Nausea', 'Vomiting', 'Headaches', 'Abdominal_pain', 'Diarrhea___gt__3_loose_looser', 'Fatigue_Lethargy_Weakness', 'Congestion__Coryza_', 'Encephalopathy_Encephalitis', 'Wheezing', 'Difficulty_Breathing', 'Chest_Pain', 'Loss_of_Taste', 'Loss_of_Smell', 'Evidence_of_Pneumonia', 'Seizure', 'Multi_organ_Dysfunction_Syndr', 'Acute_Respiratory_Distress_Sy', 'Toxic_state__Sepsis_', 'Stroke_Venous_Thromboembolism', 'Multisystem_Inflammatory_Synd'
]]:

    percentsm[column] = percentsm[column].replace(np.nan, '')
    


# In[48]:


columns = ['Fever','Chills', 'Rigors', 'Muscle_aches__myalgia_', 'Runny_nose__rhinorrhea_', 'Sore_Throat', 'Cough__new_onset_or_worsening', 'Shortness_of_breath__dyspnea_', 'Nausea', 'Vomiting', 'Headaches', 'Abdominal_pain', 'Diarrhea___gt__3_loose_looser', 'Fatigue_Lethargy_Weakness', 'Congestion__Coryza_', 'Encephalopathy_Encephalitis', 'Wheezing', 'Difficulty_Breathing', 'Chest_Pain', 'Loss_of_Taste', 'Loss_of_Smell', 'Evidence_of_Pneumonia', 'Seizure', 'Multi_organ_Dysfunction_Syndr', 'Acute_Respiratory_Distress_Sy', 'Toxic_state__Sepsis_', 'Stroke_Venous_Thromboembolism', 'Multisystem_Inflammatory_Synd'
]

percentsm['symptoms'] = percentsm[columns].sum(axis=1).astype(str)


# In[49]:


p = percentsm.copy()
p[['Symptoms', 'Answers']]=p.symptoms.apply(
   lambda x: pd.Series(str(x).rsplit("_",1)))


# In[50]:


percentsfin = p[['Symptoms', 'Answers', 'Cases', 'Percentage']]


# In[51]:


percentsfin.to_excel(r'C:\Users\JasonMessner\Health Department of Northwest Michigan\CDCF - HDNW - General\Dashboards\Dashboard Project\Dashboards\DashDataPercents2.xlsx', sheet_name='Percents', index=False)


# In[ ]:





# In[ ]:




