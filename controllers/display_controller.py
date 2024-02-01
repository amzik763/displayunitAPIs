from app import app
# from user_model.user_model import user_model
from model.display_model import display_unit_model
from flask import Flask,request
# obj1=user_model()
obj2=display_unit_model()

# @app.route("/user/getall")
# def user_signup_controller():
#     return obj1.user_getall_model()

# @app.route("/user/addone",methods=["POST"])
# def user_addone_controller():
#     # print(request.form)
#     return obj1.user_addone_model(request.form)


@app.route("/stationadd",methods=["POST"])
def Station_controller():
    return obj2.Station_model(request.json)

@app.route("/getprocess",methods=["POST"])
def process_controller():
    return obj2.get_process(request.form)

@app.route("/getlogin_process",methods=["POST"])
def login_process_controller():
    return obj2.get_process_and_login_data(request.form)

@app.route("/task_assigned",methods=["POST"])
def task_assigned_controller():
    return obj2.task_assigned_model(request.json)

# @app.route("/get/task_assigned",methods=["POST"])
# def get_task_assigend_model():
#     return obj2.get_task_assigend_model()

@app.route("/get/assigend_parts",methods=["POST"])
def get_assigned_parts_controller():
    return obj2.get_asssigned_parts_model()

@app.route("/get/task_assigned",methods=["POST"])
def get_task_assigend_model():
    return obj2.get_task_assigend_model(request.form)

@app.route("/update/assigned_parts_stations",methods=["POST"])
def update_assigned_parts_controller():
    return obj2.update_assigned_parts_model(request.form)

@app.route("/get/task",methods=["POST"])
def get_task_controller():
    return obj2.get_task_model()