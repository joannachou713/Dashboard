from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from .models import Order
import os
import sqlite3
from .forms import FormStatus
from .forms import FormSetID
from .forms import checkReturn

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
                replysql = "UPDATE order_list SET status = '已審核' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()

            elif response == '備貨中':
                print('按備貨中')
                replysql = "UPDATE order_list SET status = '備貨中' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()

            elif response == '已達包裹中心':
                replysql = "UPDATE order_list SET status = '已達包裹中心' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()

            elif response == '已達物流中心':
                replysql = "UPDATE order_list SET status = '已達物流中心' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()
                
            elif response == '已出貨':
                replysql = "UPDATE order_list SET status = '已出貨' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()
                
            elif response == '已到達':
                replysql = "UPDATE order_list SET status = '已到達' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()

            elif response == '已辦理退貨':
                replysql = "UPDATE order_list SET status = '已辦理退貨' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()

            elif response == '退貨審核不通過':
                replysql = "UPDATE order_list SET status = '退貨審核不通過' WHERE order_id = ?"
                cursor.execute(replysql, (set_orderid,))
                db.commit()
            
        else:
            form = FormStatus()
            print('fail')

    context = {'orderlist':orderlist, 'form':form, 'form2':form2}
    return render(request, 'order.html', context)


def refund(request):
    
    db = sqlite3.connect('mainApp.db')
    cursor = db.cursor()

    id_list = []
    ###抓退貨單商品資料列表
    sql = "SELECT order_id FROM return"
    cursor.execute(sql)
    res = cursor.fetchall()
    #print('RESSSS', res)
    return_id = list(res)
    #print('IDDDDDDD', return_id)
    for i in return_id:
        orderid, = i
        orderid = '{}'.format(orderid)
        id_list.append(orderid)
    #print(id_list)
    #orderid, = res
	#orderid1, orderid2, orderid3 = tem_teamid
    #data = '{}'.format(teamid)
    #data1 = '{}'.format(wholesaler)
    #get_teamid = int(data)
    #get_wholesaler = int(data1)
 

    namelist = []
    returnlist = []
    detaillist = []
    wholelist = []
    for i in return_id:
        orderid, = i
        orderid = '{}'.format(orderid)
        sqlorder = "SELECT * FROM order_list WHERE order_id = ?"
        cursor.execute(sqlorder, (orderid,))
        res2 = cursor.fetchall()
        returnlist.extend(res2)
        #returnlist.extend(res2)
        sqlreturn = "SELECT logistic_id, return_time, order_product_id, reason FROM return WHERE order_id = ?"
        cursor.execute(sqlreturn, (orderid,))
        res3 = cursor.fetchall()
        detaillist.extend(res3)
        sqlname = "SELECT product FROM order_list WHERE order_id = ?"
        cursor.execute(sqlname, (orderid,))
        res4 = cursor.fetchall()
        namelist.extend(res4)
    wholelist = list(x + y for x, y in zip(returnlist, detaillist))
    print('EVERYYYYYYY', wholelist)
    #print(returnlist)

    form = checkReturn()
    if request.method == 'POST':
        form2 = FormSetID(request.POST)
        if form2.is_valid():
            
            set_orderid = request.POST.get('set_orderid')
            #print('order id:',set_orderid)
            sql_sta = "SELECT status FROM order_list WHERE order_id = ?"
            cursor.execute(sql_sta, (set_orderid,))
            res = cursor.fetchall()
            rep, = res
            rep, = rep
            status = '{}'.format(rep)
            if status == "退貨審核不通過":
                form2 = '此訂單先前已被審核為不通過，貨品已退回顧客'
                #print("STATUS: ",status)
            elif status == "已辦理退貨":
                form2 = '此訂單先前已被審核為通過，貨品已退回倉庫'
            else:
                if request.method == "POST":
                    form = checkReturn(request.POST)		
                    if form.is_valid():
                        response = request.POST.get('response')
                        

                        if response =='資格不符':
                            replysql = "UPDATE order_list SET status = '退貨審核不通過' WHERE order_id = ?"
                            cursor.execute(replysql, (set_orderid,))
                            db.commit()
                            

                        elif response == '確認退貨':
                            sql = "SELECT quantity, product FROM order_list WHERE order_id = ?"
                            cursor.execute(sql, (set_orderid,))
                            res = cursor.fetchall()
                            num_name, = res
                            num, name = num_name
                            quantity = '{}'.format(num)
                            name = '{}'.format(name)
                            #print('name: ', name, 'quantity: ', quantity)

                            sql_inv = "SELECT inventory, safety_stock FROM product WHERE product_name = ?"
                            cursor.execute(sql_inv, (name,))
                            res = cursor.fetchall()
                            inv, = res
                            inventory, safety = inv
                            inventory = '{}'.format(inventory)
                            safety = '{}'.format(safety)
                            #print('inventory: ', inventory, 'safety: ', safety)
                            final_inv = int(inventory) + int(quantity)

                            sql_inv = "UPDATE product SET inventory = ? WHERE product_name = ?"
                            content = (final_inv, name)
                            cursor.execute(sql_inv, content)
                            db.commit()

                            replysql = "UPDATE order_list SET status = '已辦理退貨' WHERE order_id = ?"
                            cursor.execute(replysql, (set_orderid,))
                            db.commit()
                    else:
                        print("qqqqq")
    else:
        form2 = FormSetID()
    
    

    context = {'wholelist':wholelist, 'form':form, 'form2':form2, 'id_list':id_list}
    return render(request, 'return.html', context)   