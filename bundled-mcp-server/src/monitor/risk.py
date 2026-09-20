def run(positions,total_equity,cash):
 if total_equity<=0:raise ValueError('total_equity must be positive')
 w={k:max(0,float(v))/total_equity for k,v in positions.items()}; invested=max(0,total_equity-cash)/total_equity; largest=max(w.values(),default=0)
 return {'total_equity':total_equity,'cash':cash,'cash_ratio':cash/total_equity,'invested_ratio':invested,'largest_position_ratio':largest,'position_weights':w,'flags':{'high_exposure':invested>0.8,'high_single_position':largest>0.3}}
