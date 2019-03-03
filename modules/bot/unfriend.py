# desc: unfriend all friends at once

import os
import requests

def __init__(access_token, logging):
    token = open(access_token).read().strip() if os.path.isfile(access_token) else access_token
    logging.info('make requests with access token: %s..', token[:32])

    r = requests.get('https://graph.facebook.com/me/friends?fields=id,name&limit=5000&access_token={}'.format(token)).json()
    if 'error' in r.keys():
        logging.error('error: %s', r['error']['message'])
    else:
        logging.info('take %s friend IDs from your account', len(r['data']))

        for i in r['data']:
            logging.info('delete friend: %s', str(i))
            requests.post('https://graph.facebook.com/me/friends?uid={0}&method=delete&access_token={1}'.format(i['id'], token))
