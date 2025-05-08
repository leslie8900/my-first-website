from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///show_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Show model
class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Route to view all shows
@app.route("/shows")
def view_shows():
    shows = Show.query.all()
    return render_template("view_shows.html", shows=shows)

# Route to add a new show
@app.route("/add", methods=["GET", "POST"])
def add_show():
    if request.method == "POST":
        name = request.form.get("name")
        status = request.form.get("status")
        new_show = Show(name=name, status=status)
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for("view_shows"))
    return render_template("add_show.html")

# Route to edit an existing show
@app.route("/edit/<int:show_id>", methods=["GET", "POST"])
def edit_show(show_id):
    show = Show.query.get_or_404(show_id)
    if request.method == "POST":
        show.name = request.form.get("name")
        show.status = request.form.get("status")
        db.session.commit()
        return redirect(url_for("view_shows"))
    return render_template("edit_show.html", show=show)

# Route to delete a show
@app.route("/delete/<int:show_id>")
def delete_show(show_id):
    show = Show.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    return redirect(url_for("view_shows"))

# Main entry point
if __name__ == "__main__":
    # Create the database tables inside the application context
    with app.app_context():
        db.create_all()
    app.run(debug=True)