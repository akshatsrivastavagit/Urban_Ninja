from flask import url_for, session,redirect
from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template,request, jsonify,session,flash
from collections import OrderedDict
import mysql.connector
import json,math
import datetime
import random
import razorpay
app = Flask(__name__)

# MySQL configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'group-project-1',
    'autocommit': True  
}


razorpay_client = razorpay.Client(auth=("rzp_live_43e1pUrpHcn2bx", "RjM9HVzuS0xJIkQpvpdNELkx"))

@app.route('/create_order', methods=['POST'])
def create_order():
    amount = request.form.get('amount')
    order = razorpay_client.order.create({
        "amount": int(amount),
        "currency": "INR",
        "payment_capture": "1"
    })
    return order

@app.route('/payment_success', methods=['GET'])
def payment_success():
    payment_id = request.args.get('payment_id')
    # Fetch payment details from Razorpay and update your database
    payment_details = razorpay_client.payment.fetch(payment_id)
    # Your logic to save payment details in the database

    return render_template('payment_success.html', payment_details=payment_details)

@app.route('/payment_failure')
def payment_failure():
    return render_template('payment_failure.html')

COMPANY_KEY = ["mehak875preet@gmail.com","akshatgreninja@gmail.com","12213088","12212952","12215849","12221451"]

@app.route('/show_database')
def show_database():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    tables = ['users_table','user_bookings','user_booked_services','user_cart_table','technician_booking_table','technician_table','tech_expertise_table','payments_table',
        'major_category_table', 'sub_category_table','segmentation_table','package_table','service_table','offers_table','warranty_table','reviews'
    ]
    
    database_info = {}
    
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        columns = cursor.column_names
        rows = cursor.fetchall()
        database_info[table] = {'columns': columns, 'rows': rows}
    
    cursor.close()
    conn.close()
    
    return render_template('show_database.html', database_info=database_info)







app.secret_key = '!secret'
app.config.from_object('config')
# Google OAuth configuration
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/login')
def login():
    
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    user = session['user']
    insert_user(user.name,user.email)
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

def insert_user(name:str, email:str):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users_table")
        getall_data=[dict(x) for x in cursor.fetchall()]
        for x in getall_data:
            if x['user_email'] == email:
                return None
        sql = "INSERT INTO `users_table` (`user_name`, `user_email`) VALUES (%s, %s)"
        try:
            cursor.execute(sql, (name, email))
        except mysql.connector.Error as err:
            print(f"Error inserting user: {err}")
    except: 
        return "connection error"







@app.route('/')
@app.route('/homepage')
def homepage():

    try:
        session['counter']=0
        session["varforrouteauth"]=''
        # Connect to MySQL database
        session['booking_confirmed']=False
        # Connect to MySQL database
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        print("Connection successfull in homepage")
        # Fetch major categories
        cursor.execute("SELECT mc_id, mc_name FROM major_category_table")
        major_categories = cursor.fetchall()

        # Iterate through major categories and fetch their subcategories
        for category in major_categories:
            cursor.execute("SELECT sc_id, sc_name FROM sub_category_table WHERE mc_id = %s", (category['mc_id'],))
            subcategories = cursor.fetchall()
            category['subcategories'] = subcategories
        city_message = session.pop('city_message', None)

        cursor.close()
        conn.close()
        return render_template('homepage.html', major_categories=major_categories,city_message=city_message)
    
    except Exception as e:
        print("Error fetching major categories:", e)
        return "Error fetching major categories"

@app.route("/subcategory/<sc_id>")
def show_subcategory(sc_id):
    # user = session.get('user')
    # if not user:
    #     global session["varforrouteauth"]
    #     session["varforrouteauth"] = f'/segment/{sc_id}'
    #     return redirect(url_for('login'))

    # # Fetch user details from session

    # user_email = user['email']
    # user_name = user['name']
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        print(1)
        cursor.execute("select * from reviews")
        reviews = cursor.fetchall()
        print(2)
        print(reviews)
        # Fetch segmentation types for the given subcategory
        cursor.execute("SELECT segmentation_type_id, segmentation_type_name FROM segmentation_table WHERE sc_id = %s", (sc_id,))
        segments = cursor.fetchall()
        
        print(3)
        # Fetch packages for the given subcategory
        cursor.execute("SELECT package_id, package_name, package_front_description, faq,segmentation_type_id FROM package_table WHERE sc_id = %s", (sc_id,))
        packages = cursor.fetchall()
        
        print(4)
        # Fetch services for each package
        for package in packages:
            cursor.execute("SELECT * FROM service_table  WHERE package_id = %s", (package['package_id'],))
            package['services'] = cursor.fetchall()
        print(5)
        print("PACKAGE:",package)
        print("\nPACKAGE SERVICE:",package['services'])
        print("\nPACKAGE FAQ",package['faq'])
        if(package['faq'] != None):
            print(6)
            faq_dict = json.loads(package['faq'])
            conn.close()
            print(7)
            if(len(reviews)==0):
                return render_template('segment.html', segments=segments, packages=packages,subcategory_id=sc_id,fq=faq_dict)
            elif(reviews[0]['reviewText'] != None):
                return render_template('segment.html', segments=segments, packages=packages, reviews=reviews,subcategory_id=sc_id,fq=faq_dict)
            else:
                return render_template('segment.html', segments=segments, packages=packages,subcategory_id=sc_id,fq=faq_dict,reviews=reviews)
        else:
            print(8)
            if(len(reviews)==0):
                return render_template('segment.html', segments=segments, packages=packages,subcategory_id=sc_id,fq=faq_dict)
            elif(reviews[0]['reviewText'] != None):
                return render_template('segment.html', segments=segments, packages=packages, reviews=reviews,subcategory_id=sc_id)
            else:
                return render_template('segment.html', segments=segments, packages=packages,subcategory_id=sc_id,reviews=reviews)
    except Exception as e:
        print("Error in in subcategory page:", e)
        print("ERROR IS HERE")
        return "Error fetching details"


