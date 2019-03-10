from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from collections import namedtuple
import datetime

# Create your views here.
def entrance(request):
    return HttpResponseRedirect(reverse('booking_system:login'))


def index(request):
    if request.session.get('is_login'):
        context = {
            'is_login' : request.session.get('is_login'),
            'username' : request.session.get('username'),
        }
        return render(request, 'booking_system/index.html', context)
    else:
        '''不允许未登录用户访问主页'''
        return HttpResponseRedirect(reverse('booking_system:login'))


def login(request):
    if request.method == 'POST':
        '''方法字段为POST表示用户提交了用户名和密码'''
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_name = %s", [username])
            result = namedtuple_fetchall(cursor)

        if len(result) == 0:
            '''用户名不存在'''
            context = {
                'nonexisting' : True,
            }
            return render(request, 'booking_system/login.html', context)

        if result[0].password != password:
            '''密码不正确'''
            context = {
                'wrong_password' : True,
            }
            return render(request, 'booking_system/login.html', context)

        request.session['is_login'] = True
        request.session['username']= username
        return HttpResponseRedirect(reverse('booking_system:index'))
    else:
        '''方法字段为GET表示未登录用户访问页面'''
        return render(request, 'booking_system/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        ID = request.POST.get('ID')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_name = %s", [username])
            result = namedtuple_fetchall(cursor)

        if len(result) != 0:
            '''用户名重复'''
            context = {
                'username_duplicate' : True,
            }
            return render(request, 'booking_system/register.html', context)

        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM persons WHERE person_id = %s", [ID])
            result = namedtuple_fetchall(cursor)

        if len(result) == 0 or result[0].name.strip() != name:
            '''查无此人或信息不正确'''
            context = {
                'wrong_info' : True,
            }
            return render(request, 'booking_system/register.html', context)

        if password != confirmation:
            '''两次密码不相同'''
            context = {
                'password_not_same' : True,
            }
            return render(request, 'booking_system/register.html', context)

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users(user_name, password, person_id)\
                VALUES(%s, %s, %s)", [username, password, ID])
        return HttpResponseRedirect(reverse('booking_system:login'))
    else:
        return render(request, 'booking_system/register.html')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('booking_system:login'))


def flight_query(request):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        dept = request.POST.get('dept')
        dest = request.POST.get('dest')
        dept_date = request.POST.get('dept_date')
        with connection.cursor() as cursor:
            cursor.execute("SELECT *\
                            FROM v_flight_info\
                            WHERE dept_city = %s AND dest_city = %s AND DATE(dept_datetime) = %s", [dept, dest, dept_date])
            result = namedtuple_fetchall(cursor)
        
        '''把城市名和机场名拼接在一起，把时间的最后三个字符去掉'''
        for i in range(len(result)):
            '''SQL的datetime类型返回到python中是datetime.datetime类型'''
            dept_datetime = datetime.datetime.strftime(result[i].dept_datetime, '%Y-%m-%d %H:%M')
            dest_datetime = datetime.datetime.strftime(result[i].dest_datetime, '%Y-%m-%d %H:%M')
            result[i] = result[i]._replace(dept_airport=result[i].dept_city + result[i].dept_airport,
                                           dest_airport=result[i].dest_city + result[i].dest_airport,
                                           dept_datetime=dept_datetime,
                                           dest_datetime=dest_datetime,)

        context = {
            'show_table' : True,
            'result' : result,
            'is_login' : request.session.get('is_login'),
            'username' : request.session.get('username'),
        }

        return render(request, 'booking_system/flight_query.html', context)

    else:
        context = {
            'is_login' : request.session.get('is_login'),
            'username' : request.session.get('username'),
        }
        return render(request, 'booking_system/flight_query.html', context)


def book_tickets(request, flight_id, dept_datetime):
    if request.method == 'POST':
        ticket_num = request.POST.get('ticket_num')
        ticket_num = int(ticket_num)
        return HttpResponseRedirect(reverse('booking_system:fill_information', args=(flight_id, dept_datetime, ticket_num,)))
            
    else:
        context = {
            'flight_id' : flight_id,
            'dept_datetime' : dept_datetime,
            'is_login' : request.session.get('is_login'),
            'username' : request.session.get('username'),
        }
        return render(request, 'booking_system/book_tickets.html', context)


