import mysql.connector
from mysql.connector import Error
from bs4 import BeautifulSoup
import requests
import os

# Read MySQL connection details from environment variables
mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_db = os.getenv("MYSQL_DB")

# Database connection setup
try:
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )
    if connection.is_connected():
        print("Connected to MySQL database")

except Error as e:
    print(f"Error: {e}")
    exit()


def create_table():
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db
        )
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS properties (
            id INT AUTO_INCREMENT PRIMARY KEY,
            apartment_type VARCHAR(100),
            price VARCHAR(100),
            location TEXT,
            bedrooms VARCHAR(50),
            bathrooms VARCHAR(50),
            area VARCHAR(50),
            building VARCHAR(100),
            residence VARCHAR(100),
            city VARCHAR(50),
            date_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table `properties` ensured to exist.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Call this at the start of your scraper
create_table()

url = 'https://www.propertyfinder.ae/en/rent/dubai/apartments-for-rent.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# List to store parsed results
list_items = soup.find_all('li', attrs={'data-testid': lambda x: x and x.startswith('list-item')})

# Process each item
for item in list_items:
    apt_tag = item.find('p', attrs={'data-testid': 'property-card-type'})
    apt = apt_tag.get_text(strip=True) if apt_tag else None

    price_tag = item.find('p', attrs={'data-testid': 'property-card-price'})
    price = price_tag.get_text(strip=True) if price_tag else None

    location_tag = item.find('div', attrs={'data-testid': 'property-card-location'})
    location_full = location_tag.get_text(strip=True) if location_tag else None

    # Split location to building, residence area, and city
    building, residence_area, city = None, None, None
    if location_full:
        parts = location_full.split(', ')
        if len(parts) >= 3:
            building, residence_area, city = parts[-3], parts[-2], parts[-1]

    bedroom_tag = item.find('p', attrs={'data-testid': 'property-card-spec-bedroom'})
    bedrooms = bedroom_tag.get_text(strip=True) if bedroom_tag else None

    bathroom_tag = item.find('p', attrs={'data-testid': 'property-card-spec-bathroom'})
    bathrooms = bathroom_tag.get_text(strip=True) if bathroom_tag else None

    area_tag = item.find('p', attrs={'data-testid': 'property-card-spec-area'})
    area = area_tag.get_text(strip=True) if area_tag else None

    # SQL Insert Statement
    insert_query = """
    INSERT INTO properties (apartment_type, price, location, building, residence, city, bedrooms, bathrooms, area)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (apt, price, location_full, building, residence_area, city, bedrooms, bathrooms, area)

    # Insert into MySQL
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query, data)
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Failed to insert data into MySQL table: {e}")

# Close the database connection
if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection closed")
