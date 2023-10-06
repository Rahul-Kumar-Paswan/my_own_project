from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'mysql'  # This should match the service name in docker-compose.yaml
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'my_db'

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_PORT'] = 3306  # Change to the port you set in docker-compose.yaml



mysql = MySQL(app)


# Secret key for sessions
app.secret_key = 'your_secret_key'

# ... routes and other app configurations ...

# Set cache control headers to prevent caching for protected routes

@app.after_request
def add_no_cache_headers(response):
    if 'user' not in session:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response


@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials in the MySQL database (users table)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and user[2] == password:  # Index 2 corresponds to the 'password' column
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            return redirect(url_for('index'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            flash('User already exists. Please log in.', 'warning')
            return redirect(url_for('index'))
        else:
            # Create a new user in the MySQL database
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            cur.close()

            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        username = session['user']
        return render_template('dashboard.html', username=username)
    else:
        flash('You must log in first.', 'warning')
        return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))  # Redirect to the login page after logout

if __name__ == '__main__':
    app.run(host="0.0.0.0" , port=int("3000"),debug=True)