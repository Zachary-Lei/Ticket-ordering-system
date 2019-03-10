from django.urls import path
from . import views

app_name = 'booking_system'
urlpatterns = [
    path('',views.entrance, name='entrance'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('flight-query/', views.flight_query, name='flight_query'),
    path('book-tickets/<str:flight_id>/<str:dept_datetime>/', views.book_tickets, name='book_tickets'),
    path('fill-information/<str:flight_id>/<str:dept_datetime>/<int:ticket_num>/', views.fill_information, name='fill_information'),
    path('order-query/',views.order_query,name='order_query'),
    path('ticket-query/<str:order_id>/',views.ticket_query,name='ticket_query'),
    path('order-cancel/<str:order_id>/',views.order_cancel,name='order_cancel'),
    path('order-status-update/<str:order_id>/',views.order_status_update,name='order_status_update'),
]
