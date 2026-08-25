import os
import sqlite3
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'martial_arts.db')


def create_database():
    """Create the database and initialize tables."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
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
        ''')
        
        conn.commit()
        logger.info(f"Database created successfully at {DATABASE}")
        
    except sqlite3.Error as e:
        logger.error(f"Database creation error: {e}")
        raise
    finally:
        conn.close()


def get_all_students():
    """Retrieve all students from the database."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
        students = cursor.fetchall()
        
        return [dict(student) for student in students]
    
    except sqlite3.Error as e:
        logger.error(f"Error fetching students: {e}")
        return None
    finally:
        conn.close()


def get_student_by_id(student_id):
    """Retrieve a specific student by ID."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        return dict(student) if student else None
    
    except sqlite3.Error as e:
        logger.error(f"Error fetching student {student_id}: {e}")
        return None
    finally:
        conn.close()


def add_student(student_data):
    """Add a new student to the database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO students (
                student_name, parent_name, dob, age, gender,
                mobile, email, address, previous_martial_art,
                martial_art_details, medical_condition, joined_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_data['student_name'],
            student_data['parent_name'],
            student_data['dob'],
            student_data['age'],
            student_data['gender'],
            student_data['mobile'],
            student_data['email'],
            student_data['address'],
            student_data.get('previous_martial_art', ''),
            student_data.get('martial_art_details', ''),
            student_data.get('medical_condition', ''),
            student_data['joined_date']
        ))
        
        conn.commit()
        student_id = cursor.lastrowid
        logger.info(f"Student {student_data['student_name']} added with ID {student_id}")
        
        return student_id
    
    except sqlite3.Error as e:
        logger.error(f"Error adding student: {e}")
        return None
    finally:
        conn.close()


def delete_student(student_id):
    """Delete a student from the database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        
        logger.info(f"Student {student_id} deleted")
        return True
    
    except sqlite3.Error as e:
        logger.error(f"Error deleting student: {e}")
        return False
    finally:
        conn.close()


def update_student(student_id, student_data):
    """Update student information."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE students SET
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
        ''', (
            student_data['student_name'],
            student_data['parent_name'],
            student_data['dob'],
            student_data['age'],
            student_data['gender'],
            student_data['mobile'],
            student_data['email'],
            student_data['address'],
            student_data.get('previous_martial_art', ''),
            student_data.get('martial_art_details', ''),
            student_data.get('medical_condition', ''),
            student_id
        ))
        
        conn.commit()
        logger.info(f"Student {student_id} updated")
        return True
    
    except sqlite3.Error as e:
        logger.error(f"Error updating student: {e}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
