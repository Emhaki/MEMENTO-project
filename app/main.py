from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine, Base, get_db
import datetime


Base.metadata.create_all(bind=engine)

app = FastAPI()

# APScheduler 인스턴스 생성
scheduler = BackgroundScheduler()

@app.on_event("startup")
def startup_event():
    # 스케줄러 작업 추가
    scheduler.add_job(delete_expired_urls_job, 'interval', minutes=1)
    print("스케줄러 실행")
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

def delete_expired_urls_job():
    db = SessionLocal()
    try:
        crud.delete_expired_urls(db)
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(url: str, expiration_time: int = None, db: Session = Depends(get_db)):
    db_url = crud.create_url(db=db, url=url, expires_at=expiration_time)
    return db_url

@app.get("/{short_key}")
def redirect_original_url(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short_key(db=db, short_url=short_key)
    
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL Not Found")
    
    if db_url.expires_at and db_url.expires_at < datetime.datetime.utcnow():
        raise HTTPException(status_code=404, detail="URL has expired")

    # 방문횟수 카운트
    crud.increment_visit_count(db, db_url)

    return db_url.original_url

@app.get("/stats/{short_key}")
def get_status(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_status(db, short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL Not Found")
    
    return db_url.visit_count

