import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate(df,days):  # some factors cannot be found in financial statement, and we need to calculate them
    code = list(df['code'].unique())
    data = pd.DataFrame()
    for i in code[:]:
        tem = df.loc[df['code'] == i]
        tem = tem.replace(0,np.nan)  # shift the abnormal value and NA
        tem = tem.fillna(method='pad')
    
        # in this case, we take the square of return, positive return, negative return as examples
        tem['return'] = ((tem['adjust_price_f'] - tem['adjust_price_f'].shift(1))/tem['adjust_price_f'].shift(1)).fillna(0)
        tem['positive'] = tem.loc[tem['return'] > 0, 'return']
        tem['negative'] = tem.loc[tem['return'] < 0, 'return']
        tem = tem.fillna(0)
    
        tem['ret_var'] = pd.rolling_var(tem['return'],days)
        tem['pos_var'] = pd.rolling_var(tem['positive'],days)
        tem['neg_var'] = pd.rolling_var(tem['negative'],days)
        tem['pos_neg_rate'] = tem['pos_var'] / tem['neg_var']
        tem['return'] = pd.rolling_mean(tem['return'],days)
        data = data.append(tem)
    return data
   
   
# then just use the same code as the "factors in financial statement to test"   