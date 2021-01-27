from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from quora import app, db, bcrypt
from quora.forms import LoginForm, RegistrationForm, AskQuestion, AnswerForm
from quora.forms import UpdateAccountForm
from quora.models import User, Question, Answer


@app.route('/')
@app.route('/home')
def home():
    # all the rows in question table ordered in desceneding manner of date.
    questions = Question.query.order_by(Question.date_asked.desc()).all()

    # all the rows in answer table ordered in descending manner of date
    # answered.
    answers = Answer.query.order_by(Answer.date_answered.desc()).all()

    # Any questions that are Unanswered in the database will be listed
    un_answered = [
        question for question in questions if question.answers == []
        ]

    # creating the dictionary for mapping all answeres for each question
    # each question object will be a key and all corresponding answer objects
    # will be stored in list which is a value to that key.
    answers_dict = {}

    for answer in answers:
        answers_dict.setdefault(answer.question_info, [])
        answers_dict[answer.question_info] += [answer]

    return render_template(
                        'home.html',
                        title='home',
                        un_answered=un_answered,
                        answers=answers_dict
                        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
            # remebers the user session with remember variable setting to true
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            # if a user tries to access a page that requres login, that page
            # info will be stored in url in variable 'next', with request
            # module we can redirect when login is successful
            next_page = request.args.get('next')
            return redirect(next_page) if next_page \
                else redirect(url_for('home'))

        else:
            flash('Login Failed! Please Check Email & Password!', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        # bcrypt instance of Bcrypt class will be user to
        # generate and validate hashed passwords
        hashed_pwd = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pwd
            )
        db.session.add(user)
        db.session.commit()
        flash(
            f'Registration Successful for User {form.username.data}',
            'success'
            )

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/account')
@login_required
def account():
    answers = Answer.query.filter_by(answer_by=current_user)\
            .order_by(Answer.date_answered.desc()).all()

    questions = Question.query.filter_by(question_by=current_user)\
        .order_by(Question.date_asked.desc()).all()

    return render_template(
                            'account.html',
                            title='Account',
                            answers=answers, questions=questions
                            )


@app.route('/account/update', methods=['GET', 'POST'])
@login_required
def update_account():
    # sending current user name, email as arguments to the class
    # UpdateAccountForm
    form = UpdateAccountForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # populating existing particulars on update form
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template(
                            'update_account.html',
                            title='Update Account',
                            form=form
                            )


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    form = AskQuestion()
    if form.validate_on_submit():

        if current_user.is_authenticated:
            question = Question(
                        title=form.question.data, question_by=current_user
                        )
            db.session.add(question)
            db.session.commit()
            flash('You just asked a Question!', 'success')
            return redirect(url_for('home'))
        else:
            # if the guest user asks a quetion
            question = Question(title=form.question.data)
            db.session.add(question)
            db.session.commit()
            flash('You just asked a Question!')
            return redirect(url_for('home'))

    return render_template('ask.html', title='Question', form=form)


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    question = Question.query.get_or_404(question_id)

    if current_user.is_authenticated:
        answered_id = None
        for answer in question.answers:
            if answer.answer_by.id == current_user.id:
                answered_id = answer.id
        if answered_id is not None:
            # for rendering update and delete options for the login user who
            # answered the question
            return render_template(
                                'question.html',
                                question=question,
                                title='Question', answer_id=answered_id)
        else:
            return render_template(
                        'question.html', question=question, title='Question'
                        )
    return render_template(
                        'question.html', question=question, title='Question'
                        )


@app.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        answer = Answer(
                    answer_by=current_user,
                    answer_text=form.content.data,
                    question_info=question
                    )
        db.session.add(answer)
        db.session.commit()
        flash('You Just Answered the Question Successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('answer.html', form=form, question=question)


@app.route('/answer/<int:answer_id>/update', methods=['GET', 'POST'])
@login_required
def update_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question = answer.question_info

    # to deny permission for user who tries to manually configure URL and
    # tries to update other users' answer
    if answer.answer_by != current_user:
        abort(403)

    form = AnswerForm()
    if form.validate_on_submit():
        answer.answer_text = form.content.data
        db.session.commit()
        flash('Your answer has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.content.data = answer.answer_text

    return render_template('answer.html', form=form, question=question)


@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
@login_required
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if answer.answer_by != current_user:
        abort(403)
    db.session.delete(answer)
    db.session.commit()
    flash('Your answer has been deleted!', 'warning')
    return redirect(url_for('home'))
