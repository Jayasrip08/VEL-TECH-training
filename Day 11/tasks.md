# Day 1 Task – Student Registration System (Flask + HTML + CSS)

## Objective

Today your goal is to build the frontend structure of the Student Registration System using Flask Template Rendering (`render_template`), HTML, and CSS.

No database integration is required today.

You must create professional-looking web pages and connect them using Flask routing.

---

# Software Installation

## Step 1: Install Python

Download Python from:

https://www.python.org/downloads/

During installation, make sure to select:

✓ Add Python to PATH

Verify installation:

```cmd
python --version
pip --version
```

---
 ## Step 2: Create Project Folder Using Command Prompt

Open Command Prompt and execute the following commands:

Move to Desktop:

cd Desktop

Create Project Folder:

mkdir StudentRegistrationSystem

Move Inside the Folder:

cd StudentRegistrationSystem

Open the Project in VS Code:

code .

If the code command is not recognized, open VS Code manually and select:

File → Open Folder → StudentRegistrationSystem

---

## Step 3: Create Project Structure Using VS Code

After opening the project folder in VS Code:

Create the Main Folders
In the Explorer panel on the left side, right-click on the project folder (StudentRegistrationSystem).

Select New Folder.
Create the following folders:
templates
static

Create Subfolders Inside Static
Right-click on the static folder.
Select New Folder.
Create:
css
images

Create Files
In the Project Root Folder

Create:

app.py
Inside Templates Folder

Create:

index.html
register.html
students.html
about.html
Inside CSS Folder

Create:

style.css
Verify Folder Structure

Your project should look like this:

StudentRegistrationSystem
│
├── app.py
│
├── templates
│   ├── index.html
│   ├── register.html
│   ├── students.html
│   └── about.html
│
└── static
    ├── css
    │   └── style.css
    │
    └── images

---

## Step 4: Install Flask

Install Flask:

```cmd
pip install flask
```

Verify Installation:

```cmd
pip list
```

---

# Flask Routing Task

Create routes using `render_template()` for:

```text
/
```

(Home Page)

```text
/register
```

(Student Registration Page)

```text
/students
```

(Student Records Page)

```text
/about
```

(About Page)

---

# Page Requirements

## Home Page

Include:

* College Name
* Project Title
* Navigation Bar
* Welcome Section
* Project Description
* Professional Hero Section

---

## Registration Page

Create a registration form containing:

* Student Name
* Roll Number
* Department
* Year
* Email
* Phone Number
* Gender
* Address

(No database connection today)

---

## Students Page

Display at least 10 student records using dummy data in a table.

Example:

| Roll No | Name  | Department | Year |
| ------- | ----- | ---------- | ---- |
| 101     | Arjun | IT         | 3    |
| 102     | Priya | CSE        | 2    |

---

## About Page

Include:

* Project Overview
* Features
* Team Information
* Footer

---

# CSS Requirements

All pages must contain:

* Responsive Navigation Bar
* Hover Effects
* Professional Color Theme
* Responsive Design
* Form Styling
* Table Styling
* Buttons
* Cards
* Footer

Do not use plain HTML pages.

---

# Running the Project

Open Command Prompt inside the project folder and run:

```cmd
python app.py
```

Open Browser:

```text
http://127.0.0.1:5000
```

---

# Deliverables

Every team must demonstrate:

✓ Flask installed successfully

✓ Correct project structure

✓ Working Flask routes

✓ Usage of `render_template()`

✓ Four designed pages

✓ Navigation between pages

✓ Professional HTML & CSS design

✓ Students page displaying dummy data

Tomorrow we will integrate SQLite and store real student records in the database.
