# Written by Federico v.d.Pahlen 2017,10,29, modified from programs by Carlos Avila.
#input masses & XS. loop on masses.
# First time one runs the program: 
# set variable Background=1. Later, set to 0 to avoid reading already processed background event root-files.
# shell scripts should be executable (chmod ugo+x *.sh)
# check paths in *.sh: output in signal/results, wz/results, etc ; input /DiscoB/... 
# Uses only 1 set of signalevents for every point. To use several sets either
# a) modify sumsignalevents1.cc and scansignal1.sh
# b) or modify sumsignalevents.cc and scansignal.sh (currently for 5 sets).

# Output: significance.dat (check if its for last point), significancemax.dat 
# now output: significancenb.dat nsignalnb.dat (python list). Eventually modify order of data: now writes from DeltaM=10 to DeltaM=1.

if (("$#" != 5));
    then echo " illegal number of parameters ("$#"):\n massF_i massF_f DeltaM_i DeltaM_f [GeV] XS[fb, fi 331.5  or  0 to use fixed vals.]"
    echo " example: ./scanloop_xs.sh 100 150 1 10 0"
else
Background=1    #1: scan background also. check flag!!!

if (( $Background != 1 )); then
   echo "=================================================================================================="
   echo "warning! Background !=1, will not scan background (reads from last scan, ok cuts have not changed)"
   echo "=================================================================================================="
fi

# signal cross sections evaluated in madgraph, include cuts in run_card (=> smaller than wo cuts, prospino, etc.)
XS50=5135.7
XS60=1816.8
XS70=1032.2
XS80=668.4
XS90=461.6

XS100=331.5
XS105=284.8
XS110=246.5
XS115=214.2
XS120=187.3
XS125=164.6
XS130=145.3
XS135=128.9
XS140=114.5
XS145=102.2
XS150=91.5
XS155=82.3
XS160=74.2
XS165=67.0
XS170=60.7
XS175=55.1
XS180=50.1
XS185=45.8
XS190=41.8
XS195=38.3
XS200=35.1
#==========
# fyi: bkg XS: XSwj=...; XSwz=...; XSt=....
# generated raw events: nwj0=4031859; nwz0=45693 ; nt0=255207 
#==========

MassFi=$1
MassFf=$2
DeltaMi=$3
DeltaMf=$4
XS_input=$5
StepMassF=5
StepMassS=1

