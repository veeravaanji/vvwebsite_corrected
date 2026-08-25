import os
import sqlite3
import logging

# ================== LOGGING ==================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ================== DATABASE CONFIG ==================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "martial_arts.db")


# ================== CREATE DATABASE ==================

def create_database():
    """Create database and students table if they do not exist."""

    conn = None

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                parent_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                mobile TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                previous_martial_art TEXT,
                martial_art_details TEXT,
                medical_condition TEXT,
                joined_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

        logger.info("========================================")
        logger.info("DATABASE INITIALIZED SUCCESSFULLY")
        logger.info(f"DATABASE PATH: {DATABASE}")
        logger.info("STUDENTS TABLE READY")
        logger.info("========================================")

        return True

    except sqlite3.Error as e:

        logger.error(f"Database creation error: {e}")
        return False

    finally:

        if conn:
            conn.close()


# ================== DATABASE CONNECTION ==================

def get_connection():
    """
    Create a database connection.
    The database/table is checked before every connection.
    """

    try:

        # Make sure database and table exist
        create_database()

        conn = sqlite3.connect(DATABASE)

        conn.row_factory = sqlite3.Row

        return conn

    except sqlite3.Error as e:

        logger.error(f"Database connection error: {e}")

        return None


# ================== GET ALL STUDENTS ==================

def get_all_students():

    conn = None

    try:

        conn = get_connection()

        if conn is None:
            return []

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM students
            ORDER BY id DESC
        """)

        students = cursor.fetchall()

        return [dict(student) for student in students]

    except sqlite3.Error as e:

        logger.error(f"Error fetching students: {e}")

        return []

    finally:

        if conn:
            conn.close()


# ================== GET STUDENT BY ID ==================

def get_student_by_id(student_id):

    conn = None

    try:

        conn = get_connection()

        if conn is None:
            return None

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM students
            WHERE id = ?
        """, (student_id,))

        student = cursor.fetchone()

        if student:
            return dict(student)

        return None

    except sqlite3.Error as e:

        logger.error(
            f"Error fetching student {student_id}: {e}"
        )

        return None

    finally:

        if conn:
            conn.close()


# ================== ADD STUDENT ==================

def add_student(student_data):

    conn = None

    try:

        conn = get_connection()

        if conn is None:
            return None

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students (
                student_name,
                parent_name,
                dob,
                age,
                gender,
                mobile,
                email,
                address,
                previous_martial_art,
                martial_art_details,
                medical_condition,
                joined_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            student_data["student_name"],
            student_data["parent_name"],
            student_data["dob"],
            student_data["age"],
            student_data["gender"],
            student_data["mobile"],
            student_data["email"],
            student_data["address"],
            student_data.get(
                "previous_martial_art",
                ""
            ),
            student_data.get(
                "martial_art_details",
                ""
            ),
            student_data.get(
                "medical_condition",
                ""
            ),
            student_data["joined_date"]
        ))

        conn.commit()

        student_id = cursor.lastrowid

        logger.info(
            f"Student added successfully. "
            f"Name: {student_data['student_name']}, "
            f"ID: {student_id}"
        )

        return student_id

    except sqlite3.Error as e:

        logger.error(
            f"Error adding student: {e}"
        )

        return None

    finally:

        if conn:
            conn.close()


# ================== DELETE STUDENT ==================

def delete_student(student_id):

    conn = None

    try:

        conn = get_connection()

        if conn is None:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE id = ?
        """, (student_id,))

        conn.commit()

        logger.info(
            f"Student {student_id} deleted."
        )

        return True

    except sqlite3.Error as e:

        logger.error(
            f"Error deleting student: {e}"
        )

        return False

    finally:

        if conn:
            conn.close()


# ================== UPDATE STUDENT ==================

def update_student(student_id, student_data):

    conn = None

    try:

        conn = get_connection()

        if conn is None:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE students
            SET
                student_name = ?,
                parent_name = ?,
                dob = ?,
                age = ?,
                gender = ?,
                mobile = ?,
                email = ?,
                address = ?,
                previous_martial_art = ?,
                martial_art_details = ?,
                medical_condition = ?
            WHERE id = ?
        """, (

            student_data["student_name"],
            student_data["parent_name"],
            student_data["dob"],
            student_data["age"],
            student_data["gender"],
            student_data["mobile"],
            student_data["email"],
            student_data["address"],
            student_data.get(
                "previous_martial_art",
                ""
            ),
            student_data.get(
                "martial_art_details",
                ""
            ),
            student_data.get(
                "medical_condition",
                ""
            ),
            student_id
        ))

        conn.commit()

        logger.info(
            f"Student {student_id} updated."
        )

        return True

    except sqlite3.Error as e:

        logger.error(
            f"Error updating student: {e}"
        )

        return False

    finally:

        if conn:
            conn.close()


# ================== DIRECT EXECUTION ==================

if __name__ == "__main__":

    create_database()
