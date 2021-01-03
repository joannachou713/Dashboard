from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from .models import Order
import os
import sqlite3
from .forms import FormStatus
from .forms import FormSetID

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

    