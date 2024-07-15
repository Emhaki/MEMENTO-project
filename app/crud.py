import datetime
from sqlalchemy.orm import Session
from . import models, schemas
import string, random

def get_url_by_short_key(db: Session, short_url: str):
    try:
        return db.query(models.URL).filter(models.URL.short_url == short_url).first()
    except Exception as e:
        print(f"Error fetching URL by short_key: {e}")
        return None

def create_short_key(length: int = 8):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def create_url(db: Session, url: models.URL, expires_at: int = None):
    short_url = create_short_key()
    while get_url_by_short_key(db, short_url) is not None:
        short_url = create_short_key()
    
    # 만료시간을 설정하지 않았을 경우 10분으로 지정
    if expires_at is None:
        expires_at = 10

    db_url = models.URL(
        original_url=url,
        short_url=short_url,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_at)
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def increment_visit_count(db: Session, db_url: models.URL):
    db_url.visit_count += 1
    db.commit()
    db.refresh(db_url)

def get_url_status(db: Session, short_url: str):
    return db.query(models.URL).filter(models.URL.short_url == short_url).first()

def delete_expired_urls(db: Session):
    now = datetime.datetime.utcnow()
    db.query(models.URL).filter(models.URL.expires_at < now).delete()
    db.commit()