from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import os
import sqlite3
from .forms import FormStatus
from .forms import FormSetID
import django_filters
from .filter import *

def template_test(request):
    return render(request, 'example.html')

def order(request):

    db = sqlite3.connect('mainApp.db')
    cursor = db.cursor()

    ###Show 訂單列表
    sql = "SELECT * FROM order_list"
    cursor.execute(sql)
    res = cursor.fetchall()
    orderlist = list(res)

    ### 輸入order id 

    if request.method == 'POST':
        form2 = FormSetID(request.POST)
        if form2.is_valid():
            print('form2 valid')
            set_orderid = request.POST.get('set_orderid')
            print('order id:',set_orderid)
    else:
        form2 = FormSetID()
    
    

    ###更改 訂單狀態
    form = FormStatus()
    if request.method == "POST":
        form = FormStatus(request.POST)		
        if form.is_valid():
            response = request.POST.get('response')
            print('form valid Response:',response)

            if response =='已審核':
                replysql = "UPDATE order_list SET status = '已審核' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()

            elif response == '備貨中':
                print('按備貨中')
                replysql = "UPDATE order_list SET status = '備貨中' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()

            elif response == '已達包裹中心':
                replysql = "UPDATE order_list SET status = '已達包裹中心' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()

            elif response == '已達物流中心':
                replysql = "UPDATE order_list SET status = '已達物流中心' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()
                
            elif response == '已出貨':
                replysql = "UPDATE order_list SET status = '已出貨' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()
                
            elif response == '已到達':
                replysql = "UPDATE order_list SET status = '已到達' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()

            elif response == '已辦理退貨':
                replysql = "UPDATE order_list SET status = '已辦理退貨' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()

            elif response == '退貨審核未通過':
                replysql = "UPDATE order_list SET status = '退貨審核不通過' WHERE order_id LIKE ?"
                cursor.execute(replysql, set_orderid)
                db.commit()
            
        else:
            form = FormStatus()
            print('fail')

    context = {'orderlist':orderlist, 'form':form, 'form2':form2}
    return render(request, 'order.html', context)

def product(request):
    db = sqlite3.connect('mainApp.db')
    cursor = db.cursor()

    ###Show 訂單列表
    sql = "SELECT * FROM product"
    cursor.execute(sql)
    res = cursor.fetchall()
    product_info = list(res)
    # product_info = ''
    
    pid = filterSetID()
    ### 輸入order id 
    if request.method == 'POST':
        pid = filterSetID(request.POST)
        if pid.is_valid():
            print('Product query valid')
            set_productid = request.POST.get('set_productid')
            print('product id:',set_productid)

            id_replysql = "SELECT * FROM product WHERE product_id={}".format(set_productid)
            print(id_replysql)
            cursor.execute(id_replysql)
            res = cursor.fetchall()
            product_info = list(res)

        else:
            pid = filterSetID()
    
    all_info = []
    reorder_points = []
    preorder_days = []

    pcategory = filterCategory()
    if request.method == "POST":
        pcategory = filterCategory(request.POST)		
        if pcategory.is_valid():
            response = request.POST.get('response')
            print(response)
            
            #沒選類別時
            replysql = "SELECT * FROM product WHERE product_category='{}'".format(response)
            cursor.execute(replysql)
            res = cursor.fetchall()
            product_info = list(res)
            for p in product_info:
                print(p)
                numberOrder_sql = "SELECT COUNT(product) FROM order_list WHERE product='{}'".format(p[1])
                cursor.execute(numberOrder_sql)
                numberOfOrder = cursor.fetchall()[0][0]
                print(numberOfOrder)   

                day_sql = "SELECT COUNT(DISTINCT order_time) FROM order_list"
                cursor.execute(day_sql)
                numberOfDay = cursor.fetchall()[0][0]
                
                #再訂購點 = 平均日需求×訂貨天數+安全儲備量
                daily_demand = round(numberOfOrder/numberOfDay, 2)
                reorder_point = round(daily_demand*p[8]+p[9])
                print(reorder_point)
                reorder_points.append(reorder_point)

                #預訂日期 = (存貨數量-再訂購點)/平均日需求
                preorder_day = round((p[6]-reorder_point) / daily_demand,2)
                preorder_days.append(preorder_day)
                
        else:
            pcategory = filterCategory()
            print('fail')
    all_info = zip(product_info, reorder_points)
    all_info2 = zip(product_info, preorder_days)


    context= {'product_info':product_info, 'pcategory':pcategory, 'pid':pid, 
    'reorder':reorder_points, 
    'all_info':all_info, 'all_info2':all_info2}

    return render(request, 'product.html', context)

    