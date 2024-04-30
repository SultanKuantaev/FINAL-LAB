import csv
import psycopg2

# Replace these variables with your own configuration
db_name = "postgre"
db_user = "postgre"
db_password = "1234"
db_host = "localhost"  # or your database server address

# Connect to the PostgreSQL database
def connect_to_db():
    return psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )

# Function to create the PhoneBook table
def create_phonebook_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone_number VARCHAR(15) UNIQUE NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Function to insert data from a CSV file
def upload_data_from_csv(csv_file_path):
    conn = connect_to_db()
    cur = conn.cursor()
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s) ON CONFLICT (phone_number) DO NOTHING",
                row
            )
    conn.commit()
    cur.close()
    conn.close()

# Function to insert data from console input
def insert_data_from_console():
    conn = connect_to_db()
    cur = conn.cursor()
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")
    cur.execute(
        "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s) ON CONFLICT (phone_number) DO NOTHING",
        (first_name, last_name, phone_number)
    )
    conn.commit()
    cur.close()
    conn.close()

# Function to update data in the table
def update_data(id, first_name=None, phone_number=None):
    conn = connect_to_db()
    cur = conn.cursor()
    if first_name:
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE id = %s",
            (first_name, id)
        )
    if phone_number:
        cur.execute(
            "UPDATE phonebook SET phone_number = %s WHERE id = %s",
            (phone_number, id)
        )
    conn.commit()
    cur.close()
    conn.close()

# Function to query data from the table with filters
def query_data(filter_by=None, filter_value=None):
    conn = connect_to_db()
    cur = conn.cursor()
    sql = "SELECT * FROM phonebook"
    if filter_by and filter_value:
        sql += " WHERE {} = %s".format(filter_by)
        cur.execute(sql, (filter_value,))
    else:
        cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        print(record)
    cur.close()
    conn.close()

# Function to delete data from the table by username or phone
def delete_data(delete_by, value):
    conn = connect_to_db()
    cur = conn.cursor()
    sql = "DELETE FROM phonebook WHERE {} = %s".format(delete_by)
    cur.execute(sql, (value,))
    conn.commit()
    cur.close()
    conn.close()

# Main execution
if __name__ == "__main__":
    create_phonebook_table()
    # You can uncomment the following lines to use the other functions:
    # upload_data_from_csv('path_to_your_csv.csv')
    # insert_data_from_console()
    # update_data(id=1, first_name="NewName")
    # query_data(filter_by="first_name", filter_value="John")
    # delete_data(delete_by="phone_number", value="1234567890")
