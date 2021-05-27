# -*- coding: utf-8 -*-
"""
Created on Thu May 27 18:21:07 2021

@author: erdem
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import data_preprocessing 
import model
from PIL import Image, ImageTk
import pandas as pd
import numpy as np

model=model.model
x_train_mean=data_preprocessing.x_train_mean
x_train_std=data_preprocessing.x_train_std
skin_cancer_table=data_preprocessing.skin_cancer_table

img_name = ""
count = 0
img_jpg = ""
window= tk.Tk()

window.geometry("1080x640")
window.title("Skin Cancer")

left=tk.Frame(window,width=600,height=640,bd="2")
left.grid(row=0,column=0)

right=tk.Frame(window,width=480,height=640,bd="2")
right.grid(row=0,column=1)    

fr1= tk.LabelFrame(left, text="Images",width=600,height=500)
fr1.grid(row=0,column=0)

fr2= tk.LabelFrame(left, text="Save",width=600,height=140)
fr2.grid(row=1,column=0)

fr3= tk.LabelFrame(right, text="Patient's Attribute",width=240,height=640)
fr3.grid(row=0,column=0)

fr4= tk.LabelFrame(right, text="Patient's Result",width=240,height=640)
fr4.grid(row=0,column=1,padx=10)

def imageResize(img):
    
    basewidth = 500
    wpercent = (basewidth/float(img.size[0]))   # 1000 *1200
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize),Image.ANTIALIAS)
    return img

def openImage():
    
    global img_name
    global count
    global img_jpg
    
    count += 1
    if count != 1:
        messagebox.showinfo(title = "Warning", message = "Only one image can be opened")
    else:
        img_name = filedialog.askopenfilename(initialdir = "D:\codes",title = "Select an image file")
        
        img_jpg = img_name.split("/")[-1].split(".")[0]
        # image label
        tk.Label(fr1, text =img_jpg, bd = 3 ).pack(pady = 10)
    
        # open and show image
        img = Image.open(img_name)
        img = imageResize(img)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(fr1, image = img)
        panel.image = img
        panel.pack(padx = 15, pady = 10)
        
        # image feature
        data = pd.read_csv("HAM10000_metadata.csv")
        cancer = data[data.image_id == img_jpg]
        
        for i in range(cancer.size):
            x = 0.4
            y = (i/10)/2
            tk.Label(fr3, font = ("Times",12), text = str(cancer.iloc[0,i])).place(relx = x, rely = y)
                   
menubar = tk.Menu(window)
window.config(menu = menubar)
file = tk.Menu(menubar)
menubar.add_cascade(label = "File",menu = file)
file.add_command(label = "Open", command = openImage)

# frame3
def classification():
    
    if img_name != "" and models.get() != "":
        
        # model selection
        if models.get() == "model":
            classification_model = model
        else:
            classification_model = model
        
        z = skin_cancer_table[skin_cancer_table.image_id == img_jpg]
        z = z.image.values[0].reshape(1,75,100,3)
        
        # 
        z = (z - x_train_mean)/x_train_std
        h = classification_model.predict(z)[0]
        h_index = np.argmax(h)
        predicted_cancer = list(skin_cancer_table.dx.unique())[h_index]
        
        for i in range(len(h)):
            x = 0.5
            y = (i/10)/2
            
            if i != h_index:
                tk.Label(fr4,text = str(h[i])).place(relx = x, rely = y)
            else:
                tk.Label(fr4,bg = "green",text = str(h[i])).place(relx = x, rely = y)
        
        if chvar.get() == 1:
            
            val = entry.get()
            entry.config(state = "disabled")
            path_name = val + ".txt" # result1.txt
            
            save_txt = img_name + "--" + str(predicted_cancer)
            
            text_file = open(path_name,"w")
            text_file.write(save_txt)
            text_file.close()
        else:
            print("Save is not selected")
    else:
        messagebox.showinfo(title = "Warning", message = "Choose image and Model First!")
        tk.Label(fr3, text = "Choose image and Model First!" ).place(relx = 0.1, rely = 0.6)
                          
columns = ["lesion_id","image_id","dx","dx_type","age","sex","localization"]
for i in range(len(columns)):
    x = 0.1
    y = (i/10)/2
    tk.Label(fr3, font = ("Times",12), text = str(columns[i]) + ": ").place(relx = x, rely = y)

classify_button = tk.Button(fr3, bg = "red", bd = 4, font = ("Times",13),activebackground = "orange",text = "Classify",command = classification)
classify_button.place(relx = 0.1, rely = 0.5)
# frame 4
labels = skin_cancer_table.dx.unique()

for i in range(len(columns)):
    x = 0.1
    y = (i/10)/2
    tk.Label(fr4, font = ("Times",12), text = str(labels[i]) + ": ").place(relx = x, rely = y)
# frame 2 
# combo box
model_selection_label = tk.Label(fr2, text = "Choose classification model: ")
model_selection_label.grid(row = 0, column = 0, padx = 5)

models = tk.StringVar()
model_selection = ttk.Combobox(fr2,textvariable = models, values = ("Model1","Model2"), state = "readonly")
model_selection.grid(row = 0, column = 1, padx = 5)

# check box
chvar = tk.IntVar()
chvar.set(0)
xbox = tk.Checkbutton(fr2, text = "Save Classification Result", variable = chvar)
xbox.grid(row = 1, column =0 , pady = 5)

# entry
entry = tk.Entry(fr2, width = 23)
entry.insert(string = "Saving name...",index = 0)
entry.grid(row = 1, column =1 )


window.mainloop()