from .indicators import add_indicators
def run(df,strategy='macd'):
 x=add_indicators(df).dropna().copy()
 if x.empty:return {'error':'not enough data'}
 if strategy=='macd':p=(x.macd_dif>x.macd_dea).astype(int)
 elif strategy=='ma':p=(x.close>x.ma20).astype(int)
 elif strategy=='rsi':p=((x.rsi14>50)&(x.rsi14<70)).astype(int)
 else:raise ValueError('strategy must be macd, ma, or rsi')
 r=x.close.pct_change().fillna(0); s=r*p.shift(1).fillna(0); eq=(1+s).cumprod(); dd=eq/eq.cummax()-1
 return {'strategy':strategy,'bars':len(x),'total_return_pct':float((eq.iloc[-1]-1)*100),'max_drawdown_pct':float(dd.min()*100),'trade_count':int(p.diff().abs().fillna(0).sum())}
