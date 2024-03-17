from datetime import datetime

from flask_login import UserMixin

import markdown

from werkzeug.security import check_password_hash, generate_password_hash

from app import mongo, login
from app.helpers import pretty_date

user_vote = mongo.mongo.db.Table(
    "user_vote",
    mongo.db.Column("user.id", mongo.db.Integer, mongo.db.ForeignKey("user.id"), primary_key=True),
    mongo.db.Column("post.id", mongo.db.Integer, mongo.db.ForeignKey("post.id"), primary_key=True),
)

comment_vote = mongo.db.Table(
    "comment_vote",
    mongo.db.Column("user.id", mongo.db.Integer, mongo.db.ForeignKey("user.id"), primary_key=True),
    mongo.db.Column("comment.id", mongo.db.Integer, mongo.db.ForeignKey("comment.id"), primary_key=True),
)


class User(UserMixin, mongo.db.Model):
    id = mongo.db.Column(mongo.db.Integer, primary_key=True)
    username = mongo.db.Column(mongo.db.String(64), index=True, unique=True)
    email = mongo.db.Column(mongo.db.String(120), index=True, unique=True)
    password_hash = mongo.db.Column(mongo.db.String(128))
    posts = mongo.db.relationship(
        "Post", order_by="desc(Post.timestamp)", backref="author", lazy="dynamic"
    )
    last_seen = mongo.db.Column(mongo.db.DateTime, default=datetime.utcnow)
    post_votes = mongo.db.relationship(
        "Post", secondary=user_vote, back_populates="user_votes"
    )
    comments = mongo.db.relationship(
        "Comment",
        order_by="desc(Comment.timestamp)",
        backref="author",
        lazy="dynamic"
    )
    comment_votes = mongo.db.relationship(
        "Comment", secondary=comment_vote, back_populates="user_votes"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id {self.id} - {self.username}>"


class Post(mongo.db.Model):
    id = mongo.db.Column(mongo.db.Integer, primary_key=True)
    title = mongo.db.Column(mongo.db.String(256))
    body = mongo.db.Column(mongo.db.Text)
    link = mongo.db.Column(mongo.db.Boolean, default=False)
    url = mongo.db.Column(mongo.db.String(256))
    timestamp = mongo.db.Column(mongo.db.DateTime, index=True, default=datetime.utcnow)
    user_id = mongo.db.Column(mongo.db.Integer, mongo.db.ForeignKey("user.id"))
    category_id = mongo.db.Column(mongo.db.Integer, mongo.db.ForeignKey("category.id"))
    vote_count = mongo.db.Column(mongo.db.Integer, default=0)
    user_votes = mongo.db.relationship(
        "User", secondary=user_vote, back_populates="post_votes"
    )
    comments = mongo.db.relationship(
        "Comment", order_by="desc(Comment.timestamp)", back_populates="post"
    )

    def __repr__(self):
        return f"<Post id {self.id} - {self.title}>"

    @classmethod
    def recent_posts(cls):
        return cls.query.order_by(Post.timestamp.desc())

    def body_as_html(self):
        if not self.body:
            return None
        return markdown.markdown(self.body)

    def pretty_timestamp(self):
        return pretty_date(self.timestamp)

    def already_voted(self, user):
        return user in self.user_votes

    def adjust_vote(self, amount):
        if self.vote_count is None:
            self.vote_count = 0
        self.vote_count += amount
        mongo.db.session.add(self)

    def up_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(1)
        mongo.db.session.commit()

    def down_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(-1)
        mongo.db.session.commit()

    def add_comment(self, comment, user):
        comment = Comment(body=comment,
                          user_id=user.id)
        self.comments.append(comment)
        mongo.db.session.commit()
        comment.up_vote(user)
        return comment

    def comment_count(self):
        return len(self.comments)


class Category(UserMixin, mongo.db.Model):
    id = mongo.db.Column(mongo.db.Integer, primary_key=True)
    title = mongo.db.Column(mongo.db.String(64), index=True, unique=True)
    posts = mongo.db.relationship(
        "Post", order_by="desc(Post.timestamp)", backref="category", lazy="dynamic"
    )


class Comment(mongo.db.Model):
    id = mongo.db.Column(mongo.db.Integer, primary_key=True)
    body = mongo.db.Column(mongo.db.Text)
    timestamp = mongo.db.Column(mongo.db.DateTime, index=True, default=datetime.utcnow)
    user_id = mongo.db.Column(mongo.db.Integer, mongo.db.ForeignKey("user.id"))
    post_id = mongo.db.Column(mongo.db.Integer, mongo.db.ForeignKey("post.id"))
    post = mongo.db.relationship("Post", back_populates="comments")
    vote_count = mongo.db.Column(mongo.db.Integer, default=0)
    user_votes = mongo.db.relationship(
        "User", secondary=comment_vote, back_populates="comment_votes"
    )

    def __repr__(self):
        return f"<Comment id {self.id} - {self.body[:20]}>"

    def pretty_timestamp(self):
        return pretty_date(self.timestamp)

    def already_voted(self, user):
        return user in self.user_votes

    def adjust_vote(self, amount):
        if self.vote_count is None:
            self.vote_count = 0
        self.vote_count += amount
        mongo.db.session.add(self)

    def up_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(1)
        mongo.db.session.commit()

    def down_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(-1)
        mongo.db.session.commit()


class ActivityLog(mongo.db.Model):
    id = mongo.db.Column(mongo.db.Integer, primary_key=True)
    timestamp = mongo.db.Column(mongo.db.DateTime, index=True, default=datetime.utcnow)
    user_id = mongo.db.Column(mongo.db.Integer, mongo.db.ForeignKey("user.id"))
    details = mongo.db.Column(mongo.db.Text)

    def __repr__(self):
        return f"<ActivityLog id {self.id} - {self.details[:20]}>"

    @classmethod
    def latest_entry(cls):
        return cls.query.order_by(ActivityLog.id.desc()).first()

    @classmethod
    def log_event(cls, user_id, details):
        e = cls(user_id=user_id, details=details)
        mongo.db.session.add(e)
        mongo.db.session.commit()


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
