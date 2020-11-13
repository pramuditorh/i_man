from datetime import date
from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.main.forms import PatchCordForm, SFPForm, IOMForm, MDAForm
from app.models import User, Item
from app.decorators import admin_required
from app.main import bp
from app import db, images

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated and current_user.is_admin == True:
        return redirect(url_for('admin.admin'))
    return render_template('main/index.html', title='i-man')

@bp.route('/input', methods=['GET'])
@login_required
def input():
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(page, current_app.config['DISPLAY_PER_PAGE'], False)
    next_url = url_for('main.input', page=items.next_num) if items.has_next else None
    prev_url = url_for('main.input', page=items.prev_num) if items.has_prev else None
    return render_template('main/input.html', title='Input Item', items=items.items, \
        next_url=next_url, prev_url=prev_url)

@bp.route('/input/<items>', methods=['GET', 'POST'])
@login_required
def input_item(items):
    if items == 'patch_cord':
        form = PatchCordForm()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item = Item(name='patch_cord', type=form.type.data, in_timestamp= date.today(), \
                    length=form.length.data, note=form.note.data, user_id=current_user.name, \
                        in_filename_record_of_transfer=filename, \
                            in_url_record_of_transfer=url_file)
            else:
                item = Item(name='patch_cord', type=form.type.data, in_timestamp= date.today(), \
                    length=form.length.data, note=form.note.data, user_id=current_user.name)
            db.session.add(item)
            db.session.commit()
            flash(f'Item {item.name}, {item.type} successfully entered!')
            return redirect(url_for('main.input_item', items='patch_cord'))
        return render_template('main/patch_cord.html', title='Input Patch Cord', form=form)
    if items == 'sfp':
        form = SFPForm()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item = Item(name='sfp', type=form.type.data, in_timestamp= date.today(), length=form.length.data, capacity=form.capacity.data, \
                    serial_number=form.serial_number.data, product_number=form.product_number.data, \
                        note=form.note.data, user_id=current_user.name, in_filename_record_of_transfer=filename, \
                            in_url_record_of_transfer=url_file)
            else:
                item = Item(name='sfp', type=form.type.data, in_timestamp= date.today(), length=form.length.data, capacity=form.capacity.data, \
                    serial_number=form.serial_number.data, product_number=form.product_number.data, \
                        note=form.note.data, user_id=current_user.name)
            db.session.add(item)
            db.session.commit()
            flash(f'Item {item.name}, {item.type} successfully entered!')
            return redirect(url_for('main.input_item', items='sfp'))
        return render_template('main/sfp.html', title='SFP', form=form)
    if items == 'iom':
        form = IOMForm()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item = Item(name='iom', type=form.type.data, in_timestamp= date.today(), note=form.note.data, user_id=current_user.name, \
                    in_filename_record_of_transfer=filename, in_url_record_of_transfer=url_file)
            else:
                item = Item(name='iom', type=form.type.data, in_timestamp= date.today(), note=form.note.data, user_id=current_user.name)
            db.session.add(item)
            db.session.commit()
            flash(f'Item {item.name}, {item.type} successfully entered!')
            return redirect(url_for('main.input_item', items='iom'))
        return render_template('main/iom.html', title='IOM/Slot', form=form)
    if items == 'mda':
        form = MDAForm()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item = Item(name='mda', type=form.type.data, in_timestamp= date.today(), capacity=form.capacity.data, \
                    note=form.note.data, user_id=current_user.name, in_filename_record_of_transfer=filename, \
                        in_url_record_of_transfer=url_file)
            else:
                item = Item(name='mda', type=form.type.data, in_timestamp= date.today(), capacity=form.capacity.data, \
                    note=form.note.data, user_id=current_user.name)
            db.session.add(item)
            db.session.commit()
            flash(f'Item {item.name}, {item.type} successfully entered!')
            return redirect(url_for('main.input_item', items='mda'))
        return render_template('main/mda.html', title='MDA', form=form)

