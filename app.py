import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func, extract, desc
from extensions import db, login_manager
from models import User, Expense

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    if os.environ.get('DATABASE_URL'):
        # Production (PostgreSQL)
        database_url = os.environ.get('DATABASE_URL')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Development (SQLite)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            # Validation
            if len(username) < 3:
                flash('Username must be at least 3 characters long.', 'danger')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('register.html')
            
            # Check if user exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
                return render_template('register.html')
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Get current month expenses
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        monthly_total = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            extract('month', Expense.date) == current_month,
            extract('year', Expense.date) == current_year
        ).scalar() or 0
        
        # Get category-wise expenses for current month
        category_expenses = db.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == current_user.id,
            extract('month', Expense.date) == current_month,
            extract('year', Expense.date) == current_year
        ).group_by(Expense.category).all()
        
        # Get recent expenses
        recent_expenses = Expense.query.filter_by(user_id=current_user.id)\
            .order_by(desc(Expense.date)).limit(10).all()
        
        # Get total expenses
        total_expenses = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id
        ).scalar() or 0
        
        return render_template('dashboard.html',
                             monthly_total=monthly_total,
                             total_expenses=total_expenses,
                             category_expenses=category_expenses,
                             recent_expenses=recent_expenses)
    
    @app.route('/expenses', methods=['GET', 'POST'])
    @login_required
    def expenses():
        if request.method == 'POST':
            amount = float(request.form['amount'])
            description = request.form['description']
            category = request.form['category']
            date_str = request.form['date']
            
            # Parse date
            expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            expense = Expense(
                amount=amount,
                description=description,
                category=category,
                date=expense_date,
                user_id=current_user.id
            )
            
            db.session.add(expense)
            db.session.commit()
            
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expenses'))
        
        # Get filters
        search = request.args.get('search', '')
        category_filter = request.args.get('category', '')
        
        # Build query
        query = Expense.query.filter_by(user_id=current_user.id)
        
        if search:
            query = query.filter(Expense.description.contains(search))
        
        if category_filter:
            query = query.filter_by(category=category_filter)
        
        expenses_list = query.order_by(desc(Expense.date)).all()
        
        # Get all categories for filter dropdown
        categories = db.session.query(Expense.category.distinct()).filter_by(user_id=current_user.id).all()
        categories = [cat[0] for cat in categories]
        
        return render_template('expenses.html',
                             expenses=expenses_list,
                             categories=categories,
                             search=search,
                             category_filter=category_filter)
    
    # Edit expense route
    @app.route('/edit-expense/<int:expense_id>', methods=['GET', 'POST'])
    @login_required
    def edit_expense(expense_id):
        expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
        
        if request.method == 'POST':
            expense.amount = float(request.form['amount'])
            expense.description = request.form['description']
            expense.category = request.form['category']
            expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            
            db.session.commit()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('expenses'))
        
        return jsonify({
            'id': expense.id,
            'amount': expense.amount,
            'description': expense.description,
            'category': expense.category,
            'date': expense.date.strftime('%Y-%m-%d')
        })

    # Delete expense route
    @app.route('/delete-expense/<int:expense_id>', methods=['POST'])
    @login_required
    def delete_expense(expense_id):
        expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
        return redirect(url_for('expenses'))
    
    @app.route('/api/chart-data')
    @login_required
    def chart_data():
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        category_expenses = db.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == current_user.id,
            extract('month', Expense.date) == current_month,
            extract('year', Expense.date) == current_year
        ).group_by(Expense.category).all()
        
        return jsonify({
            'categories': [exp.category for exp in category_expenses],
            'amounts': [float(exp.total) for exp in category_expenses]
        })
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
