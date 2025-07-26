from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    posts = db.relationship('Post', backref='author')

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Author name must be present.")
        existing = Author.query.filter_by(name=name).first()
        if existing:
            raise ValueError("Author name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone(self, key, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    summary = db.Column(db.String)
    category = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be no more than 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait):
            raise ValueError("Title must be clickbait-y.")
        return title

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
