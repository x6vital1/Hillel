from flask import Flask, request
from database_utils import SQLiteDatabase

app = Flask(__name__)


@app.get('/')
def index():
    return 'Welcome to the main page'


@app.route('/register', methods=['GET', 'POST'])
def get_register_page():
    if request.method == 'GET':
        return """
        <form action="/register" method="post">
            <label for="username">Имя пользователя:</label>
            <input type="text" name="username" placeholder="Username"><br>
            <br>
            <label for="password">Пароль:</label>
            <input type="password" name="password" placeholder="Password"><br>
            <br>
            <label for="birthday">Дата рождения:</label>
            <input type="date" name='birthday' placeholder="Birthday"><br>
            <br>
            <label for="phone">Телефон:</label>
            <input type="text" name='phone' placeholder="+380(__)___-__-__"><br>
            <br>
            <button type="submit">Регистрация</button>
        </form>
        """
    else:
        with SQLiteDatabase('base.db') as db:
            form_data = request.form
            user_name = form_data.get('username')
            password = form_data.get('password')
            birthday = form_data.get('birthday')
            phone = form_data.get('phone')
            db.commit(
                'INSERT INTO users (login, password, birth_date, phone) VALUES (?, ?, ?, ?)',
                (user_name, password, birthday, phone)
            )

        return 'Registration success'


@app.route('/login', methods=['GET', 'POST'])
def get_login_page():
    if request.method == 'GET':
        return '''
    <form action="/login" method="post">
        <label for="username">Имя пользователя:</label>
        <input type="text" name="username" placeholder="Username"><br>
        <br>
        <label for="password">Пароль:</label>
        <input type="password" name="password" placeholder="Password"><br>
        <br>
        <button type="submit">Вход</button>
    </form>
    '''
    else:
        form_data = request.form
        user_name = form_data.get('username')
        password = form_data.get('password')
        with SQLiteDatabase('base.db') as db:
            user = db.fetch_one('SELECT * FROM users WHERE login = ? AND password = ?', (user_name, password))
            if user:
                return 'Login success'
            else:
                return 'Login failed'


@app.route('/user', methods=['GET', 'POST', 'PUT'])
def get_user_page():
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            users = db.fetch_all('SELECT * FROM users')
            return users
    if request.method == 'POST':
        return 'User created'
    if request.method == 'PUT':
        return 'User updated'


@app.route('/user/funds', methods=['GET', 'POST'])
def get_funds_page():
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            funds = db.fetch_all('SELECT funds FROM users')
            return funds
    if request.method == 'POST':
        return 'Add something to funds'


@app.route('/user/reservations', methods=['GET', 'POST', 'PUT'])
def get_reservations_page():
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            reservations = db.fetch_all('SELECT * FROM reservations')
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
            reservation = db.fetch_one('SELECT * FROM reservations WHERE id = ?', (reservation_id,))
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


@app.get('/fitness_center')
def get_fitness_center_page():
    with SQLiteDatabase('base.db') as db:
        fitness_centers = db.fetch_all('SELECT * FROM fitness_centers')
        if not fitness_centers:
            return 'Fitness centers not found'
        return fitness_centers


@app.get('/fitness_center/<int:fitness_center_id>')
def get_fitness_center_id_page(fitness_center_id):
    with SQLiteDatabase('base.db') as db:
        fitness_center = db.fetch_one('SELECT * FROM fitness_centers WHERE id = ?', (fitness_center_id,))
        if not fitness_center:
            return 'Fitness center not found'
        return fitness_center


@app.get('/fitness_center/<int:fitness_center_id>/trainers')
def get_trainer_page(fitness_center_id):
    with SQLiteDatabase('base.db') as db:
        trainers = db.fetch_all('SELECT * FROM trainers WHERE fitness_center_id = ?', (fitness_center_id,))
        if not trainers:
            return 'Trainers not found'
        return trainers


@app.get('/fitness_center/<int:fitness_center_id>/trainers/<int:trainer_id>')
def get_trainer_id_page(fitness_center_id, trainer_id):
    with SQLiteDatabase('base.db') as db:
        trainer = db.fetch_one('SELECT * FROM trainers WHERE fitness_center_id = ? AND id = ?',
                               (fitness_center_id, trainer_id))
        if not trainer:
            return 'Trainer not found'
        return trainer


@app.route('/fitness_center/<int:fitness_center_id>/trainers/<int:trainer_id>/rating', methods=['GET', 'POST', 'PUT'])
def get_trainer_rating_page(fitness_center_id, trainer_id):
    if request.method == 'GET':
        with SQLiteDatabase('base.db') as db:
            rating = db.fetch_one('SELECT * from reviews WHERE trainer_id = ?',
                                  (trainer_id,))
            if not rating:
                return 'Rating not found'
            return rating
    if request.method == 'POST':
        return f'Rating of the trainer {trainer_id} created! Fitness center id: {fitness_center_id}'
    if request.method == 'PUT':
        return f'Rating of the trainer {trainer_id} updated! Fitness center id: {fitness_center_id}'


@app.get('/fitness_center/<int:fitness_center_id>/services')
def get_services_page(fitness_center_id):
    with SQLiteDatabase('base.db') as db:
        services = db.fetch_all('SELECT * FROM services WHERE fitness_center_id = ?', (fitness_center_id,))
        if not services:
            return 'Services not found'
        return services


@app.get('/fitness_center/<int:fitness_center_id>/services/<int:service_id>')
def get_service_id_page(fitness_center_id, service_id):
    with SQLiteDatabase('base.db') as db:
        service = db.fetch_one('SELECT * FROM services WHERE fitness_center_id = ? AND id = ?',
                               (fitness_center_id, service_id))
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
