from source.models import VkEvent
from source.api.vk.bot_api import BotAPI
from source.utils.utils import get_keyboard
import re
from core import config
import json
from threading import Thread


class MainHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.__instance = super(MainHandler, cls).__new__(cls)
        return cls.__instance

    def add_action(self, action: VkEvent):
        Thread(target=self.handler, args=(action,)).start()

    def handler(self, item: VkEvent) -> None:
        vk = BotAPI()
        u_vk = BotAPI(config['me']['token'])

        if item.payload or item.message:
            if item.payload == 'define' and not item.ext:
                vk.message_send('Введите url группы', item.user_id)
                return

            if not re.match(r'(http(s)?://)?vk\.com/.{3,}', item.message):
                vk.message_send('Неправильная ссылка.', item.user_id)
                return

            group_id = vk.get_group_id(item.message)

            if not group_id:
                vk.message_send('Неправильная ссылка.', item.user_id)
                return

            vk.message_send('Обработка...', item.user_id)

            storage = []

            for member in u_vk.get_members(group_id):
                temp = {
                    'user_id': member['id'],
                    'link': 'https://vk.com/id' + str(member['id']),
                    'first_name': member['first_name'],
                    'last_name': member['last_name']
                }

                if member.get('universities'):
                    if member['universities'][-1]['id'] != config['university']['id']:
                        temp['university'] = member['universities'][-1]['name']
                else:
                    temp['university'] = None

                if member.get('schools'):
                    temp['schools'] = ','.join(x['name'] for x in member['schools'])
                else:
                    temp['schools'] = None

                storage.append(temp)

            res_json = json.dumps({
                'count': len(storage),
                'items': storage
            }, ensure_ascii=False, sort_keys=True, indent=4)
            result = vk.load_doc(res_json, item.user_id)

            vk.message_send(attachment=result, user_id=item.user_id)
            return
        else:
            vk.message_send('Не надо так.', item.user_id, keyboard=get_keyboard('default'))
            return
