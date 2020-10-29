# PASSer: Protein Allosteric Sites Server CLI

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)


This is the command line interface (CLI) for [PASSer](https://passer.smu.edu). 

## Dependencies

passerCLI depends on [FPocket](https://github.com/Discngine/fpocket). Please install and compile it first. 

The following modules are required and will be installed upon installation:

-   [dgl](https://github.com/dmlc/dgl) 0.4.3
-   [numpy](https://github.com/numpy/numpy)
-   [requests](https://github.com/psf/requests)
-   [scikit-learn](https://github.com/scikit-learn/scikit-learn) 0.23.2
-   [torch](https://github.com/pytorch/pytorch) 1.6.0
-   [xgboost](https://github.com/dmlc/xgboost) 1.2.0

## Install

```
git clone https://github.com/smutaogroup/passerCLI
cd passerCLI
python setup.py install init
```

## Usage

1. Users can either specify a PDB ID or the direction of a local PDB file. 
2. Chain ID is optional. If no chain ID is given, all chains in the PDB file will be analyzed. 
3. Top 3 pockets with corresponding probabilities and pocket residues are displayed on screen. 

```
usage: passer [-h] [-i ID] [-f FILE] [-c CHAIN]

PASSer CLI

optional arguments:
  -h, --help            show this help message and exit
  -i ID, --id ID        PDB ID
  -f FILE, --file FILE  PDB file
  -c CHAIN, --chain CHAIN
                        chain ID
```

**Example**:

Input:

```
passer -i 5DKK -c A
passer -f ./pdbFolder/5DKK.pdb -c A
passer -i 5DKK
```

Output:

```
Pocket 1: 89.6%
ASN262 VAL253 GLU308 GLN291 THR255 ARG288 ILE303 LEU290 CYS287 ASN286 ILE333 GLY348 ASN319 ILE307 PHE346 ARG304 LEU317 PHE331 GLN350 VAL300 ASP261 ASN329
Pocket 2: 20.2%
ASN251 GLN246 GLN250 GLY270 LYS352 SER268 ARG321 LEU274 GLN269 ASN273 TYR266 GLN249
Pocket 3: 16.8%
GLU301 LYS298 MET313 ALA306 GLU369 GLN309 ARG302 ASN311 LYS305 PRO297
```

## License

MIT