@app.route('/add_review', methods=['POST'])
def add_review():
    review = request.form['review']
    booking_id = request.form['booking_id']
    rating = request.form['rating']
    print("REVIEW OF",booking_id)
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reviews set reviewText = %s , rating = %s WHERE booking_id= %s",
            (review, rating,booking_id)
        )
        conn.commit()
        flash('Review submitted successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f"Error submitting review: {err}", 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('show_profile'))


@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    booking_id = request.form['booking_id']
    user_email=session['user']['email']
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user_bookings SET booking_status='Cancelled' WHERE booking_id=%s",
            (booking_id,)
        )
        cursor.execute("select amount from payments_table p Join user_bookings ub on p.UPI_Ref_No = ub.UPI_Ref_No WHERE ub.booking_id = %s", (booking_id,))
        amount_result = cursor.fetchone()
        if amount_result:
            amount = amount_result[0]
        cursor.fetchall()

        cursor.execute("delete from technician_booking_table where booking_id = %s", (booking_id,))
        print("No error")
        print("success in deletion from technician table")

        cursor.execute("select credits from users_table where user_email = %s", (user_email,))
        cred_result = cursor.fetchone()
        if cred_result:
            cred = cred_result[0]

        if(cred is not None):
            total=cred+amount
        else:
            total=amount
        cursor.execute("UPDATE users_table SET credits = %s WHERE user_email = %s",(total,user_email))
        conn.commit()
        flash('Booking cancelled successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f"Error cancelling booking: {err}", 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('show_profile'))

@app.route('/profile')
def show_profile():
    user_email = session.get('user', {}).get('email')
    if not user_email:
        return redirect(url_for('login'))

    profile = get_user_profile(user_email)
    return render_template('profile.html', profile=profile)

def get_user_profile(user_email):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch bookings along with reviews for the user
        cursor.execute("""
            SELECT 
                b.*,
                r.reviewText,
                r.rating,
                s.*,
                u.*    
            FROM 
                user_bookings b
            JOIN 
                user_booked_services bs ON b.booking_id = bs.booking_id
            JOIN 
                service_table s ON bs.service_id = s.service_id
            JOIN 
                reviews r ON r.booking_id = b.booking_id
            JOIN 
                users_table u on u.user_email = b.user_email
            WHERE 
                b.user_email = %s
        """, (user_email,))
        
        rows = cursor.fetchall()
        profile = {}

        for row in rows:
            booking_id = row['booking_id']
            session['user']['credits']=row['credits']
            if booking_id not in profile:
                profile[booking_id] = {
                    'booking_date_time': row['booking_date_time'],
                    'booked_date': row['booked_date'],
                    'booked_time': row['booked_time'],
                    'booking_status': row['booking_status'],
                    'OTP':row['otp'],
                    'credits':row['credits'],
                    'services': []
                }
            
            # Collect service details
            if row['service_id']:
                service_details = {
                    'service_name': row['service_name'],
                    'service_id': row['service_id'],
                    'price': row['price'],
                    'service_duration': row['service_duration']
                }
                profile[booking_id]['services'].append(service_details)
            
            # Add review details if present
            if row['reviewText'] and row['rating']:
                profile[booking_id]['reviewText'] = row['reviewText']
                profile[booking_id]['rating'] = row['rating']

    except mysql.connector.Error as err:
        flash(f"Error retrieving profile: {err}", 'danger')
        return {}
    finally:
        cursor.close()
        conn.close()
    sorted_profile = OrderedDict(
        sorted(profile.items(), key=lambda item: item[1]['booking_date_time'], reverse=True)
    )
    return sorted_profile


@app.route('/save_cart/<user_email>/<sc_id>', methods=['POST'])
def save_cart(user_email, sc_id):
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401

    try:
        data = request.json
        services = data['services']

        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch existing service IDs in the user's cart
        cursor.execute("SELECT service_id FROM user_cart_table WHERE user_email = %s", (user_email,))
        existing_services = cursor.fetchall()

        s_id_list = [service['service_id'] for service in existing_services]

        for service_id, service_data in services.items():
            if int(service_id) in s_id_list:
                # Service already exists in cart, update quantity
                cursor.execute("UPDATE user_cart_table SET quantity = quantity + %s WHERE service_id = %s AND user_email = %s",
                               (service_data['quantity'], service_id, user_email))
            else:
                # Service does not exist in cart, insert new record
                cursor.execute("INSERT INTO user_cart_table (user_email, sc_id, service_id, quantity) VALUES (%s, %s, %s, %s)",
                               (user_email, sc_id, service_id, service_data['quantity']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Cart saved successfully"}), 200

    except mysql.connector.Error as e:
        print("MySQL Error saving cart:", e)
        return jsonify({"error": "Error saving cart"}), 500


@app.route('/view_cart')
def view_cart():
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        user = session.get('user')
        if not user:
            session["varforrouteauth"] = '/view_cart'
            return redirect(url_for('login'))
        user_email = user['email']
        cursor.execute("""
            SELECT uc.service_id, s.service_name, s.price, uc.quantity, mc.mc_id, mc.mc_name, sc.sc_id, sc.sc_name
            FROM user_cart_table uc
            JOIN service_table s ON uc.service_id = s.service_id
            JOIN segmentation_table st ON s.segmentation_type_id = st.segmentation_type_id
            JOIN sub_category_table sc ON st.sc_id = sc.sc_id
            JOIN major_category_table mc ON sc.mc_id = mc.mc_id
            WHERE uc.user_email = %s
        """, (user_email,))

        cart_items = cursor.fetchall()

        grouped_items = {}
        for item in cart_items:
            sc_id = item['sc_id']
            if sc_id not in grouped_items:
                grouped_items[sc_id] = {
                    'sc_name': item['sc_name'],
                    'iitems': []
                }
            grouped_items[sc_id]['iitems'].append(item)
        
        sc_id = cart_items[-1]['sc_id'] if cart_items else None
        
        return render_template('cart.html', grouped_items=grouped_items, sc_id=sc_id)

    except mysql.connector.Error as e:
        print("Error fetching cart details:", e)
        return "Error fetching cart details"



@app.route('/remove_service', methods=['POST'])
def remove_service():
    data = request.json
    service_id = data['service_id']
    user = session.get('user')

    if not user:
        return jsonify({"error": "User not logged in"}), 401

    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch the current quantity of the service
        cursor.execute("SELECT quantity FROM user_cart_table WHERE user_email = %s AND service_id = %s", (user['email'], service_id))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "Service not found in cart"}), 404

        current_quantity = result['quantity']

        if current_quantity > 1:
            # Update the quantity and price if the quantity is greater than one
            cursor.execute(
                "UPDATE user_cart_table SET quantity = quantity - 1 WHERE user_email = %s AND service_id = %s",
                (user['email'], service_id)
            )
        else:
            # Delete the row if the quantity is one
            cursor.execute(
                "DELETE FROM user_cart_table WHERE user_email = %s AND service_id = %s",
                (user['email'], service_id)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Service removed successfully"}), 200
    except Exception as e:
        print("Error removing service:", e)
        return jsonify({"message": "Error removing service"}), 500

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    user = session.get('user')

    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM user_cart_table WHERE user_email = %s", (user['email'],))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Cart cleared successfully"}), 200
    except Exception as e:
        print("Error clearing cart:", e)
        return jsonify({"message": "Error clearing cart"}), 500




