import os
import sqlite3
import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response, session
import logging
from database import add_student, get_all_students, get_student_by_id, delete_student, update_student

# ================== DIRECTORY & DATABASE CONFIG ==================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DATABASE = os.path.join(BASE_DIR, 'martial_arts.db')

# Initialize Flask app
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

# App Configuration & Secret Key for Admin Login
app.secret_key = "veera_vaanji_super_secret_key_2026"
app.config['DATABASE'] = DATABASE
app.config['JSON_SORT_KEYS'] = False

# Set your Admin Credentials here
ADMIN_USERNAME = "user"
ADMIN_PASSWORD = "user@123"  # Change to your chosen password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ================== DATABASE HELPERS ==================

def get_db_connection():
    """Create a database connection with dict-like row access."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None


def init_db():
    """Initialize database tables."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
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
                joined_date TEXT NOT NULL
            )
        ''')
        conn.commit()
        logger.info("Database initialized successfully")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        return False
    finally:
        conn.close()


# ================== PUBLIC WEBSITE ROUTES ==================

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/admission")
@app.route("/admission.html")
def admission():
    return render_template("admission.html")


@app.route("/achievement")
@app.route("/achievement.html")
def achievement():
    return render_template("achievement.html")


@app.route("/gallery")
@app.route("/gallery.html")
def gallery():
    return render_template("gallery.html")


@app.route("/mentors")
@app.route("/mentors.html")
def mentors():
    return render_template("mentors.html")


@app.route("/trainers")
@app.route("/trainers.html")
def trainers():
    return render_template("trainers.html")


@app.route("/testimonials")
@app.route("/testimonials.html")
def testimonials():
    return render_template("testimonials.html")


@app.route("/contact")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")


# ================== STUDENT REGISTRATION ==================

@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            student_name = request.form.get("student_name", "").strip()
            parent_name = request.form.get("parent_name", "").strip()
            dob = request.form.get("dob", "").strip()
            age = request.form.get("age", "").strip()
            gender = request.form.get("gender", "").strip()
            mobile = request.form.get("mobile", "").strip()
            email = request.form.get("email", "").strip()
            address = request.form.get("address", "").strip()
            previous_martial_art = request.form.get("previous_martial_art", "No").strip()
            martial_art_details = request.form.get("martial_art_details", "").strip()
            medical_condition = request.form.get("medical_condition", "").strip()
            
            # Validation
            if not all([student_name, parent_name, dob, age, gender, mobile, email, address]):
                return jsonify({
                    "success": False,
                    "message": "Please fill in all required fields."
                }), 400
            
            joined_date = datetime.now().strftime("%d-%m-%Y %H:%M")
            
            conn = get_db_connection()
            if conn is None:
                return jsonify({"success": False, "message": "Database connection error."}), 500
            
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (
                    student_name, parent_name, dob, age, gender,
                    mobile, email, address, previous_martial_art,
                    martial_art_details, medical_condition, joined_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_name, parent_name, dob, int(age), gender,
                mobile, email, address, previous_martial_art,
                martial_art_details, medical_condition, joined_date
            ))
            
            new_student_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return jsonify({
                "success": True,
                "message": "Registration Completed Successfully!",
                "student": {
                    "id": f"{new_student_id}",
                    "name": student_name,
                    "joined_date": joined_date,
                    "mobile": mobile
                }
            }), 201
            
        except Exception as e:
            logger.error(f"Error registering student: {e}")
            return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
    
    return render_template("register.html")


# ================== ADMIN AUTHENTICATION ==================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin Login Page"""
    if session.get("is_admin"):
        return redirect("/admin")
        
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect("/admin")
        else:
            error = "Invalid Username or Password!"
            
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    """Admin Logout"""
    session.pop("is_admin", None)
    return redirect("/admin/login")


# ================== PROTECTED ADMIN DASHBOARD ==================

@app.route("/admin")
@app.route("/admin.html")
def admin_dashboard():
    """Admin page to view and manage all student registrations"""
    # Check if admin is logged in
    if not session.get("is_admin"):
        return redirect("/admin/login")

    students = []
    stats = {"total": 0, "male": 0, "female": 0, "experienced": 0}
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY id DESC")
            rows = cursor.fetchall()
            students = [dict(row) for row in rows]
            
            stats["total"] = len(students)
            stats["male"] = sum(1 for s in students if str(s.get('gender', '')).strip().lower() == 'male')
            stats["female"] = sum(1 for s in students if str(s.get('gender', '')).strip().lower() == 'female')
            stats["experienced"] = sum(1 for s in students if str(s.get('previous_martial_art', '')).strip().lower() == 'yes')
            conn.close()
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {e}")
        
    return render_template("admin.html", students=students, stats=stats)


@app.route("/admin/delete/<int:student_id>", methods=["GET", "POST"])
def delete_student(student_id):
    """Delete a student record (Admin Only)"""
    if not session.get("is_admin"):
        return redirect("/admin/login")
        
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            conn.close()
            logger.info(f"Student ID {student_id} deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {e}")

    return redirect("/admin")


@app.route("/admin/export-csv")
@app.route("/admin/export_csv")
def export_csv():
    """Export all student registrations into a CSV file (Admin Only)"""
    if not session.get("is_admin"):
        return redirect("/admin/login")

    try:
        conn = get_db_connection()
        if not conn:
            return "Database error", 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        output = io.StringIO()
        writer = csv.writer(output)

        # Header row
        writer.writerow([
            "ID", "Student Name", "Parent Name", "DOB", "Age", "Gender",
            "Mobile", "Email", "Address", "Previous Martial Art",
            "Details", "Medical Condition", "Joined Date"
        ])

        # Data rows
        for r in rows:
            s = dict(r)
            writer.writerow([
                f"VV-{s.get('id', '')}",
                s.get('student_name', ''),
                s.get('parent_name', ''),
                s.get('dob', ''),
                s.get('age', ''),
                s.get('gender', ''),
                s.get('mobile', ''),
                s.get('email', ''),
                s.get('address', ''),
                s.get('previous_martial_art', 'No'),
                s.get('martial_art_details', ''),
                s.get('medical_condition', 'None'),
                s.get('joined_date', '')
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=Veera_Vaanji_Students.csv"}
        )
    except Exception as e:
        return f"Error exporting CSV: {e}", 500


# ================== ERROR HANDLERS ==================

@app.errorhandler(404)
def not_found(error):
    return "<h2>404 - Page Not Found</h2><p><a href='/'>Return to Home</a></p>", 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"success": False, "message": "Internal server error"}), 500


# ================== CONTEXT PROCESSORS ==================

@app.context_processor
def inject_config():
    return {
        'app_name': 'Veera Vaanji Martial Arts Academy',
        'app_year': datetime.now().year
    }


# ================== MAIN ==================

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)