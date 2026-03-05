from fastapi import FastAPI, Request, Form, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, crud, auth

from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --- DATABASE SESSION ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ADMIN AUTH DEPENDENCY ---
def admin_required(admin: str = Cookie(default=None)):
    if admin != "true":
        raise HTTPException(status_code=401, detail="Unauthorized")


# --- PUBLIC ROUTES ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#Gallery
@app.get("/gallery", response_class=HTMLResponse)
def gallery_page(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@app.post("/register")
def register_team(
        team_name: str = Form(...),
        robot_name: str = Form(...),
        category: str = Form(...),
        student_id: str = Form(...),
        name: str = Form(...),
        email: str = Form(...),
        description: str = Form(...),
        # members: int = Form(...),  
        db: Session = Depends(get_db)
):
    if datetime.now() > datetime(2026, 11, 15):
        return templates.TemplateResponse("register.html", {"request": {}, "error": "Registration closed."})

    if not student_id.isdigit() or len(student_id) != 9:
        return templates.TemplateResponse("register.html", {"request": {}, "error": "Student ID must be 9 digits."})

    if "@sheridancollege.ca" not in email:
        return templates.TemplateResponse("register.html", {"request": {}, "error": "Sheridan email required."})

    if len(description.strip()) < 20:
        return templates.TemplateResponse("register.html", {"request": {}, "error": "Project description must be at least 20 characters."})

    existing = db.query(models.Team).filter(models.Team.student_id == student_id).first()
    if existing:
        return templates.TemplateResponse("register.html", {"request": {}, "error": "Student ID already registered."})

    total_teams = db.query(models.Team).count()
    if total_teams < 18:
        status = "Confirmed"
    elif total_teams < 22:
        status = "Waitlisted"
    else:
        return templates.TemplateResponse("register.html", {"request": {}, "error": "Max teams reached."})

    team = schemas.TeamCreate(
        team_name=team_name, robot_name=robot_name, category=category,
        student_id=student_id, name=name, email=email, description=description
    )
    crud.create_team(db, team, status)
    return RedirectResponse("/teams", status_code=303)


@app.get("/teams", response_class=HTMLResponse)
def teams(request: Request, db: Session = Depends(get_db)):
    teams = crud.get_teams(db)
    return templates.TemplateResponse("teams.html", {"request": request, "teams": teams})


@app.get("/feedback", response_class=HTMLResponse)
def feedback_page(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})


@app.post("/feedback")
def submit_feedback(
        student_id: str = Form(...),
        email: str = Form(...),
        rating: int = Form(...),
        comments: str = Form(...),
        db: Session = Depends(get_db)
):
    fb = schemas.FeedbackCreate(student_id=student_id, email=email, rating=rating, comments=comments)
    crud.create_feedback(db, fb)
    return RedirectResponse("/", status_code=303)

# --- PUBLIC RESULTS PAGE ---
@app.get("/results", response_class=HTMLResponse)
def results(request: Request, db: Session = Depends(get_db)):
    results = crud.get_results(db)

    # If database is empty, add default dummy data
    if not results:
        default_results = [
            {"team_name": "Alpha Bots", "robot_name": "RoboX", "category": "Autonomous",
             "position": "Winner", "remarks": "Excellent design and performance"},
            {"team_name": "Beta Mechanics", "robot_name": "MechaRunner", "category": "Line Following",
             "position": "Runner-up", "remarks": "Great speed and accuracy"},
            {"team_name": "Gamma Coders", "robot_name": "CodeRacer", "category": "Obstacle",
             "position": "Third Place", "remarks": "Well-programmed, minor errors"},
        ]
        for r in default_results:
            crud.create_result(db, schemas.ResultCreate(**r))
        results = crud.get_results(db)

    return templates.TemplateResponse("results.html", {"request": request, "results": results})


# --- ADMIN LOGIN ---
@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": None})


@app.post("/admin/login")
def admin_login(username: str = Form(...), password: str = Form(...)):
    if auth.authenticate(username, password):
        response = RedirectResponse("/admin/dashboard", status_code=303)
        response.set_cookie(key="admin", value="true")
        return response
    return templates.TemplateResponse("admin_login.html", {"request": {}, "error": "Invalid credentials"})


# --- ADMIN DASHBOARD ---
@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db), _: None = Depends(admin_required)):
    teams = crud.get_teams(db)
    feedback = crud.get_feedback(db)
    results = crud.get_results(db)
    return templates.TemplateResponse("admin.html", {"request": request, "teams": teams, "feedback": feedback, "results": results})


# --- ADMIN ACTIONS ---
# --- ADMIN CRUD FOR TEAMS ---
@app.post("/admin/teams/add")
def add_team(
    team_name: str = Form(...),
    robot_name: str = Form(...),
    category: str = Form(...),
    student_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    description: str = Form(...),
    status: str = Form("Confirmed"),
    db: Session = Depends(get_db),
    _: None = Depends(admin_required)
):
    team = schemas.TeamCreate(
        team_name=team_name,
        robot_name=robot_name,
        category=category,
        student_id=student_id,
        name=name,
        email=email,
        description=description
        
    )
    crud.create_team(db, team, status)
    return RedirectResponse("/admin/dashboard", status_code=303)


@app.post("/admin/teams/update/{team_id}")
def update_team_admin(
    team_id: int,
    team_name: str = Form(...),
    robot_name: str = Form(...),
    category: str = Form(...),
    student_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
    _: None = Depends(admin_required)
):
    data = schemas.TeamCreate(
        team_name=team_name,
        robot_name=robot_name,
        category=category,
        student_id=student_id,
        name=name,
        email=email,
        description=description
    )
    crud.update_team(db, team_id, data, status)
    return RedirectResponse("/admin/dashboard", status_code=303)


@app.get("/admin/teams/delete/{team_id}")
def delete_team_admin(team_id: int, db: Session = Depends(get_db), _: None = Depends(admin_required)):
    crud.delete_team(db, team_id)
    return RedirectResponse("/admin/dashboard", status_code=303)


# --- ADMIN CRUD FOR RESULTS ---
@app.post("/admin/results/add")
def add_result(
    team_name: str = Form(...),
    robot_name: str = Form(...),
    category: str = Form(...),
    position: str = Form(...),
    remarks: str = Form(...),
    db: Session = Depends(get_db),
    _: None = Depends(admin_required)
):
    data = schemas.ResultCreate(
        team_name=team_name,
        robot_name=robot_name,
        category=category,
        position=position,
        remarks=remarks
    )
    crud.create_result(db, data)
    return RedirectResponse("/admin/dashboard", status_code=303)
@app.post("/admin/results/update/{result_id}")
def update_result(
    result_id: int,
    team_name: str = Form(...),
    robot_name: str = Form(...),
    category: str = Form(...),
    position: str = Form(...),
    remarks: str = Form(...),
    db: Session = Depends(get_db),
    _: None = Depends(admin_required)
):
    data = schemas.ResultCreate(
        team_name=team_name,
        robot_name=robot_name,
        category=category,
        position=position,
        remarks=remarks
    )
    crud.update_result(db, result_id, data)
    return RedirectResponse("/admin/dashboard", status_code=303)

@app.get("/admin/results/delete/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db), _: None = Depends(admin_required)):
    crud.delete_result(db, result_id)
    return RedirectResponse("/admin/dashboard", status_code=303)