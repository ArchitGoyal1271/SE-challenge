alter table alooma.engagement alter column createdate type bigint using (createdate::bigint);

select to_char(to_timestamp(createdate/1000),'YYYY-MM-DD') AS ENGAGMENT_DATE
    ,ETYPE
    ,COUNT(*) DAY_COUNT 
        FROM ALOOMA.ENGAGEMENT 
            GROUP BY to_char(to_timestamp(createdate/1000),'YYYY-MM-DD'), ETYPE 
                ORDER BY ENGAGMENT_DATE ASC 
