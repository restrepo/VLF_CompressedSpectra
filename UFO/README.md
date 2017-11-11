# README in SSSFDM:

##  To run an example:
```bash
git clone https://github.com/restrepo/SimplifiedDM-SSSFDM-Toolbox
```

copy the SimplifiedDMSSSFDM folder into  `SimplifiedDM-SSSFDM-Toolbox/madgraph/models` dir:
```bash
cp -r SimplifiedDMSSSFDM/ SimplifiedDM-SSSFDM-Toolbox/madgraph/models/
```

### Compile SPHENO
```bash
cd SimplifiedDM-SSSFDM-Toolbox/SPHENO
make
make Model=SimplifiedDMSSSFDM
cd -
```
Optional: Follow the instructions in index.ipynb to generate code for other tools like micrOMEGAS.

You must be now in the initial directory

### Run SPHENO
This check was done on November 11, 2017 17:00

The Benchmark point chossen have
* MF=150 GeV
* MS=140 GeV 
* Other input
```
Block MINPAR      # Input parameters 
1   2.5500000E-01    # Lambda1IN
2   0.0000000E+00    # LamSHIN
3   0.1000000E+00    # LamSIN
4   1.9600000E+04    # MS2Input
5   1.5000000E+02    # MSFIN
```
The output, to be used as the `madgraph param.card.dat`, is obtained with:
```bash
./SimplifiedDM-SSSFDM-Toolbox/SPHENO/bin/SPhenoSimplifiedDMSSSFDM ./Input/LesHouches.in.SimplifiedDMSSSFDM
```
The output is: `SPheno.spc.SimplifiedDMSSSFDM`
```bash
mv  SPheno.spc.SimplifiedDMSSSFDM Run/direcorio_con_cards/param_card.dat
```

## Install madgraph tools
Requires CERN-Root installation and setup 

```bash
./SimplifiedDM-SSSFDM-Toolbox/madgraph/bin/mg5_aMC
# skip update
MG5_aMC>install pythia-pgs
MG5_aMC>install Delphes
MG5_aMC>exit
```

## run model with madgraph

```bash
cd Run
../SimplifiedDM-SSSFDM-Toolbox/madgraph/bin/mg5_aMC FFjll_3.mdg
```

## Test

* Check root file:
```bash
if [ ! -f "FFjll_3/Events/run_01/tag_1_delphes_events.root" ];then echo ERROR: run failed;fi
```
* Compare header of event file
```bash
gunzip FFjll_3/Events/run_01/events.lhe
grep -B10000 "</header>" FFjll_3/Events/run_01/events.lhe > /tmp/header.lhe
diff header.lhe /tmp/header.lhe
# an empty output is expected for this diff command
gzip FFjll_3/Events/run_01/events.lhe
```

## Final remarks

* To run the model madgraph version 2_3_3  is requiered with pythia-pgs and Delphes installed.