@bp.route('/edit/<items>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(items, id):
    if items == 'patch_cord':
        form = PatchCordForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.length = form.length.data
                item.note = form.note.data
                item.in_filename_record_of_transfer = filename
                item.in_url_record_of_transfer = url_file
            else:
                item.type = form.type.data
                item.length = form.length.data
                item.note = form.note.data
            db.session.commit()
            flash(f'Item {item.name} has been updated!')
            return redirect(url_for('main.input', items=item.name))
        elif request.method == 'GET':
            form.type.data = item.type
            form.length.data = item.length
            form.note.data = item.note
            form.in_record_of_transfer.data = item.in_filename_record_of_transfer
        return render_template('main/patch_cord.html', title='Edit Patch Cord', form=form)
    if items == 'sfp':
        form = SFPForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.length = form.length.data
                item.capacity = form.capacity.data
                item.serial_number = form.serial_number.data
                item.product_number = form.product_number.data
                item.note = form.note.data
                item.in_filename_record_of_transfer = filename
                item.in_url_record_of_transfer = url_file
            else:
                item.type = form.type.data
                item.length = form.length.data
                item.capacity = form.capacity.data
                item.serial_number = form.serial_number.data
                item.product_number = form.product_number.data
                item.note = form.note.data
            db.session.commit()
            flash(f'Item {item.name} has been updated!')
            return redirect(url_for('main.input', items=item.name))
        elif request.method == 'GET':
            form.type.data = item.type
            form.length.data = item.length
            form.capacity.data = item.capacity
            form.serial_number.data = item.serial_number
            form.product_number.data = item.product_number
            form.note.data = item.note
            form.in_record_of_transfer.data = item.in_filename_record_of_transfer
        return render_template('main/sfp.html', title='Edit SFP', form=form)
    if items == 'iom':
        form = IOMForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.note = form.note.data
                item.filename_record_of_transfer = filename
                item.in_url_record_of_transfer = url_file
            else:
                item.type = form.type.data
                item.note = form.note.data
            db.session.commit()
            flash(f'Item {item.name} has been updated!')
            return redirect(url_for('main.input', items=item.name))
        elif request.method == 'GET':
            form.type.data = item.type
            form.note.data = item.note
            form.in_record_of_transfer.data = item.in_filename_record_of_transfer
        return render_template('main/iom.html', title='Edit IOM', form=form)
    if items == 'mda':
        form = MDAForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['in_record_of_transfer']:
                filename = images.save(request.files['in_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.capacity = form.capacity.data
                item.note = form.note.data
                item.in_filename_record_of_transfer = filename
                item.in_url_record_of_transfer = url_file
            else:
                item.type = form.type.data
                item.capacity = form.capacity.data
                item.note = form.note.data
            db.session.commit()
            flash(f'Item {item.name} has been updated!')
            return redirect(url_for('main.input', items=item.name))
        elif request.method == 'GET':
            form.type.data = item.type
            form.capacity.data = item.capacity
            form.note.data = item.note
            form.in_record_of_transfer.data = item.in_filename_record_of_transfer
        return render_template('main/mda.html', title='Edit MDA', form=form)

@bp.route('/takeout/<items>/<int:id>', methods=['GET', 'POST'])
@login_required
def takeout_item(items, id):
    if items == 'patch_cord':
        form = PatchCordForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['out_record_of_transfer']:
                filename = images.save(request.files['out_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.length = form.length.data
                item.note = form.note.data
                item.out_filename_record_of_transfer = filename
                item.out_url_record_of_transfer = url_file
            item.taken_out()
            db.session.commit()
            flash(f'Item {item.name} has been taken out!')
            return redirect(url_for('main.takeout'))
        elif request.method == 'GET':
            form.type.data = item.type
            form.length.data = item.length
            form.note.data = item.note
        return render_template('main/patch_cord.html', title='Takeout Patch Cord', form=form, item=item)
    if items == 'sfp':
        form = SFPForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['out_record_of_transfer']:
                filename = images.save(request.files['out_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.length = form.length.data
                item.capacity = form.capacity.data
                item.serial_number = form.serial_number.data
                item.product_number = form.product_number.data
                item.note = form.note.data
                item.out_filename_record_of_transfer = filename
                item.out_url_record_of_transfer = url_file
            item.taken_out()
            db.session.commit()
            flash(f'Item {item.name} has been taken out!')
            return redirect(url_for('main.takeout'))
        elif request.method == 'GET':
            form.type.data = item.type
            form.length.data = item.length
            form.capacity.data = item.capacity
            form.serial_number.data = item.serial_number
            form.product_number.data = item.product_number
            form.note.data = item.note
        return render_template('main/sfp.html', title='Takeout SFP', form=form, item=item)
    if items == 'iom':
        form = IOMForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['out_record_of_transfer']:
                filename = images.save(request.files['out_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.note = form.note.data
                item.out_filename_record_of_transfer = filename
                item.out_url_record_of_transfer = url_file
            item.taken_out()
            db.session.commit()
            flash(f'Item {item.name} has been taken out!')
            return redirect(url_for('main.input', items=item.name))
        elif request.method == 'GET':
            form.type.data = item.type
            form.note.data = item.note
        return render_template('main/iom.html', title='Takeout IOM', form=form, item=item)
    if items == 'mda':
        form = MDAForm()
        item = Item.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if request.files['out_record_of_transfer']:
                filename = images.save(request.files['out_record_of_transfer'])
                url_file = images.url(filename)
                item.type = form.type.data
                item.length = form.length.data
                item.note = form.note.data
                item.out_filename_record_of_transfer = filename
                item.out_url_record_of_transfer = url_file
            item.taken_out()
            db.session.commit()
            flash(f'Item {item.name} has been taken out!')
            return redirect(url_for('main.input', items=item.name))
        elif request.method == 'GET':
            form.type.data = item.type
            form.capacity.data = item.capacity
            form.note.data = item.note
        return render_template('main/mda.html', title='Takeout MDA', form=form, item=item)

@bp.route('/detail/<items>/<int:id>')
@login_required
def detail_item(items, id):
    item = Item.query.filter_by(id=id).first()
    return render_template('main/detail.html', title='Detail', item=item)

@bp.route('/takeout', methods=['GET'])
@login_required
def takeout():
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(page, current_app.config['DISPLAY_PER_PAGE'], False)
    next_url = url_for('main.takeout', page=items.next_num) if items.has_next else None
    prev_url = url_for('main.takeout', page=items.prev_num) if items.has_prev else None
    return render_template('main/takeout.html', title='Takeout Item', items=items.items, \
        next_url=next_url, prev_url=prev_url)