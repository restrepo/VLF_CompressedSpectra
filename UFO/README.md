# README in SSSFDM:

##  To run an example:
```bash
git clone https://github.com/restrepo/SimplifiedDM-SSSFDM-Toolbox
```

copy the SimplifiedDMSSSFDM folder into  `SimplifiedDM-SSSFDM-Toolbox/madgraph/models` dir:
```bash
cp -r SimplifiedDMSSSFDM/ SimplifiedDM-SSSFDM-Toolbox/madgraph/models/
```

## Prepare input param.card
Write input parameters for SPHENO from `./Input/LesHouches.in.SimplifiedDMSSSFDM`

### Compile SPHENO
```bash
cd SimplifiedDM-SSSFDM-Toolbox/SPHENO
make
make Model=SimplifiedDMSSSFDM
cd -
```
Follow the instructions in index.ipynb to generate code for other tools like micrOMEGAS.

You must be now in the initial directory

### Run SPHENO

```bash
./SimplifiedDM-SSSFDM-Toolbox/SPHENO/bin/SPhenoSimplifiedDMSSSFDM ./Input/LesHouches.in.SimplifiedDMSSSFDM
```
The output is: `SPheno.spc.SimplifiedDMSSSFDM`
```bash
mv  SPheno.spc.SimplifiedDMSSSFDM Run/direcorio_con_cards/param_card.dat
```

## run model with madgraph

```bash
./SimplifiedDM-SSSFDM-Toolbox/madgraph/bin/mg5_aMC
# skip update
MG5_aMC>install pythia-pgs
MG5_aMC>install Delphes
MG5_aMC>exit
```



```bash
cd Run
../SimplifiedDM-SSSFDM-Toolbox/madgraph/bin/mg5_aMC FFjll_3.mdg
```

## Final remarks

* To run the model need madgraph version 2_3_3 with pythia-pgs and Delphes.





