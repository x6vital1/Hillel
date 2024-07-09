from functools import wraps
from dotenv import load_dotenv
import os
import Project_utils
from Project_utils.models import *
from sendmail import send_mail

from flask import Flask, request, render_template, redirect, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return func(*args, **kwargs)

    return wrapper


@app.get('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/register', methods=['GET', 'POST'])
def get_register_page():
    if request.method == 'GET':
        return render_template('register.html', title='Регистрация')
    else:
        form_data = request.form
        user_name = form_data.get('username')
        password = form_data.get('password')
        birthday = form_data.get('birthday')
        phone = form_data.get('phone')
        email = form_data.get('email')
        user = User(login=user_name, password=password, birth_date=birthday, phone=phone, email=email)
        Project_utils.db_session.add(user)
        Project_utils.db_session.commit()
        session['user'] = {'id': user.id, 'login': user.login, 'email': user.email}
        return redirect('/user')


@app.route('/login', methods=['GET', 'POST'])
def get_login_page():
    if request.method == 'GET':
        if 'user' in session:
            return redirect('/user')
        return render_template('login.html', title='Авторизация')
    else:
        form_data = request.form
        user_name = form_data.get('username')
        password = form_data.get('password')
        user = Project_utils.db_session.query(User).filter_by(login=user_name, password=password).first()
        if user:
            session['user'] = {'id': user.id, 'login': user.login, 'email': user.email}
            return redirect('/user')
        else:
            return 'Login failed'


@app.route('/logout')
@login_required
def get_logout_page():
    session.pop('user', None)
    return redirect('/')


@app.route('/user', methods=['GET', 'POST'])
@login_required
def get_user_page():
    if request.method == 'GET':
        user_id = session.get('user')['id']
        user = Project_utils.db_session.query(User).filter_by(id=user_id).first()
        return render_template('user.html', title='Личный кабинет', user=user)
    if request.method == 'POST':
        return 'User created'


@app.route('/user/<int:user_id>/funds', methods=['GET', 'POST'])
@login_required
def get_funds_page(user_id):
    if request.method == 'GET':
        funds = Project_utils.db_session.query(User).filter_by(id=user_id).first().funds
        return {'funds': funds}
    if request.method == 'POST':
        return 'Add something to funds'


@app.route('/user/reservations', methods=['GET', 'POST'])
@login_required
def get_reservations_page():
    user = session.get('user')
    if request.method == 'GET':
        reservations = Project_utils.db_session.query(Reservation).join(Service,
                                                                        Reservation.service_id == Service.id).join(
            Trainer,
            Reservation.trainer_id == Trainer.id).join(
            FitnessCenter, Trainer.fitness_center_id == FitnessCenter.id).filter(
            Reservation.user_id == user['id']).all()
        return render_template('reservations.html', title='Мои бронирования', reservations=reservations)

    if request.method == 'POST':
        form_data = request.form
        service_id = form_data.get('service_id')
        trainer_id = form_data.get('trainer_id')
        date = form_data.get('date')
        time = form_data.get('time')
        message_text = (f'Ваше бронирование подтверждено.\n'
                        f'Сервис: {Project_utils.db_session.query(Service).filter_by(id=service_id).first().name}\n'
                        f'Тренер: {Project_utils.db_session.query(Trainer).filter_by(id=trainer_id).first().name}\n'
                        f'Дата: {date}\n'
                        f'Время: {time}')
        try:
            reservation = Reservation(user_id=user['id'], service_id=int(service_id), trainer_id=int(trainer_id),
                                      date=date,
                                      time=time)
            Project_utils.db_session.add(reservation)
            Project_utils.db_session.commit()
            send_mail.delay(user['email'], 'Ваше бронирование подтверждено', message_text)
            return redirect('/user/reservations')
        except Exception as e:
            print(f'Error sending email: {e}')


