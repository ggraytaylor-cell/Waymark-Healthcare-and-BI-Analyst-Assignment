# Waymark Assignment for Healthcare Informatics and Business Intelligence Analyst position 
# Developed by Genevieve Taylor, last updated 2025-09-08
# Code Objectives: 
#    Task 1;
#       Use provided patient_id_month_year.csv with variables patient_id and month_year;
#       Transform this dataset from patient_id x month_year level to patient_id x enrollment_start_date x enrollment_end_date level using Python;
#       Save the result as patient_enrollment_span.csv;
#           Answer 1: Report the number of rows in patient_enrollment_span.csv.
#    Task 2;
#       Use provided outpatient_visits_file.csv with variables patient_id, date, outpatient_visit_count;
#       Using patient_enrollment_span.csv and outpatient_visits_file.csv,create a single CSV file with the 5 fields mentioned in the objective;
#       Save the result as result.csv;
#           Answer 2: Report the number of distinct values of ct_days_with_outpatient_visit in result.csv.

import pandas as pd

### Task 1: ###
# Load the patient_id_month_year.csv file
dftsk1 = pd.read_csv("C:\\Users\\ggray\\Desktop\\Python files\\patient_id_month_year.csv")

# Convert month_year to datetime format
dftsk1['month_year'] = pd.to_datetime(dftsk1['month_year'], format= '%m/%d/%Y')

# Reshape with groupby to get min and max date values by patient; create new start/end enrollment date variables based on min/max month_year values
tsk1exprt = dftsk1.groupby('patient_id').agg(enrollment_start_date = ('month_year', 'min'), 
                                                           enrollment_end_date = ('month_year', 'max')).reset_index()

# Question 1: Report the number of rows in patient_enrollment_span.csv
tsk1exprt.shape 
    # answer 1 = 1000 rows 

# Save task 1 file 
tsk1exprt.to_csv("C:\\Users\\ggray\\Desktop\\Python files\\patient_enrollment_span.csv", index=False)

#####################################################################################

### Task 2: ###
# Load the outpatient_visits_file.csv file
dftsk2 = pd.read_csv("C:\\Users\\ggray\\Desktop\\Python files\\outpatient_visits_file.csv")

# Convert visit date to datetime format
dftsk2['date'] = pd.to_datetime(dftsk2['date'], format= '%m/%d/%Y')

# Merge/join on patient ID to combine the two datasets
mergeddf = tsk1exprt.merge(dftsk2, on='patient_id', how = 'inner')

# Filter to outpatient visit dates within enrollment period by patient
    # group by patient, filter between a patient's enrollment start and end dates 
filtereddf = mergeddf.loc[mergeddf['date'].between(mergeddf['enrollment_start_date'], mergeddf['enrollment_end_date'])]

# Find the number of outpatient visits a patient had within the enrollment period and name new column 'ct_outpatient_visits'
  # group by patient ID, sum count values 
filtereddf['ct_outpatient_visits'] = filtereddf.groupby('patient_id')['outpatient_visit_count'].transform('sum')

# Find the number of distinct days within an enrollment period where a patient had 1+ otp visits and name 'ct_days_with_outpatient_visit'
    # group by patient ID, use lambda function to count unique values in 'date' variable by patient
filtereddf['ct_days_with_outpatient_visit'] = filtereddf.groupby('patient_id')['date'].transform(lambda x: x.nunique())

# Select five variables of interest for assignment 
fordedup = filtereddf[['patient_id', 'enrollment_start_date', 'enrollment_end_date', 'ct_outpatient_visits', 'ct_days_with_outpatient_visit']]

# Deduplicate to only keep unique combinations of patient id, enrollment start date, enrollment end date
dedup = fordedup.drop_duplicates()

# Save task 2 file
dedup.to_csv("C:\\Users\\ggray\\Desktop\\Python files\\result.csv", index=False)

# Question 2: Report the number of distinct values of ct_days_with_outpatient_visit in result.csv
dedup['ct_days_with_outpatient_visit'].nunique()
    # answer = 28 unique


####### END SCRIPT #######

