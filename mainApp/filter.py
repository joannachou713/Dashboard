from django import forms
from django.db import models
import sqlite3

class filterSetID(forms.Form):
    set_productid = forms.IntegerField(label='請輸入產品編號', min_value = 1)
    
class filterCategory(forms.Form):

    PCATEGORY = (
       ('廚具', '廚具'),
       ('水壺', '水壺'),
       ('電冰箱', '電冰箱'),
       ('電子廚具', '電子廚具'),
       ('電子清潔用具', '電子清潔用具'),
    )
    response = forms.CharField(label="response",widget=forms.widgets.Select(choices=PCATEGORY),initial=PCATEGORY[0])
