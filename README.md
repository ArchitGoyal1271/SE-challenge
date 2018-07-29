# SE-challenge

Task
The task is to demonstrate the capability to connect to hubspot api and fetch all the
engagements. Each API call extracts 250 records (max limit).Offset elements is used
to page through results. 

Packages Used
Below are the packages used:
a) requests
b) psycopg2
c) json
d) matplotlib
e) time

Python version used is 3.6.6 on Windows. Additionally, we are using Postgres 10 to load data from API to database.

Issues faced:

Datetime conversion in python was failing due to bug reported in python version 3.6. Here is the link to the bug
(https://bugs.python.org/issue30684). Alternative was to load the date as epoch time and convert into human-readable
dates in Postgres



