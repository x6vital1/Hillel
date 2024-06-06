from Project_utils.database_utils import SQLiteDatabase
from datetime import datetime, timedelta


def get_schedule_slots(trainer_id, service_id, date):
    with SQLiteDatabase('base.db') as db:
        booked_time = db.select(table_name='reservations', method='fetchall', conditions={'trainer_id': trainer_id, 'date': date},
                                join_conditions={'services': {'reservations.service_id': 'services.id'}}
                                )
        trainer_schedule = db.select(table_name='trainer_schedule', method='fetchone',
                                     conditions={'trainer_id': trainer_id, 'date': date})
        trainer_capacity = db.select(table_name='trainer_services', method='fetchone',
                                     conditions={'trainer_id': trainer_id, 'service_id': service_id})
        service_info = db.select(table_name='services', method='fetchone', conditions={'id': service_id})
        available_slots = []
        start_dt = datetime.strptime(trainer_schedule['date'] + ' ' + trainer_schedule['start_time'], '%Y-%m-%d %H:%M')
        end_dt = datetime.strptime(trainer_schedule['date'] + ' ' + trainer_schedule['end_time'], '%Y-%m-%d %H:%M')
        curr_dt = start_dt
        schedule = {}
        while curr_dt < end_dt:
            schedule[curr_dt] = trainer_capacity['capacity']
            curr_dt += timedelta(minutes=15)
        for one_booking in booked_time:
            booking_date = one_booking['date']
            booking_time = one_booking['time']
            booking_duration = one_booking['duration']
            one_booking_start = datetime.strptime(booking_date + ' ' + booking_time, '%Y-%m-%d %H:%M')
            booking_end = one_booking_start + timedelta(minutes=booking_duration)
            curr_dt = one_booking_start
            while curr_dt < booking_end:
                schedule[curr_dt] -= 1
                curr_dt += timedelta(minutes=15)
        service_start_time = start_dt
        while service_start_time < end_dt:
            service_end_time = service_start_time + timedelta(minutes=service_info['duration'])
            is_free = True
            iter_time = service_start_time
            while iter_time < service_end_time:
                if schedule[iter_time] == 0 or service_end_time > end_dt:
                    is_free = False
                    break
                iter_time += timedelta(minutes=15)
            if is_free:
                available_slots.append(service_start_time)
            service_start_time += timedelta(minutes=15)
    return available_slots