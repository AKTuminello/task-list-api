import os
import requests
from datetime import datetime
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from app.routes_helpers import validate_model

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
from app import db


SLACKBOT_TOKEN = os.environ.get("SLACKBOT_TOKEN")



@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not request_body:
        return make_response({"details": "Invalid data"}, 400)

    title = request_body.get("title")
    description = request_body.get("description")

    if not title or not description:
        return make_response({"details": "Invalid data"}, 400)

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

    return make_response(jsonify(response), 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    sort = request.args.get("sort")

    if sort == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = []

    for task in tasks:
        response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })

    return jsonify(response)




@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_model(Task, task_id)
    goal_id = task.goal_id if task.goal_id else None

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

    if goal_id:
        response["task"]["goal_id"] = goal_id

    return jsonify(response)



@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    if not request_body:
        return make_response({"details": "Invalid data"}, 400)

    title = request_body.get("title")
    description = request_body.get("description")

    if not title or not description:
        return make_response({"details": "Invalid data"}, 400)

    task.title = title
    task.description = description

    db.session.commit()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

    return make_response(jsonify(response), 200)



@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)

#FIRST TRY

# SLACKBOT_TOKEN = os.environ.get("SLACKBOT_TOKEN")

# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):
#     task = validate_model(Task, task_id)

#     if task.completed_at:
#         response = {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": True
#             }
#         }
#     else:
#         task.completed_at = datetime.now()
#         db.session.commit()
#         send_slack_notification(task.title)
#         response = {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": True
#             }
#         }

#     return jsonify(response)

# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = validate_model(Task, task_id)

#     if task.completed_at is None:
#         response = {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": False
#             }
#         }
#         return make_response(jsonify(response), 200)

#     task.completed_at = None
#     db.session.commit()

#     response = {
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": False
#         }
#     }

#     return make_response(jsonify(response), 200)

# def send_slack_notification(task_title):
#     url = "https://slack.com/api/chat.postMessage"
#     headers = {
#         "Authorization": "Bearer " + SLACKBOT_TOKEN
#     }
#     data = {
#         "channel": "api_test_channel",
#         "text": f"Someone just completed the task {task_title}"
#     }
#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
#     print(response.json())  # Print the response for debugging purposes
#     print(SLACKBOT_TOKEN)


# #Second try
# # @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):
#     task = validate_model(Task, task_id)

#     if task.completed_at:
#         response = {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": True
#             }
#         }
#     else:
#         task.completed_at = datetime.now()
#         db.session.commit()
#         send_slack_notification(task.title)
#         response = {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": True
#             }
#         }

#     return jsonify(response)


# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = validate_model(Task, task_id)

#     if task.completed_at is None:
#         response = {
#             "task": {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": False
#             }
#         }
#         return make_response(jsonify(response), 200)

#     task.completed_at = None
#     db.session.commit()

#     response = {
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": False
#         }
#     }

#     return make_response(jsonify(response), 200)


# def send_slack_notification(task_title):
#     url = "https://slack.com/api/chat.postMessage"
#     headers = {
#         "Authorization": "Bearer " + SLACKBOT_TOKEN
#     }
#     data = {
#         "channel": "api_test_channel",
#         "text": f"Someone just completed the task {task_title}"
#     }
#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
#     print(SLACKBOT_TOKEN)

# EMBED try--immediately after implementation, tests ran green

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at:
        response = {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True
            }
        }
    else:
        task.completed_at = datetime.now()
        db.session.commit()

        # Send Slack notification
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": "Bearer " + SLACKBOT_TOKEN
        }
        data = {
            "channel": "api_test_channel",
            "text": f"Someone just completed the task {task.title}"
        }
        response_slack = requests.post(url, headers=headers, json=data)
        response_slack.raise_for_status()

        response = {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True
            }
        }

    return jsonify(response)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is None:
        response = {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        }
        return make_response(jsonify(response), 200)

    task.completed_at = None
    db.session.commit()

    # Send Slack notification
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": "Bearer " + SLACKBOT_TOKEN
    }
    data = {
        "channel": "api_test_channel",
        "text": f"Someone just marked the task {task.title} as incomplete"
    }
    response_slack = requests.post(url, headers=headers, json=data)
    response_slack.raise_for_status()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

    return make_response(jsonify(response), 200)




#GOALS routes to begin here:


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response = []

    for goal in goals:
        response.append({
            "id": goal.goal_id,
            "title": goal.title
        })

    return jsonify(response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response = {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

    return jsonify(response)

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body:
        return make_response({"details": "Invalid data"}, 400)

    title = request_body.get("title")

    if not title:
        return make_response({"details": "Invalid data"}, 400)

    goal = Goal(title=title)
    db.session.add(goal)  # Add the goal object to the session
    db.session.commit()  # Commit the changes to assign a goal_id

    response = {
        "goal": {
            "id": goal.goal_id,  # Now goal.goal_id will have a value
            "title": goal.title
        }
    }

    return make_response(jsonify(response), 201)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if not request_body:
        return make_response({"details": "Invalid data"}, 400)

    title = request_body.get("title")
    description = request_body.get("description")

    if not title or not description:
        return make_response({"details": "Invalid data"}, 400)

    goal.title = title
    goal.description = description

    db.session.commit()

    response = {
        "goal": {
            "goal_id": goal.goal_id,
            "title": goal.title,
            "description": goal.description,
            "is_complete": False
        }
    }

    return make_response(jsonify(response), 200)




@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)

#relationships start here:@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def associate_tasks_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if not request_body:
        return make_response({"details": "Invalid data"}, 400)

    task_ids = request_body.get("task_ids")

    if not task_ids or not isinstance(task_ids, list):
        return make_response({"details": "Invalid data"}, 400)

    tasks = Task.query.filter(Task.task_id.in_(task_ids)).all()

    if len(tasks) != len(task_ids):
        return make_response({"details": "Invalid task IDs"}, 400)

    for task in tasks:
        task.goal_id = goal.goal_id

    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": task_ids
    }

    return make_response(jsonify(response), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks = Task.query.filter_by(goal_id=goal.goal_id).all()

    response = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }

    for task in tasks:
        response["tasks"].append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False  # Modify this based on your task model
        })

    return make_response(jsonify(response), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def associate_tasks_with_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response(jsonify({"error": "Goal not found"}), 404)

    request_body = request.get_json()

    if not request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)

    task_ids = request_body.get("task_ids")

    if not task_ids or not isinstance(task_ids, list):
        return make_response(jsonify({"details": "Invalid data"}), 400)

    tasks = Task.query.filter(Task.task_id.in_(task_ids)).all()

    if len(tasks) != len(task_ids):
        return make_response(jsonify({"details": "Invalid task IDs"}), 400)

    for task in tasks:
        task.goal_id = goal.goal_id

    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": task_ids
    }

    return make_response(jsonify(response), 200)
