from pathlib import Path
import yaml
from .data import history
from .indicators import latest_signal
ROOT=Path(__file__).resolve().parents[2]; CONFIG=yaml.safe_load((ROOT/'config/stocks.yaml').read_text(encoding='utf-8'))
def technical(s,tfs):
 o={'symbol':s,'timeframes':{}}
 for tf in tfs:
  try:o['timeframes'][tf]=latest_signal(history(s,tf))
  except Exception as e:o['timeframes'][tf]={'error':str(e)}
 return o
def state(tfs):
 v=[x for x in tfs.values() if isinstance(x,dict) and 'macd_dif' in x]
 if not v:return 'data_unavailable'
 a=sum(x['macd_dif']>=0 for x in v); e=sum(x['hist_direction']=='expanding' for x in v); c=sum(x['hist_direction']=='contracting' for x in v)
 if a>=max(1,len(v)-1) and e>=max(1,len(v)//2):return 'trend_strengthening'
 if c>=max(1,len(v)//2):return 'momentum_weakening'
 return 'range_repair'
