import random
import datetime
random.seed(20181226)

def random_time():
    return str(random.randint(0, 23)) + ':' +\
           str(random.randint(0, 59)) + ':' +\
           '00'

airlines = [
    ('CA', '中国国际航空'),
    ('CZ', '中国南方航空'),
    ('MU', '中国东方航空'),
    ('HU', '海南航空'),
    ('SC', '山东航空'),
    ('ZH', '深圳航空'),
    ('3U', '四川航空'),
    ('MF', '厦门航空'),
    ('FM', '上海航空'),
]
n_airline = len(airlines)

cities = [
    ('广州', 'Guangzhou'),
    ('深圳', 'Shenzhen'),
    ('上海', 'Shanghai'),
    ('杭州', 'Hangzhou'),
    ('成都', 'Chengdu'),
    ('北京', 'Beijing'),
    ('武汉', 'Wuhan'),
    ('昆明', 'Kunming'),
    ('重庆', 'Chongqing'),
    ('南京', 'Nanjing'),
    ('厦门', 'Xiamen'),
    ('福州', 'Fuzhou'),
    ('青岛', 'Qingdao'),
]
n_city = len(cities)

airports = [
    ('CAN', '广州', '白云机场'),
    ('SZX', '深圳', '宝安机场'),
    ('PVG', '上海', '浦东机场'),
    ('HGH', '杭州', '萧山机场'),
    ('CTU', '成都', '双流机场'),
    ('PEK', '北京', '首都机场'),
    ('WUH', '武汉', '天河机场'),
    ('SHA', '上海', '虹桥机场'),
    ('NKG', '南京', '禄口机场'),
    ('XMN', '厦门', '高崎机场'),
    ('TAO', '青岛', '流亭机场'),
]
n_airport = len(airports)

persons = [
    ('000', '黄', '21', 'Male'),
    ('001', '雷', '20', 'Male'),
    ('002', '徐', '20', 'Male'),
    ('003', '甲', '20', 'Male'),
    ('004', '乙', '20', 'Male'),
    ('005', '丙', '20', 'Female'),
    ('006', '丁', '20', 'Female'),
]
n_person = len(persons)

models = [
    ('A321', '10', '20', '100', 'AIRBUS'),
    ('A330', '10', '20', '100', 'AIRBUS'),
    ('A340', '15', '25', '150', 'AIRBUS'),
    ('A350', '20', '30', '200', 'AIRBUS'),
    ('Boeing737', '10', '20', '100', 'BOEING'),
    ('Boeing747', '15', '25', '150', 'BOEING'),
    ('Boeing787', '20', '30', '200', 'BOEING'),
]
n_model = len(models)

flight_code = set()
'''每天100趟航班'''
while len(flight_code) < 100:
    flight_code.add(str(random.randint(1000, 9999)))

with open(r'sql\data.sql', 'w', encoding='utf-8') as fout:
    for person in persons:
        text = "INSERT INTO persons VALUES('{}', '{}', {}, '{}');".format(
                person[0], person[1], person[2], person[3])
        fout.write(text)
        fout.write('\n')

    for city in cities:
        text = "INSERT INTO cities VALUES('{}', '{}');".format(
                city[0], city[1])
        fout.write(text)
        fout.write('\n')

    for airline in airlines:
        text = "INSERT INTO airlines VALUES('{}', '{}');".format(
                airline[0], airline[1])
        fout.write(text)
        fout.write('\n')

    for airport in airports:
        text = "INSERT INTO airports VALUES('{}', '{}', '{}');".format(
                airport[0], airport[1], airport[2])
        fout.write(text)
        fout.write('\n')

    for model in models:
        text = "INSERT INTO models VALUES('{}', {}, {}, {}, '{}');".format(
                model[0], model[1], model[2], model[3], model[4])
        fout.write(text)
        fout.write('\n')

    for code in flight_code:
        airline_id = airlines[random.randint(0, n_airline - 1)][0]
        flight_id = airline_id + code
        model_id = models[random.randint(0, n_model - 1)][0]

        departure_id = airports[random.randint(0, n_airport - 1)][0]
        destination_id = airports[random.randint(0, n_airport - 1)][0]
        while departure_id == destination_id:
            destination_id = airports[random.randint(0, n_airport - 1)][0]

        economy_price = random.randint(500, 2000)
        business_price = economy_price + random.randint(100, 500)
        first_price = business_price + random.randint(300, 1000)

        t = random_time()
        for i in range(10):
            dt = '2019-01-' + str(i + 1) + ' ' + t
            takeoff_time = datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
            landing_time = datetime.timedelta(hours=random.randint(2, 7)) + takeoff_time
            takeoff_time = datetime.datetime.strftime(takeoff_time, '%Y-%m-%d %H:%M:%S')
            landing_time = datetime.datetime.strftime(landing_time, '%Y-%m-%d %H:%M:%S')

            text = "INSERT INTO flights(flight_id, model_id, airline_id, departure_id, destination_id, takeoff_time, landing_time, economy_price, business_price, first_price) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {});".format(
                    flight_id, model_id, airline_id, departure_id, destination_id, takeoff_time, landing_time, economy_price, business_price, first_price)
            fout.write(text)
            fout.write('\n')

