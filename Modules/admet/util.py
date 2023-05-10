import os
import sys
from math import inf
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
import pandas as pd
from rdkit import Chem
from rdkit.Chem.rdmolfiles import MolFromMol2File
from pandas import DataFrame
def converter(file_name):



        return (Chem.MolToSmiles(MolFromMol2File(file_name)))

def concat_csv(dir_path):
    # final_csv=
    if not  os.path.exists(dir_path+"final.csv"):
        open(dir_path+"final.csv",'w')
    inital_csv=pd.read_csv(dir_path+"final.csv")
    for i,file in enumerate(os.listdir(dir_path)):
        if file.__contains__("final"):
            continue
        else:
            file_path=dir_path+file
            csv=pd.read_csv(file_path)
            inital_csv=pd.concat([inital_csv,csv])
    inital_csv.to_csv(dir_path+"final.csv")
def to_dist(csv_file_col):
    # library & dataset
    import pandas as pd
    df = pd.read_csv('final_.csv')
    plt.figure(figsize=(30,30))
    s=df[csv_file_col]
    print(type(s))
    s[s==inf]=999
    plt.hist(s, bins=60,  alpha=0.7, histtype='stepfilled',
             color='steelblue', edgecolor='none')
    x_min=min(s)
    x_max=max(s)
    xlin=(arange(x_min,x_max,step=(x_max-x_min)/15))
    # plt.xlim(np.arange(0,100,10))
    xlin=np.around(xlin,1)
    print(xlin)
    plt.xticks(xlin)
    plt.grid(True)
    plt.xlabel(csv_file_col)
    plt.ylabel("frequency")
    plt.savefig("dist_result/"+csv_file_col+".jpg")
    plt.show()

def count_series(csv_file_col):
    df = pd.read_csv('final_.csv')
    print(type(df[csv_file_col].value_counts()/len(df[csv_file_col])))
    return (df[csv_file_col].value_counts()/len(df[csv_file_col])).sort_values(ascending=False)
def csv_to_dict(csv_path):
    dict={}
    df=pd.read_csv(csv_path)
    for index, row in df.iteritems():
        print(type(row))
        dict[index]=row.tolist()
        print("index:{},row:{}".format(index,row.tolist()))

    open('result.txt','a').write(str(dict))
if __name__ == "__main__":
      #
    for index,row in pd.read_csv("final_.csv").iteritems():
        try:
            to_dist(index)
        except:
            print(index)
   
