from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quotes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

limiter = Limiter(key_func=get_remote_address, app=app, default_limits=["200/day", "50/hour"])

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

@app.route("/")
def home():
    from models import Quote
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    featured = quotes[0].text if quotes else "Add your first quote!"
    return render_template("index.html", featured=featured, quotes=quotes)

@app.route("/add", methods=["GET","POST"])
@login_required
def add_quote():
    from models import Quote
    if request.method == "POST":

        new_quote = (request.form.get("quote") or "").strip()

        if not new_quote:
            flash("Please enter a quote.", "error")
            return render_template("add.html")

        q = Quote(text=new_quote, user=current_user)
        db.session.add(q)
        db.session.commit()
        flash("Quote added!", "success")
        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/register", methods=["GET","POST"])
def register():
    from models import User
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()
        if not username or not password:
            flash("Username and password required.", "error")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return render_template("register.html")
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    from models import User
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash("Invalid credentials.", "error")
            return render_template("login.html")
        login_user(user)
        next_url = request.args.get("next")
        return redirect(next_url or url_for("home"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("home"))

@app.route("/api/quotes")
def api_quotes():
    from models import Quote
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return jsonify([
        {
            "id": q.id,
            "text": q.text,
            "user": q.user.username if q.user else None,
            "created_at": q.created_at.isoformat()
        }
        for q in quotes
    ])

if __name__ == "__main__":
    app.run(debug=True)
