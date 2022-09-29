import datetime
import pandas as pd
from datetime import datetime

pd.set_option('display.max_rows', 2643)

def calculateyob(yob):
    current_year = datetime.now().year
    age = yob - current_year
    age = abs(age)
    return int(age)

def calculateDiabetesFirstDiagnose(yob, year_diagnosis):
    year_diagnose = int(yob) - int(year_diagnosis)
    return abs(year_diagnose)

df_demographic = pd.read_csv(
    './data/demographics.csv', 
    index_col='patientuid'
)

df_measurements = pd.read_csv(
    './data/measurements.csv', 
    sep='|', 
    on_bad_lines='warn',
    index_col='patientuid'
)

df_demographic = df_demographic.sort_values(['patientuid'])

df_demographic_i = df_demographic[['zip_code', 'income']]

df_measurements_i = df_measurements[['label', 'value', 'date']]

df = pd.DataFrame(
    {
        'patientuid': [0], 
        'age': [0], 
        'sex': [0], 
        'income': [0], 
        'zip_code': [0], 
        'hef_1hour': [0], 
        'hef_24hour': [0], 
        'diabetes': [-99]
    }
)


# Ordenamos por 'patientuid' desde 0 de manera ascendente.
df_measurements_i = df_measurements_i.sort_values(['patientuid'], axis=0, ascending=True)


df = pd.merge(df_demographic_i, df_measurements_i, left_index=True, right_index=True)

df = df.sort_values('patientuid')

# Recogemos todas las filas donde este el año de nacimiento.
yob_search = df.where(df.label == 'YOB')
yob_search = yob_search.dropna()

df2 = pd.DataFrame()
df2.index.name = 'patientuid'

for i, row in yob_search.iterrows():
    df2.at[i, 'age'] = calculateyob(int(row['value']))
    df2.at[i, 'zip_code'] = row['zip_code']
    df2.at[i, 'income'] = row['income']
    

df2 = df2.astype(int)

# looking for men values
# df_measurements_i.where(df_measurements_i.value == 'Male').dropna().sort_values('patientuid')

for i, row in df_measurements_i.where(df_measurements_i.value == 'Male').dropna().sort_values('patientuid').iterrows():
    df2.at[i, 'sex'] = row['value']
    
# The same but for 'Man'
for i, row in df_measurements_i.where(df_measurements_i.value == 'Man').dropna().sort_values('patientuid').iterrows():
    df2.at[i, 'sex'] = row['value']
    
# looking for female values
# df_measurements_i.where(df_measurements_i.value == 'Male').dropna().sort_values('patientuid')
for i, row in df_measurements_i.where(df_measurements_i.value == 'Female').dropna().sort_values('patientuid').iterrows():
    df2.at[i, 'sex'] = row['value']
    
# The same but for 'Woman'
for i, row in df_measurements_i.where(df_measurements_i.value == 'Woman').dropna().sort_values('patientuid').iterrows():
    df2.at[i, 'sex'] = row['value']


df2.fillna('Unkown')

hef_search = df.where(df.label == 'Heart Ejection Fraction').dropna().sort_values('patientuid')

# diabetes: must be equal to the age when the first Diabetes diagnoses was registered for that patient, 
# -99 if no Diabetes diagnosis is present for that patient.

diabetes_search = df.where((df.label == 'Diagnosis') & (df.value == 'Diabetes')).dropna().sort_values('patientuid')

# Iterating hef search for insert into df2 values
for i, row in hef_search.iterrows():
    df2.at[i, 'hef_1hour'] = int(row['value'])
    df2.at[i, 'hef_24hour'] = int(row['value'])
    

# Fill the DF with -99 for diabetes first, then replace with age if diabetes
df2['diabetes'] = -99


# Search in Diabetes diagnosis and change -99 per age if diagnosis of diabetes
for i, row in diabetes_search.iterrows():
    yob = int(yob_search.loc[i]['value'])
    year_diagnose = diabetes_search.loc[i]['date'].split('-')[0]
    df2.at[i, 'diabetes'] = calculateDiabetesFirstDiagnose(yob, year_diagnose)
    

df2.fillna(-99, inplace=True)
df2 = df2.astype({'hef_1hour': 'int32', 'hef_24hour': 'int32'})
df2.to_csv('./data/output.csv')