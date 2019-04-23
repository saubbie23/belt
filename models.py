from sqlalchemy.sql import func
from config import db, bcrypt
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

likes_table = db.Table("likes",
              db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
              db.Column("wish_id", db.Integer, db.ForeignKey("wishes.id"), primary_key=True)  )

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    liked_wishes = db.relationship("Wishes", secondary=likes_table)

    @classmethod
    def validate_user(cls, user_data):
        is_valid = True
        if len(user_data['first_name']) < 1:
            flash('First Name required!')
            is_valid = False
        if len(user_data['last_name']) < 1:
            flash('Last Name required!')
            is_valid = False
        if user_data['password'] != user_data['confirm_password']:
            flash('Passwords must match!')
            is_valid = False
        if len(user_data['password']) < 8:
            flash("Password must be at least 8 characters long!")
            is_valid = False

        # Validate Email
        if not EMAIL_REGEX.match(user_data['email']):    
            flash("Invalid email address!")
            is_valid = False

        return is_valid

    @classmethod
    def add_user(cls, user_data):
        hashed_pw = bcrypt.generate_password_hash(user_data["password"])
        new_user = cls(first_name= user_data["first_name"], last_name= user_data["last_name"], email= user_data["email"], password= hashed_pw)

        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def login(cls, form_data):
        success = False
        user_info = Users.query.filter_by(email=form_data["email"])

        if bcrypt.check_password_hash(user_info[0].password, form_data["password"]):
            success = True
        else:
            flash('Incorect username/password combination!')

        return success

class Wishes(db.Model):
    __tablename__ = "wishes"
    id = db.Column(db.Integer, primary_key= True)
    wish = db.Column(db.String(255))
    description = db.Column(db.String(255))
    granted = db.Column(db.String(3))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    granted_at = db.Column(db.DateTime)
    granted_by = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    user = db.relationship('Users', foreign_keys=[user_id], backref= "wish", cascade="all")
    user_likes = db.relationship("Users", secondary=likes_table)

    @classmethod
    def validate_wish(cls, wish_data):
        is_valid = True
        if len(wish_data['wish']) < 3:
            flash('Wishes must be at least 3 characters!')
            is_valid = False
        if len(wish_data['description']) < 3:
            flash('Wish descriptions must be at least 3 characters!')
            is_valid = False

        return is_valid

    @classmethod
    def add_wish(cls, wish_data):
        new_wish = cls(wish= wish_data["wish"], description= wish_data["description"], user_id=session['user_id'], granted='No')

        db.session.add(new_wish)
        db.session.commit()
        return new_wish

    @classmethod
    def edit_wish(cls, wish_data):
        wish_to_update = Wishes.query.get(wish_data['wish_id'])
        wish_to_update.wish = wish_data['wish']
        wish_to_update.description = wish_data['description']

        db.session.commit()
        return wish_to_update

    @classmethod
    def grant_wish(cls, wish_id):
        wish_to_update = Wishes.query.get(wish_id)
        wish_to_update.granted = 'Yes'
        wish_to_update.granted_at = func.now()
        wish_to_update.granted_by = session['user_id']

        db.session.commit()
        return wish_to_update

    @classmethod
    def add_like(cls, id):
        curr_user = Users.query.get(session["user_id"])
        curr_wish = Wishes.query.get(id)
        for user_like in curr_wish.user_likes:
            print('one')
            if user_like.id == session["user_id"]:
                 flash('You already liked this wish!')
                 return False
        curr_wish.user_likes.append(curr_user)
        db.session.commit()
        return True

    @classmethod
    def count_likes(cls):
        total_likes = db.session.query(Wishes, Wishes.id, func.count(likes_table.c.user_id).label('likes')).join(likes_table).group_by(Wishes.id)
        return total_likes

    @classmethod
    def all_granted(cls):
        granted = db.session.query(Wishes.granted).filter(Wishes.granted == "Yes").count()
        return granted

    @classmethod
    def user_granted(cls):
        user_granted = db.session.query(Wishes.granted).filter(Wishes.granted == "Yes",Wishes.user_id == session["user_id"]).count()
        return user_granted

    @classmethod
    def user_pending(cls):
        user_pending = db.session.query(Wishes.granted).filter(Wishes.granted == "No", Wishes.user_id == session["user_id"]).count()
        return user_pending