from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# ✅ MySQL Database Connection using PyMySQL
try:
    db = pymysql.connect(
        host="localhost",
        user="root",  # Default XAMPP MySQL username
        password="",  # Leave blank if no password in XAMPP
        database="food_order_db",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True  # Auto-commit enabled
    )
except Exception as e:
    db = None

# ✅ Route to render checkout page
@app.route("/")
def checkout():
    return render_template("phone17.html")  # Load the checkout page

# ✅ Route to handle order submission
@app.route("/place_order", methods=["POST"])
def place_order():
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400  # Handle empty request

        pay_mode = str(data.get("pay_mode", "Unknown")).strip()

        if not pay_mode:
            pay_mode = "Unknown"

        # Insert into database
        restaurant_name = "La Pinoz’s Pizza"
        total_pay = "160.00"
        query = "INSERT INTO customer_order (restaurant_name, total_pay, pay_mode) VALUES (%s, %s, %s)"
        values = (restaurant_name, total_pay, pay_mode)

        with db.cursor() as cursor:
            cursor.execute(query, values)
            db.commit()
        return jsonify({"message": "Order placed successfully!", "redirect_url": "/order_success"}), 200

    except pymysql.MySQLError as e:
        db.rollback()
        return jsonify({"error": "Order failed!", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
