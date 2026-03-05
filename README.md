# Sheridan College Group Registration System

This is a **full-stack registration website** built for Sheridan College competitions.  
It includes a backend built with **FastAPI** and **SQLAlchemy**, and a frontend using **HTML, CSS, and JavaScript**.

---

## Features

- **Group Registration**
  - Validate Sheridan College email
  - Group size 3–4 members
  - Maximum 10 groups
  - Registration closes 3 days before the competition

- **Admin Dashboard** (optional)
  - View registered participants

- **Feedback Form**
  - Collect user feedback and store in database

- **Responsive Frontend**
  - Works on desktop and mobile
  - Styled with CSS (Bootstrap optional)

---

## Project Structure


project/
│
├── backend/
│ ├── main.py # FastAPI app
│ ├── models.py # SQLAlchemy models
│ ├── database.py # DB connection & session
│
├── frontend/
│ ├── index.html # Home page
│ ├── register.html # Registration form
│ ├── contact.html # Feedback form
│ ├── style.css # CSS styling
│ └── script.js # JS for API calls
│
└── database/
└── registration.db # SQLite database


---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite  
- **Frontend:** HTML, CSS, JavaScript  
- **Deployment:** Localhost (Uvicorn). Can be deployed on Render, Railway, or AWS.

---

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/sheridan-registration-system.git
cd sheridan-registration-system/backend