global quantitylist
quantitylist = []

@app.route('/proceed_to_booking', methods=['POST'])
def proceed_to_booking():
    data = request.json
    sc_id = data['sc_id']
    
    return jsonify({"message": "Proceeding to booking for sc_id " + str(sc_id)})


# if __name__ == '__main__':
#     app.run(debug=True)

def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/company_login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        key = request.form['key']
        if key in COMPANY_KEY:
            session['authenticated'] = True
            return redirect(url_for('admin_home'))
        else:
            flash('Invalid key, please try again.')
    return render_template('company_login.html')


@app.route('/admin')
def admin_home():
    return render_template('admin_home.html')


@app.route('/validate_upi', methods=['POST'])
def validate_upi():
    upi_ref_no = request.form['upi_ref_no']
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM payments_table WHERE UPI_Ref_no = %s", (upi_ref_no,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        if count > 0:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/update_payment', methods=['GET', 'POST'])
def update_payment():
    if 'authenticated' not in session:
        return redirect(url_for('company_login'))

    if request.method == 'POST':
        upi_ref_no = request.form['upi_ref_no']
        amount = request.form['amount']
        try:
            conn = mysql.connector.connect(**mysql_config)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM payments_table WHERE UPI_Ref_no = %s", (upi_ref_no,))
            count = cursor.fetchone()[0]
            if count > 0:
                flash('UPI Reference Number already exists. Please enter another one.')
            else:
                cursor.execute("INSERT INTO payments_table (UPI_Ref_no, amount) VALUES (%s, %s)", (upi_ref_no, amount))
                conn.commit()
                flash('Payment updated successfully!')
        except Exception as e:
            flash(f'Error updating payment: {e}')
        finally:
            cursor.close()
            conn.close()

    return render_template('update_payment.html')



@app.route('/company_logout')
def company_logout():
    session.pop('authenticated', None)
    return redirect(url_for('home'))

# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/technician_login', methods=['GET', 'POST'])
def technician_login():
    if request.method == 'POST':
        email = request.form['email']
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM technician_table WHERE tech_email = %s', (email,))
        technician = cursor.fetchone()
        cursor.close()
        conn.close()
        if technician:
            session['technician_id'] = technician['tech_id']
            return redirect(url_for('technician_portal'))
        else:
            flash('Invalid email, please try again.')
    return render_template('technician_login.html')

# Technician portal route
@app.route('/technician_portal')
def technician_portal():
    if 'technician_id' not in session:
        return redirect(url_for('technician_login'))

    technician_id = session['technician_id']
    print("TECHNICIAN ENTERED IN TECHNICIAN PORTAL:",technician_id)
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
        SELECT b.*,ub.*, t.tech_name, t.tech_email
