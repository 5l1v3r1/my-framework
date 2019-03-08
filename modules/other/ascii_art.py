# desc: random ascii art generator
# author: zvtyrdt.id

import re, requests

def __zvm__(total):
    """
    :> total: 1
    """
    for i in range(int(total)):
        content = requests.get('http://www.asciiartfarts.com/random.cgi').read()
        print ('#{0:^20}\n\x1b[36m{1}\x1b[0m'.format(
            ': '.join(re.findall(r'<h1>#<a href=".*?">(.*?)</a>: (.*?)</h1>', content)[0]),
            re.sub(r'&.*?;', '', re.findall(r"pre>(.*?)</pre>", content, re.S)[1])))
