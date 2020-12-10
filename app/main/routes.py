from flask_login import login_required
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from app.main.forms import GroupIdsForm
from app.main import bp
from app.main.utils import build_it

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = GroupIdsForm()
    if form.validate_on_submit():
        result_html = build_it(form.data)
        return render_template('index.html', \
            group_ids_form=form, \
            result_html=result_html['plane_links_html'], \
            wrapped_html = result_html['wrapped_html'])

    return render_template('index.html', group_ids_form=form)
