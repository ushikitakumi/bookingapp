from django import forms
from .models import Schedule
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

# class ScheduleForm(forms.ModelForm):
#     class Meta:
#         model = Schedule
#         fields = ('start','end','personCount')
#         labels = {'start':'開始時間','end':'終了時刻','personCount':'ご利用人数'}
#         widgets = {
#             'start': DateTimePickerInput(options={"format": "YYYY/MM/DD HH:00"}),
#             'end': DateTimePickerInput(options={"format": "YYYY/MM/DD HH:00"})
#         }