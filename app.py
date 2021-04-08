from flask import Flask
import decimal
from os import stat, path
import numpy as np
from flask import Flask, render_template, url_for
import json
import pymysql
from datetime import timedelta
from datetime import datetime
import pandas as pd
import xlwt as xlwt
from flask import jsonify
from flask import request
import warnings
import openpyxl
import xlrd
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'

def save():
    con = pymysql.connect(host='192.168.86.79', user='wanjunsheng', passwd='df2932141LFDF', db='warehouse',
                          port=3307, charset='utf8')
    cur = con.cursor()
    # sql_updata='UPDATE ueb_warehouse_shelf_sku_map  SET shelf_type = 99 WHERE shelf LIKE "%BGA%";'
    sql = 'SELECT	warehouse_code,	purchase_order_no,	storage_position,	sku,	actual_num,	CASE		WHEN post_code_start_time IS NOT NULL 		AND post_code_end_time IS NOT NULL 		AND quality_time IS NOT NULL 		AND upper_start_time IS NOT NULL 		AND upper_end_time IS NULL THEN			"SJZ" 			WHEN post_code_start_time IS NOT NULL 			AND post_code_end_time IS NOT NULL 			AND quality_time IS NOT NULL 			AND paragraph != 11 			AND upper_start_time IS NULL THEN				"DSJ" 				WHEN post_code_start_time IS NOT NULL 				AND post_code_end_time IS NOT NULL 				AND quality_time IS NOT NULL 				AND paragraph = 11 				AND upper_start_time IS NULL THEN					"DGNZJ" 					WHEN post_code_start_time IS NULL THEN					"DTM" ELSE "else" 				END AS type,				cast(ROUND( ( unix_timestamp( now()) - unix_timestamp( quality_start_time ) ) / 3600, 2 ) as DECIMAL  ) AS s 			FROM				ueb_quality_warehousing_record 			WHERE				paragraph != 5 				AND purchase_order_no NOT LIKE "ABD%" 				AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 			GROUP BY				purchase_order_no,				sku,				warehouse_code UNION			SELECT				warehouse_code,				"RK" AS purchase_order_no,				car_no AS storage_position,				"RK" AS sku,				box_number AS quality_num,				"DRK" AS type,				cast(ROUND( ( unix_timestamp( now()) - unix_timestamp( add_time ) ) / 3600, 2 ) as DECIMAL   )AS s 			FROM				ueb_express_receipt 			WHERE				STATUS = 1 				AND warehouse_type = 1 				AND is_abnormal = "2" 			AND is_quality = "2" 	AND is_end = "1"'
    sql_fba = 'select * from (select warehouse_code,order_id,case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DJH"when pay_time >0 and wait_pull_time =0  then "DLD"ELSE "else" end as `status`,CAST(order_product_number AS SIGNED) as `order_product_number`,ROUND(( unix_timestamp(now()) - greatest(pay_time,wait_pull_time,pick_time,choice_time,pack_time) ) / 3600, 2 ) AS time from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and order_id like "FB%"  union    select warehouse_code,order_id,case when wh_order_status=-1 then "DPK" when wh_order_status in (1)then  "DFPLD" when wh_order_status in (2)then  "DLD" else "else" end  as `status`,CAST(sum(order_product_number) AS SIGNED) as `order_product_number`,case  when wh_order_status=-1 then ROUND(( unix_timestamp(now()) - paytime_int) / 3600, 2 )  when wh_order_status in (1,2) then     ROUND(( unix_timestamp(now()) - wait_pull_time) / 3600, 2 ) else "else" end  AS time       from ueb_order where order_id like "FB%" and wh_order_status in(-1,1,2)  group by warehouse_code,order_id) a  order by time  DESC'
    sql_xb = 'select * from (select warehouse_code,order_id,case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DJH"when pay_time >0 and wait_pull_time =0  then "DLD"ELSE "else" end as `status`,CAST(order_product_number AS SIGNED) as `order_product_number`,ROUND(( unix_timestamp(now()) - greatest(pay_time,wait_pull_time,pick_time,choice_time,pack_time) ) / 3600, 2 ) AS time from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and 	 batch_no NOT LIKE "%-6-%"  union   select warehouse_code,order_id,case when wh_order_status=-1 then "DPK" when wh_order_status in (1)then  "DFPLD" when wh_order_status in (2)then  "DLD" else "else" end  as `status`,CAST(sum(order_product_number) AS SIGNED) as `order_product_number`,case  when wh_order_status=-1 then ROUND(( unix_timestamp(now()) - paytime_int) / 3600, 2 )  when wh_order_status in (1,2) then     ROUND(( unix_timestamp(now()) - wait_pull_time) / 3600, 2 ) else "else" end  AS time       from ueb_order  WHERE batch_type != 6 and wh_order_status < 9  group by warehouse_code,order_id) a  order by time  DESC'
    cur.execute(sql)
    
    see = cur.fetchall()
    print(see)
    cur.close()
    see2 = xlrd.open_workbook('1.xlsx')
    # a1 = see2['warehouse_code']
    # a2 = see2['purchase_order_no']
    print(see2)
    # print(a1,a2)

save()



if __name__ == '__main__':
    app.run()

