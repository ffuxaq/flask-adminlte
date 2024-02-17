from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
from apps import db
from apps.stats_report import bp
from flask_babel import _
# from app.auth.forms import LoginForm, RegistrationForm, \
#     ResetPasswordRequestForm, ResetPasswordForm
from apps.authentication.models import Users as User
# from apps.auth.email import send_password_reset_email
from werkzeug.security import generate_password_hash, check_password_hash
from apps.stats_report.forms import ReportForm


@bp.route('/stats_report', methods=['GET', 'POST'])
def stats_report_do():
    if (current_user.is_authenticated == False):
        return redirect(url_for('main.index'))
    form = ReportForm()
    if form.validate_on_submit():
        pass
        # next_page = request.args.get('next')
        # if not next_page or urlsplit(next_page).netloc != '':
        #     next_page = url_for('main.index')
        # return redirect(next_page)
    return render_template('auth/cdc_report.html', title=_('Sign In'), form=form)