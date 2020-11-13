from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    position = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(15), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', backref='pic', lazy='dynamic')

    def __repr__(self):
        return f'<User: username={self.username}, is_admin={self.is_admin}>'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email in current_app.config['ADMINS']:
            self.is_admin = True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_as_admin(self):
        self.is_admin = True

    def remove_as_admin(self):
        self.is_admin = False

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, default='-')
    type = db.Column(db.String(20), index=True, default='-')
    in_timestamp = db.Column(db.Date, index=True)
    out_timestamp = db.Column(db.Date, index=True)
    serial_number = db.Column(db.String(20), index=True, default='-')
    product_number = db.Column(db.String(20), index=True, default='-')
    note = db.Column(db.String(100), index=True, default='-')
    length = db.Column(db.String(20), index=True, default='-')
    capacity = db.Column(db.String(20), index=True, default='-')
    status = db.Column(db.String(20), index=True)
    in_filename_record_of_transfer = db.Column(db.String(100), default='-', nullable=True)
    in_url_record_of_transfer = db.Column(db.String(100), default='-', nullable=True)
    out_filename_record_of_transfer = db.Column(db.String(100), default='-', nullable=True)
    out_url_record_of_transfer = db.Column(db.String(100), default='-', nullable=True)
    user_id = db.Column(db.String(20), db.ForeignKey('user.name'))

    def __repr__(self):
        return f'<Item {self.name}, {self.type}, {self.in_timestamp}, {self.in_timestamp}, \
            {self.serial_number}, {self.product_number}, {self.note}, {self.length}, {self.capacity}, \
                {self.status}, {self.in_filename_record_of_transfer}, {self.in_url_record_of_transfer}, \
                    {self.out_filename_record_of_transfer}, {self.out_url_record_of_transfer}>'

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.status = 'available'

    def taken_out(self):
        self.status = 'taken-out'