# code-test-b

# Coding exercise for AIO candidates

Please clone the repo, creat a new branch with your username and push your work after finished IN A NEW REPO in github.
Share with us the new repo you created so we can take a look at your work.

You are provided with a dataset containing some clinical information about patients that you can find in two tables:

`./data/demographics.csv`
`./data/measurements.csv`

## TASK 1:

The task is to build, using python, a new table with the following structure:

```
patientuid: Unique ID of a single patient.
age: Age in years of the patient when the last measurement of this patient (in measurements.csv) is available.
sex: Sex of the patient.
income: Income of the patient.
zip_code: Zip code of the patient.
hef_1hour: average of Heart Ejection Fraction values in the last hour (using last measurement present for that patient as reference)
hef_24hour: average of Heart Ejection Fraction values in the last 24 hours (using last measurement present for that patient as reference)
diabetes: must be equal to the age when the first Diabetes diagnoses was registered for that patient, -99 if no Diabetes diagnosis is present for that patient.
```
Save the python code you create as a ./src/task_1.py file ready to be run from terminal with `python task_1.py`
Save the new table as `./data/output.csv`.

## Task 2:

Repeat the same exercise but now use sqlite.db as the source, create the required SQL queries running them from python script

Save the python code (including SQL pieces of code) in a file named ./src/task_2.py
Save the new table as `output` in the sqlite.db file.

**This exercise is expected to be finished in less than 4 hours. We just want to see how do you approach the ETL problem and if you are able to produce ready-to-use code and work in a remote team.**

