from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('',views.IndexListView.as_view(), name='index'),

    path('<int:pk>/calendar/',views.StudioCalendar.as_view(),name='calendar'),
    path('<int:pk>/calendar/<int:year>/<int:month>/<int:day>/',views.StudioCalendar.as_view(),name='calendar'),

    path('<int:pk>/booking/<int:year>/<int:month>/<int:day>/<int:hour>/',views.Booking,name='booking'),
]