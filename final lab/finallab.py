import psycopg2
import csv
from config import *

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = conn.cursor()


# Insert data into phonebook table (option 1: from CSV file)
def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            name, number = row
            cur.execute(
                'INSERT INTO phonebook2(name,number) VALUES(%s,%s)',
                (name, number)
            )


# Insert data into phonebook table (option 2: from console)
def insert_data_from_console():
    name = input("Enter name: ")
    number = input("Enter phone: ")
    cur.execute(
        'INSERT INTO phonebook2(name,number) VALUES(%s,%s)',
        (name, number)
    )
    conn.commit()
    print("Data uploaded successfully from console.")


# Update data in phonebook table
def update_data():
    name = input("Enter the name of the user to update: ")
    field = input("Enter the field to update (name/phone): ")
    value = input("Enter the new value: ")
    if field == "name":
        cur.execute(
            "UPDATE phonebook2 SET name = %s WHERE name = %s",
            (value, name)
        )
    elif field == "phone":
        cur.execute(
            "UPDATE phonebook2 SET number = %s WHERE name = %s",
            (value, name)
        )
    conn.commit()
    print("Data updated successfully.")


# Query data from phonebook table
def query_data():
    field = input("Enter the field to query (name/number/all): ")
    if field == "name":
        name = input("Enter the name: ")
        cur.execute(
            "SELECT * FROM phonebook2 WHERE name = %s",
            (name,)
        )
    elif field == "number":
        phone = input("Enter the phone: ")
        cur.execute(
            "SELECT * FROM phonebook2 WHERE number = %s",
            (phone,)
        )
    elif field == "all":
        cur.execute("SELECT * FROM phonebook2")
    else:
        print("Invalid input.")
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Query data from phonebook table by pattern
def query_data_by_pattern():
    pattern = input("Enter a search pattern: ")
    if pattern:
        cur.execute(
            "SELECT * FROM phonebook2 WHERE name LIKE %s OR number LIKE %s",
            ('%' + pattern + '%', '%' + pattern + '%')
        )
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No results found for pattern: {}".format(pattern))
    else:
        print("Error: Please enter a valid search pattern.")


# Insert new user or update phone if user already exists
def insert_or_update_user():
    name = input('enter a name that u want to update or insert: ')
    number = input('enter a phone that u want to update or insert: ')
    if name and number:
        cur.execute(
            "INSERT INTO phonebook2(name, number) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET number = excluded.number",
            (name, number)
        )
        conn.commit()
        print("Data inserted or updated successfully.")
    else:
        print("Error: Please enter a valid name and phone number.")


# Insert many new users into phonebook table
def insert_many_users():
    users = []
    while True:
        name = input("Enter a name (or press enter to finish): ")
        if not name:
            break
        phone = input("Enter a phone number: ")
        users.append((name, phone))

    invalid_data = []
    for user1 in users:
        name, phone = user1
        if len(phone)  != 11 or not phone.isdigit():
            invalid_data.append(user1)
        else:
            cur.execute(
                "INSERT INTO phonebook2(name, number) VALUES (%s, %s)",
                (name, phone)
            )
    conn.commit()
    if invalid_data:
        print("The following data was invalid and could not be inserted:")
        for user2 in invalid_data:
            print(user2)
    else:
        print("All data was inserted successfully.")


# Query data from phonebook table with pagination
def query_data_with_pagination():
    limit = input("Enter the number of rows to retrieve: ")
    offset = input("Enter the starting row number: ")
    if limit and offset:
        cur.execute(
            "SELECT * FROM phonebook2 ORDER BY name LIMIT %s OFFSET %s",
            (limit, offset)
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)
    else:
        print("Error: Please enter valid limit and offset values.")


# Delete data from phonebook table
def delete_data():
    field = input("Enter the field to delete by (name/number): ")
    value = input("Enter the value: ")
    if field == "name":
        cur.execute(
            "DELETE FROM phonebook2 WHERE name = %s",
            (value,)
        )
    elif field == "number":
        cur.execute(
            "DELETE FROM phonebook2 WHERE number = %s",
            (value,)
        )
    conn.commit()
    print("Data deleted successfully.")


# Main program loop
while True:
    print("PhoneBook options:")
    print("1. Insert data from CSV file.")
    print("2. Insert data from console.")
    print("3. Update data.")
    print("4. Query data.")
    print("5. Delete data.")
    print('6. Query data by pattern.')
    print('7. Insert or update user.')
    print('8. Insert many users.')
    print('9. Query data with pagination')
    print("0. Exit.")
    choice = input("Enter your choice: ")
    if choice == "1":
        filename = input("Enter the filename:")
        insert_from_csv(filename)
    elif choice == "2":
        insert_data_from_console()
    elif choice == "3":
        update_data()
    elif choice == "4":
        query_data()
    elif choice == "5":
        delete_data()
    elif choice == '6':
        query_data_by_pattern()
    elif choice == '7':
        insert_or_update_user()
    elif choice == '8':
        insert_many_users()
    elif choice == '9':
        query_data_with_pagination()
    elif choice == "0":
        break
    else:
        print("Invalid input. Please enter a valid option.")
conn.commit()
cur.close()
conn.close()