from flask import render_template, redirect, request, session, flash
from models import Users, Wishes


# LOGIN FUNCTIONS
def index():
    return render_template('index.html')

def register():
    validate = Users.validate_user(request.form)
    if not validate:
        return redirect('/')
    else:
        new_user = Users.add_user(request.form)
        session["user_id"] = new_user.id
        session["first_name"] = new_user.first_name
        return redirect('/')

def login():
    success = Users.login(request.form)

    if not success:
        return redirect('/')
    else:
        # Get user info
        user = Users.query.filter_by(email= request.form["email"])
        session["user_id"] = user[0].id
        session["first_name"] = user[0].first_name
       
        return redirect('/dashboard')

def dashboard():
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        wish = Users.query.get(session['user_id'])
        all_wishes = Wishes.query.all()
        wish_likes = Wishes.count_likes()
        for like in wish_likes:
            print('Wish ID:', like.id)
            print('Wish Likes:', like.likes)
        return render_template('dashboard.html', wishes= wish, all_wishes= all_wishes, wish_likes= wish_likes)
    
def success():
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        # Get user data
        user = Users.query.filter_by(username=session["first_name"])
        return render_template('home.html', users = user)

def logout():
    session.clear()
    return redirect('/')


# WISH FUNCTIONS
def make_wish():
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        return render_template('make_wish.html')

def create_wish():
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        validate = Wishes.validate_wish(request.form)
        if not validate:
            return redirect('/make_wish')
        else:
            new_wish = Wishes.add_wish(request.form)
            return redirect('/dashboard')

def edit_page(id):
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        wish = Wishes.query.get(id)
        return render_template('edit_wish.html', wish= wish)

def edit_wish(id):
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        validate = Wishes.validate_wish(request.form)
        if not validate:
            return redirect('/edit_wish/' + str(id))
        else:
            edited_wish = Wishes.edit_wish(request.form)
            return redirect('/dashboard')

def grant_wish(id):
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        granted_wish = Wishes.grant_wish(id)
        return redirect('/dashboard')

def like_wish(id):
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        liked_wish = Wishes.add_like(id)
        return redirect('/dashboard')

def view_stats():
    if not "user_id" in session.keys():
        flash("You must log in to see this page!")
        return redirect('/')
    else:
        all_granted = Wishes.all_granted()
        user_granted = Wishes.user_granted()
        user_pending = Wishes.user_pending()
    
        return render_template('stats.html', all_granted= all_granted, user_granted= user_granted, user_pending= user_pending)


