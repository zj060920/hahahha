import sys
from pathlib import Path
import numpy as np,pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parent/'bundled-mcp-server/src'))
from monitor.indicators import add_indicators
def test_indicators():
 c=pd.Series(np.linspace(100,120,100));d=pd.DataFrame({'open':c,'high':c+1,'low':c-1,'close':c,'volume':np.ones(100)*1000});x=add_indicators(d);assert {'macd_dif','macd_dea','macd_hist','rsi14','volume_ratio20','support20','resistance20'}<=set(x.columns)
