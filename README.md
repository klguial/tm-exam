Outputs of the Data Engineering Exam
---

### Code Structure
We have 3 main parts:
1. `TM_1_algo.ipynb` (Algorithmic Problem)
2. `TM_2_etl.py` (ETL)
3. `TM_2_app.py` (Web app)

### ETL
We have /data/dailycheckins.csv data containing logs of hours spent of a user on a project.

Cleaned data is then loaded to a table in BigQuery using `google-cloud-bigquery` API.

### Web app
We use the streamlit library to create a web dashboard showing the daily checkins data that is able to filter per user.
See deplyed app here [Daily Checkins Web](https://tm-exam-43umqmr5jh2ppyf5ika3sh.streamlit.app/).

![ETL diagram](/img/web_app.png "")

### Authentication
We use a service account to connect to the BigQuery API programatically which is stored in a **secrets.toml** file.

### Follow-up questions
1. <em>If the data is to be ingested periodically, what changes will you make to your current
approach?</em>

For periodic ingestion of data, it is a best to organize folder structure of raw data pull from a source by `year/month/day/filename.csv`.

Then another job would clean, validate, and load the data into our target table (BigQuery).

A log file containing the file_paths, status of data pull, and status of data load is required to keep track of where things are. With this method, in case of failure, we can easily reprocesses backlogs without affecting the current jobs.


2. <em>Draw a data architecture showing different components of your ETL process.</em>

This is a simple ETL where the data is already in a CSV file and no extraction for API pull or integration to a 3P service is needed.

Transform is done by running a python script to clean the data and ensure that the data types are correct and assigning a unique ID for each record.

Then data is loaded to BigQuery.

![ETL diagram](/img/ETL_diagram.png "")


3. <em>How will you verify correctness of data?</em>

For this particular case, we can check if the daily number of work hours per user does not exceed 24hrs.