
import os

dir_path=sys.argv[0]

for mol_file in os.listdir(dir_path):
    if mol_file.__contains__(".mol2"):
        pdbqt_file=mol_file.split(".mol2")[0]+".pdbqt"
        print("babel -imol2 "+dir_path+mol_file+" -opdbqt -O "+dir_path+pdbqt_file)
        os.system("babel -imol2 "+dir_path+mol_file+" -opdbqt -O "+dir_path+pdbqt_file)
ligands=dir_path+"ligands"
if not os.path.exists(ligands):
    open(ligands,'w')
for file in os.listdir(dir_path):
    if file.__contains__(".pdbqt"):
        open(ligands,'a').write(file.split(".pdbqt")[0]+'\n')
        lines=open(dir_path+file,'r').readlines()
        lines[0]=lines[0].replace("*****", file.split(".pdbqt")[0])
        open(ligands,'a').writelines(lines)
        open(ligands, 'a').write("$$$$\n")

