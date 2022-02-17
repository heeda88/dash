#%%
import json
import pandas as pd
from glob import glob



#%%
data=open('data_ignore/0207_0214_user.json').read()
# obj=json.loads('0207_0214_user.json')
obj=json.loads(data)
print(obj[0])

#%%

# 오브젝트형태가 리스트 오젝트로 들어오므로 json.normalize로  활용하면 된다.
df=pd.json_normalize(obj)
print(df.columns)
print(df.loc[:,'type'].unique())

cond_list=df.loc[:,'type']=='DISTANCE_DELTA'

step_df=df.loc[cond_list,:].reset_index().iloc[:,1:].copy()

#%%
print(f"""
      {step_df.to_markdown()}
""")
#%%

step_df

#%%cond_list= df.loc[:,'dateFrom']

csv_list=glob('data_ignore/*.csv')

map_obj={}
for index in csv_list:
      map_obj[f'{index}']= pd.read_csv(f'{index}',sep='\t')


#%%
map_df=pd.concat(objs=map_obj)

# %%
map_df