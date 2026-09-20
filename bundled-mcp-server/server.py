import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from mcp.server.fastmcp import FastMCP
from monitor.data import get_quote,history
from monitor.engine import technical,state,CONFIG
from monitor.indicators import latest_signal
from monitor.backtest import run as backtest
from monitor.risk import run as risk
from monitor.news import search as news_search
mcp=FastMCP('ai-hardware-market-monitor')
@mcp.tool()
def quote_tool(symbol:str)->dict:return get_quote(symbol)
@mcp.tool()
def technical_analysis(symbol:str,timeframes:list[str]|None=None)->dict:
 t=technical(symbol,timeframes or ['1m','5m','15m','30m','60m','1d']);t['state']=state(t['timeframes']);return t
@mcp.tool()
def compare_symbols(symbols:list[str],timeframe:str='15m')->dict:
 o={}
 for s in symbols:
  try:o[s]=latest_signal(history(s,timeframe))
  except Exception as e:o[s]={'error':str(e)}
 return {'timeframe':timeframe,'symbols':o}
@mcp.tool()
def sector_linkage(sectors:list[str]|None=None,timeframe:str='15m')->dict:
 out={}
 for sec in sectors or ['CPO','PCB','STORAGE']:
  rows={}
  for s in CONFIG['sectors'].get(sec,{}).get('A股',[]):
   try:rows[s]=latest_signal(history(s,timeframe))
   except Exception as e:rows[s]={'error':str(e)}
  v=[x for x in rows.values() if 'macd_dif' in x]; b=sum(x['macd_dif']>x['macd_dea'] for x in v);out[sec]={'timeframe':timeframe,'symbols':rows,'breadth_ratio':b/len(v) if v else None,'synchronization':f'{b}/{len(v)}' if v else '0/0'}
 return out
@mcp.tool()
def strategy_backtest(symbol:str,timeframe:str='1d',strategy:str='macd')->dict:return backtest(history(symbol,timeframe),strategy)
@mcp.tool()
def risk_manager_tool(positions:dict,total_equity:float,cash:float)->dict:return risk(positions,total_equity,cash)
@mcp.tool()
def screen_stock(symbol:str)->dict:
 t=technical(symbol,['15m','60m','1d']);return {'symbol':symbol,'quote':get_quote(symbol),'technical':t,'state':state(t['timeframes'])}
@mcp.tool()
def news_impact(query:str,limit:int=10)->dict:return {'query':query,'items':news_search(query,limit)}
@mcp.tool()
def daily_market_brief(symbols:list[str]|None=None)->dict:
 syms=symbols or ['300308','300502','300394','002916','002463','603986','301308','LITE','MU','SOXX'];rows=[]
 for s in syms:
  try:t=technical(s,['15m','60m','1d']);rows.append({'symbol':s,'state':state(t['timeframes']),'technical':t})
  except Exception as e:rows.append({'symbol':s,'error':str(e)})
 return {'symbols':rows,'note':'研究型技术分析，不是买卖指令。'}
if __name__=='__main__':mcp.run()
