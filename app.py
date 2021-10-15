from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


def get_time_now():
    current_time = datetime.utcnow()
    day = current_time.day
    month = current_time.month
    year = current_time.year
    return f"{day}/{month}/{year}"


class TodoDataBaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String, default='In progress')
    date_created = db.Column(db.String, default=get_time_now())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    show_alert = False
    if request.method == 'POST':
        task_content = request.form['content']

        if len(task_content.strip()) == 0:
            show_alert = True

            tasks = TodoDataBaseModel.query.order_by(TodoDataBaseModel.id).all()
            return render_template("index.html", alert=show_alert, tasks=tasks)

        else:
            new_task = TodoDataBaseModel(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'An error occurred :('

    else:
        tasks = TodoDataBaseModel.query.order_by(TodoDataBaseModel.id).all()
        return render_template("index.html", alert=show_alert, tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TodoDataBaseModel.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'An error occurred :('


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task_to_update = TodoDataBaseModel.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred, when updating the task :('

    else:
        return render_template('update.html', task=task_to_update)


if __name__ == '__main__':
    app.run(debug=True)

# TODO: Make a warning when you enter a task, which is already in the task list
# TODO: Make a cancel button on the update.html page
# TODO: Change Update to Edit