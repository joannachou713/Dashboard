from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import os
import sqlite3
from .forms import FormStatus
from .forms import FormSetID
import django_filters
from .filter import *
import math
import datetime

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
    i=0
    ###Show 訂單列表
    sql = "SELECT * FROM product"
    cursor.execute(sql)
    res = cursor.fetchall()
    product_info = list(res)
    # product_info = ''
    print(request.POST)
    
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
    preorder_info = []

    pcategory = filterCategory()
    if request.method == "POST":
        pcategory = filterCategory(request.POST)		
        if pcategory.is_valid():
            response = request.POST.get('response')
            # print(response)
            
            #沒選類別時
            replysql = "SELECT * FROM product WHERE product_category='{}'".format(response)
            cursor.execute(replysql)
            res = cursor.fetchall()
            product_info = list(res)
            for p in product_info:

                preorder_combo = []
                p_status = ''
                print(p)
                numberOrder_sql = "SELECT COUNT(product) FROM order_list WHERE product='{}'".format(p[1])
                cursor.execute(numberOrder_sql)
                numberOfOrder = cursor.fetchall()[0][0]
                # print(numberOfOrder)   

                day_sql = "SELECT COUNT(DISTINCT order_time) FROM order_list"
                cursor.execute(day_sql)
                numberOfDay = cursor.fetchall()[0][0]
                
                if numberOfOrder == 0:
                    numberOfOrder = 1
                if numberOfDay == 0:
                    numberOfDay = 1
            

                #再訂購點 = 平均日需求×訂貨天數+安全存貨量
                daily_demand = round(numberOfOrder/numberOfDay, 2)
                reorder_point = round(daily_demand*p[8]+p[9])
                # print(reorder_point)
                reorder_points.append(reorder_point)

                #最佳訂購量 = ((2*需求*單位訂購成本)/單位持有成本)^1/2
                purchase_quantity = round(math.sqrt(2*numberOfOrder*p[4]/p[5]))

                #購買成本 = 需購數量*購買成本
                purchase_cost = purchase_quantity*p[4]
                
                #預訂日期 = (存貨數量-再訂購點)/平均日需求
                preorder_day = round((p[6]-reorder_point) / daily_demand,2)
                
                #訂購狀況
                if purchase_quantity <= 0:
                    p_status = '無須訂購'
                elif purchase_quantity > 0:
                    p_status = '需要訂購'
                elif preorder_day <= 0:
                    p_status = '已達再訂購點'
                
                replysql = "UPDATE product SET p_status = '{}' WHERE product_id = {}".format(p_status, p[0])
                cursor.execute(replysql)
                db.commit()

                preorder_combo.append(purchase_quantity)
                preorder_combo.append(purchase_cost)
                preorder_combo.append(p_status)
                preorder_combo.append(preorder_day)
                
                preorder_info.append(preorder_combo)

        else:
            pcategory = filterCategory()
            print('fail')
    
    
    # 下訂單
    for r in request.POST:
        if 'btn' in r:
            index = i
            print(request.POST)
            try:
                index_r = 0
            
                for r in request.POST:
                    if index_r == index-2:
                        purchasing_c = r
                        index_r = index_r+1
                        idsql = "SELECT COUNT(purchasing_id) FROM purchasing"
                        cursor.execute(idsql)

                        purchasing_id = cursor.fetchall()[0][0]
                        purchasing_t = datetime.datetime.now()
                        print(purchasing_t)
                        ordersql = "INSERT INTO purchasing (purchasing_id, purchasing_time, purchasing_item, purchasing_quantity, purchasing_cost, supplier, status) VALUES ({},'{}','{}',{},{},'XXX', '出貨中')".format(purchasing_id, purchasing_t, purchasing_i, purchasing_q, purchasing_c)
                        cursor.execute(ordersql)
                        db.commit()

                    elif index_r == index-3:
                        purchasing_q = r
                        index_r = index_r+1

                    elif index_r == index-5:
                        purchasing_i = r
                        index_r = index_r+1
                        
                    elif index_r == index-6:
                        print('rrrrrrr', r)
                        replysql = "UPDATE product SET p_status = '{}' WHERE product_id = {}".format('已下訂', r)
                        cursor.execute(replysql)  
                        db.commit()    
                        i=0   
                        index_r = index_r+1
                        
                    else:
                        index_r = index_r+1
            

            except:
                
                index_r = 0
            
                for r in request.POST:
                    if index_r == index-1:
                        purchasing_c = r
                        index_r = index_r+1
                        idsql = "SELECT COUNT(purchasing_id) FROM purchasing"
                        cursor.execute(idsql)
                        
                        purchasing_id = cursor.fetchall()[0][0]
                        purchasing_t = datetime.datetime.now()
                        ordersql = "INSERT INTO purchasing (purchasing_id, purchasing_time, purchasing_item, purchasing_quantity, purchasing_cost, supplier, status) VALUES ({},{},'{}',{},{},'XXX', '已下訂')".format(purchasing_id, purchasing_t, purchasing_i, purchasing_q, purchasing_c)
                        cursor.execute(ordersql)
                        db.commit()

                    elif index_r == index-2:
                        purchasing_q = r
                        index_r = index_r+1

                    elif index_r == index-4:
                        purchasing_i = r
                        index_r = index_r+1
                        
                    elif index_r == index-5:
                        print('rrrrrrr', r)
                        replysql = "UPDATE product SET p_status = '{}' WHERE product_id = {}".format('已下訂', r)
                        cursor.execute(replysql)  
                        db.commit()    
                        i=0   
                        index_r = index_r+1
                        
                    else:
                        index_r = index_r+1
        else:
            i = i+1
        
    h = 0
    # 確認訂單
    for r in request.POST:
        if 'confirm' in r:
            index = h
            print(request.POST)
            print(index)
            try:
                index_r = 0
            
                for r in request.POST:

                    if index_r == index-3:
                        purchasing_q = r
                        index_r = index_r+1
                        replysql = "UPDATE product SET inventory = '{}' WHERE product_id = {}".format(int(purchasing_i)+int(purchasing_q), purchasing_id)
                        cursor.execute(replysql)  
                        db.commit()

                    elif index_r == index-4:
                        purchasing_i = r
                        index_r = index_r+1
                        
                    elif index_r == index-5:
                        print('rrrrrrr', r)
                        replysql = "UPDATE purchasing SET status = '{}' WHERE purchasing_item = '{}'".format('貨到啦', r)
                        cursor.execute(replysql)
                        db.commit()   
                        i=0   
                        index_r = index_r+1
                    
                    elif index_r == index-6:
                        purchasing_id = r
                        index_r = index_r+1
                        
                    else:
                        index_r = index_r+1
            

            except:
                
                index_r = 0
            
                for r in request.POST:

                    if index_r == index-2:
                        purchasing_q = r
                        index_r = index_r+1
                        replysql = "UPDATE product SET inventory = '{}' WHERE product_id = {}".format(purchasing_i+purchasing_q, purchasing_id)
                        cursor.execute(replysql)  
                        db.commit()

                    elif index_r == index-3:
                        purchasing_i = r
                        index_r = index_r+1
                        
                    elif index_r == index-4:
                        print('rrrrrrr', r)
                        replysql = "UPDATE purchasing SET status = '{}' WHERE purchasing_item = {}".format('貨到啦', r)
                        cursor.execute(replysql)
                        db.commit()   
                        i=0   
                        index_r = index_r+1
                    
                    elif index_r == index-5:
                        purchasing_id = r
                        index_r = index_r+1
                        
                    else:
                        index_r = index_r+1
                

        else:
            h = h+1


    all_info = zip(product_info, reorder_points)
    all_info2 = zip(product_info, preorder_info)


    context = {'product_info':product_info, 'pcategory':pcategory, 'pid':pid, 
    'reorder':reorder_points, 
    'all_info':all_info, 'all_info2':all_info2}

    return render(request, 'product.html', context)


