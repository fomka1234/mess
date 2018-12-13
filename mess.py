import os

from flask import Flask, jsonify, url_for, render_template, redirect, request

import actions
from database import Message, db

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "msgdb.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file


@app.route("/api/msg/create/database", methods=["GET"])
def msg_create_db():
    db.create_all()
    return jsonify({ 'status': 'ok' })


add_actions = {
    'add_new': actions.add_new_message,
    'add_sub': actions.add_sub_message
}


@app.route("/ui/msgs", methods=["GET", "POST"])
@app.route("/ui/msgs/<int:msg_id>", methods=["GET", "POST"])
def ui_msgs(msg_id=None):
    action = request.values.get('action')
    msg_id = -1 if msg_id is None else msg_id
    parent_id = request.values.get('parent_id')

    visible_msg_ids = request.values.getlist('visible_msg_ids')

    if action is not None:
        new_id = (add_actions[action])(msg_id=parent_id).id
        visible_msg_ids.append(new_id)

    visible_msg_ids = None if len(visible_msg_ids) == 0 else visible_msg_ids
    msgs_dict = actions.get_messages_dict(visible_msg_ids)

    return render_template("home.html", msgs=msgs_dict, top_id=msg_id)


@app.route("/", methods=["GET", "POST"])
def ui_home():
    return redirect(url_for('ui_msgs'))


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, port=8080)