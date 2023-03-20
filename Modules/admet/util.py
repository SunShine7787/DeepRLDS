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
    # print(open(file_name,'a'))
    # output_filename=os.path.join("drug_bank_smi",file_name.split("drug_bank/")[1].split(".sdf")[0]+".smi")
    # sdf_convert_order="obabel -isdf '"+file_name+"' -osmi '"+output_filename+"' -b"
    # print(sdf_convert_order)
    # os.system(sdf_convert_order)
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
    # Make default density plot
    # plt.hist(df[csv_file_col])
    # plt.xlabel(csv_file_col)
    # plt.ylabel("frequency")
    # # sns.kdeplot(df[csv_file_col])
    # plt.savefig("../d/"+csv_file_col+".jpg")
    # se=count_series(csv_file_col)
    plt.figure(figsize=(30,30))
    # print(type(df[csv_file_col]=="inf"))
    # for i,b in (df[csv_file_col]==inf).iteritems():
    #     print(i,b)
    #     if b:
    #         print(i)
    #         df[csv_file_col].iloc[i]=14
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
    # converter("E:/scarpy/drug_bank/DB00114.sdf")
    # concat dir csv
    # dir_path="../drug_bank_csv/"
    # concat_csv(dir_path)
    # concat files
    # inital_csv=pd.concat([pd.read_csv('../drug_bank_csv/final.csv'),pd.read_csv('../final.csv')])
    # inital_csv.to_csv("../drug_bank_csv/final_.csv")
    # df = pd.read_csv('../drug_bank_csv/final_.csv')
    #
    for index,row in pd.read_csv("final_.csv").iteritems():
        try:
            to_dist(index)
        except:
            print(index)
    # to_dist("MW")
    # csv变字典
    # csv_to_dict("验证(1).csv")
    # count_series("F(20%)")
    # 将final.CSV的每一列排序之后分别取出第20%的点和第80%的点
    # final_df=pd.read_csv("final_.csv")
    # for index,row in final_df.iteritems():
    #     # print(f"index:{index},row:{row.tolist()}")
    #     try:
    #         rowS=row.tolist()
    #         rowS.sort()
    #         print(type(rowS))
    #         print(rowS)
    #         var1 = rowS[int(len(rowS) * 0.2)]
    #         var2 = rowS[int(len(rowS) * 0.8)]
    #         print(f"列名:{index},区间:{var1,var2}\n")
    #         open("final_.txt",'a').write(f"列名:{index},区间:{var1,var2}")
    #     except:
    #         print("e")