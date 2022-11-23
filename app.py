from datetime import datetime

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Local
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:elvis99@localhost/articles"

# Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://rlnnkkeopqspqy:0760abfaa00662978b8634c017cf87a90b188de71ad79a8f0dad2e90349af166@ec2-35-170-21-76.compute-1.amazonaws.com:5432/d16il1nq6hbkl1"

db = SQLAlchemy(app)
ma = Marshmallow(app)

app.app_context().push()


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, description):
        self.title = title
        self.description = description


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route("/get", methods=['GET'])
def get_all_articles():
    all_articles = Articles.query.all()
    print(all_articles)
    results = articles_schema.dump(all_articles)
    return jsonify(results), 200


@app.route("/get/<id>/", methods=['GET'])
def get_article(id):
    target_article = Articles.query.get(id)
    if target_article:
        return article_schema.jsonify(target_article), 200
    return abort(404)


@app.route("/add", methods=['POST'])
def add_articles():
    title = request.json['title']
    description = request.json['description']

    article = Articles(title, description)

    if article.title is title:
        return print("Title already exists"), 409
    db.session.add(article)
    db.session.commit()
    return article_schema.jsonify(article), 201


@app.route("/update/<id>/", methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)
    title = request.json['title']
    description = request.json['description']

    article.title = title
    article.description = description

    db.session.commit()
    return article_schema.jsonify(article), 204


@app.route("/delete/<id>/", methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)

    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article), 204


if __name__ == '__main__':
    app.run(debug=True)
