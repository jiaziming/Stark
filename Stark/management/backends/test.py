#!/usr/bin/python
# -*-coding:utf-8-*-
import pymysql

select_config = {
    "host": "localhost",
    "user": "root",
    "password": "ws@2017",
    "database": "rpt",
    "charset": "utf8"
}

update_db_config = {
    "host": "172.16.103.1",
    "user": "root",
    "password": "",
    "database": "ws_manage",
    "charset": "utf8"
}

db = pymysql.connect(**select_config)

cursor = db.cursor()
select_sql = ('''
                select t1.product_name from market_product t1
                left join
                (select product_name,click_user from rpt_ieh_sougu_overall_daichao where etl_date=date_format(now(),'%Y%m%d')) t2
                on
                t1.product_name = t2.product_name
                left join
                (select product_name,sum(amount) amount from market_product_recharge where status=1 group by product_name) t3
                on
                t1.product_name = t3.product_name
                left join
                (select product_name,sum(total) total from
                (select t1.etl_date,t1.product_name,sum(t1.click_user)*t2.price as total from
                rpt_ieh_sougu_overall_daichao t1
                inner join
                market_price_perday t2
                on t1.etl_date = t2.date
                and t1.product_name = t2.product_name
                group by t1.etl_date,t1.product_name) v where etl_date>='20190617' group by product_name) t4
                on t1.product_name = t4.product_name
                left join
                (select * from market_price_perday where date=date_format(now(),'%Y%m%d')) t5
                on t1.product_name = t5.product_name
                where t1.init_balance+ifnull(t3.amount,0)-ifnull(t4.total,0) < 0
            ''')

data = cursor.execute(select_sql)

print(data)