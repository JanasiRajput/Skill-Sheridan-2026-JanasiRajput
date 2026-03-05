from sqlalchemy.orm import Session
import models, schemas
# --- TEAMS CRUD ---
def create_team(db, team, status):
    new_team = models.Team(
        team_name=team.team_name,
        robot_name=team.robot_name,
        category=team.category,
        student_id=team.student_id,
        name=team.name,
        email=team.email,
        description=team.description,
        # members=team.members,  
        status=status
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

def get_teams(db):
    return db.query(models.Team).all()

def update_team(db, team_id, data, status=None):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team:
        team.team_name = data.team_name
        team.robot_name = data.robot_name
        team.category = data.category
        team.student_id = data.student_id
        team.name = data.name
        team.email = data.email
        team.description = data.description
        # team.members = data.members  
        if status:
            team.status = status
        db.commit()
        db.refresh(team)
    return team

def delete_team(db, team_id):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team:
        db.delete(team)
        db.commit()

# FEEDBACK
def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    fb = models.Feedback(**feedback.dict())
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

def get_feedback(db: Session):
    return db.query(models.Feedback).all()

def delete_feedback(db: Session, feedback_id: int):
    fb = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if fb:
        db.delete(fb)
        db.commit()

# Create Result
def create_result(db, result: ResultCreate):
    r = models.Result(**result.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

# Get all results
def get_results(db):
    return db.query(models.Result).all()

# Delete Result
def delete_result(db, result_id: int):
    r = db.query(models.Result).filter(models.Result.id == result_id).first()
    if r:
        db.delete(r)
        db.commit()

# Update Result
def update_result(db, result_id: int, data: ResultCreate):
    r = db.query(models.Result).filter(models.Result.id == result_id).first()
    if r:
        r.team_name = data.team_name
        r.robot_name = data.robot_name
        r.category = data.category
        r.position = data.position
        r.remarks = data.remarks
        db.commit()
        db.refresh(r)
    return r