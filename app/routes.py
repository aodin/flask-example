from urllib.parse import urljoin, urlparse

from flask import current_app, flash
from flask import Blueprint, jsonify, render_template, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .files import Example
from .forms import LoginForm
from .users.models import normalize_email, User


main = Blueprint("main", __name__, cli_group=None)


def is_local_url(host: str, target: str) -> bool:
    ref_url = urlparse(host)
    test_url = urlparse(urljoin(host, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@main.route("/")
def index():
    """Index route with jinja context and filter examples."""
    context = {
        "number": 1200.34000,
    }
    return render_template("index.html", **context)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = normalize_email(form.email.data)

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(form.password.data):
            flash(f"Invalid email, password, or token", category="danger")
            return redirect(url_for("main.login"))

        login_user(user)
        flash("Logged in successfully.", category="info")
        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@main.route("/example.json", methods=["GET"])
def get_file():
    example = Example.load(current_app.config["S3_BUCKET"])
    return jsonify(example.mapping)


@main.route("/example.json", methods=["POST"])
def update_file():
    example = Example.load(current_app.config["S3_BUCKET"])
    example.update()
    example.save(current_app.config["S3_BUCKET"])
    return redirect(url_for("main.get_file"))
