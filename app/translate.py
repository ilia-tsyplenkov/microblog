import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATION_KEY' not in current_app.config or not current_app.config['MS_TRANSLATION_KEY']:
        return _('Error: the translation is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATION_KEY'],
            'Ocp-Apim-Subscription-Region': 'eastus'}
    url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}".format(source_language, dest_language)
    r = requests.post(url, json=[{'Text': text}], headers=auth)
    if r.status_code != 200:
        return _('Error: the translation service is failed.')
    return json.loads(r.content.decode('utf-8-sig'))[0]['translations'][0]['text']
