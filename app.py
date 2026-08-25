import os
import sqlite3
import csv
import io
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    Response,
    session
)

import logging

from database import (
    create_database,
    get_connection
)


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# =========================================================
# DIRECTORY CONFIGURATION
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

TEMPLATE_DIR = os.path.join(
    BASE_DIR,
    "templates"
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    "static"
)

DATABASE = os.path.join(
    BASE_DIR,
    "martial_arts.db"
)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)


# =========================================================
# FLASK CONFIGURATION
# =========================================================

app.secret_key = "veera_vaanji_super_secret_key_2026"

app.config["DATABASE"] = DATABASE


# =========================================================
# ADMIN LOGIN
# =========================================================

ADMIN_USERNAME = "user"

ADMIN_PASSWORD = "user@123"


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

# This runs when Gunicorn starts on Render.

logger.info("Starting Veera Vaanji application...")

logger.info(
    f"Database path: {DATABASE}"
)

create_database()


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    try:

        # Make sure database/table exists
        create_database()

        conn = sqlite3.connect(
            DATABASE
        )

        conn.row_factory = sqlite3.Row

        return conn

    except sqlite3.Error as e:

        logger.error(
            f"Database connection error: {e}"
        )

        return None


# =========================================================
# HOME
# =========================================================

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
@app.route("/about.html")
def about():

    return render_template(
        "about.html"
    )


# =========================================================
# ADMISSION
# =========================================================

@app.route("/admission")
@app.route("/admission.html")
def admission():

    return render_template(
        "admission.html"
    )


# =========================================================
# ACHIEVEMENT
# =========================================================

@app.route("/achievement")
@app.route("/achievement.html")
def achievement():

    return render_template(
        "achievement.html"
    )


# =========================================================
# GALLERY
# =========================================================

@app.route("/gallery")
@app.route("/gallery.html")
def gallery():

    return render_template(
        "gallery.html"
    )


# =========================================================
# MENTORS
# =========================================================

@app.route("/mentors")
@app.route("/mentors.html")
def mentors():

    return render_template(
        "mentors.html"
    )


# =========================================================
# TRAINERS
# =========================================================

@app.route("/trainers")
@app.route("/trainers.html")
def trainers():

    return render_template(
        "trainers.html"
    )


# =========================================================
# TESTIMONIALS
# =========================================================

@app.route("/testimonials")
@app.route("/testimonials.html")
def testimonials():

    return render_template(
        "testimonials.html"
    )


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact")
@app.route("/contact.html")
def contact():

    return render_template(
        "contact.html"
    )


# =========================================================
# STUDENT REGISTRATION
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)

@app.route(
    "/register.html",
    methods=["GET", "POST"]
)

