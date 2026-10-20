import sqlite3

DB_NAME = "campus.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campuses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_code TEXT UNIQUE,
        resource_name TEXT,
        campus_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        resource_id INTEGER,
        booking_date TEXT,
        start_time TEXT,
        duration INTEGER
    )
    """)

    conn.commit()
    conn.close()


def add_resource(code, name, campus_id):
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO resources
            (resource_code, resource_name, campus_id)
            VALUES (?, ?, ?)
        """, (code, name, campus_id))

        conn.commit()

    except sqlite3.IntegrityError:
        print("Resource code already exists")

    finally:
        conn.close()


def campus_report():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM bookings
    """)
    total_bookings = cursor.fetchone()[0]

    cursor.execute("""
        SELECT resource_id, COUNT(*)
        FROM bookings
        GROUP BY resource_id
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    most_used = cursor.fetchone()

    cursor.execute("""
        SELECT AVG(duration)
        FROM bookings
    """)
    avg_duration = cursor.fetchone()[0]

    conn.close()

    return total_bookings, most_used, avg_duration


def cross_campus_report():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT campuses.name,
               COUNT(bookings.id)
        FROM bookings
        JOIN resources
            ON bookings.resource_id = resources.id
        JOIN campuses
            ON resources.campus_id = campuses.id
        GROUP BY campuses.name
    """)

    results = cursor.fetchall()

    conn.close()

    return results