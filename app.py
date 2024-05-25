from flask import Flask, request, render_template
from Project_utils import SQLiteDatabase

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/register', methods=['GET', 'POST'])
def get_register_page():
    if request.method == 'GET':
        return render_template('register.html', title='Регистрация')
    else:
        with SQLiteDatabase('base.db') as db:
            form_data = request.form
            user_name = form_data.get('username')
            password = form_data.get('password')
            birthday = form_data.get('birthday')
            phone = form_data.get('phone')
            db.commit('users', {'login': user_name, 'password': password, 'birth_date': birthday, 'phone': phone})

        return 'Registration success'


@app.route('/login', methods=['GET', 'POST'])
def get_login_page():
    if request.method == 'GET':
        return render_template('login.html', title='Авторизация')
    else:
        form_data = request.form
        user_name = form_data.get('username')
        password = form_data.get('password')
        with SQLiteDatabase('base.db') as db:
            user = db.select(table_name='users', method='fetchone',
                             conditions={'login': user_name, 'password': password})
            if user:
                print(user)
                return render_template('user.html', title='Личный кабинет', user=user)
            else:
                return 'Login failed'


@app.route('/user/<int:user_id>', methods=['GET', 'POST', 'PUT'])
def get_user_page(user_id):
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            users = db.select(table_name='users', method='fetchone', conditions={'id': user_id})
            return users
    if request.method == 'POST':
        return 'User created'
    if request.method == 'PUT':
        return 'User updated'


@app.route('/user/<int:user_id>/funds', methods=['GET', 'POST'])
def get_funds_page(user_id):
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            funds = db.select(table_name='users', method='fetchall', columns=['funds'], conditions={'id': user_id})
            return funds
    if request.method == 'POST':
        return 'Add something to funds'


@app.route('/user/<int:user_id>/reservations', methods=['GET', 'POST', 'PUT'])
def get_reservations_page(user_id):
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            reservations = db.select(table_name='reservations', method='fetchall', conditions={'user_id': user_id},
                                     columns=['reservations.id AS reservation_id', 'reservations.date',
                                              'reservations.time',
                                              'services.name AS service_name', 'users.login AS user_name'],
                                     join_conditions={'users': {'reservations.user_id': 'users.id'}, 'services': {
                                         'reservations.service_id': 'services.id'
                                     }})
            if not reservations:
                return 'Reservations not found'
            return reservations
    if request.method == 'POST':
        return 'Reservations created'
    if request.method == 'PUT':
        return 'Reservations updated'


@app.route('/user/reservations/<int:reservation_id>', methods=['GET', 'PUT', 'DELETE'])
def get_reservation_page(reservation_id):
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            reservation = db.select(table_name='reservations', method='fetchone', conditions={'id': reservation_id})
            if not reservation:
                return 'Reservation not found'
            return reservation
    if request.method == 'PUT':
        return f'Reservation {reservation_id} updated'
    if request.method == 'DELETE':
        return f'Reservation {reservation_id} deleted'


@app.route('/user/checkout', methods=['GET', 'POST', 'PUT'])
def get_checkout_page():
    if request.method == 'GET':
        return 'Checkout page'
    if request.method == 'POST':
        return 'Checkout created'
    if request.method == 'PUT':
        return 'Checkout updated'


@app.get('/fitness_centers')
def get_fitness_center_page():
    with SQLiteDatabase('base.db') as db:
        fitness_centers = db.select(table_name='fitness_centers', method='fetchall')
        if not fitness_centers:
            return 'Fitness centers not found'
        return render_template('fitness_centers.html', title='Фитнес центры', fitness_centers=fitness_centers)


@app.get('/fitness_center/<int:fitness_center_id>')
def get_fitness_center_id_page(fitness_center_id):
    with SQLiteDatabase('base.db') as db:
        fitness_center = db.select(table_name='fitness_centers', method='fetchone',
                                   conditions={'id': fitness_center_id})
        if not fitness_center:
            return 'Fitness center not found'
        return fitness_center


