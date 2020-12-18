from django import forms
from django.db import models


class FormStatus(forms.Form):

    SELVALUE = (
       ('已審核', '已審核'),
       ('備貨中', '備貨中'),
       ('已達包裹中心', '已達包裹中心'),
       ('已達物流中心', '已達物流中心'),
       ('已出貨', '已出貨'),
       ('已到達', '已到達')
    )
    response = forms.CharField(label="response",widget=forms.widgets.Select(choices=SELVALUE),initial=SELVALUE[0])