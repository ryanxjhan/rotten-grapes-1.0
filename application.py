from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')


class Wines(db.Model):
    __tablename__ = 'wines'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    variety = db.Column(db.String(200))
    winery = db.Column(db.String(200))
    country = db.Column(db.String(100))
    province = db.Column(db.String(100))
    description = db.Column(db.String(2000))
    designation = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    price = db.Column(db.Integer)
    valid = db.Column(db.Boolean)

    def __repr__(self):
        return '<Wines {}>'.format(self.title)


# db.create_all()


@app.route('/')
def index():
    wine_list = Wines.query.limit(20)
    return render_template("index.html", wine_list=wine_list)


@app.route('/detail/<int:key>/')
def detail(key):
    entry = Wines.query.get(key)
    return render_template('detail.html', entry=entry)


@app.route("/results", methods=["POST"])
def results():
    query = request.form.get("query")
    wine_list = Wines.query.filter(Wines.title.contains(query)).limit(50)
    display = wine_list.count()
    return render_template("results.html", wine_list=wine_list, display=display, query=query)


@app.route("/admin")
@app.route("/admin/<int:page>/")
def admin(page=None):
    if page is None:
        page = 1
    wine_list = Wines.query.paginate(page, per_page=10)
    return render_template("admin/index.html", wine_list=wine_list)


@app.route("/admin/add")
def add():
    return render_template("admin/add.html")


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