FROM technician_booking_table b
JOIN user_bookings ub ON ub.booking_id = b.booking_id
JOIN technician_table t ON b.tech_id = t.tech_id
WHERE b.tech_id = %s;

    ''', (technician_id,))
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('technician_portal.html', bookings=bookings)
    except:
        print("You have no bookings")
        return "VOILA you have no bookings"

# Update booking status route
@app.route('/update_booking_status', methods=['POST'])
def update_booking_status():
    if 'technician_id' not in session:
        return redirect(url_for('technician_login'))

    booking_id = request.form['booking_id']
    entered_otp = request.form['otp']

    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT otp from
user_bookings 
WHERE booking_id = %s

""",(booking_id,))
    booking = cursor.fetchone()
    if booking:
        if booking['otp'] == int(entered_otp):
            cursor.execute('UPDATE user_bookings SET booking_status = "Completed" WHERE booking_id = %s ', (booking_id,))
            conn.commit()
            flash('Booking status updated successfully.')
        else:
            flash('Invalid OTP, please try again.')
    else:
        flash('Booking not found.')

    cursor.close()
    conn.close()
    return redirect(url_for('technician_portal'))

# Logout route
@app.route('/technician_logout')
def technician_logout():
    session.pop('technician_id', None)
    return redirect(url_for('technician_login'))

# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/get_package_details')
def get_package_details():
    package_id = request.args.get('package_id')
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        # Query to fetch services
        cursor.execute("SELECT service_name, price, service_duration FROM service_table WHERE package_id = %s", (package_id,))
        services = cursor.fetchall()

        # Query to fetch FAQ
        cursor.execute("SELECT faq FROM package_table WHERE package_id = %s", (package_id,))
        faq = cursor.fetchone()

        conn.close()

        if faq:
            return jsonify({'services': services, 'faq': faq['faq']})
        else:
            return jsonify({'services': services, 'faq': ''})

    except Exception as e:
        print("Error fetching package details:", e)
        return jsonify({'error': 'Error fetching package details'}), 500


@app.route('/dashboard')
def dashboard():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)

    # Total sales
    cursor.execute("SELECT SUM(amount) AS total_sales FROM payments_table")
    total_sales = cursor.fetchone()

    # Total bookings
    cursor.execute("SELECT COUNT(*) AS total_bookings FROM user_bookings")
    total_bookings = cursor.fetchone()

    # Total cancelled bookings
    cursor.execute("SELECT COUNT(*) AS total_cancelled_bookings FROM user_bookings WHERE booking_status = 'Cancelled'")
    total_cancelled_bookings = cursor.fetchone()

    # Sales data for line chart
    cursor.execute("""
        SELECT DATE(booking_date_time) as date, SUM(amount) as amount 
        FROM user_bookings
        JOIN payments_table ON user_bookings.UPI_Ref_No = payments_table.UPI_Ref_No
        GROUP BY DATE(booking_date_time)
    """)
    sales_data = cursor.fetchall()
    sales_data = {
        'dates': [row['date'].strftime('%Y-%m-%d') for row in sales_data],
        'amounts': [row['amount'] for row in sales_data]
    }

    # Bookings data for bar chart
    cursor.execute("SELECT DATE(booking_date_time) as date, COUNT(*) as count FROM user_bookings GROUP BY DATE(booking_date_time)")
    bookings_data = cursor.fetchall()
    bookings_data = {
        'dates': [row['date'].strftime('%Y-%m-%d') for row in bookings_data],
        'counts': [row['count'] for row in bookings_data]
    }

    # Top booked services
    cursor.execute("""
        SELECT service_table.service_name, COUNT(user_booked_services.service_id) as count 
        FROM user_booked_services
        JOIN service_table ON user_booked_services.service_id = service_table.service_id
        GROUP BY user_booked_services.service_id
        ORDER BY count DESC
        LIMIT 10
    """)
    top_services_data = cursor.fetchall()
    top_services_data = {
        'names': [row['service_name'] for row in top_services_data],
        'counts': [row['count'] for row in top_services_data]
    }

    # Revenue by location
    cursor.execute("""
        SELECT booked_location, SUM(final_amount) as amount 
        FROM user_bookings
        GROUP BY booked_location
    """)
    revenue_location_data = cursor.fetchall()
    revenue_location_data = {
        'locations': [row['booked_location'] for row in revenue_location_data],
        'amounts': [row['amount'] for row in revenue_location_data]
    }

    return render_template('dashboard.html', 
                           total_sales=total_sales, 
                           total_bookings=total_bookings, 
                           total_cancelled_bookings=total_cancelled_bookings,
                           sales_data=sales_data,
                           bookings_data=bookings_data,
                           top_services_data=top_services_data,
                           revenue_location_data=revenue_location_data)


@app.route('/technician_regularity')
def technician_regularity():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)
    
    # Fetching technician details and total bookings
    cursor.execute("""
        SELECT t.tech_id, t.tech_name, t.tech_email, COUNT(*) AS total_bookings 
        FROM user_bookings b 
        JOIN technician_table t ON b.tech_id = t.tech_id 
        GROUP BY t.tech_id, t.tech_name
    """)
    technicians = cursor.fetchall()
    
    # Fetching booking trends for each technician
    booking_trends = {}
    for tech in technicians:
        cursor.execute("""
            SELECT DATE(booking_date_time) as date, COUNT(*) as count 
            FROM user_bookings 
            WHERE tech_id = %s 
            GROUP BY DATE(booking_date_time)
        """, (tech['tech_id'],))
        trends = cursor.fetchall()
        booking_trends[tech['tech_id']] = {
            'dates': [row['date'].strftime('%Y-%m-%d') for row in trends],
            'counts': [row['count'] for row in trends]
        }
    
    return render_template('technician_regularity.html', 
                           technicians=technicians, 
                           booking_trends=booking_trends)





# @app.route('/distribution_of_amount')
# def distribution_of_amount():
#     conn = mysql.connector.connect(**mysql_config)
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT b.booking_id, b.user_email, b.tech_id, p.amount FROM user_bookings b JOIN payments_table p ON b.UPI_Ref_No = p.UPI_Ref_no")
#     bookings = cursor.fetchall()
#     return render_template('distribution_of_amt.html', bookings=bookings)



@app.route('/distribution_of_amount')
def distribution_of_amount():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT b.booking_id, b.user_email, b.tech_id, p.amount FROM user_bookings b JOIN payments_table p ON b.UPI_Ref_No = p.UPI_Ref_no")
    bookings = cursor.fetchall()
    return render_template('distribution_of_amt.html', bookings=bookings)
# if __name__ == '__main__':
#     app.run(debug=True)


cityname=""
@app.route('/check_city', methods=['POST'])
def check_city():
    global cityname
    city_name=request.form.get('cityName')
    phone=request.form.get('phoneNumber')
    session['city_name'] = city_name
    session['phone_number']=phone
    try:
        conn=mysql.connector.connect(**mysql_config)
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT available_for_cities FROM technician_table")
        cities_list=[row['available_for_cities'] for row in cursor.fetchall()]
        session['city_message']="Currently, we do not provide service at your city, but feel free to browse our services."
        for i in cities_list:
            if i.lower() in city_name.lower():
                cityname=i
                session['city_message']="Congratulations! We provide service at your location. Bookings are open!"
                break
        return redirect('/')
    
    except Exception as e:
        print("Error checking city:", e)
        session['city_message'] = "Error checking city"
        return "Error checking city"
    



def reset():
    session["selected_services"] = {
            "user_email":"",
            "sc_id":0,
            "services": [],
            "total_amount": 0,
            "total_duration": "",  # Initialize total_duration
            "total_minutes": 0,
            "offer_name": None,
            "offer_discount": 0,
            "discount_amt": 0,
            "discounted_total": 0,
            "offer_id": None,
            "credits_used": 0,
            "final_amount": 0,
            "phone":"",
            "slotdate":"",
            "slottime":"",
            "address":"",
            "upirefno":"",
            "tech_id":""
        }
# def get_service(user_email,sc_id):
#         session["selected_services"] = get_selected_services(user_email, sc_id)
@app.route('/payment_slot_booking/<sc_id>', methods=['GET', 'POST'])
def payment_slot_booking(sc_id):
    global counter
    session["varforrouteauth"] = f'/payment_slot_booking/{sc_id}'

    if session.get('booking_confirmed'):
        return redirect(url_for('homepage'))
    address=""
    user = session.get('user')
    if not user:
        session["varforrouteauth"] = '/payment_slot_booking/' + sc_id
        return redirect(url_for('login'))
    user_email = user['email']
    # session["selected_services"]["user_email"]=user["email"]
    if 'address' not in session:
        session['address'] = ''
    if 'phoneNumber' not in session:
        session['phoneNumber'] = ''
    if 'slot_date' not in session:
        session['slot_date'] = ''
    if 'slot_time' not in session:
        session['slot_time'] = ''
    session['sc_id']=sc_id
    if request.method == 'POST':
        purpose = request.form['purpose']
        if purpose == 'addressDetails':
            address = request.form['address']
            phone_number = request.form['phoneNumber']
            print("User address:", address, "\nPhone number:", phone_number)
            availability_result = availability(int(sc_id), session["selected_services"]['total_minutes'],address)
            print("SLOTS FETCHED:",availability_result)
            available_slots = json.loads(availability_result)
            session["selected_services"]['address'] = address
            session["selected_services"]['phone'] = phone_number
            return render_template('payment_slot.html', available_slots=available_slots,selected_services=session["selected_services"]) # Redirect to a success page after processing

        elif purpose == 'slotBooking':
            print("SELECTED SERVICES FOR SLOT BOOKIGN POST REQUEST\n",session["selected_services"])
            slot_date = request.form['slot_date']
            slot_time = request.form['slot_time']
            print("Date:", slot_date, "\nTime:", slot_time)
            session["selected_services"]['slotdate'] = slot_date
            session["selected_services"]['slottime'] = slot_time
            return render_template('payment_slot.html', available_slots={},selected_services=session["selected_services"])

        elif purpose=="verifyPayment":
            upiref= request.form.get('upiRefNo')
            print("VEIRFY PAYMENT POST REQUEST SELECTED SERVICES:\n",session["selected_services"])
            verify_payment_route(upiref)
            return render_template('payment_slot.html', available_slots={},selected_services=session["selected_services"])

    reset()
    get_selected_services(user_email,sc_id)
    print("PAYMENT_SLOT SELECTED SERVICES\n",session["selected_services"])
    if 'total_duration' in session["selected_services"]:
        availability_result = availability(int(sc_id), session["selected_services"]['total_minutes'],address)
        print("AVAILABILITY FETCHED BEFORE ADDRESS SELECTION:",availability_result)
        try:
            available_slots = json.loads(availability_result)
            return render_template('payment_slot.html', available_slots=available_slots,selected_services=session["selected_services"])
        except json.JSONDecodeError:
            return {"message": "Error processing availability."}
    return {"message": "No services selected or unable to calculate duration."}



def verify_payment(upi_ref_no, amount):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        # Query to check if the payment reference number and amount match in the database
        query = "SELECT * FROM payments_table WHERE UPI_Ref_No = %s AND Amount = %s"
        cursor.execute(query, (upi_ref_no, amount))
        result = cursor.fetchone()
        if result:
            if result['consumed']==1:
                return 'PAYMENT INVALID'  # Payment already consumed
            else:
                # update_query = "UPDATE payments_table SET Consumed = 1 WHERE UPI_Ref_No = %s"
                # cursor.execute(update_query, (upi_ref_no,))
                # conn.commit()
                session["selected_services"]['upirefno']=upi_ref_no
                return 'VALID PAYMENT'  # Payment valid and not consumed
        else:
            return 'PAYMENT INVALID'  # No matching payment found
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 'PAYMENT INVALID'  # Error occurred
    finally:
        cursor.close()
        conn.close()
def verify_payment_route(upiref):
    amount = session["selected_services"]['final_amount']
    payment_validity = verify_payment(upiref, amount)
    session["selected_services"]['payment_validity'] = payment_validity
# if __name__ == '__main__':
#     app.run(debug=True)
# @app.route('/availability/<int:sc_id>/<int:duration>', methods=['GET'])


def availability(sc_id, duration,address):
    print("\t\t\t\tRUNNING AVAILABILITY ROUTE")
    # address = "Jalna"
    city_name = ""
    if address == "":
        print("address==nope",address)
        return json.dumps({})
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT available_for_cities FROM technician_table")
        cities_list = [row['available_for_cities'].lower() for row in cursor.fetchall()]
        session['city_message'] = "Currently, we do not provide service at your city, but feel free to browse our services."
        for i in cities_list:
            if i in address.lower():
                city_name = i
                session['city_message'] = "Congratulations! We provide service at your location. Bookings are open!"
                break
    except Exception as e:
        print("Error checking city in availability route: ", e)
        return json.dumps({"error": "Error checking city in availability route"})
    
    try:
        cursor.execute("SELECT tech_id FROM technician_table WHERE available_for_cities LIKE %s ", ('%' + city_name + '%',))
        technician_ids = [row['tech_id'] for row in cursor.fetchall()]
        if not technician_ids:
            return json.dumps({"error": "No technicians available in your city."})
        print("TECHNICIAN ID's AVAILABLE IN CITY:",technician_ids)
        technician_slots = {tech_id: {} for tech_id in technician_ids}
        workload = {tech_id: 0 for tech_id in technician_ids}
        
        for tech_id in technician_ids:
            cursor.execute("SELECT sc_id FROM tech_expertise_table WHERE tech_id = %s", (tech_id,))
            tech_expertise = [row['sc_id'] for row in cursor.fetchall()]
            if sc_id not in tech_expertise:
                continue
            
            upcoming_dates = [(datetime.date.today() + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(5)]
            for date in upcoming_dates:
                cursor.execute("SELECT slot_time, service_duration FROM technician_booking_table WHERE tech_id = %s AND slot_date = %s", (tech_id, date))
                booked_slots = cursor.fetchall()
                booked_duration = sum(row['service_duration'] for row in booked_slots)
                workload[tech_id] += booked_duration
                
                all_slots = [(hour, minute) for hour in range(9, 21) for minute in [0, 30]]
                available_time_slots = []
                for start_hour, start_minute in all_slots:
                    end_minute = start_minute + duration
                    end_hour = start_hour + end_minute // 60
                    end_minute = end_minute % 60
                    if end_hour >= 21:
                        continue
                    
                    slot_start_time = f"{start_hour:02d}:{start_minute:02d}"
                    slot_end_time = f"{end_hour:02d}:{end_minute:02d}"
                    slot_str = f"{slot_start_time} - {slot_end_time}"
                    
                    is_conflicting = False
                    for booked_slot in booked_slots:
                        booked_start_time, booked_end_time = booked_slot['slot_time'].split(' - ')
                        if (slot_start_time < booked_end_time and slot_end_time > booked_start_time):
                            is_conflicting = True
                            break
                    
                    if not is_conflicting:
                        available_time_slots.append(slot_str)
                
                if available_time_slots:
                    technician_slots[tech_id][date] = available_time_slots
        
        if not technician_slots:
            return json.dumps({"error": "we do not provide service here."})

        # Select the technician with the least number of bookings
        least_busy_tech = min(workload, key=workload.get)
        
        print("WORKLOAD:", workload)
        print("\nALL TECHNICIAN SLOTS:\n",technician_slots)
        print("\nSELECTED TECHNICIAN WITH LEAST BOOKINGS:\n", least_busy_tech)
        print("\nLEAST BUSY TECH SLOTS:",technician_slots[least_busy_tech])
        session["selected_services"]['tech_id']=least_busy_tech
        return json.dumps(technician_slots[least_busy_tech])
    
    except Exception as e:
        print("Error fetching availability:", e)
        return json.dumps({"error": "Error fetching availability"})
    
    finally:
        cursor.close()
        conn.close()
def get_selected_services(user_email, sc_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch services from user_cart_table
        cursor.execute(
            "SELECT service_id, quantity FROM user_cart_table WHERE user_email = %s AND sc_id = %s",
            (user_email, sc_id)
        )
        services_rows = cursor.fetchall()
        if not services_rows:
            return {
                "services": [],
                "total_amount": 0,
                "total_duration": "0 minutes",
                "message": "Bonjour! Please add some items to your cart then visit this page."
            }

        session["selected_services"]['user_email']=user_email
        session["selected_services"]['sc_id']=sc_id
        total_minutes = 0

        for row in services_rows:
            service_id = row['service_id']
            quantity = row['quantity']

            # Fetch service details including price, duration, and warranty_id
            cursor.execute("SELECT service_name, price, service_duration, warranty_id FROM service_table WHERE service_id = %s", (service_id,))
            service_details = cursor.fetchone()

            if service_details:
                total_price = service_details['price'] * quantity
                total_minutes += service_details['service_duration'] * quantity

                cursor.execute("SELECT warranty_duration FROM warranty_table WHERE warranty_id = %s", (service_details['warranty_id'],))
                warranty_details = cursor.fetchone()

                warranty_duration = warranty_details['warranty_duration'] if warranty_details else None

                service_entry = {
                    'id': service_id,
                    'name': service_details['service_name'],
                    'price': service_details['price'],
                    'quantity': quantity,
                    'total': total_price,
                    'duration': service_details['service_duration'] * quantity,
                    'warranty_duration': warranty_duration
                }

                session["selected_services"]['services'].append(service_entry)
                session["selected_services"]['total_amount'] += total_price

        hours = total_minutes // 60
        minutes = total_minutes % 60
        total_duration = f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}" if hours else f"{minutes} minute{'s' if minutes != 1 else ''}"
        session["selected_services"]['total_duration'] = total_duration
        session["selected_services"]['total_minutes'] = total_minutes

        # Fetch applicable offers
        cursor.execute("SELECT * FROM offers_table")
        offers = cursor.fetchall()
        
        for offer in offers:
            if session["selected_services"]['total_amount'] >= offer['min_amt'] and len(services_rows) >= offer['no_of_services']:
                session["selected_services"]['offer_name'] = offer['offer_name']
                session["selected_services"]['offer_discount'] = offer['offer_discount']
                session["selected_services"]['offer_id'] = offer['offer_id']
                session["selected_services"]['discount_amt'] = session["selected_services"]['total_amount'] * (offer['offer_discount'] / 100)
                break

        # Calculate discounted amount
        discounted_total = math.ceil(session["selected_services"]['total_amount'] - session["selected_services"]['discount_amt'])
        session["selected_services"]['discounted_total'] = discounted_total
        
        # Fetch user credits
        cursor.execute("SELECT credits FROM users_table WHERE user_email = %s", (user_email,))
        user_details = cursor.fetchone()
        user_credits = user_details['credits'] if user_details else 0
        if user_credits > 0:
            if user_credits >= discounted_total:
                credits_used = discounted_total
                final_amount = 0
            else:

                credits_used = user_credits
                final_amount = discounted_total - user_credits

            # Update user credits in the users_table
            cursor.execute("UPDATE users_table SET credits = credits - %s WHERE user_email = %s", (credits_used, user_email))
            conn.commit()
        else:
            credits_used = 0
            final_amount = discounted_total
            conn.commit()

        session["selected_services"]['credits_used'] = credits_used
        session["selected_services"]['final_amount'] = final_amount
        return session["selected_services"]

    except mysql.connector.Error as err:
        return {"error": str(err)}

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    user_email = session["selected_services"]['user_email']
    sc_id = session["selected_services"]['sc_id']
    address = session["selected_services"]['address']
    phone = session["selected_services"]['phone']
    slot_date = session["selected_services"]['slotdate']
    slot_time = session["selected_services"]['slottime']
    total_duration = session["selected_services"]['total_duration']
    total_amount = session["selected_services"]['total_amount']
    credits_used = session["selected_services"]['credits_used']
    offer_id = session["selected_services"]['offer_id']
    offer_name = session["selected_services"]['offer_name']
    discounted_total = session["selected_services"]['discounted_total']
    final_amount = session["selected_services"]['final_amount']
    total_minutes = session["selected_services"]['total_minutes']
    tech_id = session["selected_services"]['tech_id']
    booking_date_time = datetime.datetime.now()
    print("\n\nFINAL AMOUNT: ",final_amount)
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        if final_amount == 0:
            # Fetch the last entry from the payments_table
            cursor.execute("SELECT UPI_Ref_No FROM payments_table ORDER BY UPI_Ref_No DESC LIMIT 1")
            last_payment = cursor.fetchone()
            
            if last_payment:
                last_upi_ref_no = last_payment['UPI_Ref_No']
                if '_free_' in last_upi_ref_no:
                    parts = last_upi_ref_no.rsplit('_free_', 1)
                    number = int(parts[1])
                    upi_ref_no = f"{parts[0]}_free_{number + 1}"
                else:
                    upi_ref_no = f"{last_upi_ref_no}_free_1"
            else:
                return jsonify({'error': 'No payment records found'}), 400
        else:
            data = request.get_json()
            upi_ref_no = data.get('upi_ref_no')
            print("\n\n\n\nAMOUNT:", final_amount)
            print("\nUPI WE GOT::", upi_ref_no)
            if not upi_ref_no:
                return jsonify({'error': 'UPI reference number is missing for paid transaction'}), 400
        print("UPI REF NO ENTERING THE TABLE IS:",upi_ref_no)
        print("final amount:",final_amount)
        otp = generate_otp()
        cursor.execute("INSERT INTO payments_table (UPI_Ref_no, amount) VALUES (%s, %s)", (upi_ref_no, final_amount))
        conn.commit()        
        # Insert data into user_bookings
        cursor.execute("""
            INSERT INTO user_bookings (user_email, booked_location, phone_no, booking_date_time, booked_date, booked_time, 
                                       UPI_Ref_No, duration, total_amount, offer_id, discounted_total, credits_used, sc_id, 
                                       final_amount, total_minutes, offer_name, tech_id, otp, booking_status)
            VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_email, address, phone, slot_date, slot_time, upi_ref_no, total_duration, total_amount, offer_id, 
              discounted_total, credits_used, sc_id, final_amount, total_minutes, offer_name, tech_id, otp, "pending"))
        conn.commit()

        # Fetch the auto-incremented booking_id from user_bookings table
        booking_id = cursor.lastrowid
        cursor.execute("INSERT INTO reviews (booking_id) values (%s)", (booking_id,))
        
        # Insert data into user_booked_services
        for service in session["selected_services"]['services']:
            service_id = service['id']
            price = service['price']
            quantity = service['quantity']
            total = service['total']
            duration = service['duration']
            warranty_duration = service.get('warranty_duration')
            cursor.execute("""
                INSERT INTO user_booked_services (booking_id, service_id, price, quantity, total, duration, warranty_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (booking_id, service_id, price, quantity, total, duration, warranty_duration))
            conn.commit()

        # Insert data into technician_booking_table
        cursor.execute("""
            INSERT INTO technician_booking_table (tech_id, sc_id, location, slot_date, slot_time, booking_id, service_duration)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (tech_id, sc_id, address, slot_date, slot_time, booking_id, total_minutes))
        conn.commit()

        # Delete from user_cart_table
        cursor.execute("""
            DELETE FROM user_cart_table WHERE user_email = %s AND sc_id = %s
        """, (user_email, sc_id))
        conn.commit()

        # Update user_table with new credits
        cursor.execute("""
            UPDATE users_table SET credits = credits - %s WHERE user_email = %s
        """, (credits_used, user_email))
        conn.commit()
        print(session)
        # session.clear()
        session["varforrouteauth"] = '/'

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return booking_id as JSON response
        return jsonify({'booking_id': booking_id})

    except Exception as e:
        # Handle any exceptions (e.g., log them)
        print(f"Error in confirm_booking: {e}")
        return jsonify({'error': 'An error occurred while processing your booking.'}), 500


# @app.route('/bill/<int:booking_id>')
# def bill(booking_id):
#     conn = mysql.connector.connect(**mysql_config)
#     cursor = conn.cursor(dictionary=True)
#     # Fetch the booking details
#     cursor.execute("""
#         SELECT * FROM user_bookings b join technician_table t on t.tech_id = b.tech_id WHERE booking_id = %s
#     """, (booking_id,))
#     booking_details = cursor.fetchone()
#     print("I cam here in generating bill route")
#     # Fetch the services for this booking
#     cursor.execute("""
#         SELECT * FROM user_booked_services WHERE booking_id = %s
#     """, (booking_id,))
#     booked_services = cursor.fetchall()
    
#     return render_template('bill.html', booking=booking_details, services=booked_services)


@app.route('/bill/<int:booking_id>')
def bill(booking_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)
    
    # Fetch the booking details
    cursor.execute("""
        SELECT * FROM user_bookings b
        JOIN technician_table t ON t.tech_id = b.tech_id
        WHERE booking_id = %s
    """, (booking_id,))
    booking_details = cursor.fetchone()
    
    # Fetch the services for this booking, including service names
    cursor.execute("""
        SELECT ubs.*, st.service_name FROM user_booked_services ubs
        JOIN service_table st ON ubs.service_id = st.service_id
        WHERE booking_id = %s
    """, (booking_id,))
    booked_services = cursor.fetchall()
    
    conn.close()
    
    return render_template('bill.html', booking=booking_details, services=booked_services)


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')



@app.route('/find_technician_cities', methods=['GET', 'POST'])
def find_technician_cities():
    cities = []
    if request.method == 'POST':
        service_name = request.form['service_name']
        try:
            conn = mysql.connector.connect(**mysql_config)
            cursor = conn.cursor()

            # Fetch segmentation_type_id from service_table
            cursor.execute("SELECT segmentation_type_id FROM service_table WHERE service_name = %s", (service_name,))
            segmentation_type_id = cursor.fetchone()
            if segmentation_type_id:
                segmentation_type_id = segmentation_type_id[0]

                # Fetch sc_id from segmentation_table
                cursor.execute("SELECT sc_id FROM segmentation_table WHERE segmentation_type_id = %s", (segmentation_type_id,))
                sc_id = cursor.fetchone()
                if sc_id:
                    sc_id = sc_id[0]

                    # Fetch tech_id from tech_expertise_table
                    cursor.execute("SELECT tech_id FROM tech_expertise_table WHERE sc_id = %s", (sc_id,))
                    tech_ids = cursor.fetchall()

                    if tech_ids:
                        tech_ids = [tech_id[0] for tech_id in tech_ids]

                        # Fetch available_for_cities from technician_table
                        cursor.execute("SELECT available_for_cities FROM technician_table WHERE tech_id IN (%s)" % ','.join(['%s']*len(tech_ids)), tech_ids)
                        cities = cursor.fetchall()

                        # Flatten the list and remove duplicates
                        cities = list(set([city for sublist in cities for city in sublist[0].split(',')]))

            cursor.close()
            conn.close()
        except Exception as e:
            flash(f'Error fetching technician cities: {e}')

    return render_template('find_technician_cities.html', cities=cities)

if __name__ == '__main__':
    app.run(debug=True)
