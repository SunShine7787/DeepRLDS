import rdkit.Chem as Chem
from rdkit.Chem import Descriptors
import numpy as np
from build_encoding import decode
import rdkit.Chem.Crippen as Crippen
import rdkit.Chem.rdMolDescriptors as MolDescriptors
from rdkit.Chem import Descriptors

import os, time
import numpy as np
import h5py
from pybel import *
import subprocess
import logging
from admet.static import admet_static
import _thread
import threading
from remote_server import sftpClient
from global_parameters import FEATURES

# Cache evaluated molecules (rewards are only calculated once)
evaluated_mols = {}



def modify_fragment(f, swap):
    f[-(1 + swap)] = (f[-(1 + swap)] + 1) % 2
    return f




def get_key(fs):
    return tuple([np.sum([(int(x) * 2 ** (len(a) - y))
                          for x, y in zip(a, range(len(a)))]) if a[0] == 1 \
                      else 0 for a in fs])






def Client(filename):
    result_list_str = sftpClient(
        _ligandListFilePath=filename,
        _remotepath='xxxxxxxx',
        _hostname='xxxxxxxx',
        _username='xxxxxxxx',
        _passwd='xxxxxxxx'
    )
    return result_list_str


# **# 批量处理分子奖励
def evaluate_batch_mol(org_mols, batch_mol, epoch, decodings):
    fr = [False] * FEATURES
    rootPath = "/home/developer/wq/rldmpo"
    frs = [fr] * batch_mol.shape[0]
    global evaluated_mols
    path = rootPath + "/vina/ligands/" + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()) + "/"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        # os.system('sudo mkdir '+path)
    filename = path + 'ligands'
    # print(filename)
    # 构建需要计算的小分子的列表
    mollist = []
    pdbqt_list=[]
    keylist = []
    # 获取感知机模型
    file1 = h5py.File(rootPath + '/stat1.h5', 'r')
    W = file1['W'][:]
    b = file1['b'][:]
    file1.close()
    for i in range(batch_mol.shape[0]):
        if not np.all(org_mols[i] == batch_mol[i]):
            print("i="+str(i))
            key = get_key(batch_mol[i])
            if key in evaluated_mols:
                # print("rewards : this is if----")
                frs[i] = evaluated_mols[key][0]
                continue
            try:
                mol = decode(batch_mol[i], decodings)
                Smiles=str(Chem.MolToSmiles(mol))
                print("this is try .....,smile:{}".format(Smiles))
                # 转换成mol2文件
                # mol = Chem.MolFromSmiles('COc1cc(ccc1OCC2CN(CCCO2)Cc3ccc(cc3)Br)Cl')
                # print("++++++++++++++++++++++")
                # 计算前4个属性值
                Chem.GetSSSR(mol)
                clogp = Crippen.MolLogP(mol)
                mw = MolDescriptors.CalcExactMolWt(mol)
                tpsa = Descriptors.TPSA(mol)
                # # 计算相似性
                frs[i][0] = True
                frs[i][1]=400 < mw < 605
                frs[i][2]=4 < clogp < 7
                frs[i][3]=80 < tpsa < 102
                print("mw:{},clogP:{},tpsa:{}".format(mw,clogp,tpsa))
                # os.system("obabel -ismiles /home/b519/lyy/lyy2/deep/ligand/temp.smi -omol2 -O /home/b519/lyy/lyy2/deep/ledock/ligand/temp.mol2 --gen3D")
                # print("*****************************")
                # mymol = readstring("smi", smi)
                # mymol.write("smi", path+str(i)+".smi",overwrite=True)
                # os.system("obabel -ismiles "+path+str(i)+".smi -omol2 -O "+path+str(i)+".mol2 --gen3D")
                print('obabel -:"' + Smiles + '" --gen3d -omol2 -O ' + path + str(i) + '.mol2')
                os.system('obabel -:"' + Smiles + '" --gen3d -omol2 -O ' + path + str(i) + '.mol2')
                os.system("python ../vina/prepare.py "+str(path))
                pdbqt_list.append(i)
                keylist.append(key)
            except:
                frs[i] = [False] * FEATURES
        else:
            frs[i] = [False] * FEATURES

    # # 调用对接接口
    if len(pdbqt_list) == 0:
        # print('len(mollist) == 0'+str(len(evaluated_mols)))
        return frs
  
    # 获取对接结果，拼接成模型输入
    # 将获得的结果转换成字典
    # 死循环，只有当try到正确结果时，才会退出循环，否则将等待6s后重新执行，同时将这次的中断输出到日志
    result_list_str = Client(filename)
    while True:
        if (result_list_str==None):
            #当result_list_str为None的时候，走if
            time.sleep(6)  # 等待6s
            # 日志输出
            _now_time = time.time()
            logging.info('=' * 100)
            logging.info(str((time.strftime('%Y-%m-%d %H:%M:%S'))))
            logging.info('The result_list_str is None')
            logging.info('=' * 100)
            # 重新执行
            result_list_str = Client(filename)
        else :
            #如果result_list_str不为None的话，就尝试
            try:

                result_list = result_list_str.strip('[]').split('], [')

                break;
            except BaseException as e:
                time.sleep(6)  # 等待6s
                # 日志输出
                _now_time = time.time()
                logging.info('=' * 100)
                logging.info(str((time.strftime('%Y-%m-%d %H:%M:%S'))))
                logging.info('The interrupted service has been restarted')
                logging.error(e)
                logging.info('=' * 100)
                # 重新执行
                result_list_str = Client(filename)
    # result_list = result_list_str.strip('[]').split('], [')
    # TDO 容错机制，若没有结果，则继续检测
    # del(result_list[-1])#删除掉最后的空格元素
    # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    # print(len(result_list))
    # print(result_list)
    result_key_value = {}
    # print("---------------------------------------")
    for result in result_list:
        # result= result.strip('[]')
        # print(result)
        strs = result.split(', ')
        # print(strs)
        pdbId = strs[0].strip("'").split('.pdbqt')[0]
        ligandNo = strs[1].strip("'").split('.pdbqt')[1]
        key = ligandNo + "_" + pdbId
        # print("key="+key)
        value = [float(strs[2]), float(strs[3]), float(strs[4])]
        result_key_value[key] = value
        ##拼接结果为感知机的输入
    PDBpath = rootPath + '/vina/ledock_in.list'
    print(len(result_key_value))
    for i, key in zip(pdbqt_list, keylist):
        X = []
        with open(PDBpath, "r") as f:
            for line in f:
                # ('./SARS-CoV-2/7JQ4', '7JQ4_ledock.in')
                p1, f1 = os.path.split(line)
                # ('./SARS-CoV-2', '7JQ4')
                p2, pdbID = os.path.split(p1)
                k = str(i) + "_" + pdbID
                try:
                    val = result_key_value[k]
                except:
                    val = [0.0, 0.0, 0.0]
                X.append(val[0])
                X.append(val[1])
                X.append(val[2])
                # print(len(X))
            
        print("activity:"+str(np.dot(X, W) + b[0]))
        activity =((np.dot(X, W) + b[0]) > 0)
        frs[i][4] = activity

    # admet
    os.system("python ../experiment/admet.py "+path)
    admet_dict=admet_static(path+"result/")
    for i, key in zip(pdbqt_list, keylist):
        X = []
        frs[i][5] = admet_dict[i]
        evaluated_mols[key] = (np.array(frs[i]), epoch)
    # print("final_frs")
    # print(frs)
    return frs

# Get initial distribution of rewards among lead molecules
def get_init_dist( X, decodings):
    # arr = np.asarray([evaluate_mol(X[i], -1, decodings) for i in range(X.shape[0])])
    # X_mat=np.full(X.shape,np.nan)
    # arr = np.asarray(evaluate_batch_mol(X_mat,X,-1,decodings))
    X_mat = np.full(X.shape, np.nan)
    frs = evaluate_batch_mol(X_mat, X, -1, decodings)
    arr = np.asarray(frs)
    dist = arr.shape[0] / (1.0 + arr.sum(0))
    return dist


# Discard molecules which fulfills all targets (used to remove to good lead molecules).
def clean_good(X, decodings):
    X_mat = np.full(X.shape, np.nan)
    frs = evaluate_batch_mol(X_mat, X, -1, decodings)
    X = [X[i] for i in range(X.shape[0]) if not
    np.array(frs[i]).all()]
    return np.asarray(X), frs



