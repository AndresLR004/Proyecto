from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from .models import User, db, BlockedUser, Product, BanProduct
from .helper_role import Role, role_required
from .routes_products import products_bp
from .forms import FormUserBlock, FormProductsBan
from . import db_manager as db


# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = db.session.query(User).all()
    blocked_user = [blocked_user.user_id for blocked_user in BlockedUser.query.all()]
    return render_template('admin/users_list.html', users=users, blocked_user=blocked_user)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=['POST', 'GET'])
@role_required(Role.admin)
def block_user(user_id):
    user = User.query.get(user_id)
    form = FormUserBlock()
    if user:
        if request.method == 'POST' and form.validate_on_submit():
            blocked_user = BlockedUser.query.filter_by(user_id=user.id).first()

            if not blocked_user:
                blocked_user = BlockedUser(user_id=user.id, message=form.message.data)
                db.session.add(blocked_user)
                db.session.commit()

                if user.role != Role.admin:
                    user.can_create = False
                    db.session.commit()

                flash(f'El usuario {user.name} ha sido baneado con mensaje: {form.message.data}', 'success')
                return redirect(url_for('admin_bp.admin_users'))

            flash('Usuario actualmente bloqueado.', 'warning')
        
        return render_template('admin/block_user.html', form=form, user=user)

    flash('User not found.', 'danger')
    return redirect(url_for('admin_bp.admin_users'))



@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['GET', 'POST'])
@role_required(Role.admin)
def unblock_user(user_id):
    user = User.query.get(user_id)
    
    if user:
        blocked_user = BlockedUser.query.filter_by(user_id=user.id).first()
        
        if blocked_user:
            db.session.delete(blocked_user)
            db.session.commit()
            flash(f'El usuario {user.name} se ha desbloqueado.', 'success')
        else:
            flash(f'EL usuario {user.name} no esta bloqueado.', 'warning')
    else:
        flash('User not found.', 'danger')
    
    return redirect(url_for('admin_bp.admin_users'))

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=['POST', 'GET'])
@login_required
@role_required('admin')
def ban_product(product_id):
    product = Product.query.get(product_id)
    ban_form = FormProductsBan()

    if product:
        if request.method == 'POST' and ban_form.validate_on_submit():
            ban_product = BanProduct.query.filter_by(product_id=product.id).first()

            if not ban_product:
                ban_product = BanProduct(product_id=product.id, reason=ban_form.reason.data)
                db.session.add(ban_product)
                db.session.commit()

                flash(f'El producto {product.title} ha sido bloqueado con mensaje: {ban_form.reason.data}', 'success')
                return redirect(url_for('admin_bp.product_list'))

            flash('Producto actualmente bloqueado.', 'warning')
        return render_template('admin/ban_product.html', form=ban_form, product=product)

    flash('Producto no encontrado.', 'danger')
    return redirect(url_for('admin_bp.product_list'))


@admin_bp.route('/admin/products/<int:product_id>/unban', methods=['POST'])
@login_required
@role_required('moderator')
def unban_product(product_id):
    product = Product.query.get(product_id)

    if product:
        ban_product = BanProduct.query.filter_by(product_id=product.id).first()

        if ban_product:
            db.session.delete(ban_product)
            db.session.commit()
            flash(f'El producto {product.title} ha sido desbloqueado correctamente.', 'success')
        else:
            flash('El producto no estaba bloqueado.', 'warning')

    else:
        flash('Producto no encontrado.', 'danger')

    return redirect(url_for('admin_bp.product_list'))


@admin_bp.route('/admin/products/list')
def product_list():
    return redirect(url_for('products_bp.product_list'))

