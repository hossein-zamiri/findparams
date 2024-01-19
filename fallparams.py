import bs4 as bs
import urllib.request
import re
from urllib.parse import urlparse
from urllib.parse import parse_qs
listparams = []
url = input("enter your target: ")
headers = {
    'User-Agent': 'Mozilla/5.0',  # Example user-agent header
    }
req = urllib.request.Request(f"{url}", headers=headers)
def input_param():
    source = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(source,'lxml')
    inputs = soup.findAll('input')
    regex_input_id = r'id="([^"]*)"'
    regex_input_name = r'name="([^"]*)"'
    for i in inputs:  
        try:
            regex_match = re.search(regex_input_id,str(i),re.DOTALL)
            id = regex_match.group(1)
            listparams.append(id)
        except:
            continue
    for j in inputs:
        try:
            regex_match = re.search(regex_input_name,str(j),re.DOTALL)
            name = regex_match.group(1)
            listparams.append(name)
        except:
             continue
def href_param():
    source = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(source,'lxml')
    regex_href = r'href="([^"]*)"'
    hrefs = soup.findAll(href=True)
    tmp = []
    tmp2 = []
    for i in hrefs:
        try:
            regex_match = re.search(regex_href,str(i))
            urls = (regex_match.group(1))
            tmp.append(urls)
        except:
            continue
    for urlss in tmp:    
        try:
            parsed_url = urlparse(urlss)
            captured_value = parse_qs(parsed_url.query,keep_blank_values=True)
            keys = list(captured_value.keys())
            tmp2.append(keys)
        except:
            continue
    for k in tmp2:
        try:
            for kk in k:
                if "amp;" in kk:
                    listparams.append(kk.strip("amp;"))
                else:
                    listparams.append(kk)
        except: 
            continue
def js_varibale():
    source = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(source,'lxml')
    regex_href = r'(var|let|const)\s+(\w+)'
    hrefs = soup.findAll('script')

    t = re.findall(regex_href,str(soup))
    for i in t:
        listparams.append(i[1])

def json_params():
    source = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(source,'lxml')
    regex_href = r"\{.*\}"
    hrefs = soup.findAll('script')

    t = re.findall(regex_href,str(hrefs),re.DOTALL)
    for i in t:
        
        p = re.findall(r'(["\']?)([\w-]+)\1\s*?:',i,re.DOTALL)
        for j in p:
            for x in j:
                listparams.append(x)
json_params()
href_param()
input_param()
js_varibale()
res = [*set(listparams)]
for i in res:
    print(i.replace('"',''))
