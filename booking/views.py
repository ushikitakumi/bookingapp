import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views import generic
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Studio, Schedule
import sys
sys.path.append('../')
from accounts.models import User

class IndexListView(generic.ListView):
    template_name = 'booking/index.html'
    model = Studio

class StudioCalendar(generic.TemplateView):
    template_name = 'booking/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        studio = get_object_or_404(Studio, pk=self.kwargs['pk'])
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 9時から24時、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for time in range(9,24):
            row = {}
            for day in days:
                row[day] = True
            calendar[time] = row
        
        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=9, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=23, minute=0, second=0))
        for schedule in Schedule.objects.filter(studio=studio).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            start_dt = timezone.localtime(schedule.start)
            end_dt = timezone.localtime(schedule.end)
            booking_date = start_dt.date()
            booking_start_hour = start_dt.hour
            booking_end_hour = end_dt.hour 

            for hour in range(booking_start_hour,booking_end_hour):
                if hour in calendar and booking_date in calendar[hour]:
                    calendar[hour][booking_date] = False
                
        context['studio'] = studio
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        return context

@login_required
def Booking(request,pk,year,month,day,hour):
    studio = get_object_or_404(Studio, pk=pk)
    user = get_object_or_404(User, pk=request.user.id)
    context = {'studio': studio,
                'user' : user,
                'year' : year,
                'month': month,
                'day'  : day,
                'hour' : hour}

    if request.method == 'POST':
        start_hour = datetime.datetime(year=year, month=month, day=day, hour=int(request.POST['start'].replace(':00','')))
        end_hour = datetime.datetime(year=year, month=month, day=day, hour=int(request.POST['end'].replace(':00','')))

        if Schedule.objects.filter(studio=studio).exclude(Q(start__gte=end_hour) | Q(end__lte=start_hour)).exists():
            messages.error(request, 'すでに予約が入っています。別の日時をお選びください')
        else:
            object = Schedule.objects.create(
                    start = start_hour,
                    end = end_hour,
                    personCount = request.POST['personCount'],
                    user = user,
                    studio = studio)
            object.save()
        return redirect('booking:calendar', pk=studio.pk, year=year, month=month, day=day)

    else:
        return render(request, 'booking/booking.html', context)

# class Booking(LoginRequiredMixin,generic.CreateView):
#     login_url = '/accounts/login/'
#     template_name = 'booking/booking.html'
#     model = Schedule
#     fields = ['start','end','personCount']

#     def get_context_data(self, **kwargs):
#         context =super().get_context_data(**kwargs)
#         context['studio'] = get_object_or_404(Studio, pk=self.kwargs['pk'])
#         context['user'] = self.request.user
#         return context

#     def form_valid(self, request, form):
#         studio = get_object_or_404(Studio, pk=self.kwargs['pk'])
#         user = self.request.user.id
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         day = self.kwargs.get('day')
        
#         schedule = form.save(commit=False)
#         end_r = schedule.end
#         start_r = schedule.start

#         if Schedule.objects.filter(studio=studio).exclude(Q(start__gt=end_r) | Q(end__lt=start_r)).exists():
#             messages.error(self.request, 'すでに予約が入っています。別の日時をお選びください')

#         else:
#             schedule.studio = studio
#             schedule.user = user
#             schedule.save()
#             return redirect('booking:calendar', pk=studio.pk, year=year, month=month, day=day)