# Veera Vaanji Martial Arts Academy - Website

A Flask-based web application for managing a martial arts academy's website and student registrations.

## 📁 Project Structure

```
vvwebsite/
├── app.py                    # Main Flask application
├── database.py               # Database functions and utilities
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── martial_arts.db          # SQLite database
│
├── templates/               # HTML templates
│   ├── index.html
│   ├── about.html
│   ├── admission.html
│   ├── achievement.html
│   ├── contact.html
│   ├── gallery.html
│   ├── mentors.html
│   ├── register.html
│   ├── testimonials.html
│   └── trainers.html
│
└── static/                  # Static files
    ├── css/                 # CSS stylesheets
    ├── images/              # Image assets
    └── js/                  # JavaScript files
```

## ✨ Key Features

- ✅ **Proper Flask Folder Configuration** - Absolute paths for templates and static files
- ✅ **Efficient Database Management** - SQLite with proper connection handling
- ✅ **Error Handling** - Comprehensive error handling with logging
- ✅ **Multiple Routes** - All pages configured as separate routes
- ✅ **Student Registration** - Form submission with database storage
- ✅ **API Endpoints** - JSON API for fetching student data
- ✅ **Configuration Management** - .env file support

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or extract the project**
   ```bash
   cd vvwebsite
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The application will start at `http://localhost:5000`

## 📋 Usage

### Home Page
Visit `http://localhost:5000/` or `http://localhost:5000/index` to view the home page.

### Available Routes
- `/` - Home page
- `/index` - Index page
- `/about` - About page
- `/admission` - Admission page
- `/achievement` - Achievement page
- `/gallery` - Gallery page
- `/mentors` - Mentors page
- `/trainers` - Trainers page
- `/testimonials` - Testimonials page
- `/contact` - Contact page
- `/register` - Student registration (GET/POST)
- `/api/students` - API endpoint to fetch all registered students

### Student Registration
1. Navigate to `/register`
2. Fill in all required fields
3. Submit the form
4. Data will be stored in the SQLite database

## 🔧 Configuration

### Create .env file
Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=5000
```

## 📊 Database

The application uses SQLite3 with the following student table:

```sql
CREATE TABLE students (
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
```

### Initialize Database Manually
```python
from database import create_database
create_database()
```

## 🛠️ Development

### View Logs
Application logs are printed to console. Check console output for registration logs and errors.

### Database Functions (from database.py)
- `create_database()` - Initialize database and tables
- `get_all_students()` - Fetch all students
- `get_student_by_id(id)` - Fetch specific student
- `add_student(data)` - Add new student
- `update_student(id, data)` - Update student info
- `delete_student(id)` - Delete student

## 🚨 Improvements Made

1. ✅ **Proper Path Handling** - Uses `os.path` for absolute paths
2. ✅ **Static Files Organization** - JS files moved to `static/js/`
3. ✅ **Database Connection** - Centralized connection management
4. ✅ **Error Handling** - Try-catch blocks with logging
5. ✅ **All Routes** - Complete route configuration for all pages
6. ✅ **API Endpoints** - JSON responses for data fetching
7. ✅ **Validation** - Form validation and input sanitization
8. ✅ **Logging** - Comprehensive application logging

## 📝 API Responses

### Successful Registration
```json
{
    "success": true,
    "message": "Registration Successful! Welcome to Veera Vaanji!"
}
```

### Fetch Students
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "student_name": "John Doe",
            "parent_name": "Jane Doe",
            "joined_date": "21-08-2026"
        }
    ],
    "total": 1
}
```

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
**Solution:** Change port in app.py
```python
app.run(port=5001)  # Use different port
```

### Issue: Module 'flask' not found
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Database file not found
**Solution:** Database will be created automatically on first run. If not, run:
```python
python database.py
```

## 📧 Contact & Support

For issues or questions, please contact the development team.

## 📄 License

This project is proprietary to Veera Vaanji Martial Arts Academy.

---

**Last Updated:** August 21, 2026
**Version:** 2.0 (Corrected & Optimized)
