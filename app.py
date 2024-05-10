from flask import Flask, request

app = Flask(__name__)


@app.get('/')
def index():
    return 'Welcome to the main page!'


@app.route('/register', methods=['GET', 'POST'])
def get_register_page():
    if request.method == 'GET':
        return 'Welcome to the registration page'
    else:
        return 'Registration success'


@app.route('/login', methods=['GET', 'POST'])
def get_login_page():
    if request.method == 'GET':
        return 'Welcome to the login page'
    else:
        return 'Login success'


@app.route('/user', methods=['GET', 'POST', 'PUT'])
def get_user_page():
    if request.method == 'GET':
        return 'Welcome to your profile page'
    if request.method == 'POST':
        return 'User created'
    if request.method == 'PUT':
        return 'User updated'


@app.route('user/funds', methods=['GET', 'POST'])
def get_funds_page():
    if request.method == 'GET':
        return 'Welcome to your funds page'
    if request.method == 'POST':
        return 'Add something to funds'


@app.route('/user/reservations', methods=['GET', 'POST', 'PUT'])
def get_reservations_page():
    if request.method == 'GET':
        return 'Welcome to your reservations page'
    if request.method == 'POST':
        return 'Reservations created'
    if request.method == 'PUT':
        return 'Reservations updated'


@app.route('/user/reservations/<int:reservation_id>', methods=['GET', 'PUT', 'DELETE'])
def get_reservation_page(reservation_id):
    if request.method == 'GET':
        return f'Your reservation id is: {reservation_id}'
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
    return 'welcome to the list of the fitness centers'


@app.get('/fitness_center/<int:fitness_center_id>')
def get_fitness_center_id_page(fitness_center_id):
    return f'Welcome to the Fitness center {fitness_center_id}'


@app.get('/fitness_center/<int:fitness_center_id>/trainer')
def get_trainer_page(fitness_center_id):
    return f'Welcome to the list of the trainers! Fitness center id: {fitness_center_id}'


@app.get('/fitness_center/<int:fitness_center_id>/trainer/<int:trainer_id>')
def get_trainer_id_page(fitness_center_id, trainer_id):
    return f'Welcome to the trainer {trainer_id}! Fitness center id: {fitness_center_id}'


@app.route('/fitness_center/<int:fitness_center_id>/trainer/<int:trainer_id>/rating', methods=['GET', 'POST', 'PUT'])
def get_trainer_rating_page(fitness_center_id, trainer_id):
    if request.method == 'GET':
        return f'Rating of the trainer {trainer_id}! Fitness center id: {fitness_center_id}'
    if request.method == 'POST':
        return f'Rating of the trainer {trainer_id} created! Fitness center id: {fitness_center_id}'
    if request.method == 'PUT':
        return f'Rating of the trainer {trainer_id} updated! Fitness center id: {fitness_center_id}'


@app.get('/fitness_center/<int:fitness_center_id>/services')
def get_services_page(fitness_center_id):
    return f'Welcome to the list of the services! Fitness center id: {fitness_center_id}'


@app.get('/fitness_center/<int:fitness_center_id>/services/<int:service_id>')
def get_service_id_page(fitness_center_id, service_id):
    return f'Welcome to the service {service_id}! Fitness center id: {fitness_center_id}'


@app.route('/fitness_center/<int:fitness_center_id>/loyalty_program', methods=['GET', 'POST', 'PUT'])
def get_loyalty_program_page(fitness_center_id):
    if request.method == 'GET':
        return f'Welcome to the list of the loyalty programs! Fitness center id: {fitness_center_id}'
    if request.method == 'POST':
        return f'Loyalty program created! Fitness center id: {fitness_center_id}'
    if request.method == 'PUT':
        return f'Loyalty program updated! Fitness center id: {fitness_center_id}'


if __name__ == '__main__':
    app.run()
