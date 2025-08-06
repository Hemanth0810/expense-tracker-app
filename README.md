# Expense Tracker

## Live Demo
Check out the live application hosted on Render:  
[Expense Tracker Live Demo](https://my-expense-tracker-z8u3.onrender.com)

## Overview
This modern, user-friendly **Expense Tracker** web application helps users track personal expenses, visualize spending trends by category, and manage finances efficiently. Built with Python and Flask, it features a responsive and attractive dashboard with interactive charts and secure user management.

## Features
- ✅ User registration and login with secure password hashing using Flask-Login  
- 💸 Add, view, and categorize expenses with descriptions  
- 📊 Interactive dashboard with category-wise doughnut/pie charts and monthly spending trend line charts using Chart.js  
- 🔍 Search and filter recent transactions with live frontend search functionality  
- 🌙 Responsive dark-themed UI inspired by professional finance apps like PocketGuard  
- 🚀 Ready for deployment on Render (or Heroku) with PostgreSQL support for production

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy  
- **Frontend:** Bootstrap 5, Chart.js, Bootstrap Icons  
- **Database:** SQLite (development), PostgreSQL (production)  
- **Authentication:** Flask-Login  
- **Deployment:** Render / Heroku compatible  

## Installation
To run the project locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/yourusername/expense_tracker.git
cd expense_tracker

# (Optional) Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# (Optional) Set environment variables for local development
export FLASK_ENV=development
export SECRET_KEY='your-secret-key'

# Initialize the database tables (first time only)
python app.py
```

## Usage
- Run the Flask app locally:  
  ```bash
  python app.py
  ```
- Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)  
- Register a new user, log in, add expenses, and track your spending.

## Deployment

### Live App URL
Access the live deployed app here:  
[https://my-expense-tracker-z8u3.onrender.com](https://my-expense-tracker-z8u3.onrender.com)

### Render Deployment
- Ensure a `Procfile` exists in the root with:  
  ```
  web: gunicorn app:app
  ```
- Set environment variables in your Render dashboard:  
  - `SECRET_KEY`  
  - `DATABASE_URL` (PostgreSQL connection string)

- Connect your GitHub repo and enable automatic deploys for seamless updates.



## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes and new features.

#Finance #ExpenseTracker #Flask #Python #Bootstrap #ChartJS #WebApp #RenderDeployment
