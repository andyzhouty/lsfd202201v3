from app import db

class Article(db.Model):
    __tablename__ = 'articles'
    title = db.Column(db.String(64), primary_key=True, index=True)
    author = db.Column(db.String(64), primary_key=True)
    time = db.Column(db.String(64), primary_key=True)
    content = db.Column(db.Text(2048), primary_key=True)

    def __repr__(self):
        return '<Article %r>' % self.title

    def query_one(self, id=1):
        return {'title': self.query.all()[id-1].title,
                'author': self.query.all()[id-1].author,
                'time': self.query.all()[id-1].time,
                'content': self.query.all()[id-1].content}

    def query_all(self):
        return self.query.all()
