from datetime import datetime
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Expense {self.description}: ${self.amount}>'

class UserLoginLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # Supports IPv6
    user_agent = db.Column(db.Text, nullable=True)  # Browser/device info
    login_successful = db.Column(db.Boolean, default=True, nullable=False)
    logout_time = db.Column(db.DateTime, nullable=True)
    session_duration = db.Column(db.Integer, nullable=True)  # Duration in minutes
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('login_logs', lazy=True, cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<LoginLog {self.user.username} at {self.login_time}>'
