# database.py

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import random

DATABASE_URL = 'sqlite:///quotes.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quotes'
    uid = Column(String, primary_key=True)
    quote = Column(String)
    author = Column(String)

Base.metadata.create_all(engine)

_session_factory = sessionmaker(bind=engine)

def _get_session():
    """Return a new Session object for each call"""
    return _session_factory()

def add_quote(uid, quote, author):
    """Add a quote if the UID is not in the database yet"""
    session = _get_session()
    if not session.query(Quote).filter_by(uid=uid).first():
        new_quote = Quote(uid=uid, quote=quote, author=author)
        session.add(new_quote)
        session.commit()
        return True
    return False

def delete_quote(uid):
    """Delete a quote by its UID"""
    session = _get_session()
    quote_obj = session.query(Quote).filter_by(uid=uid).first()
    if quote_obj:
        session.delete(quote_obj)
        session.commit()
        return True
    return False

def fetch_quote_by_uid(uid):
    """Fetch a quote by its UID"""
    session = _get_session()
    return session.query(Quote).filter_by(uid=uid).first()

def fetch_random_quote():
    """Fetch a random quote"""
    session = _get_session()
    count = session.query(Quote).count()
    random_index = random.randint(1, count)
    return session.query(Quote).offset(random_index-1).limit(1).first()

def edit_quote(uid, quote=None, author=None):
    """Edit a quote by its UID"""
    session = _get_session()
    quote_obj = session.query(Quote).filter_by(uid=uid).first()
    if quote_obj:
        if quote:
            quote_obj.quote = quote
        if author:
            quote_obj.author = author
        session.commit()
        return True
    return False

def fetch_multiple_quotes(count=10):
    """Fetch multiple quotes"""
    session = _get_session()
    return session.query(Quote).order_by(func.random()).limit(count).all()

def get_quote_count():
    """Get the total count of quotes"""
    session = _get_session()
    query = session.query(Quote)
    return query.count()
