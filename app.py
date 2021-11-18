from flask import Flask, request
# from werkzeug.wrappers import request
from flask_restful import Resource, Api
import logging
from flask import render_template
from models import db,Task



logging.basicConfig(filename='flask_server_logs.log',filemode='w',level=logging.DEBUG, format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')
print('Hello')
app = Flask(__name__)
app.config['SECRET_KEY'] = '0zx5c34as65d4654&%^#$#$@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<db_name>.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initiate the database
db.init_app(app)
# create table 
@app.before_first_request
def initiate_data_base_tables():
    db.create_all()
# configure the api before creating the class api 
api = Api(app)

class TaskRDU(Resource):
    def get(self, **kwargs):
        id = kwargs.get('id')
        task_list = []
        task = Task.query.get(id)
        
        data = {
               'id':  task.id,
               'name':task.name,
               'description': task.description,
               'completed': task.completed
            }
        task_list.append(data)
        return task_list


    def delete(self, **kwargs):
        id = kwargs.get('id')
        task_list = []
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return {'msg': 'task deleted'}

    def patch(self, **kwargs): # this method to update the task name only 
        id = kwargs.get('id')
        task = Task.query.get(id)
        task.name = request.form.get('name')
        print(task.name)
        db.session.commit()
        task_updated = []
        task = Task.query.get(id)
        data = {
               'id':  task.id,
               'name':task.name,
               'description': task.description,
               'completed': task.completed
            }
        task_updated.append(data)
        return task_updated
    def put(self, **kwargs):
        id = kwargs.get('id')
        task = Task.query.get(id)
        task.name = request.form.get('name')
        task.description = request.form.get('description')
        print(task.name)
        db.session.commit()
        task_updated = []
        task = Task.query.get(id)
        data = {
               'id':  task.id,
               'name':task.name,
               'description': task.description,
               'completed': task.completed
            }
        task_updated.append(data)
        return task_updated

class TaskLC(Resource):
    def get(self):
        task_list = []
        objs = Task.query.filter().all()
        for task in objs:
            data = {
               'id':  task.id,
               'name':task.name,
               'description': task.description,
            #    'created_at': task.created_at, Object of type datetime is not JSON serializable
               'completed': task.completed
            }
            task_list.append(data)
        return task_list
    def post(self):
        print(request.form.get('name'))
        data = {
               'id':  request.form.get('id'),
               'name':request.form.get('name'),
               'description': request.form.get('description'),
               'completed': False
            }
        task_obj = Task(**data)   
        db.session.add(task_obj)
        db.session.commit()
        return {'msg':'Task created'}


api.add_resource(TaskRDU, '/todo/<int:id>')
api.add_resource(TaskLC, '/todo')
app.run(debug=True)    