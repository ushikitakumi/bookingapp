import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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

        # 9:00~26:00、1週間分の、値がTrueなカレンダーを作る
        # "9:00"~"23:30","0:00"~"1:30"の配列
        time = []
        for i in range(9, 24):
            for j in range(0, 60, 30):
                hour = str(i).zfill(2)
                minute = str(j).zfill(2)
                time.append(hour + ":" + minute)
        for i in range(2):
            for j in range(0, 60, 30):
                hour = str(i).zfill(2)
                minute = str(j).zfill(2)
                time.append(hour + ":" + minute)

        #カレンダーの配列
        calendar = {}
        for count in range(34):
            row = {}
            for day in days:
                row[day] = True
            calendar[time[count]] = row
        
        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=9, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day+datetime.timedelta(days=1), datetime.time(hour=2, minute=0, second=0))
        for schedule in Schedule.objects.filter(studio=studio).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            start_dt = timezone.localtime(schedule.start)
            end_dt = timezone.localtime(schedule.end)
            booking_start_hour = start_dt.hour
            booking_date = start_dt.date()
            if booking_start_hour <= 2:
                booking_date -= datetime.timedelta(days=1)

            num_start_hour = time.index(start_dt.time().strftime("%H:%M"))
            num_end_hour = time.index(end_dt.time().strftime("%H:%M")) 
            for num in range(num_start_hour,num_end_hour):
                if time[num] in calendar and booking_date in calendar[time[num]]:
                    calendar[time[num]][booking_date] = False
                
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
    # 予約の開始時刻が0:00~1:30であれば日付を+1する
    if hour == ("00:00" or "00:30" or "01:00" or "01:30"):
        day += 1

    context = {'studio': studio,
                'user' : user,
                'year' : year,
                'month': month,
                'day'  : day,
                'hour' : hour}

    if request.method == 'POST':
        start_time = datetime.datetime.strptime(request.POST['start'],'%Y/%m/%d %H:%M')
        end_time = datetime.datetime.strptime(request.POST['end'],'%Y/%m/%d %H:%M')

        if Schedule.objects.filter(studio=studio).exclude(Q(start__gte=end_time) | Q(end__lte=start_time)).exists():
            messages.error(request, 'すでに予約が入っています。別の日時をお選びください')
        else:
            object = Schedule.objects.create(
                    start = start_time,
                    end = end_time,
                    personCount = request.POST['personCount'],
                    user = user,
                    studio = studio)
            object.save()
        return redirect('booking:calendar', pk=studio.pk, year=year, month=month, day=day)

    else:
        return render(request, 'booking/booking.html', context)

class StaffStudioCalendar(StudioCalendar):
    template_name = 'booking/staffcalendar.html'

class Detail(generic.TemplateView):
    template_name = 'booking/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        studio = get_object_or_404(Studio, pk=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = datetime.date(year=year, month=month, day=day)

        calendar = {}
        for time in range(9,24):
            calendar[time] = []

        start_time = datetime.datetime.combine(date, datetime.time(hour=10, minute=0, second=0))
        end_time = datetime.datetime.combine(date, datetime.time(hour=23, minute=0, second=0))
        for schedule in Schedule.objects.filter(studio=studio).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            start_dt = timezone.localtime(schedule.start)
            end_dt = timezone.localtime(schedule.end)
            booking_start_hour = start_dt.hour
            booking_end_hour = end_dt.hour 

            for hour in range(booking_start_hour,booking_end_hour):
                calendar[hour].append(schedule)

        context = { 'studio'  :studio,
                    'year'    :year,
                    'month'   :month,
                    'day'     :day,
                    'calendar':calendar}
        return context