ln -sf   cutsinfo10095.dat CUTSINFO.DAT

 if (( $Background == 1 )); then
    g++ sumwevents.cc -o sumwevents
    g++ sumtopevents.cc -o sumtopevents 
    g++ sumwzevents.cc -o sumwzevents  
    source scanwjets.sh 1 183
    source scantop.sh 2 6
    source scanwz.sh 1 17
    ./sumwevents
    ./sumtopevents
    ./sumwzevents
 fi

 echo "# MassF   MassS   XS  signif  bkg: nwjets ntop nwz"  > significancemax.dat
 #start loops in MassF,MassS -----------------------------------
 #cross-sections evaluated with madgraph (see cuts in run_card).


 rm -f nsignaltmp.dat
 rm -f significancetmp.dat

 echo "[ " >> nsignaltmp.dat
 echo "[ " >> significancetmp.dat
 for MassF in `seq $MassFi $StepMassF $MassFf` ; do
   if (( $XS_input == 0 )); then
     if (($MassF == 100)); then XS=$XS100; 
     elif (($MassF == 105)); then XS=$XS105; 
     elif (($MassF == 110)); then XS=$XS110; 
     elif (($MassF == 115)); then XS=$XS115; 
     elif (($MassF == 120)); then XS=$XS120; 
     elif (($MassF == 125)); then XS=$XS125; 
     elif (($MassF == 130)); then XS=$XS130; 
     elif (($MassF == 135)); then XS=$XS135; 
     elif (($MassF == 140)); then XS=$XS140; 
     elif (($MassF == 145)); then XS=$XS145; 
     elif (($MassF == 150)); then XS=$XS150; 
     elif (($MassF == 145)); then XS=$XS145; 
     elif (($MassF == 150)); then XS=$XS150; 
     elif (($MassF == 155)); then XS=$XS155; 
     elif (($MassF == 160)); then XS=$XS160; 
     elif (($MassF == 165)); then XS=$XS165; 
     elif (($MassF == 170)); then XS=$XS170; 
     elif (($MassF == 175)); then XS=$XS175; 
     elif (($MassF == 180)); then XS=$XS180; 
     elif (($MassF == 185)); then XS=$XS185; 
     elif (($MassF == 190)); then XS=$XS190; 
     elif (($MassF == 195)); then XS=$XS195; 
     elif (($MassF == 200)); then XS=$XS200; 
     else XS=1000; echo "Warning, setting XS=1000  !!!!!!!!!!!" 
     fi
   else
     XS=$XS_input
   fi
  echo "using XS=$XS"

  MassSi=$(python -c "print (int($MassF - $DeltaMf + 0.00001))")
  MassSf=$(python -c "print (int($MassF - $DeltaMi + 0.00001))")

  #echo "debug: $MassF  $MassSi $MassSf "
  echo "[ " >> nsignaltmp.dat
  echo "[ " >> significancetmp.dat
  for MassS in `seq $MassSi $StepMassS $MassSf` ; do
     #echo "debug MassS: $MassS "

     sed -e 's/MassF/'$MassF'/g' -e 's/MassS/'$MassS'/g' sumsignalevents1.cc.gen > sumsignalevents1.cc
     sed -e 's/MassF/'$MassF'/g' -e 's/MassS/'$MassS'/g' -e 's/SignalXS/'$XS'/g' significancexs.cc.gen > significance.cc

     g++ sumsignalevents1.cc -o sumsignalevents1
     g++ significance.cc -o significance
     source scansignal1.sh 1 1 $MassF $MassS 
     ./sumsignalevents1

     ./significance
     sig=`awk '(NR == 1){print$15;}' significance.dat`
     nsignal=`awk '(NR == 1){print$17;}' significance.dat | sed -e 's/nsignal=/ /g' -e 's/;/ /g'`
     nwjets=`awk '(NR == 1){print$18;}' significance.dat | sed -e 's/nwjets=/ /g'`
     ntop=`awk '(NR == 1){print$20;}' significance.dat | sed -e 's/ntop=/ /g'`
     nwz=`awk '(NR == 1){print$22;}' significance.dat | sed -e 's/nwz=/ /g'`

     echo "$MassF  $MassS   $XS   $sig   $nsignal   $nwjets   $ntop   $nwz" >> significancemax.dat
     echo "$nsignal, " >> nsignaltmp.dat
     echo "$sig, " >> significancetmp.dat
     echo " =======   $MassF  $MassS  $XS  $sig : $nsignal , $nwjets , $ntop , $nwz  =======" 

  done
  echo "], " >> nsignaltmp.dat
  echo "], " >> significancetmp.dat
 done
 echo "] " >> nsignaltmp.dat
 echo "] " >> significancetmp.dat

 tr -d "\n\r" < significancetmp.dat > significance2tmp.dat
 sed -e 's/], ]/]  ]\n/g' -e 's/, ]/ ]/g' -e 's/\[ \[/signiflist=[ [/g' significance2tmp.dat > significancenp.dat
 tr -d "\n\r" < nsignaltmp.dat > nsignal2tmp.dat
 sed -e 's/], ]/]  ]\n/g' -e 's/, ]/ ]/g' -e 's/\[ \[/nsignallist=[ [/g' nsignal2tmp.dat > nsignalnp.dat

fi
wait
rm -f significancetmp.dat
rm -f significance2tmp.dat
rm -f nsignaltmp.dat
rm -f nsignal2tmp.dat
