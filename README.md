# DeepRLDS
Overview
DeepRLADS, a de novo molecular design assay, was established based on deep reinforcement learning training, integrating activity screening and structure optimization into a single artificial intelligence (AI)-based drug discovery module.

Requirements

Python == 3.7.3

tensorflow == 2.3.1

keras == 2.4.3

pandas == 0.24.0

numpy == 1.19.5

scikit-learn == 0.24.2

selenium 4.2.0

sklearn

rdkit

vina

Prepare molecular dataset
1. The virtual fragment combinatorial library for drug design contains many fragmenting compounds with 9823 Mpro inhibitory activity from the ChEMBL database which was crawled by using reptile tool- selenium 4.2.0. The initial lead compound molecular group as input data that contains 175 lead compounds after filtering 969 lead compounds for the seven targets of COVID-19 by virtual screening tool

2. In the pretraining process of the perceptron classifier, the positive and negative sample data were from the dekois 2.0 benchmark data set library provided by Tubingen University that contained the SARS coronavirus 3CL protease data set. Taking the ic50 value as the standard, 407 active samples were taken as positive samples and 1254 inactive samples as negative samples for training perceptron classifier.

Instructions

To run the main program on the same data as described in the paper just run:

install rdkit

conda create -c rdkit -n my-rdkit-env rdkit

activate rdkit

conda activate my-rdkit-env

Install dependent libraries

pip install -U numpy==1.19.5 scipy matplotlib

pip install -U scikit-learn

pip install keras

conda install Pandas

pip install -U python-Levenshtein

pip install -U tensorflow==2.3.1

conda install -c conda-forge openbabel

pip install -U mpi4py

python run.py

It is also possible to run the program on a custom set of lead molecules and/or fragments.

python run.py fragment_molecules.smi lead_file.smi

Molecules that are genertated during the process can be vied by running:

python Show_Epoch.py n

where n is the epoch that should be viewed. This shows two columns of molecules. The first column contains the original lead molecule, while the second column contains modified molecules. Any global parameters can be changed by changing them in the file "Modules/global_parameters.py"
