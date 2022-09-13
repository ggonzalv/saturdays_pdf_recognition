from flask import request, jsonify, Blueprint
from datetime import datetime

from database import tasks

tasks_bp = Blueprint('routes-tasks', __name__)


@tasks_bp.route('/tasks', methods=['POST']) #http://127.0.0.1:5000/tasks
def add_task():
    title = request.json('title')
    created_date = datetime.now().strftime("%x")

    data = (title, created_date)
    tasks_id = tasks.insert_task(data)

    if tasks_id:
        return jsonify({'message': 'Task Created'})
    return jsonify({'message': 'Internal Error'})

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    data = get_tasks.select_all_tasks()

    if data:
        return jsonify({'tasks': data})
    elif data == False:
        return jsonify({'message': 'Internal Error'})
    else:
        return jsonify({'tasks': {}})

@tasks_bp.route('/tasks', methods=['PUT'])
def update_task():
    title = request.json['title']
    id_arg = request.args.get('id')

    if tasks.update_task(id_arg, (title,)):
        task = tasks,tasks.select_task_by_id(id_arg)
        return jsonify(task)
    return jsonify({'message': 'Internal Error'})

@tasks_bp.route('/tasks', methods=['DELETE'])
def delete_task():
    id_arg = request.arg.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({'message': 'Task Deleted'})
    return jsonify({'message': 'Internal Error'})

@tasks_bp.route('/tasks/completed', methods=['PUT'])
def completed_task():
    id_arg = request.args.get('id')
    completed = request.args.get('completed')

    if tasks.completed_task(id_arg, completed):
        return jsonify({'message': 'Succesfully'})
    return jsonify({'message': 'Internal Error'})