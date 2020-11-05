# -*- coding: utf-8 -*-

import os
import requests
import glob
import numpy as np
import pickle
import torch as th
import dgl
import subprocess
from dgl.nn.pytorch import GraphConv
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path
from passer import GCNN

class Passer(object):
    def __init__(self, pdbID, pdbFile, chain, save):
        self.PDBFILE = pdbFile
        # indicate whether user have input PDB file
        self.UPLOAD = False
        self.save = True if save == "Y" or save == "y" else False
        self.PDB = pdbID
        self.pdbDIRECTION = "./"
        if self.PDBFILE:
            self.UPLOAD = True
            slashIndex = self.PDBFILE.rfind("/")
            self.PDB = self.PDBFILE[slashIndex + 1:].split(".")[0]
            self.pdbDIRECTION = self.PDBFILE[:slashIndex + 1]
        self.pocketDirection = "%s%s_out/pockets/"\
            %(self.pdbDIRECTION, self.PDB)
        self.CHAIN = chain
        self.HOME = str(Path.home()) + "/"
        self.modelDirection = self.HOME + ".passerModels/"

    def __download(self):
        self.URL = "https://files.rcsb.org/download/" + self.PDB + ".pdb"
        if self.PDB:
            r = requests.get(url = self.URL)
            open("%s.pdb" %self.PDB, "wb").write(r.content)

    def __runFPocket(self):
        if self.CHAIN:
            subprocess.call(["fpocket", "-f", "%s%s.pdb" \
                %(self.pdbDIRECTION, self.PDB), "-k", "%s" %self.CHAIN])
        else:
            subprocess.call(["fpocket", "-f", "%s%s.pdb" \
                %(self.pdbDIRECTION, self.PDB)])
        self.fileDirection = "%s%s_out/%s_info.txt" \
            %(self.pdbDIRECTION, self.PDB, self.PDB)

    def __extractPocket(self):
        pocket = open(self.fileDirection + "", "r").readlines()
        pocket_num = len(pocket) // 21
        features = []
        for index in range(pocket_num):
            cur_feature = []
            cur = pocket[index * 21 : (index + 1) * 21]
            for line in cur[1:-1]:
                cur_feature.append(float(line.split("\t")[2][:-1]))
            if len(cur_feature) == 18:
                warnings.warn("potential error in features of %s" \
                    %self.fileDirection)
            features.append(cur_feature)
        return features

    def __rank(self, cur_feature, index):
        score = [cur_feature[m][index] for m in range(len(cur_feature))]
        score = sorted(score, reverse = True)
        for p in range(len(cur_feature)):
            cur_feature[p].append(score.index(cur_feature[p][index]) + 1)
        return cur_feature

    def __collectFPocket(self):
        self.features = self.__extractPocket()
        # add additional ranking features
        self.features = np.array(self.features)

    def __graph(self, fileDirection, BOND_THRESHOLD = 10):
        # define atom and bond value
        atom_map = {"C": 12, "N": 14, "O": 16, "S": 32}
        pocket = open(fileDirection, "r").readlines()
        coordinates = []
        atom_type = []

        for line in pocket:
            if line[:4] == "ATOM":
                info = line.split()
                if len(info[-2]) == 1:
                    atom_type.append(info[-2])
                else:
                    atom_type.append(info[-1])
                try:
                    coordinates.append(list(map(float, info[6:9])))
                except:
                    try:
                        dot_index = info[7].index(".")
                        coordinates.append([float(info[6]), \
                            float(info[7][:dot_index+4]), \
                            float(info[7][dot_index+4:])])
                    except:
                        dot_index = info[6].index(".")
                        coordinates.append([float(info[6][:dot_index+4]), \
                            float(info[6][dot_index+4:]), float(info[7])])

        coordinates = np.array(coordinates)
        
        NUM_OF_NODES = len(atom_type)
        start_node = []
        end_node = []

        for i in range(NUM_OF_NODES):
            connected_index = []
            for j in range(i + 1, NUM_OF_NODES):
                distance = np.sqrt(sum(np.square(coordinates[i] \
                    - coordinates[j])))
                # if distance is within threshold
                if distance <= BOND_THRESHOLD:
                    connected_index.append(j)
            if connected_index:
                start_node.extend([i] * len(connected_index))
                end_node.extend(connected_index)
        
        u = start_node + end_node
        v = end_node + start_node

        g = dgl.DGLGraph()
        g.add_nodes(NUM_OF_NODES)
        g.add_edges(u, v)
        return g

    def __collectPockets(self):
        fileNames = glob.glob(self.pocketDirection + "*.pdb")
        fileNames = sorted(fileNames, key = \
            lambda x : int(x.split("pocket")[-1].split("_")[0]))
        self.pockets = []
        for fileN in fileNames:
            self.pockets.append(self.__graph(fileN, 10))

    def __collectModels(self):
        self.xgbmodels = pickle.load(open(self.modelDirection + "xgboost.pkl", "rb"))

        ## collect GCNN models
        model = GCNN.Classifier(1, 256, 2)
        self.gcnnmodels = []
        checkpoint = th.load(self.modelDirection + "GCNN.pt")
        for param in checkpoint.values():
            model.load_state_dict(param)
            self.gcnnmodels.append(model)

    def __extractResidue(self):
        pocketFiles = glob.glob(self.pocketDirection + "*.pdb")
        pocketFiles = sorted(pocketFiles, key = lambda x : \
            int(x[x.rfind("pocket") + 6:x.rfind("_")]))
        residues = []
        for index in range(min(3, len(pocketFiles))):
            curFile = open(pocketFiles[index], "r").readlines()
            curResidues = []
            for line in curFile:
                if line[:4] == "ATOM":
                    info = line.split()
                    curResidues.append(info[4] + ":" + info[3] + info[5])
            residues.append(" ".join(set(curResidues)))
        return residues

    def predict(self):
        self.__download()
        self.__runFPocket()
        self.__collectFPocket()
        self.__collectPockets()
        self.__collectModels()

        # predict using each model
        self.xgboostProbs = []
        for model in self.xgbmodels:
            self.xgboostProbs.append(model.predict_proba(self.features))

        self.xgboostProbs = np.array(self.xgboostProbs)
        self.xgboostProbs = np.mean(self.xgboostProbs, axis = 0)

        self.gcnnProbs = []
        for model in self.gcnnmodels:
            # Convert a list of tuples to two lists
            test_bg = dgl.batch(self.pockets)
            probs_Y = th.softmax(model(test_bg), 1)
            self.gcnnProbs.append(probs_Y.tolist())

        self.gcnnProbs = np.array(self.gcnnProbs)
        self.gcnnProbs = np.mean(self.gcnnProbs, axis = 0)

        # combine probabilities
        self.meanValues = (self.xgboostProbs + self.gcnnProbs) / 2
        residues = self.__extractResidue()

        for i in range(0, min(len(self.meanValues), 3)):
            print("Pocket %d: %.1f%%" %(i+1, self.meanValues[i][1]*100))
            print(residues[i])

        # remove intermediate files
        if not self.UPLOAD:
            os.system("rm %s.pdb" %self.PDB)
        if not self.save:
            os.system("rm -r %s%s_out" %(self.pdbDIRECTION, self.PDB))

