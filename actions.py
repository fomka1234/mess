
from flask import request

from database import Message, db


def add_sub_message(msg_id=None):
    msg = Message(text=request.values.get('msg_text'), parent_id=msg_id)
    db.session.add(msg)
    db.session.commit()
    return msg

def add_new_message(msg_id=None):
    return add_sub_message(msg_id=None)


def get_unique_messages(msg_ids=None):
    msg_ids = [None] if msg_ids is None else msg_ids

    unique_msgs = set()
    unique_msg_ids = set()

    for msg_id in msg_ids:
        if msg_id is None and len(unique_msgs) == 0:
            root_msgs = Message.query \
                               .filter_by(parent_id=None) \
                               .order_by(Message.id) \
                               .all()
            unique_msgs.update(root_msgs)
        else:
            unique_msg_ids.add(msg_id)

    msgs = Message.query.all()  

    unique_msgs.update(msgs)

    return unique_msgs

def get_messages_dict(msg_ids=None):
    unique_msgs = get_unique_messages(msg_ids)

    msg_dict = dict()
    for umsg in unique_msgs:
        parent_id = -1 if umsg.parent_id is None else umsg.parent_id
        if parent_id not in msg_dict:
            msg_dict[parent_id] = list()
        msg_dict[parent_id].append(umsg)

    return msg_dict