@app.get('/fitness_center/<int:fitness_center_id>/trainers')
def get_trainer_page(fitness_center_id):
    with SQLiteDatabase('base.db') as db:
        trainers = db.select(table_name='trainers', method='fetchall',
                             conditions={'trainers.fitness_center_id': fitness_center_id},
                             columns=['trainers.id', 'trainers.name AS trainer_name', 'trainers.age', 'trainers.gender',
                                      'fitness_centers.name AS fitness_center_name', 'trainers.fitness_center_id'],
                             join_conditions={'fitness_centers': {'trainers.fitness_center_id': 'fitness_centers.id'}})
        if not trainers:
            return 'Trainers not found'
        return render_template('trainers.html', title='Тренеры', trainers=trainers)


@app.get('/fitness_center/<int:fitness_center_id>/trainers/<int:trainer_id>')
def get_trainer_id_page(fitness_center_id, trainer_id):
    with SQLiteDatabase('base.db') as db:
        trainer = db.select(table_name='trainers', method='fetchone',
                            conditions={'trainers.fitness_center_id': fitness_center_id, 'trainers.id': trainer_id},
                            columns=['trainers.id', 'trainers.name AS trainer_name', 'trainers.age', 'trainers.gender',
                                     'fitness_centers.name AS fitness_center_name'],
                            join_conditions={'fitness_centers': {'trainers.fitness_center_id': 'fitness_centers.id'}})
        if not trainer:
            return 'Trainer not found'
        return trainer


@app.route('/fitness_center/<int:fitness_center_id>/trainers/<int:trainer_id>/rating', methods=['GET', 'POST', 'PUT'])
def get_trainer_rating_page(fitness_center_id, trainer_id):
    with SQLiteDatabase('base.db') as db:
        if request.method == 'GET':
            rating = db.select(table_name='reviews', method='fetchall',
                               conditions={'trainer_id': trainer_id, 'fitness_center_id': fitness_center_id},
                               columns=['trainers.name AS trainer_name', 'reviews.points', 'reviews.user_name',
                                        'reviews.text'],
                               join_conditions={'trainers': {'reviews.trainer_id': 'trainers.id'}}
                               )
            return render_template('rating.html', title='Рейтинг', rating=rating, fitness_center_id=fitness_center_id,
                                   trainer_id=trainer_id)
        if request.method == 'POST':
            form_data = request.form
            user_name = form_data.get('name')
            points = form_data.get('points')
            text = form_data.get('text')
            db.commit('reviews', {'trainer_id': trainer_id, 'user_name': user_name, 'points': points, 'text': text})
            return render_template('index.html')
        if request.method == 'PUT':
            return f'Rating of the trainer {trainer_id} updated! Fitness center id: {fitness_center_id}'


@app.get('/fitness_center/<int:fitness_center_id>/services')
def get_services_page(fitness_center_id):
    with SQLiteDatabase('base.db') as db:
        services = db.select(table_name='services', method='fetchall',
                             conditions={'fitness_center_id': fitness_center_id},
                             columns=['services.id AS service_id', 'services.name AS service_name',
                                      'services.price',
                                      'services.duration', 'fitness_centers.name AS fitness_center_name'],
                             join_conditions={
                                 'fitness_centers': {'services.fitness_center_id': 'fitness_centers.id'}})
        if not services:
            return 'Services not found'
        return services


@app.get('/fitness_center/<int:fitness_center_id>/services/<int:service_id>')
def get_service_id_page(fitness_center_id, service_id):
    with SQLiteDatabase('base.db') as db:
        service = db.select(table_name='services', method='fetchone',
                            conditions={'fitness_center_id': fitness_center_id, 'services.id': service_id},
                            columns=['services.id AS service_id', 'services.name AS service_name', 'services.price',
                                     'services.duration', 'fitness_centers.name AS fitness_center_name'],
                            join_conditions={'fitness_centers': {'services.fitness_center_id': 'fitness_centers.id'}})
        if not service:
            return 'Service not found'
        return service


@app.route('/fitness_center/<int:fitness_center_id>/loyalty_program', methods=['GET', 'POST', 'PUT'])
def get_loyalty_program_page(fitness_center_id):
    if request.method == 'GET':
        return f'Welcome to the list of the loyalty programs! Fitness center id: {fitness_center_id}'
    if request.method == 'POST':
        return f'Loyalty program created! Fitness center id: {fitness_center_id}'
    if request.method == 'PUT':
        return f'Loyalty program updated! Fitness center id: {fitness_center_id}'


if __name__ == '__main__':
    app.run(debug=True)
