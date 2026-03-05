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

<img width="1466" height="884" alt="Screenshot 2026-03-05 at 5 07 46 PM" src="https://github.com/user-attachments/assets/7af4f57a-4cce-4252-96de-b1825b4c0bec" />
<img width="1470" height="876" alt="Screenshot 2026-03-05 at 5 08 25 PM" src="https://github.com/user-attachments/assets/5e8ca508-5e12-4013-af45-408a1706ff57" />
<img width="1470" height="956" alt="Screenshot 2026-03-05 at 5 08 18 PM" src="https://github.com/user-attachments/assets/ebe1bb29-8941-467c-b29b-ec16a853ddb9" />



