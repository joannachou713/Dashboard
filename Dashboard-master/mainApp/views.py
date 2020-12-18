from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from .models import Order
import os
import sqlite3
from .forms import FormStatus

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

    ###更改 訂單狀態
    form = FormStatus()
    if request.method == "POST":
        form = FormStatus(request.POST)		
        if form.is_valid():
            response = request.POST.get('response')
            print('Response:',response)

            if response =='已審核':
                replysql = "UPDATE order_list SET status = '已審核'"
                cursor.execute(replysql)
                db.commit()

            elif response == '備貨中':
                print('按備貨中')
                replysql = "UPDATE order_list SET status = '備貨中'"
                cursor.execute(replysql)
                db.commit()

            elif response == '已達包裹中心':
                replysql = "UPDATE order_list SET status = '已達包裹中心'"
                cursor.execute(replysql)
                db.commit()

            elif response == '已達物流中心':
                replysql = "UPDATE order_list SET status = '已達物流中心'"
                cursor.execute(replysql)
                db.commit()
                
            elif response == '已出貨':
                replysql = "UPDATE order_list SET status = '已出貨'"
                cursor.execute(replysql)
                db.commit()
                
            elif response == '已到達':
                replysql = "UPDATE order_list SET status = '已到達'"
                cursor.execute(replysql)
                db.commit()
            
        else:
            form = FormStatus()
            print('fail')

    context = {'orderlist':orderlist, 'form':form}
    return render(request, 'order.html', context)

    