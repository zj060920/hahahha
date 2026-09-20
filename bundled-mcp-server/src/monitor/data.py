import re,requests,pandas as pd
UA='Mozilla/5.0 (AI-Hardware-Monitor/1.0)'
def is_a(s): return bool(re.fullmatch(r'(sh|sz|bj)?\d{6}',str(s).strip().lower()))
def norm(s):
 s=re.sub(r'^(sh|sz|bj)','',str(s).strip().lower())
 return ('sh'+s) if s.startswith('6') else ('bj'+s if s.startswith(('8','4')) else 'sz'+s)
def quote_a(s):
 c=norm(s); r=requests.get(f'https://qt.gtimg.cn/q={c}',headers={'User-Agent':UA},timeout=8); r.raise_for_status(); p=r.text.split('~')
 if len(p)<10: raise RuntimeError('Unexpected Tencent quote response')
 price=float(p[3]); prev=float(p[4] or price)
 return {'symbol':s,'provider':'tencent','name':p[1],'price':price,'prev_close':prev,'change':price-prev,'change_pct':(price/prev-1)*100 if prev else None,'volume':float(p[6] or 0)}
def kline_a(s,interval='1m',limit=300):
 c=norm(s); period='day' if interval in ('1d','daily','D') else interval
 u=f'https://web.ifzq.gtimg.cn/appstock/app/kline/kline?_var=kline_{c}&param={c},{period},,{limit},qfq'; r=requests.get(u,headers={'User-Agent':UA},timeout=10); r.raise_for_status(); m=re.search(r'kline_[a-z0-9]+=(.*)',r.text)
 if not m: raise RuntimeError('Unexpected Tencent K-line response')
 import json
 d=json.loads(m.group(1).rstrip(';'))['data'][c]; key=period if period in d else next(iter(d)); df=pd.DataFrame(d[key]); df=df.iloc[:,:min(df.shape[1],9)]; df.columns=['datetime','open','close','high','low','volume','amount','x1','x2'][:df.shape[1]]
 for col in ['open','close','high','low','volume','amount']:
  if col in df: df[col]=pd.to_numeric(df[col],errors='coerce')
 df['datetime']=pd.to_datetime(df['datetime'],errors='coerce'); return df.dropna(subset=['close']).reset_index(drop=True)
def us_history(s,interval='5m',period='5d'):
 import yfinance as yf
 df=yf.download(s,period=period,interval=interval,auto_adjust=False,progress=False,threads=False)
 if df is None or df.empty: raise RuntimeError(f'No Yahoo Finance data for {s}')
 if hasattr(df.columns,'levels'): df.columns=df.columns.get_level_values(0)
 df=df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'}).reset_index()
 if 'Datetime' in df: df=df.rename(columns={'Datetime':'datetime'})
 if 'Date' in df: df=df.rename(columns={'Date':'datetime'})
 return df
def history(s,interval): return kline_a(s,interval) if is_a(s) else us_history(s,interval,'7d' if interval!='1d' else '2y')
def get_quote(s):
 if is_a(s): return quote_a(s)
 import yfinance as yf
 df=yf.download(s,period='2d',interval='1d',auto_adjust=False,progress=False,threads=False)
 if df is None or df.empty: raise RuntimeError(f'No Yahoo quote for {s}')
 if hasattr(df.columns,'levels'): df.columns=df.columns.get_level_values(0)
 a=df.iloc[-1]; b=df.iloc[-2]['Close'] if len(df)>1 else a['Close']
 return {'symbol':s.upper(),'provider':'yahoo_finance','price':float(a['Close']),'prev_close':float(b),'change':float(a['Close']-b),'change_pct':float((a['Close']/b-1)*100) if b else None,'volume':float(a.get('Volume',0))}
