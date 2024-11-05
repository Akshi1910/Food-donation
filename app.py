# app.py
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime
app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="college"
)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS hotels (
        id INT AUTO_INCREMENT PRIMARY KEY,
        hotel_name VARCHAR(255),
        location VARCHAR(255),
        contact_person VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(255),
        additional_info TEXT
    )
""")
db.commit()
# Create the volunteers table with relevant fields


@app.route('/')
def home():
    return render_template('index.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# @app.route('/register_hotel')
# def register_hotel():
#     return render_template('register_hotel.html')
# Register routes
@app.route('/register_volunteer', methods=['GET', 'POST'])
def register_volunteer():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get("name")
        location = request.form.get("location")
        email = request.form.get("email")
        phone = request.form.get("phone")
        additional_info = request.form.get("additional_info")
        password = request.form.get("password")

        # Insert data into the volunteers table
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO volunteers (name, location, email, phone, additional_info,password)
            VALUES (%s, %s, %s, %s, %s,%s)
        """, (name, location, email, phone, additional_info,password))
        db.commit()

        # Redirect or render a confirmation page
        return redirect(url_for('confirm_registration_volunteer'))

    return render_template('register_volunteer.html')


@app.route('/register_hotel', methods=['GET', 'POST'])
def register_hotel():
    if request.method == 'POST':
        # Get form data from the request
        hotel_name = request.form.get("hotel_name")
        location = request.form.get("location")
        contact_person = request.form.get("contact_person")
        email = request.form.get("email")
        phone = request.form.get("phone")
        additional_info = request.form.get("additional_info")
        password=request.form.get("password")

        # Insert data into hotels table
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO hotels (hotel_name, location, contact_person, email, phone, additional_info,password)
            VALUES (%s, %s, %s, %s, %s, %s,%s)
        """, (hotel_name, location, contact_person, email, phone, additional_info,password))
        db.commit()

        # Redirect or render a confirmation page
        return redirect(url_for('confirm_food'))

    return render_template('register_hotel.html')

# View and Accept Food route for volunteers
@app.route('/view_donations')
def view_donations():
    # Logic to retrieve available food donations for volunteers
    pass

# Other routes for posting food, viewing donations, etc., as needed

# Ensure tables exist
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_donations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        meal_type VARCHAR(255),
        meal_time VARCHAR(255),
        quantity INT,
        time_prepared INT
    )
""")
db.commit()

from datetime import datetime

@app.route('/food_details', methods=["GET", "POST"])
def food_details():
    if request.method == "POST":
        meal_type = request.form.get("meal_type")
        meal_time = request.form.getlist("meal_time")
        quantity = request.form.get("quantity")
        time_prepared = request.form.get("time_prepared")
        donation_time = datetime.now()  # Capture current date and time

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO food_donations (meal_type, meal_time, quantity, time_prepared, donation_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (meal_type, ', '.join(meal_time), quantity, time_prepared, donation_time))
        db.commit()

        return redirect(url_for('confirm_food'))

    return render_template("food_details.html")

@app.route('/accept_donation/<int:donation_id>', methods=['POST'])
def accept_donation(donation_id):
    cursor = db.cursor()
    cursor.execute("UPDATE food_donations SET status = %s WHERE id = %s", ('Accepted', donation_id))
    db.commit()
    return redirect(url_for('view_food_donations'))

@app.route('/confirm_food')
def confirm_food():
    return render_template("confirm_food.html")
@app.route('/hotel_donations')
def hote_donations():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_donations")
    donations = cursor.fetchall()  # Fetch all records from the table
    cursor.close()
    return render_template("hotel_donations.html",donations=donations)

# Volunteer Login Route
@app.route('/login_volunteer', methods=['GET', 'POST'])
def login_volunteer():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        cursor = db.cursor(dictionary=True, buffered=True)

        # Check in the volunteers table
        cursor.execute("SELECT * FROM volunteers WHERE email = %s AND password = %s", (email, password))
        volunteer = cursor.fetchone()
        cursor.close()

        if volunteer:
            print("Redirecting to volunteer dashboard")
            return redirect(url_for('volunteer_dashboard'))
        else:
            print("Volunteer login failed")
            return "Volunteer login failed. Please check your email and password."

    return render_template('login_volunteer.html')

# Hotel Login Route
@app.route('/login_hotel', methods=['GET', 'POST'])
def login_hotel():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        cursor = db.cursor(dictionary=True, buffered=True)

        # Check in the hotels table
        cursor.execute("SELECT * FROM hotels WHERE email = %s AND password = %s", (email, password))
        hotel = cursor.fetchone()
        cursor.close()

        if hotel:
            print("Redirecting to hotel dashboard")
            return redirect(url_for('hotel_dashboard'))
        else:
            print("Hotel login failed")
            return "Hotel login failed. Please check your email and password."

    return render_template('login_hotel.html')




# Dashboard routes
@app.route('/volunteer_dashboard')
def volunteer_dashboard():
    return "<h2>Welcome to the Volunteer Dashboard</h2>"

@app.route('/hotel_dashboard')
def hotel_dashboard():
    return render_template('hotel_dashboard.html')

@app.route('/view_food_donations')
def view_food_donations():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_donations")
    donations = cursor.fetchall()  # Fetch all records from the table
    cursor.close()
    return render_template('view_food_donations.html', donations=donations)



if __name__ == '__main__':
    app.run(debug=True)
