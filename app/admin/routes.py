from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import login_required
from app.decorators import admin_required
from app.admin import bp
from app.models import User
from app import db

@bp.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('main/index.html', title='Admin')

@bp.route('/admin/users')
@login_required
@admin_required
def admin_user():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page, current_app.config['DISPLAY_PER_PAGE'], False)
    next_url = url_for('admin.admin_user', page=users.next_num) if users.has_next else None
    prev_url = url_for('admin.admin_user', page=users.prev_num) if users.has_prev else None
    return render_template('admin/admin_user.html', title='Admin', users=users.items, \
        next_url=next_url, prev_url=prev_url)

@bp.route('/admin/<int:id>/set_admin')
@login_required
@admin_required
def admin_set_admin(id):
    users = User.query.filter_by(id=id).first()
    users.add_as_admin()
    db.session.commit()
    return render_template('admin/admin_set_admin.html', title='Admin', users=users)

@bp.route('/admin/<int:id>/unset_admin')
@login_required
@admin_required
def admin_unset_admin(id):
    users = User.query.filter_by(id=id).first()
    users.remove_as_admin()
    db.session.commit()
    return render_template('admin/admin_unset_admin.html', title='Admin', users=users)