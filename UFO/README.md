# README in SSSFDM:

##  To run an example:
```bash
git clone https://github.com/restrepo/SimplifiedDM-SSSFDM-Toolbox
```

copy the SimplifiedDMSSSFDM folder into  `SimplifiedDM-SSSFDM-Toolbox/madgraph/models` dir.

## Prepare input param.card
Write input parameters for SPHENO from `./Input/LesHouches.in.SimplifiedDMSSSFDM`

### Compile SPHENO
```bash
cd SimplifiedDM-SSSFDM-Toolbox
```
Follow the instructions in index.ipynb to compile the sevaral parts.


### Run SPHENO

```bash
./SPHENO/bin/SPhenoSimplifiedDMSSSFDM ./Input/LesHouches.in.SimplifiedDMSSSFDM
```
The output is: `SPheno.spc.SimplifiedDMSSSFDM`
```bash
cp  SPheno.spc.SimplifiedDMSSSFDM ../Run/direcorio_con_cards/param_card.dat
```

## run model with madgraph

```bash
cd ../Run
../SimplifiedDM-SSSFDM-Toolbox/madgraph/mg5_aMC FFjll_3.mdg
```

## Final remarks

To run the model need madgraph version 2_3_3 with pythia-pgs and Delphes.

###	compile SPHENO:
```bash
cd SimplifiedDM-SSSFDM-Toolbox
cd SPHENO
make
make Model=SimplifiedDMSSSFDM
```




