# desc: turn on profile picture guard
# author: zvtyrdt.id

import os
import requests

def __zvm__(access_token, status, logging):
    """
    :> access_token: None
    :> status: true
    """

    if status not in ('true', 'false'):
        logging.warning('status "%s" is not allowed, use default', status)
        status = 'true'

    token = open(access_token).read().strip() if os.path.isfile(access_token) else access_token
    logging.info('make requests with access token: %s..', token[:32])

    headers = {'Authorization': 'OAuth ' + token}
    id = requests.get('https://graph.facebook.com/me?fields=id&access_token={}'.format(token)).json()
    if 'id' in id:
        id = id['id']
        data = {'variables': '{"0":{"is_shielded":%s,"session_id":"9b78191c-84fd-4ab6-b0aa-19b39f04a6bc","actor_id":"%s","client_mutation_id":"b0316dd6-3fd6-4beb-aed4-bb29c5dc64b0"}}' % (status, id),
                'method': 'post',
                'doc_id': '1477043292367183',
                'query_name': 'IsShieldedSetMutation',
                'strip_defaults': True,
                'strip_nulls': True,
                'locale': 'en_US',
                'client_country_code': 'US',
                'fb_api_req_friendly_name': 'IsShieldedSetMutation',
                'fb_api_caller_class': 'IsShieldedSetMutation'}
        logging.info('data: {is_shielded: %s, ID: %s}', status, id)

        r = requests.post("https://graph.facebook.com/graphql", data=data, headers=headers)
        logging.info('result: %s %s', r.status_code, r.reason)
    else:
        logging.error('invalid token !')
