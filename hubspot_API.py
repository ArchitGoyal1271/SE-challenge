##base url
base = 'https://api.hubapi.com'

##engagement end point

endpoint = '/engagements/v1/engagements/paged'

##hapikey

key = {'hapikey':'demo','limit':250}


import requests as rs
import psycopg2
import datetime,json
import matplotlib.pyplot as plt

## Connecting to the postgress server on local host
try:
    conn = psycopg2.connect("dbname=postgres user=postgres host=localhost password=test")
    cur = conn.cursor()
    print('Connection to Postgress Completed')
except:
    print ("I am unable to connect to the database")

'''
Table engagement is created by the below function under alooma schema. We are extracting
createdate, type, status and offset. Offset is added to ensure that we are fetching
all the engagements
(https://developers.hubspot.com/docs/methods/engagements/get-all-engagements)

'''

def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS alooma.engagement( createdate varchar ,etype varchar,e_status varchar,e_offset varchar)")
    conn.commit()

create_table()

'''
Json elements  like created date, type, status and offset is extracted from the json. The extracted elements are used to generate query results
'''
def insert_data():
    try:
        url = rs.get(base+endpoint,params=key)
        data = url.json()
        req_data = data['results']
        for i in range(0,len(req_data)):
            dic = req_data[i]['engagement']
            createdate = dic['createdAt']
            note = dic['type']
            status = dic['active']
            offset = data['offset']
          
            cur.execute('insert into alooma.engagement(createdate, etype, e_status, e_offset) values( %s, %s, %s, %s)' ,(createdate,note,status,offset))
            conn.commit()
            

        if data['hasMore']==True :
            key['offset']=data['offset']
            insert_data()
        
        
        else:
            print('Data Insert completed')
            
    except:
        print('Error in parsing')
        conn.close()
        cur.close()

insert_data()







def graph_data():
    cur.execute('alter table alooma.engagement alter column createdate type bigint using (createdate::bigint)');
    cur.execute('''select to_char(to_timestamp(createdate/1000),'YYYY-MM-DD') AS ENGAGMENT_DATE
,ETYPE,COUNT(*) DAY_COUNT FROM ALOOMA.ENGAGEMENT GROUP BY to_char(to_timestamp(createdate/1000),'YYYY-MM-DD'), ETYPE ORDER BY ENGAGMENT_DATE ASC ''')
    data = cur.fetchall()
    
    xaxis1=[]
    yaxis1=[]
    xaxis2=[]
    yaxis2=[]
    xaxis3=[]
    yaxis3=[]
    xaxis4=[]
    yaxis4=[]
    for rows in data:
        print (rows)
        if rows[1] =='NOTE' :
            xaxis1.append(rows[0])
            yaxis1.append(rows[2])
        elif rows[1]=='TASK':
            xaxis2.append(rows[0])
            yaxis2.append(rows[2])

        
            
            
    plt.bar(xaxis1,yaxis1,label = 'NOTE',color = 'r')
    plt.bar(xaxis2,yaxis2,label = 'TASK',color = 'g')

    
    
    
    plt.xlabel('date')
    plt.ylabel('count')
    plt.legend()
    plt.show()
    conn.close()
    cur.close()

graph_data()
