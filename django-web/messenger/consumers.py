from channels.auth import channel_session_user
from channels import Channel
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import json
import datetime
from .models import Message

@channel_session_user
def send_msg(message):

    # decode message
    msg_data = json.loads(message.content['text'])

    recipient_id = msg_data['uid']
    try:
        recipient = User.objects.get(user_id=recipient_id)
    except ObjectDoesNotExist:
        error_txt = "Invalid recipient ID."
    sender = message.user
    msg_content = msg_data['content'] #should this be processed somehow?
    time_sent = datetime.datetime.now()

    #
    # first we want to store the message in the database, so it doesn't get lost
    #

    # construct new Message instance
    new_message = Message(content=msg_content,
                          time_sent=time_sent,
                          sender=sender,
                          recipient=recipient
                         )
    new_message.save()

    #
    # now we send the message to the recipient
    #
    reciever_channel = Channel("/messenger/%s" % recipient_id)
    reciever_channel.send(new_message.asdict())



    #
    # now we send a status report to the user
    #
    status_report = "success"

    if error_txt:
        status_report = error_txt
    message.reply_channel.send(status_report)
