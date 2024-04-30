import csv
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost'
}

# Function to connect to the PostgreSQL database
def connect(params):
    return psycopg2.connect(**params)

# Function to insert data from a CSV file
def insert_data_from_csv(conn, file_path):
    cursor = conn.cursor()
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            cursor.execute(
                        
                "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                row
            )
    conn.commit()
    cursor.close()

# Function to insert data from console input
def insert_data_from_console(conn):
    cursor = conn.cursor()
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")
    cursor.execute(
        "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
        (first_name, last_name, phone_number)
    )
    conn.commit()
    cursor.close()

# Function to update data
def update_data(conn):
    cursor = conn.cursor()
    choice = input("Choose what to update (1: first name, 2: last name, 3: phone number): ")
    value = input("Enter new value: ")
    identifier = input("Enter the phone number of the entry to update: ")
    if choice == '1':
        cursor.execute("UPDATE phonebook SET first_name = %s WHERE phone_number = %s", (value, identifier))
    elif choice == '2':
        cursor.execute("UPDATE phonebook SET last_name = %s WHERE phone_number = %s", (value, identifier))
    elif choice == '3':
        cursor.execute("UPDATE phonebook SET phone_number = %s WHERE phone_number = %s", (value, identifier))
    conn.commit()
    cursor.close()

# Function to query data
def query_data(conn):
    cursor = conn.cursor()
    filter_choice = input("Enter filter for search (1: first name, 2: last name, 3: phone number, 4: no filter): ")
    if filter_choice in ['1', '2', '3']:
        value = input("Enter value to filter by: ")
        column = 'first_name' if filter_choice == '1' else 'last_name' if filter_choice == '2' else 'phone_number'
        cursor.execute(sql.SQL("SELECT * FROM phonebook WHERE {} = %s").format(sql.Identifier(column)), (value,))
    else:
        cursor.execute("SELECT * FROM phonebook")
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()

# Function to delete data
def delete_data(conn):
    cursor = conn.cursor()
    choice = input("Delete by (1: first name, 2: phone number): ")
    value = input("Enter value: ")
    column = 'first_name' if choice == '1' else 'phone_number'
    cursor.execute(sql.SQL("DELETE FROM phonebook WHERE {} = %s").format(sql.Identifier(column)), (value,))
    conn.commit()
    cursor.close()

# Main function to run the program
def main():
    conn = connect(db_params)
    try:
        while True:
            print("Choose an option:")
            print("1: Insert data from CSV")
            print("2: Insert data from console")
            print("3: Update data")
            print("4: Query data")
            print("5: Delete data")
            print("Q: Quit")
            choice = input("Enter your choice: ").upper()
            if choice == 'Q':
                break
            elif choice == '1':
                file_path = input("Enter the CSV file path: ")
                insert_data_from_csv(conn, file_path)
            elif choice == '2':
                insert_data_from_console(conn)
            elif choice == '3':
                update_data(conn)
            elif choice == '4':
                query_data(conn)
            elif choice == '5':
                delete_data(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
