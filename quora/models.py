from quora import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    """
    This user loader callback is used to reload the user from the user ID
    stored in the session. User ID must be an ID that uniquely identifies the
    user. It returns the corresponding user object.
    """
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """
    User class requires this UserMixin class so that User model inherits the
    properties such as is_authenticated, is_anonymous, is_active and method
    get_id()
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60))
    # back reference to answer table in the DB
    answers = db.relationship('Answer', backref='answer_by', lazy=True)
    # back reference to question table in the DB
    questions = db.relationship('Question', backref='question_by', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_asked = db.Column(
                    db.DateTime, nullable=False, default=datetime.utcnow
                    )
    # user id of user who asked this question
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # all answer objects which are mapped to this question instance
    answers = db.relationship('Answer', backref='question_info', lazy=True)

    def __repr__(self):
        return f"Question('{self.title}')"


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    # user id of user who is answering
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answer_text = db.Column(db.Text, nullable=False)
    date_answered = db.Column(
                        db.DateTime, nullable=False, default=datetime.utcnow
                        )
    # The id of question this answer belongs to
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return f"Answer('{self.answer_text}')"
