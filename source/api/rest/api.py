from flask import render_template, request
from core import app, vk_config
from source.models import VkEvent
import json
from source.handler.main_handler import MainHandler


@app.route('/define', methods=['GET'])
def get_access():
    return render_template('index.html')


@app.route('/define', methods=['POST'])
def processing():
    try:
        data = json.loads(request.data)
        if 'type' not in data.keys():
            return 'not vk'
        if data['type'] == 'confirmation':
            return vk_config['confirmation']
        elif data['type'] == 'message_new':
            if data.get('secret') == vk_config['secret_key']:
                event = VkEvent(type=data['type'],
                                message=data['object'].get('message', {}).get('text', None),
                                attachment=data['object'].get('message', {}).get('attachments', None),
                                user_id=data['object'].get('message', {}).get('from_id', None),
                                payload=json.loads(data['object']['message'].get('payload', '{}')).get('button', None))

                MainHandler().add_action(event)
                return 'ok'
            else:
                return 'Invalid k3y, my fr1end.'
    except Exception as e:
        return 'Invalid request'
