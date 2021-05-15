from random import randint
import vk_api
from typing import List

from core import vk_config
import requests
from uuid import uuid4
from os import remove


class BotAPI:
    def __init__(self, token=None):
        self.token = token or vk_config['token']
        self.vk = vk_api.VkApi(token=self.token)

    def message_send(self, message=None, user_id=None, keyboard=None, attachment=None) -> None:
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'random_id': randint(0, 9999999),
                        'keyboard': keyboard,
                        'message': message,
                        'attachment': attachment})

    def get_users(self, ids: List[int]) -> dict:
        return self.vk.method('users.get', {
            'user_ids': ','.join([str(x) for x in ids])
        })

    def get_members(self, group_id):
        offset = 0
        while True:
            data = self.vk.method('groups.getMembers', {
                'group_id': group_id,
                'offset': offset,
                'fields': 'universities,schools,city',
                'count': 1000
            })

            if not data['items']:
                break

            sns = self.get_users([x['id'] for x in data['items']])

            for i, sn in enumerate(sns):
                data['items'][i].update(sn)

            for member in data['items']:
                yield member

            offset += 1000

    def get_group_id(self, url: str) -> int:
        data = self.vk.method('groups.getById', {'group_id': url.replace('https://vk.com/', '').replace('vk.com/', '')})
        return data[0]['id'] if data and data[0]['is_closed'] == 0 else None

    def __get_doc_upload_server(self, user_id):
        return self.vk.method('docs.getMessagesUploadServer', {'type': 'doc', 'peer_id': user_id})

    def load_doc(self, document, user_id: int) -> str:
        server = self.__get_doc_upload_server(user_id)
        filename = uuid4().hex + '.json'

        open(filename, 'w', encoding='UTF-8').write(document)

        result = requests.post(server['upload_url'], files={'file': open(filename, 'rb')}).json()
        remove(filename)

        result = self.vk.method('docs.save', {'file': result['file'], 'title': f'result_{user_id}.json'})

        return '{type}{owner_id}_{media_id}'.format(
            type=result['type'],
            owner_id=result['doc']['owner_id'],
            media_id=result['doc']['id']
        )
