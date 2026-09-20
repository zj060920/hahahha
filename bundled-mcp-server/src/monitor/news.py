import urllib.parse,requests,xml.etree.ElementTree as ET
def search(q,limit=10):
 u='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':q,'hl':'zh-CN','gl':'CN','ceid':'CN:zh-Hans'}); r=requests.get(u,headers={'User-Agent':'Mozilla/5.0'},timeout=10); r.raise_for_status(); root=ET.fromstring(r.text); out=[]
 for i in root.findall('.//item')[:limit]:out.append({'title':i.findtext('title'),'link':i.findtext('link'),'published':i.findtext('pubDate'),'source':i.findtext('source')})
 return out
