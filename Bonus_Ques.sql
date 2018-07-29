'''
We created a dim_dates table which basically consist of dates between min and max engagement date.
Summary engagement is created out of grouping the engagements by created date'''



select engagement_date
    ,total_count_per_day
    ,round(avg(total_count_per_day) over(order by dates asc rows between 13 preceding and current row),2)
        from summary_engagement right join dim_dates
            on engagement_date = dates
                order by engagement_date asc;  
                
