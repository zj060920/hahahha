import pandas as pd,numpy as np
def add_indicators(df):
 x=df.copy(); c=pd.to_numeric(x['close'],errors='coerce'); v=pd.to_numeric(x.get('volume',0),errors='coerce').fillna(0)
 for n in (5,10,20,60): x[f'ma{n}']=c.rolling(n).mean()
 e12=c.ewm(span=12,adjust=False).mean(); e26=c.ewm(span=26,adjust=False).mean(); x['macd_dif']=e12-e26; x['macd_dea']=x['macd_dif'].ewm(span=9,adjust=False).mean(); x['macd_hist']=2*(x['macd_dif']-x['macd_dea'])
 d=c.diff(); g=d.clip(lower=0).rolling(14).mean(); l=(-d.clip(upper=0)).rolling(14).mean(); x['rsi14']=100-100/(1+g/l.replace(0,np.nan))
 tr=pd.concat([x['high']-x['low'],(x['high']-c.shift()).abs(),(x['low']-c.shift()).abs()],axis=1).max(axis=1); x['atr14']=tr.rolling(14).mean(); x['obv']=(np.sign(c.diff()).fillna(0)*v).cumsum(); x['volume_ratio20']=v/v.rolling(20).mean().replace(0,np.nan); x['support20']=c.rolling(20).min(); x['resistance20']=c.rolling(20).max()
 x['macd_cross']='none'; x.loc[(x.macd_dif>x.macd_dea)&(x.macd_dif.shift(1)<=x.macd_dea.shift(1)),'macd_cross']='golden_cross'; x.loc[(x.macd_dif<x.macd_dea)&(x.macd_dif.shift(1)>=x.macd_dea.shift(1)),'macd_cross']='death_cross'; prev=x.macd_hist.shift(1); x['hist_direction']=np.select([x.macd_hist>prev,x.macd_hist<prev],['expanding','contracting'],default='flat'); return x
def latest_signal(df):
 x=add_indicators(df).dropna(subset=['close']);
 if x.empty:return {}
 r=x.iloc[-1]; n=lambda z: None if pd.isna(z) else float(z)
 return {'price':n(r.close),'ma5':n(r.ma5),'ma10':n(r.ma10),'ma20':n(r.ma20),'ma60':n(r.ma60),'macd_dif':n(r.macd_dif),'macd_dea':n(r.macd_dea),'macd_hist':n(r.macd_hist),'rsi14':n(r.rsi14),'atr14':n(r.atr14),'volume_ratio20':n(r.volume_ratio20),'support20':n(r.support20),'resistance20':n(r.resistance20),'macd_cross':r.macd_cross,'hist_direction':r.hist_direction,'zero_axis':'above' if r.macd_dif>=0 else 'below'}
