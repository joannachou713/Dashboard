from django import forms
from django.db import models


class FormSetID(forms.Form):
    set_orderid = forms.IntegerField(label='請輸入訂單編號', min_value = 1, max_value = 10000000)
    
class FormStatus(forms.Form):

    SELVALUE = (
       ('已審核', '已審核'),
       ('備貨中', '備貨中'),
       ('已達包裹中心', '已達包裹中心'),
       ('已達物流中心', '已達物流中心'),
       ('已出貨', '已出貨'),
       ('已到達', '已到達'),
       ('已辦理退貨', '已辦理退貨'),
       ('退貨審核不通過', '退貨審核不通過'),
    )
    response = forms.CharField(label="response",widget=forms.widgets.Select(choices=SELVALUE),initial=SELVALUE[0])

class checkReturn(forms.Form):

    SELVALUE = (
       ('確認退貨', '確認退貨'),
       ('資格不符', '資格不符'),
    )
