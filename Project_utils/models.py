from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db_utils import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    login = Column(String(50), unique=True, nullable=False)
    funds = Column(Integer, nullable=False, default=0)
    password = Column(String(50), nullable=False)
    birth_date = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    reservations = relationship("Reservation", back_populates="user")
    reviews = relationship("Review", back_populates="user")

    def __repr__(self):
        return f'<User {self.id}>'


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    max_attendees = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Service {self.id}>'


class Trainer(Base):
    __tablename__ = 'trainers'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50), nullable=False)
    fitness_center_id = Column(Integer, ForeignKey('fitness_centers.id'), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)
    fitness_center = relationship("FitnessCenter", back_populates="trainers")
    reviews = relationship("Review", back_populates="trainer")
    services = relationship("TrainerServices", back_populates="trainer")

    def __repr__(self):
        return f'<Trainer {self.id}>'


class FitnessCenter(Base):
    __tablename__ = 'fitness_centers'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    address = Column(String(50), nullable=False)
    contacts = Column(String(50), nullable=False)
    trainers = relationship("Trainer", back_populates="fitness_center")
    services = relationship("FitnessService", back_populates="fitness_center")

    def __repr__(self):
        return f'<FitnessCenter {self.id}>'


class TrainerServices(Base):
    __tablename__ = 'trainer_services'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    capacity = Column(Integer, nullable=False)
    services = relationship("Service")
    trainer = relationship("Trainer", back_populates="services")

    def __repr__(self):
        return f'<TrainerService {self.id}>'


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=False)
    points = Column(Integer, nullable=False)
    text = Column(String(250), nullable=False)
    user = relationship("User", back_populates="reviews")
    trainer = relationship("Trainer")

    def __repr__(self):
        return f'<Review {self.id}>'


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=False)
    date = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False)
    user = relationship("User", back_populates="reservations")
    service = relationship("Service")
    trainer = relationship("Trainer")

    def __repr__(self):
        return f'<Reservation {self.id}>'


class FitnessService(Base):
    __tablename__ = 'fitness_services'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    fitness_center_id = Column(Integer, ForeignKey('fitness_centers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    fitness_center = relationship("FitnessCenter", back_populates="services")

    def __repr__(self):
        return f'<FitnessService {self.id}>'


class TrainerSchedule(Base):
    __tablename__ = 'trainer_schedule'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=False)
    date = Column(String(50), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<TrainerSchedule {self.id}>'
