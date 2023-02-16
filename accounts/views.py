import datetime
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import sys
sys.path.append('../')
from booking.models import Schedule

# Create your views here.

app_name = 'accounts'

class MypageView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'accounts/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 現在以降の予約を取得
        reserve_schedule = []
        today = datetime.datetime.today()
        for schedule in Schedule.objects.filter(user=user).exclude(Q(end__lt=today)):
            reserve_schedule.append(schedule)

        # 現在から一ヶ月前までの予約履歴を取得
        history_schedule = []
        one_month_ago = today - datetime.timedelta(days=31)
        for schedule in Schedule.objects.filter(user=user).exclude(Q(start__gt=today) | Q(end__lt=one_month_ago)):
            history_schedule.append(schedule)

        context['user'] = user
        context['reserve_schedule'] = reserve_schedule
        context['history_schedule'] = history_schedule
        return context


        