@app.route('/user/reservations/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def get_reservation_page(reservation_id):
    if request.method == 'GET':
        reservation = Project_utils.db_session.query(Reservation).filter_by(id=reservation_id).first()
        if not reservation:
            return 'Reservation not found'
        return {'id': reservation.id, 'date': reservation.date, 'time': reservation.time,
                'service_id': reservation.service_id, 'trainer_id': reservation.trainer_id}
    if request.method == 'POST':
        return 'Reservation created'


@app.route('/user/checkout', methods=['GET', 'POST'])
@login_required
def get_checkout_page():
    if request.method == 'GET':
        return 'Checkout page'
    if request.method == 'POST':
        return 'Checkout created'


@app.get('/fitness_centers')
def get_fitness_center_page():
    fitness_centers = Project_utils.db_session.query(FitnessCenter).all()
    if not fitness_centers:
        return 'Fitness centers not found'
    return render_template('fitness_centers.html', title='Фитнес центры', fitness_centers=fitness_centers)


@app.get('/fitness_center/<int:fitness_center_id>')
def get_fitness_center_id_page(fitness_center_id):
    fitness_center = Project_utils.db_session.query(FitnessCenter).filter_by(id=fitness_center_id).first()
    if not fitness_center:
        return 'Fitness center not found'
    return {'id': fitness_center.id, 'name': fitness_center.name, 'address': fitness_center.address}


@app.get('/fitness_center/<int:fitness_center_id>/trainers')
def get_trainer_page(fitness_center_id):
    trainers = Project_utils.db_session.query(Trainer).join(FitnessCenter,
                                                            FitnessCenter.id == Trainer.fitness_center_id).filter(
        Trainer.fitness_center_id == fitness_center_id).all()
    if not trainers:
        return 'Trainers not found'
    return render_template('trainers.html', title='Тренеры', trainers=trainers)


@app.route('/fitness_center/<int:fitness_center_id>/trainers/<int:trainer_id>/<int:service_id>',
           methods=['GET', 'POST'])
def get_trainer_service_page(fitness_center_id, trainer_id, service_id):
    trainer = Project_utils.db_session.query(Trainer).join(FitnessCenter,
                                                           Trainer.fitness_center_id == FitnessCenter.id).filter(
        Trainer.id == trainer_id).first()
    trainer_schedule = Project_utils.db_session.query(TrainerSchedule).filter_by(trainer_id=trainer_id).all()
    if request.method == 'GET':
        return render_template('trainer_page.html', title=trainer.name, trainer=trainer,
                               trainer_schedule=trainer_schedule)
    if request.method == 'POST':
        form_data = request.form
        date = form_data.get('date')
        available_time = Project_utils.get_schedule_slots(trainer_id, service_id, date)
        return render_template('trainer_page.html', title=trainer.name, trainer=trainer,
                               trainer_schedule=trainer_schedule, available_time=available_time, service_id=service_id,
                               date=date)


@app.route('/fitness_center/<int:fitness_center_id>/trainers/<int:trainer_id>/rating', methods=['GET', 'POST'])
@login_required
def get_trainer_rating_page(fitness_center_id, trainer_id):
    user = session.get('user')
    user_review = Project_utils.db_session.query(Review).filter_by(user_id=user['id'], trainer_id=trainer_id).first()
    if request.method == 'GET':
        rating = Project_utils.db_session.query(Review).join(Trainer, Review.trainer_id == Trainer.id).join(User,
                                                                                                            Review.user_id == User.id).filter(
            Review.trainer_id == trainer_id).all()
        trainer = Project_utils.db_session.query(Trainer).filter_by(id=trainer_id).first()
        return render_template('rating.html', title='Рейтинг', rating=rating, fitness_center_id=fitness_center_id,
                               trainer=trainer, user_review=user_review)
    if request.method == 'POST':
        form_data = request.form
        points = form_data.get('points')
        text = form_data.get('text')
        if user_review:
            user_review.points = points
            user_review.text = text
            Project_utils.db_session.commit()
            return redirect(f'/fitness_center/{fitness_center_id}/trainers/{trainer_id}/rating')
        else:
            review = Review(user_id=user['id'], trainer_id=trainer_id, points=int(points), text=text)
            Project_utils.db_session.add(review)
            Project_utils.db_session.commit()
            return redirect(f'/fitness_center/{fitness_center_id}/trainers/{trainer_id}/rating')


@app.get('/fitness_center/<int:fitness_center_id>/services')
@login_required
def get_services_page(fitness_center_id):
    user = session.get('user')
    services = Project_utils.db_session.query(Service).join(FitnessService,
                                                            Service.id == FitnessService.service_id).join(FitnessCenter,
                                                                                                          FitnessService.fitness_center_id == FitnessCenter.id).filter(
        FitnessService.fitness_center_id == fitness_center_id).all()
    trainers = Project_utils.db_session.query(Trainer).join(TrainerServices,
                                                            Trainer.id == TrainerServices.trainer_id).filter(
        Trainer.fitness_center_id == fitness_center_id).all()
    return render_template('services.html', title='Услуги', services=services, trainers=trainers)


@app.route('/fitness_center/<int:fitness_center_id>/services/<int:service_id>', methods=['GET', 'POST'])
def get_service_id_page(fitness_center_id, service_id):
    if request.method == 'GET':
        service = Project_utils.db_session.query(Service).join(FitnessService,
                                                               Service.id == FitnessService.service_id).join(
            FitnessCenter, FitnessService.fitness_center_id == FitnessCenter.id).filter_by(id=service_id).first()
        if not service:
            return 'Service not found'
        return service


@app.route('/fitness_center/<int:fitness_center_id>/loyalty_program', methods=['GET', 'POST'])
def get_loyalty_program_page(fitness_center_id):
    if request.method == 'GET':
        return f'Welcome to the list of the loyalty programs! Fitness center id: {fitness_center_id}'
    if request.method == 'POST':
        return f'Loyalty program created! Fitness center id: {fitness_center_id}'
    if request.method == 'PUT':
        return f'Loyalty program updated! Fitness center id: {fitness_center_id}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
