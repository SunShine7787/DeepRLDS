# -*- coding: utf-8 -*-
# @Time    : 2023/3/15 1:47
# @Author  : hxt
# @FileName: convert_to_result.py
# @Software: PyCharm
#
# 2vth_pro.pdbqt&&&&DB00246.pdbqt
# 第一个是靶点，第二个是配体
# 一个文件中装有一个靶点对应1000个配体的对接结果
# 当前的情况是2*1000，但最后我们应该1000*2
import os

root_path="result/"
result_path=root_path+"readme.md"
if not os.path.exists(result_path):
    open(result_path,'w')
pdb_list = []
for file in os.listdir(root_path):
    if file.__contains__("data"):
        pdb=open(root_path+file,'r').readlines()[0].split("&&&&")[0]
        for i,line in enumerate(open(root_path+file,'r').readlines()):
            score_list=[]
            if line.__contains__(pdb):
                ligand=line.split("&&&&")[1].split("\n")[0]
                print(ligand)
                print(i)
                print(open(root_path+file,'r').readlines()[i+2])
                score=open(root_path+file,'r').readlines()[i+2].split("REMARK VINA RESULT:     ")[1].split("      0.000      0.000")[0]
                print(score)
                score_list.append(pdb)
                score_list.append(ligand)
                score_list.append(score)
        pdb_list.append(score_list)
print(pdb_list)
open(result_path,'a').write(str(pdb_list))
