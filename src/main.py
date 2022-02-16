
#%%
from autogluon.tabular import TabularDataset, TabularPredictor
from autogluon.core.utils.utils import setup_outputdir
from autogluon.core.utils.loaders import load_pkl
from autogluon.core.utils.savers import save_pkl
from src.MultiPredictor import MultilabelPredictor
from Models.utills import LogStamp
import os.path

from sklearn.model_selection import train_test_split
import pandas as pd
import csv
import warnings

warnings.filterwarnings("ignore")

print( LogStamp.logtime() )

#%%
path = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/housing.csv'
df = pd.read_csv(path, header=None)
audi_train_data=pd.read_csv('train.csv',encoding='utf-8')
#%%
df
#%%
audi_train_data
#%%


## 로딩후 데이터 분리 
audi_train_data=pd.read_csv('train.csv',encoding='utf-8')
audi_test_data=pd.read_csv('train.csv',encoding='utf-8')

columns_list=audi_train_data.columns.tolist()

print(columns_list)


#%%
# 데이터 100개씩 분리 작업 진행 
dropList=['id']
audi_train_data=audi_train_data.drop(dropList,axis=1)

label_list=[]
label_type=[]
eval_metric_list=[]

for index in columns_list:
    if "target" in index:
        if "cause_loss_priority"in index:
            continue
        label_list.append(index)
        label_type.append("regression")
        eval_metric_list.append("f1")
        
#%%
# 학습진행
problem_types = ['regression','multiclass','binary']  # type of each prediction problem 각 라벨별 형태

# ‘GBM’ (LightGBM) ‘CAT’ (CatBoost) ‘XGB’ (XGBoost) ‘RF’ (random forest) ‘XT’ (extremely randomized trees) 
# ‘KNN’ (k-nearest neighbors) ‘LR’ (linear regression) ‘NN’ (neural network with MXNet backend) ‘FASTAI’ (neural network with FastAI backend)
# '메모리 page out 방지를 위해 NN, FASTAI 모델 제외하고 진행, 메모리 32GB 이상시 NN,FASTAI 포함하여 진행'
excluded_model_types = ['KNN','RF','CAT'] # 제외 모델 

save_path = 'audioMultiLabel'

time_limit = 300
problem_type=label_type

multi_predictor = TabularPredictor(label='target', path=save_path,problem_type='regression')
multi_predictor.fit(audi_train_data, time_limit=time_limit,excluded_model_types=excluded_model_types, holdout_frac=0.1112)

#%%
multi_predictor = MultilabelPredictor(labels=label_list, problem_types=label_type, path=save_path, eval_metrics=eval_metric_list)
multi_predictor.fit(audi_train_data, time_limit=time_limit,excluded_model_types=excluded_model_types, holdout_frac=0.1112)

#%%

## 훈련된 모델 불러오고 평가 진행
test_data_nolab = audi_test_data.drop(columns=label_list)
test_data_nolab.head()

# 멀티라벨 모델 로드  & 테스트 데이터 진행 
multi_predictor = TabularPredictor.load(save_path)  
predictions = multi_predictor.predict(test_data_nolab)
print("Predictions:  \n", predictions)

df_pred=pd.DataFrame(predictions)

df_pred.to_csv("multiLabelPredictions.csv",encoding="utf-8",index=False)

# 메트릭 진행 
evaluations = multi_predictor.evaluate(audi_test_data)
print("evaluations:  \n",evaluations)
print("Evaluated using metrics:", multi_predictor.eval_metric)


#%%

print("Predictions:  \n", predictions)
audi_test_data['target'].head()

#%%
## 메트릭 결과를 CSV 로 저장
result_label_list=list(evaluations.keys())
result_metric_list=list(evaluations[result_label_list[0]].keys())

data_list=[]
for key in result_label_list:
    data_list.append(evaluations[key])
print(data_list)

with open("multiLabel.csv", 'w') as f: 
    wr = csv.DictWriter(f, fieldnames =result_metric_list) 
    wr.writeheader() 
    wr.writerows(data_list) 

    
df_pred.loc[:,'predict']=''
audi_test_data=pd.DataFrame(audi_test_data.copy())
audi_test_data.loc[:,'predict']=''
predictLIst=df_pred.loc[:,df_pred.columns!='predict'].columns.tolist()

for index in predictLIst:
    condlist=(audi_test_data.loc[:,f'{index}'].astype('float')==1)
    audi_test_data.loc[condlist,f'predict']=audi_test_data.loc[condlist,f'predict']+f'{causeList[predictLIst.index(index)]}, '
audi_test_data.loc[:,f'predict']=audi_test_data.loc[:,f'predict'].astype('str').replace(r', $', r'', regex=True)

for index in predictLIst:
    condlist=(df_pred.loc[:,f'{index}'].astype('float')==1)
    df_pred.loc[condlist,f'predict']=df_pred.loc[condlist,f'predict']+f'{causeList[predictLIst.index(index)]}, '
df_pred.loc[:,f'predict'].astype('str').replace(r', $', r'', regex=True)

total_df=pd.DataFrame(df_pred.loc[:,f'predict'].astype('str').replace(r', $', r'', regex=True))
total_df.loc[:,'label']=audi_test_data.loc[:,f'predict'].astype('str').replace(r', $', r'', regex=True)

print(total_df)

#%%
df_pred.to_csv("multiLabelPredictions.csv",encoding="utf-8",index=False)

# 메트릭 진행 
evaluations = multi_predictor.evaluate(audi_test_data)
print("evaluations:  \n",evaluations)
print("Evaluated using metrics:", multi_predictor.eval_metrics)

## 메트릭 결과를 CSV 로 저장
result_label_list=list(evaluations.keys())
result_metric_list=list(evaluations[result_label_list[0]].keys())

data_list=[]
for key in result_label_list:
    data_list.append(evaluations[key])
print(data_list)

with open("multiLabel.csv", 'w') as f: 
    wr = csv.DictWriter(f, fieldnames =result_metric_list) 
    wr.writeheader() 
    wr.writerows(data_list) 

#%%
## 메트릭 CSV 로드

print(causeList)
metric_df=pd.read_csv("multiLabel.csv")
metric_df=pd.DataFrame(metric_df)
metric_df.insert(0,'원인질환',causeList)
causeCountList=[]

for index in range(1, 20):
    causeCountList.append(list(audi_test_data[f"cause_loss_{index}"].astype('str').str.contains('1',regex=True)).count(True))
metric_df.insert(1,'원인질환 count',causeCountList)
print(metric_df)

#%%
## 메트릭 CSV 로드

print(causeList)
metric_df=pd.read_csv("multiLabel.csv")
metric_df=pd.DataFrame(metric_df)
metric_df.insert(0,'원인질환',causeList)
causeCountList=[]

#%%
predictor_class = multi_predictor.get_predictor('cause_loss_1')
model_metric=predictor_class.leaderboard(silent=True)
print(model_metric.loc[:,['model','stack_level','score_val','fit_time']])

#%%
for index in range(1, 20):
    causeCountList.append(list(audi_test_data[f"cause_loss_{index}"].astype('str').str.contains('1',regex=True)).count(True))
metric_df.insert(1,'원인질환 count',causeCountList)
print('\n\n')
print(metric_df.to_markdown())
