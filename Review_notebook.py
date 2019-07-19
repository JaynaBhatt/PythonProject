# Databricks notebook source
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# COMMAND ----------

dbutils.widgets.text("output_path","","")
dbutils.widgets.get("output_path")
FilePath = getArgument("output_path")

dbutils.widgets.text("file_name","","")
dbutils.widgets.get("file_name")
filename = getArgument("file_name")

# COMMAND ----------

storage_account_name = "azuredatatraining"
storage_account_key = "y/JLihJ5LmVHlfWWDiu4oWgeYEzluZYJM2BguxKIsVoO2KKBW63LNLSt6pYTU84PGv+VSXNaAncWPOHvbqbyKg=="

# COMMAND ----------

spark.conf.set("fs.azure.account.key."+storage_account_name+".blob.core.windows.net",storage_account_key)

# COMMAND ----------

file_type = "csv"
file_location = "wasbs://trainingcontainer@azuredatatraining.blob.core.windows.net"+FilePath+filename+"."+file_type
print(file_location)

# COMMAND ----------

df = spark.read.format(file_type).option("inferschema","true").load(file_location)

# COMMAND ----------

df.show()

# COMMAND ----------

train = df.toPandas()

# COMMAND ----------

train.head()

# COMMAND ----------

Prices = train.iloc[1:len(train),1:2].values

# COMMAND ----------

Prices

# COMMAND ----------

x=train.iloc[2:len(train),2:4].values

y=train.iloc[2:len(train),:1].values

# COMMAND ----------

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
reg = LinearRegression()
reg.fit(x_train,y_train)

y_pred= reg.predict(x_test)
print(y_pred)

# COMMAND ----------

file_name = 'HousePrice.pkl'
pkl_file = open(file_name, 'wb')
print("pickelfile",pkl_file)
model = pickle.dump(reg, pkl_file)


# COMMAND ----------

pkl_file = open(file_name, 'rb')
model_pkl = pickle.load(pkl_file)
y_pred = model_pkl.predict(x_test)
print("prediction",y_pred)
