import sqlite3

def create_database():
    # This creates the file if it doesn't exist
    conn = sqlite3.connect("NewsSentimentDB.db")
    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    create_database()