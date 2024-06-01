from database_utils import SQLiteDatabase
from datetime import datetime, timedelta


def get_schedule_slots(user_id, trainer_id, service_id):
    with SQLiteDatabase('../base.db') as db:
        booked_time = db.select(table_name='reservations', method='fetchall', conditions={'trainer_id': trainer_id},
                                join_conditions={'services': {'reservations.service_id': 'services.id'}}
                                )
        trainer_schedule = db.select(table_name='trainer_schedule', method='fetchone',
                                     conditions={'trainer_id': trainer_id})
        trainer_capacity = db.select(table_name='trainer_services', method='fetchone',
                                     conditions={'trainer_id': trainer_id, 'service_id': service_id})
        service_info = db.select(table_name='services', method='fetchone', conditions={'id': service_id})
        available_slots = []
        start_dt = datetime.strptime(trainer_schedule['date'] + ' ' + trainer_schedule['start_time'], '%d.%m.%Y %H:%M')
        end_dt = datetime.strptime(trainer_schedule['date'] + ' ' + trainer_schedule['end_time'], '%d.%m.%Y %H:%M')
        curr_dt = start_dt
        curr_slot_start = start_dt
        schedule = {}
        while curr_dt < end_dt:
            schedule[curr_dt] = trainer_capacity['capacity']
            curr_dt += timedelta(minutes=15)
        for one_booking in booked_time:
            booking_date = one_booking['date']
            booking_time = one_booking['time']
            booking_duration = one_booking['duration']
            one_booking_start = datetime.strptime(booking_date + ' ' + booking_time, '%d.%m.%Y %H:%M')
            booking_end = one_booking_start + timedelta(minutes=booking_duration)
            curr_dt = one_booking_start
            while curr_dt < booking_end:
                schedule[curr_dt] -= 1
                curr_dt += timedelta(minutes=15)
            while curr_slot_start + timedelta(minutes=service_info['duration']) < end_dt:
                booked_slots = db.select(
                    table_name='reservations',
                    method='fetchall',
                    conditions={
                        'trainer_id': trainer_id,
                        'service_id': service_id,
                        'date': curr_slot_start.strftime('%d.%m.%Y'),
                        'time': curr_slot_start.strftime('%H:%M')
                    }
                )
                curr_slot_start += timedelta(minutes=15)
    print('')


get_schedule_slots(1, 1, 1)
