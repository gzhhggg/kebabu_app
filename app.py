import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
import datetime
import json
from flask_sqlalchemy import SQLAlchemy
import pytz
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_num = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.String(200), nullable=False)

def get_last_id(data):
    old_id = 0
    for d in data:
        new_id = d.id
        if old_id < new_id:
            old_id = new_id
            last_id = d.id
            last_score = d.score_num
            last_price = d.price
            last_created = d.created_at
    return(last_id,last_score,last_price,last_created)

@app.route('/', methods=['GET', 'POST'])
def get_score():
    if request.method == 'POST':
        score_num = json.loads(request.data.decode('utf-8')).get('score')
        if score_num == "10":
            price = "0"
        else:
            price = int(score_num) * 470
        # BlogArticleのインスタンスを作成
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        created_at = now.strftime('%Y/%m/%d %H:%M:%S')
        blogarticle = BlogArticle(score_num=score_num, price=price ,created_at = created_at)
        db.session.add(blogarticle)
        db.session.commit()
        data = BlogArticle.query.order_by(desc(BlogArticle.id)).all()
        return render_template("index.html",data=data)
    else:
        data = BlogArticle.query.order_by(desc(BlogArticle.id)).all()
        last_id ,last_score ,last_price ,last_created = get_last_id(data)
        return render_template("index.html",data=data,last_score=last_score,last_price=last_price,last_created=last_created)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)