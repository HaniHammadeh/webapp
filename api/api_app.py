from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# MySQL configuration from environment variables
mysql_host = os.getenv("MYSQL_HOST", "localhost")
mysql_user = os.getenv("MYSQL_USER", "root")
mysql_password = os.getenv("MYSQL_PASSWORD", "your_password")
mysql_db = os.getenv("MYSQL_DB", "property_data")

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )

# Endpoint: Get all listings
@app.route("/listings", methods=["GET"])
def get_all_listings():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM properties ORDER BY date_scraped DESC LIMIT 20;")
    properties = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(properties)

# Endpoint: Get average price by area
@app.route("/average-price", methods=["GET"])
def get_average_price():
    area = request.args.get("area")
    if not area:
        return jsonify({"error": "Area parameter is required"}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT AVG(price) as average_price FROM properties WHERE area = %s;"
    cursor.execute(query, (area,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if result["average_price"] is None:
        return jsonify({"error": "No listings found for the specified area"}), 404

    return jsonify({
        "area": area,
        "average_price": round(result["average_price"], 2)
    })

# Endpoint: Get latest listings by city
@app.route("/latest-listings", methods=["GET"])
def get_latest_listings_by_city():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM properties WHERE city = %s ORDER BY date_scraped DESC LIMIT 10;"
    cursor.execute(query, (city,))
    listings = cursor.fetchall()
    cursor.close()
    connection.close()
    
    if not listings:
        return jsonify({"error": "No listings found for the specified city"}), 404

    return jsonify(listings)

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
