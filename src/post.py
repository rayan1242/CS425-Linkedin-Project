import mysql.connector
from tabulate import tabulate
from db import connect_to_database
connection = connect_to_database()

def create_post(connection):
    cursor = connection.cursor()

    user_id = input("\nEnter user ID: ")
    post_content = input("Enter post content: ")
    post_date = input("Enter post date (YYYY-MM-DD): ")
    likes = input("Enter number of likes: ")
    last_liked_at = input("Enter last liked at date (YYYY-MM-DD): ")

    query = """INSERT INTO post (user_id, post_content, post_date, likes, last_liked_at) 
               VALUES (%s, %s, %s, %s, %s)"""
    values = (user_id, post_content, post_date, likes, last_liked_at)

    cursor.execute(query, values)
    connection.commit()
    post_id = cursor.lastrowid

    print("\nPost created successfully with ID:", post_id)
    cursor.close()

    return post_id

def read_post(connection):
    cursor = connection.cursor(dictionary=True)

    post_id = input("\nEnter post ID: ")
    query = "SELECT * FROM post WHERE post_id = %s"

    cursor.execute(query, (post_id,))
    result = cursor.fetchone()

    if result:
        print(tabulate([result], headers="keys", tablefmt="grid"))
    else:
        print("\nPost not found")

    cursor.close()

def update_post(connection):
    cursor = connection.cursor()

    post_id = input("\nEnter post ID to update: ")
    fields = ["user_id", "post_content", "post_date", "likes", "last_liked_at"]
    updates = []
    values = []

    for field in fields:
        value = input(f"Enter new {field} (leave blank to skip): ")
        if value:
            updates.append(f"{field} = %s")
            values.append(value)

    if not updates:
        print("No fields to update")
        return

    query = f"UPDATE post SET {', '.join(updates)} WHERE post_id = %s"
    values.append(post_id)

    cursor.execute(query, tuple(values))
    connection.commit()
    print("\nPost updated successfully")
    cursor.close()

def delete_post(connection):
    cursor = connection.cursor()

    post_id = input("\nEnter post ID to delete: ")
    query = "DELETE FROM post WHERE post_id = %s"

    cursor.execute(query, (post_id,))
    connection.commit()

    print("\nPost deleted successfully")

    cursor.close()

def post_menu():
    connection = connect_to_database()
    
    while True:
        print("\nChoose an operation:")
        print("1: Create post")
        print("2: Read post")
        print("3: Update post")
        print("4: Delete post")
        print("0: Exit")

        choice = input("\nEnter your choice (0-4): ")

        if choice == '1':
            create_post(connection)
        elif choice == '2':
            read_post(connection)
        elif choice == '3':
            update_post(connection)
        elif choice == '4':
            delete_post(connection)
        elif choice == '0':
            connection.close()
            print("Database Disconnected Successfully!")
            print("\nExit from Post Menu.")
            print("\n      - X - X - X -")
            return
        else:
            print("\nInvalid choice. Please try again.")