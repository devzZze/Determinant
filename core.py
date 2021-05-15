from flask import Flask
import json

app = Flask(__name__, template_folder='source/api/rest/templates')

config = json.load(open('config.json', 'r', encoding='UTF-8'))
vk_config = config['vk']


