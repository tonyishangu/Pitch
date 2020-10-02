from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Pitch, User, Comment
from .forms import PitchForm, UpdateProfile, Commentform, Upvoteform, Downvoteform
from .. import db
from flask_login import login_required
from flask_login import login_required, current_user
from sqlalchemy import update

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.get_pitches()

    title = 'Home '
    return render_template('index.html', title = title, pitches=pitches)

@main.route('/category/<string:category>')
def cat(category):

    '''
    View categories function that returns the pitches of a given category
    '''

    cat = category
    title = f'{cat} pitches'

    pitches = Pitch.get_pitchcat(category)

    return render_template('categories.html',title = title, pitches=pitches, category=cat)


@main.route('/submitpitch/<int:userid>', methods = ['GET','POST'])
@login_required
def new_pitch(userid):
    form = PitchForm()

    pitchid = userid

    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        description = form.description.data
        new_pitch = Pitch(pitch_title=title,pitch_category=category,pitch_description=description, user=current_user)
        db.session.add(new_pitch)
        db.session.commit()


        return redirect(url_for('main.profile',uname=current_user.username))

    title = 'New Pitch'
    return render_template('new_pitch.html',title = title, pitch_form=form)


@main.route('/viewpitch/<int:pitchid>', methods = ['GET','POST'])

def comment(pitchid):
    form = Commentform()
    form2 = Upvoteform()
    form3 = Downvoteform()


    pitchid=pitchid
    pitches = Pitch.get_singlepitch(pitchid)
    comments = Comment.get_comments(pitchid)
    user = User.query.all()

    if form.validate_on_submit():
        description = form.description.data
        new_comment = Comment(comment_description=description, user=current_user, pitch_id = pitchid)
        new_comment.save_comment()

        return redirect(url_for('main.comment',pitchid=pitchid))

    if form2.validate_on_submit()and form2.submit1.data:
        pitches.pitch_votes += 1
        db.session.add(pitches)
        db.session.commit()
        return redirect(url_for('main.comment',pitchid=pitchid))

    if form3.validate_on_submit() and form3.submit2.data:
        pitches.pitch_votes = pitches.pitch_votes - 1
        db.session.add(pitches)
        db.session.commit()

        return redirect(url_for('main.comment',pitchid=pitchid))


    title = 'View pitch'
    return render_template('viewpitch.html',title = title, form=form, form2=form2, form3=form3, pitches = pitches, comments =comments, user =user)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    userid = user.id
    pitches = Pitch.get_userpitch(userid)
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, pitches=pitches)

@main.route('/user/<uname>/update',methods = ['GET','POST'])

def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.update_profile',uname=user.username))

    return render_template('profile/update.html',form =form)