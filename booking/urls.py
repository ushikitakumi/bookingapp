from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('',views.IndexListView.as_view(), name='index'),
    path('<int:pk>/calendar/',views.StudioCalendar.as_view(),name='calendar'),
    path('<int:pk>/calendar/<int:year>/<int:month>/<int:day>/',views.StudioCalendar.as_view(),name='calendar'),
    path('<int:pk>/booking/<int:year>/<int:month>/<int:day>/<str:hour>/',views.Booking,name='booking'),
    path('<int:pk>/confirm/<int:personCount>/<str:start_str>/<str:end_str>/',views.Confirm,name='confirm'),

    path('staff/<int:pk>/calendar/',views.StaffStudioCalendar.as_view(), name='staffcalendar'),
    path('staff/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/',views.StaffStudioCalendar.as_view(),name='staffcalendar'),
    path('staff/<int:pk>/detail/<int:year>/<int:month>/<int:day>/',views.Detail.as_view(),name='detail'),
]