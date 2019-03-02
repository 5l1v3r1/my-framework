#!usr/bin/python
# desc: regex form parser

import re
import requests
import sys
from urllib.parse import urlparse as parse_url

class form_parser(object):
    def execute(self, url):
        self._response = requests.get(url)
        self.html = self._response.text
        self.base_url = '{0.scheme}://{0.netloc}/'.format(parse_url(self._response.url))

        self._def_head = {'name': '', 'method': 'GET', 'enctype': 'application/x-www-form-urlencoded', 'action': self.base_url}
        self._def_button = {'name': '<None>', 'value': '', 'type': 'button'}
        self._def_input = {'name': '<None>', 'value': '', 'type': 'text'}
        self._def_textarea = {'name': '<None>', 'value': '', 'type': 'textarea'}
        self._def_select = {'name': '<None>', 'value': [], 'type': 'select'}
        self._forms = []

        self.text = self._text()
        self._parser()

    def forms(self):
        for i in self._forms:
            yield i['data']

    def _parser(self):
        for num, i in enumerate(re.findall(r'(?si)<form.*?form>', self.html), start=1):
            form = {'body': [], 'data': {}}
            head = dict(re.findall(r'(?si)((?:name|method|action|enctype))=["\'](.*?)["\']', re.search(r'(?si)<form.*?>', i).group()))
            for c in self._def_head:
                if c not in head.keys():
                    head[c] = self._def_head[c]

            if head['action'][0] in ('.', '/'):
                head['action'] = self.base_url + '/'.join(head['action'].split('/')[1:])

            form['head'] = head

            radio_name = []
            for x in re.findall(r'(?si)<(?:input|textarea|select|button).*?(?:/\w*>|>)', i):
                type_ = re.findall(r'<(.*?) ', x)[0]
                s = dict(re.findall(r'((?:name|value|type))=["\'](.*?)["\']', x))

                if type_ == 'input':
                    for p in self._def_input:
                        if p not in s:
                            s[p] = self._def_input[p]

                    if s['type'] == 'email':
                       s['type'] = 'Text'

                    if s['type'] == 'radio':
                        if s['name'] not in radio_name:
                            s['value'] = []; radio_name.append(s['name'])

                            for ri in re.findall(r'(?si)<input.*?>', i):
                                if re.search(r'name=["\']{}["\']'.format(s['name']), ri):
                                    vl = re.findall(r'(?si)value=["\'](.*?)["\']', ri)[0]
                                    if re.search(r'(?si)checked', ri):
                                        vl = '*{}'.format(vl)
                                    s['value'].append(str(vl))
                        else: continue

                elif type_ == 'select':
                    for sb in self._def_select:
                        if sb not in s:
                            s[sb] = self._def_select[sb]

                    if s['name'] != '<None>':
                        for sv in re.findall(r'(?si)<select.*?select>', self.html):
                            if re.search(r'name=["\']{}["\']'.format(s['name']), sv):
                                select_control = [sv]
                    else:
                        cl_id = dict(re.findall(r'(?i)((?:class|id))=["\'](.*?)["\']', x))
                        for sl in cl_id:
                             select_control = re.findall(r'(?si)<select.*?{0}=["\']{1}["\'].*?/select>'.format(sl, cl_id[sl]), self.html)
                             if select_control:
                                 break

                    s['value'] = []
                    for j in select_control:
                        for o in re.findall('<option.*?/option>', j):
                            ref = dict(re.findall(r'(?si)(value)=["\'](.*?)["\']', o))
                            s['value'].append(str('*{}'.format(ref['value']) if re.search(r'selected', o) else ref['value']))

                elif type_ == 'textarea':
                    s['type'] = self._def_textarea['type']
                    for tx in self._def_textarea:
                        if tx not in s:
                            s[tx] = self._def_textarea[tx]

                    value = re.findall(r'(?s)>(.*?)<', x)
                    s['value'] = value[0] if value else ''

                elif type_ == 'button':
                    s['type'] = 'SubmitButton'
                    for db in self._def_button:
                        if db not in s:
                            s[db] = self._def_button[db]

                if not s['type'][0].isupper():
                    s['type'] = s['type'].capitalize()

                if re.search(r'disabled', x):
                    s['disabled'] = True

                form['body'].append(s)

            for sx in form['body']:
                value = sx['value']
                if type(sx['value']) is list:
                    value = None
                    for vs in sx['value']:
                        if '*' in vs:
                            value = vs[1:]
                if value and sx['name'] != '<None>':
                    form['data'][sx['name']] = value

            # update forms
            self._forms.append(form)

    def _text(self):
        for i in self._forms:
            f_text = '<'

            hd = ' '.join([i['head'][s] for s in ('name', 'method', 'action', 'enctype')])
            if hd.startswith(' '):
                hd = hd[1:]
            f_text += '{}\n'.format(hd)

            F = '  <{0}Control({1}={2}){3}>\n'
            for k in i['body']:
                input_data = ''
                if k['type'].lower() not in ('text', 'textarea', 'password', 'select', 'radio'):
                    input_data = ' (readonly)'
                    if 'disabled' in k.keys():
                        input_data = ' (disabled, readonly)'
                else:
                    if 'disabled' in k.keys():
                        input_data = ' (disabled)'

                value = k['value']
                if type(value) is list:
                    value = '[{}]'.format(', '.join(value))

                f_text += F.format(
                    k['type'],
                    k['name'],
                    value,
                    input_data,
                )

            yield f_text[:-1] + '>'

def __init__(url):
    f = form_parser()
    f.execute(url)
    for i in f.text:
        print(i)
