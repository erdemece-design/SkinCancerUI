# -*- coding: utf-8 -*-
"""
@author: www.erdemece.net
"""
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model 

model=load_model("skin_cancer.h5")
data = pd.read_csv("HAM10000_metadata.csv")

import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical 
    
skin_cancer_table=pd.read_csv("HAM10000_metadata.csv")

skin_cancer_table.head()
#sns.countplot(x="dx",data=skin_cancer_table)

data_folder= "HAM10000_images_part_1/"

jpg=".jpg"

skin_cancer_table["path"] = [data_folder + i + jpg for i in skin_cancer_table["image_id"]]
skin_cancer_table["image"]=skin_cancer_table["path"].map(lambda x : np.asarray(Image.open(x).resize((100,75))))
#plt.imshow(skin_cancer_table["image"][0]) #show such as skincancer 

skin_cancer_table["dx_id"]=pd.Categorical(skin_cancer_table["dx"]).codes

x_train=np.asarray(skin_cancer_table["image"].tolist()) # new list
x_train_mean = np.mean(x_train)
x_train_std = np.std(x_train)
x_train=(x_train-x_train_mean)/x_train_std

y_train=to_categorical(skin_cancer_table["dx_id"],num_classes=7)

pred=model.predict(x_train[5].reshape(1,75,100,3))
    