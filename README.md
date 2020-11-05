# PASSer: Protein Allosteric Sites Server CLI

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4154958.svg)](https://doi.org/10.5281/zenodo.4154958)


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

1. The user can either specify a PDB ID or the direction of a local PDB file. 
2. Chain ID is optional. If no chain ID is given, all chains in the PDB file will be analyzed. 
3. The user can choose to save FPocket results. By default, all generated files will be deleted when calculation is finished. 
4. Top 3 pockets with corresponding probabilities and pocket residues are displayed on screen. 

```
usage: passer [-h] [-i ID] [-f FILE] [-c CHAIN] [-s SAVE]

PASSer CLI

optional arguments:
  -h, --help            show this help message and exit
  -i ID, --id ID        PDB ID
  -f FILE, --file FILE  PDB file
  -c CHAIN, --chain CHAIN
                        chain ID
  -s SAVE, --save SAVE  save FPocket results (y/n)
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
A:GLU308 A:CYS287 A:GLY348 A:PHE346 A:ASN286 A:ILE333 A:ILE303 A:PHE331 A:VAL300 A:ILE307 A:VAL253 A:ASN262 A:THR255 A:ASN319 A:GLN350 A:ASP261 A:ARG304 A:ARG288 A:LEU317 A:GLN291 A:ASN329 A:LEU290
Pocket 2: 20.2%
A:GLN246 A:GLN250 A:LYS352 A:LEU274 A:ASN251 A:GLN269 A:TYR266 A:ARG321 A:ASN273 A:SER268 A:GLN249 A:GLY270
Pocket 3: 16.8%
A:ASN311 A:LYS298 A:GLU301 A:GLN309 A:PRO297 A:LYS305 A:ALA306 A:GLU369 A:MET313 A:ARG302
```

## License

MIT
