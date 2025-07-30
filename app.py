from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Correct import

# Initialize Flask app
app = Flask(__name__)

# Set up the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the To-Do List model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.task}>'

# Home route to display To-Do List
@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['task']
    task_desc = request.form['desc']
    if task_content and task_desc:
        new_task = Todo(task=task_content, desc=task_desc)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))

# Route to mark a task as completed
@app.route('/complete/<int:id>')
def complete_task(id):
    task = Todo.query.get_or_404(id)
    Todo.completed = True
    db.session.commit()
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Initialize the database
with app.app_context():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=2000)