def fill_information(request, flight_id, dept_datetime, ticket_num):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        cabin_count = {
            '头等舱' : 0,
            '商务舱' : 0,
            '经济舱' : 0,
        }
        with connection.cursor() as cursor:
            cursor.execute("SELECT first_left, business_left, economy_left\
                            FROM flights\
                            WHERE flight_id = %s AND takeoff_time = %s", [flight_id, dept_datetime])
            row = cursor.fetchone()
            first_left = row[0]
            business_left = row[1]
            economy_left = row[2]

        for i in range(ticket_num):
            name = request.POST.get('name' + str(i))
            ID = request.POST.get('ID' + str(i))
            cabin = request.POST.get('cabin' + str(i))
            cabin_count[cabin] += 1

            '''检查舱位数量'''
            if cabin_count['头等舱'] > first_left or\
               cabin_count['商务舱'] > business_left or\
               cabin_count['经济舱'] > economy_left:
                context = {
                    'not_enough' : True,
                    'flight_id' : flight_id,
                    'dept_datetime' : dept_datetime,
                    'ticket_num' : ticket_num,
                    'sequence' : list(range(ticket_num)),
                    'is_login' : request.session.get('is_login'),
                    'username' : request.session.get('username'),
                }
                return render(request, 'booking_system/fill_information.html', context)

            '''检查信息是否正确'''
            with connection.cursor() as cursor:
                cursor.execute('SELECT name FROM persons WHERE person_id = %s', [ID])
                result = namedtuple_fetchall(cursor)

            if len(result) == 0 or result[0].name != name:
                context = {
                    'wrong_index' : i,
                    'flight_id' : flight_id,
                    'dept_datetime' : dept_datetime,
                    'ticket_num' : ticket_num,
                    'sequence' : list(range(ticket_num)),
                    'is_login' : request.session.get('is_login'),
                    'username' : request.session.get('username'),
                }
                return render(request, 'booking_system/fill_information.html', context)

        '''创建订单'''
        username = request.session.get('username')
        order_id = None
        with connection.cursor() as cursor:
            cursor.callproc('Proc_new_order', (username, order_id))
            cursor.execute("SELECT @_Proc_new_order_1")
            row = cursor.fetchone()
            order_id = row[0]

        '''插入机票'''
        with connection.cursor() as cursor:
            for i in range(ticket_num):
                name = request.POST.get('name' + str(i))
                ID = request.POST.get('ID' + str(i))
                cabin = request.POST.get('cabin' + str(i))
                cursor.execute("INSERT INTO tickets(person_id, order_id, flight_id, takeoff_time, class)\
                                VALUES(%s, %s, %s, %s, %s)", [ID, order_id, flight_id, dept_datetime, cabin])

        return HttpResponseRedirect(reverse('booking_system:index'))
        
    else:
        context = {
            'flight_id' : flight_id,
            'dept_datetime' : dept_datetime,
            'ticket_num' : ticket_num,
            'sequence' : list(range(ticket_num)),
            'is_login' : request.session.get('is_login'),
            'username' : request.session.get('username'),
        }
        return render(request, 'booking_system/fill_information.html', context)


def namedtuple_fetchall(cursor):
    '''以namedtuple的形式返回cursor的查询结果'''
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def dict_fetchall(cursor):
    '''以dict的形式返回cursor的查询结果'''
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def order_query(request):
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM orders')
        result = dict_fetchall(cursor)
    context = {
        'show_table' : True,
        'result' : result,
        'is_login' : request.session.get('is_login'),
        'username' : request.session.get('username'),
    }

    return render(request, 'booking_system/order_query.html', context)


def ticket_query(request,order_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM V_order_info where order_id = %s',[order_id])
        result = dict_fetchall(cursor)

    context = {
        'show_table' : True,
        'result' : result,
        'the_order_id' : order_id,
        'is_login' : request.session.get('is_login'),
        'username' : request.session.get('username'),
    }

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM orders where order_id = %s',[order_id])
        order_inf = namedtuple_fetchall(cursor)

    if order_inf[0].status == 'Valid':
        context['show_table'] = False

    return render(request, 'booking_system/ticket_query.html', context)


def order_cancel(request,order_id):
    with connection.cursor() as cursor:
        cursor.execute('delete FROM tickets where order_id = %s',[order_id])
        cursor.execute('delete FROM orders where order_id = %s',[order_id])

    return HttpResponseRedirect(reverse('booking_system:order_query'))


def order_status_update(request,order_id):
    with connection.cursor() as cursor:
        cursor.execute(' update orders set status = "Valid" where orders.order_id = %s',order_id)

    return HttpResponseRedirect(reverse('booking_system:order_query'))
