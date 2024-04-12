from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name_text):
        if name_text == "":
            raise ValueError("Name cannot be an empty string")
        elif self.query.filter_by(name=name_text).first() is not None:
            raise ValueError("This name already exists")
        return name_text
    
    @validates('phone_number')
    def validate_phone_number(self, key, pn):
        if type(int(pn)) != int:
            raise ValueError("Phone number must be an integer")
        elif len(pn) != 10:
            raise ValueError("Phone number must be 10 digits")
        return pn

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, text):
        if text == "":
            raise ValueError("Title cannot be an empty string")
        if any(substring in text for substring in ["Won't Believe", 'Secret', 'Top', 'Guess']):
            return text
        else:
            raise ValueError("Title doesn't POP")
        return text
    
    @validates('content')
    def validate_content(self, key, text):
        if len(text) < 250:
            raise ValueError("Content is too short. Must be 250 characters or more.")
        return text
    
    @validates('summary')
    def validate_summary(self, key, text):
        if len(text) > 250:
            raise ValueError("Content is too long. Must be 250 characters or less.")
        return text
    
    @validates('category')
    def validate_category(self, key, cat):
        if cat not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return cat

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
