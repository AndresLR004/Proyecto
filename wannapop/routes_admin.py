from flask import Blueprint, render_template, flash, redirect, url_for
from .models import User, db
from .helper_role import Role, role_required
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
    return render_template('admin/users_list.html', users=users)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=['POST', 'GET'])
@role_required(Role.admin)
def block_user(user_id):
    user = User.query.get(user_id)

    if user:
        user.is_blocked = True
        db.session.commit()
        flash(f'Usuario {user.name} bloqueado correctamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'error')

    return redirect(url_for('admin_bp.admin_users'))

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['POST', 'GET'])
@role_required(Role.admin)
def unblock_user(user_id):
    user = User.query.get(user_id)

    if user:
        user.is_blocked = False
        db.session.commit()
        flash(f'Usuario {user.name} desbloqueado correctamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'error')

    return redirect(url_for('admin_bp.admin_users'))