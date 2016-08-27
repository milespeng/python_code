from datetime import  datetime
from flask import render_template,session,redirect,url_for,flash,request,current_app
from flask_login import  login_required,current_user
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,PostForm
from  .. import db
from  ..models import User,Role,Permission,Post
from ..decorators import admin_required


@main.route('/',method=['GET','POST'])
def index():
	form=PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and \
		form.validate_on_submit():
		post=Post(body=form.body.data,author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	#posts=Post.query.order_by(Post.timestamp.desc()).all()
	page=request.argv.get('page',1,type=int)
	pagination=Post.querry.order_by(Post.timestamp.desc()).paginate(
		page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
	)
	posts=pagination.items
	return render_template('index.html',form=form,posts=posts,pagination=pagination)





@main.route('/user/<username>')
def user(username):
    user=User.querry.filter_by(username=username).first()
    if user is None:
        abort(404)

    #    return render_template('user.html',user=user)
	posts=user.posts.order_by(Post.timestamp.desc()).all
	return render_template('user.html',user=user,posts=posts)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form=EditProfileForm()
	if form.validate_on_submit():
		current_user.name=form.name.data
		current_user.location=form.location.data
		current_user.about_me=form.about_me.data
		db.session.add(current_user)
		flash('Your profile has been updated.')
		return redirect(url_for('.user',username=current_user.username))
	form.name.data=current_user.name
	form.location.data=current_user.location
	form.about_me.data=current_user.about_me
	return render_template('edit_profile.html',form=form)

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user=User.querry.get_or_404(id)
	form=EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email=form.email.data
		user.username=form.username.data
		user.confirm=form.confirmed.data
		user.role=Role.query.get(form.role.data)
		user.name=form.name.data
		user.location=form.location.data
		user.about_me=form.location.data
		db.session.add(user)
		flash('The profile has been updated.')
		return redirect(url_for('.user',username=user.username))
	form.email.data=user.email
	form.username.data=user.username
	form.confirmed.data=user.confirmed
	form.role.data=user.role_id
	form.name.data=user.name
	form.location.data=user.location
	form.about_me=user.about_me
	return render_template('edit_profile.html',form=form,user=user)