def register():

    if request.method == "POST":

        conn = None

        try:

            # -----------------------------------------
            # GET FORM DATA
            # -----------------------------------------

            student_name = request.form.get(
                "student_name",
                ""
            ).strip()

            parent_name = request.form.get(
                "parent_name",
                ""
            ).strip()

            dob = request.form.get(
                "dob",
                ""
            ).strip()

            age = request.form.get(
                "age",
                ""
            ).strip()

            gender = request.form.get(
                "gender",
                ""
            ).strip()

            mobile = request.form.get(
                "mobile",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip()

            address = request.form.get(
                "address",
                ""
            ).strip()

            previous_martial_art = request.form.get(
                "previous_martial_art",
                "No"
            ).strip()

            martial_art_details = request.form.get(
                "martial_art_details",
                ""
            ).strip()

            medical_condition = request.form.get(
                "medical_condition",
                ""
            ).strip()


            # -----------------------------------------
            # VALIDATION
            # -----------------------------------------

            if not all([
                student_name,
                parent_name,
                dob,
                age,
                gender,
                mobile,
                email,
                address
            ]):

                return jsonify({
                    "success": False,
                    "message":
                        "Please fill in all required fields."
                }), 400


            # -----------------------------------------
            # AGE VALIDATION
            # -----------------------------------------

            try:

                age = int(age)

            except ValueError:

                return jsonify({
                    "success": False,
                    "message":
                        "Age must be a valid number."
                }), 400


            # -----------------------------------------
            # JOINED DATE
            # -----------------------------------------

            joined_date = datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )


            # -----------------------------------------
            # DATABASE
            # -----------------------------------------

            conn = get_db_connection()

            if conn is None:

                return jsonify({
                    "success": False,
                    "message":
                        "Database connection error."
                }), 500


            cursor = conn.cursor()


            # -----------------------------------------
            # INSERT
            # -----------------------------------------

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
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?
                )
            """, (

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
            ))


            new_student_id = cursor.lastrowid

            conn.commit()


            logger.info(
                f"Student registered: "
                f"{student_name}, "
                f"ID={new_student_id}"
            )


            return jsonify({

                "success": True,

                "message":
                    "Registration Completed Successfully!",

                "student": {

                    "id":
                        str(new_student_id),

                    "name":
                        student_name,

                    "joined_date":
                        joined_date,

                    "mobile":
                        mobile
                }

            }), 201


        except Exception as e:

            if conn:

                conn.rollback()


            logger.error(
                f"Registration error: {e}"
            )


            return jsonify({

                "success": False,

                "message":
                    f"Server error: {str(e)}"

            }), 500


        finally:

            if conn:

                conn.close()


    return render_template(
        "register.html"
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)

def admin_login():

    if session.get("is_admin"):

        return redirect("/admin")


    error = None


    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()


        if (
            username == ADMIN_USERNAME
            and
            password == ADMIN_PASSWORD
        ):

            session["is_admin"] = True

            return redirect("/admin")


        error = "Invalid Username or Password!"


    return render_template(
        "admin_login.html",
        error=error
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "is_admin",
        None
    )

    return redirect(
        "/admin/login"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
@app.route("/admin.html")
def admin_dashboard():

    if not session.get("is_admin"):

        return redirect(
            "/admin/login"
        )


    students = []


    stats = {

        "total": 0,

        "male": 0,

        "female": 0,

        "experienced": 0
    }


    conn = None


    try:

        conn = get_db_connection()


        if conn:

            cursor = conn.cursor()


            cursor.execute("""
                SELECT *
                FROM students
                ORDER BY id DESC
            """)


            rows = cursor.fetchall()


            students = [
                dict(row)
                for row in rows
            ]


            stats["total"] = len(
                students
            )


            stats["male"] = sum(

                1

                for s in students

                if str(
                    s.get(
                        "gender",
                        ""
                    )
                ).strip().lower()
                == "male"
            )


            stats["female"] = sum(

                1

                for s in students

                if str(
                    s.get(
                        "gender",
                        ""
                    )
                ).strip().lower()
                == "female"
            )


            stats["experienced"] = sum(

                1

                for s in students

                if str(
                    s.get(
                        "previous_martial_art",
                        ""
                    )
                ).strip().lower()
                == "yes"
            )


    except Exception as e:

        logger.error(
            f"Admin dashboard error: {e}"
        )


    finally:

        if conn:

            conn.close()


    return render_template(
        "admin.html",
        students=students,
        stats=stats
    )


# =========================================================
# DELETE STUDENT
# =========================================================

@app.route(
    "/admin/delete/<int:student_id>",
    methods=["GET", "POST"]
)

def delete_student(student_id):

    if not session.get("is_admin"):

        return redirect(
            "/admin/login"
        )


    conn = None


    try:

        conn = get_db_connection()


        if conn:

            cursor = conn.cursor()


            cursor.execute("""
                DELETE FROM students
                WHERE id = ?
            """, (student_id,))


            conn.commit()


            logger.info(
                f"Student {student_id} deleted."
            )


    except Exception as e:

        logger.error(
            f"Delete error: {e}"
        )


    finally:

        if conn:

            conn.close()


    return redirect(
        "/admin"
    )


# =========================================================
# EXPORT CSV
# =========================================================

@app.route("/admin/export-csv")
@app.route("/admin/export_csv")

def export_csv():

    if not session.get("is_admin"):

        return redirect(
            "/admin/login"
        )


    conn = None


    try:

        conn = get_db_connection()


        if conn is None:

            return (
                "Database error",
                500
            )


        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM students
            ORDER BY id DESC
        """)


        rows = cursor.fetchall()


        output = io.StringIO()

        writer = csv.writer(
            output
        )


        # -----------------------------------------
        # CSV HEADER
        # -----------------------------------------

        writer.writerow([

            "ID",

            "Student Name",

            "Parent Name",

            "DOB",

            "Age",

            "Gender",

            "Mobile",

            "Email",

            "Address",

            "Previous Martial Art",

            "Details",

            "Medical Condition",

            "Joined Date"
        ])


        # -----------------------------------------
        # CSV DATA
        # -----------------------------------------

        for row in rows:

            student = dict(row)


            writer.writerow([

                f"VV-{student.get('id', '')}",

                student.get(
                    "student_name",
                    ""
                ),

                student.get(
                    "parent_name",
                    ""
                ),

                student.get(
                    "dob",
                    ""
                ),

                student.get(
                    "age",
                    ""
                ),

                student.get(
                    "gender",
                    ""
                ),

                student.get(
                    "mobile",
                    ""
                ),

                student.get(
                    "email",
                    ""
                ),

                student.get(
                    "address",
                    ""
                ),

                student.get(
                    "previous_martial_art",
                    "No"
                ),

                student.get(
                    "martial_art_details",
                    ""
                ),

                student.get(
                    "medical_condition",
                    "None"
                ),

                student.get(
                    "joined_date",
                    ""
                )
            ])


        output.seek(0)


        return Response(

            output.getvalue(),

            mimetype="text/csv",

            headers={
                "Content-Disposition":
                    "attachment; "
                    "filename=Veera_Vaanji_Students.csv"
            }
        )


    except Exception as e:

        logger.error(
            f"CSV export error: {e}"
        )


        return (
            f"Error exporting CSV: {e}",
            500
        )


    finally:

        if conn:

            conn.close()


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)

def not_found(error):

    return """
    <h2>404 - Page Not Found</h2>

    <p>
        <a href="/">
            Return to Home
        </a>
    </p>
    """, 404


# =========================================================
# 500 ERROR
# =========================================================

@app.errorhandler(500)

def internal_error(error):

    logger.error(
        f"Internal server error: {error}"
    )


    return jsonify({

        "success": False,

        "message":
            "Internal server error"

    }), 500


# =========================================================
# CONTEXT PROCESSOR
# =========================================================

@app.context_processor

def inject_config():

    return {

        "app_name":
            "Veera Vaanji Martial Arts Academy",

        "app_year":
            datetime.now().year
    }


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000
    )
