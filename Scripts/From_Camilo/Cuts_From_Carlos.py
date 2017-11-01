# First import the ROOT Python module.

# In[1]:

import ROOT
import os
import sys
from Generic import *

import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
from array import array
#import rootnotes
import time
import os
import commands as cmd

def YOURcanvas(name="icanvas", size=(800, 600)):
    """Helper method for creating canvas"""

    # Check if icanvas already exists
    canvas = ROOT.gROOT.FindObject(name)
    assert len(size) == 2
    if canvas:
        return canvas
    else:
        return ROOT.TCanvas(name, name, size[0], size[1])

# In[2]:
Delphes_Path="/afs/cern.ch/user/c/csalazar/WorkPublic/VLF_CompressedSpectra/Scripts/From_Nelson/Delphes"
ROOT.gSystem.AddDynamicPath(Delphes_Path)
ROOT.gSystem.AddDynamicPath(Delphes_Path +"/external")
ROOT.gSystem.AddDynamicPath(Delphes_Path +"/external/ExRootAnalysis")


ROOT.gROOT.ProcessLine("#include <math.h>")


# In[3]:

ROOT.gSystem.Load("libDelphes");


# In[4]:

ROOT.gROOT.Macro("rootphi.C")


#get_ipython().magic('jsroot on')


#If input samples is a list use 0 if is just one file use 1 on TSam variable
def ChainConstructor(Samples, TreeName, TSam):
    if TSam==1:
        MainChain=ROOT.TChain(TreeName)
        MainChain.Add(Samples)
        print Samples+" added!"
    elif TSam==0:
        MainChain=ROOT.TChain(TreeName)
        if cmd.getoutput("ls -l "+Samples+" | grep '^d'")!="":
            for filename in os.listdir(Samples):
                for newfile in os.listdir(Samples+filename):
                    NSamples=Samples+filename+'/'+ newfile  
                    MainChain.Add(NSamples)
                    print NSamples+" added!"
        else:
            for newfile in os.listdir(Samples):
                NSamples=Samples+'/'+ newfile  
                MainChain.Add(NSamples)
                print NSamples+" added!"
    return MainChain


# In[7]:

TreeName="Delphes"
SigTSam=1
Signalpath="/eos/user/j/jruizalv/VLF_Samples/"
SigName="SSSFDM_100Deltam1"
#SigName="SSSFDM_100Deltam2"
#SigName="SSSFDM_100Deltam3"
#SigName="SSSFDM_100Deltam5"
#SigName="SSSFDM_100Deltam10"
SigSamples=Signalpath+SigName+".root"

SigChain=ChainConstructor(SigSamples, TreeName, SigTSam)

#Background

#SingleTSamples="/eos/user/n/nvanegas/VLF_analysis/W+jets/tag_1_delphes_events10.root"
#SingleTTSam=1
#SingleTChain=ChainConstructor(SingleTSamples, TreeName, SingleTTSam)
SingleTChain=ROOT.TChain("Delphes")

#SingleTChain.Add("root://eosuser.cern.ch//eos/user/n/nvanegas/VLF_analysis/BackgndWZ/*.root")
SingleTChain.Add("root://eoscms.cern.ch//eos/cms/store/user/nvanegas/BckgndW+Jets/*.root")
#SingleTChain.Add("root://eosuser.cern.ch//eos/user/n/nvanegas/VLF_analysis/SingleT/*.root")
#BGName="BackgndWZ"
#BGName="BckgndW+Jets"
BGName="SingleT"

#SingleTChain.Add()


NrSingleT = SingleTChain.GetEntries()
print NrSingleT

NrSg = SigChain.GetEntries()
print NrSg

Trigger="(ScalarHT.HT>110.)&&(MissingET.MET>110.)"
Cut0="(Muon_size==1)"
Cut1="&&(Muon[0].PT<24.)"
Cut2="&&(Jet[0].PT>20.)"
Cut3="&&(TMath::Sqrt(2*Muon[0].PT*MissingET.MET*(1-TMath::Cos(deltaPhi(MissingET.Phi,Muon[0].Phi))))<50.)"
Cut4="&&(Jet_size>0.)"
Cut4="&&(TMath::Abs(deltaPhi(Muon.Phi,MissingET.Phi))>=0)"

FullCut=Trigger+"&&"+Cut0+Cut1+Cut2+Cut3+Cut4

TIMEStr=time.strftime("%H_%M_%S_")
PDFNames="Plots_"+SigName+"_"+BGName+"_"+TIMEStr
print "Plotting on:", PDFNames
HistFile= ROOT.TFile(PDFNames+".root", "recreate")

HToExtract=["Jet_size","Jet[0].PT","Jet[1].PT","Muon_size","Muon[0].PT","MissingET.MET",
            "TMath::Sqrt(2*Muon[0].PT*MissingET.MET*(1-TMath::Cos(deltaPhi(MissingET.Phi,Muon[0].Phi))))",#WE NEED TO INCLUDE MT DEFINITION
            "TMath::Abs(Jet[0].PT-MissingET.MET)/(Jet[0].PT+MissingET.MET)",
            "TMath::Abs(ScalarHT.HT-MissingET.MET)/(ScalarHT.HT+MissingET.MET)"]

Binning=["(15,0,15)","(100,0,1000)","(50,0,500)","(5,0,5)","(50,0,100)","(100,0,1000)",
         "(100,0,500)","(200,0,2)","(200,0,2)"]

EntriesListSingleT=[]
EntriesListSignal=[]
c = ROOT.TCanvas()
for i in xrange(len(HToExtract)):
    HistName=HToExtract[i].replace("(","").replace(")","").replace("[","").replace("]","").replace(":","").replace(".","").replace("-","m").replace("+","p").replace(" ","_").replace("&&","_and_").replace("&","_and_").replace("*","_").replace(">","g").replace("<","l").replace(",","l").replace("/","d")
    print "Extracting "+HToExtract[i]
    #Extracting SingleT histogram
    HistNameSingleT=HistName+"_SingleT"
    SingleTChain.Draw(HToExtract[i]+" >> "+HistNameSingleT+Binning[i],FullCut)
    TemHisto1=ROOT.gDirectory.Get(HistNameSingleT)
    EntriesListSingleT.append(TemHisto1.GetEntries())
    TemHisto1.Sumw2()
    TemHisto1.Scale(1./TemHisto1.Integral())
    TemHisto1.Write()
    TemHisto1.Draw()
    #del(TemHisto1)
    #Extracting Signal histogram
    HistNameSig=HistName+"_Sig"
    SigChain.Draw(HToExtract[i]+" >> "+HistNameSig+Binning[i],FullCut)
    TemHisto2=ROOT.gDirectory.Get(HistNameSig)
    EntriesListSignal.append(TemHisto2.GetEntries())
    TemHisto2.Sumw2()
    TemHisto2.Scale(1./TemHisto2.Integral())
    TemHisto2.Write()
    TemHisto2.Draw("same")
    c.Draw()
    #print "one more step - SingleT entries=", EntriesListSingleT[-1]
    #print "Signal entries=", EntriesListSignal[-1]
    print "-----------------------------------------"
    #del(TemHisto2)

#print "SingleT cut flow:", EntriesListSingleT
#print "Signal cut flow:", EntriesListSignal

HistFile.Close()


# In[ ]:




## Cuts optimization
# 
## In[ ]: delta phi entre el muon -met) - pi
#FullCut=FullCut
# 
#VariablesToCut=[['l',"","Muon[0].PT","(500,0,500)",FullCut],
#                ['l',"","TMath::Sqrt(2*Muon[0].PT*MissingET.MET*(1-TMath::Cos(deltaPhi(MissingET.Phi,Muon[0].Phi))))","(500,0,500)"
#                 ,FullCut],
#                ['l',"","Jet_size","(10,0,10)"
#                  ,FullCut],
#                ['l',"","TMath::Abs(ScalarHT.HT - MissingET.MET)/(ScalarHT.HT+MissingET.MET)","(10000,-1,30)"
#                 ,FullCut]]#,
#                #['l',"","TMath::Abs(ScalarHT.HT-MissingET.MET)/(ScalarHT.HT+MissingET.MET)","(200,0,2)"
#                # ,FullCut+"&&(Muon[0].PT<20)"+"&&(TMath::Sqrt(2*Muon[0].PT*MissingET.MET*(1-TMath::Cos(deltaPhi(MissingET.Phi,Muon[0].Phi))))<50)"+"&&(Jet_size < 4)"+"&&(TMath::Abs(ScalarHT.HT-MissingET.MET)/(ScalarHT.HT+MissingET.MET) < 0.4)"]
#                # ]
# 
#XSSingleT=22.82; # pb
#XSSig=0.100 #0.008599; # pb
#lumi=100 # fb-1
#ws=(lumi*XSSig*1000.)/NrSg
#wb=(lumi*XSSingleT*1000.)/NrSingleT
#print "Signal weight =", ws
#print "Signal events =", NrSg
#print "SingleT weight = ", wb
#print "SingleT events = ", NrSingleT
#print "Number of variables = ", len(VariablesToCut)
# 
# 
## In[ ]:
# 
#TIMEStr=time.strftime("%H_%M_%S_%d_%m_%y")
#PDFNames="Varibl_Eff_SingleT_DeltM10_"+TIMEStr
#print "Plotting on:", PDFNames
# 
#XVariableAxis=["MET",
#               "p_{T}(j_{1})",
#               "p_{T}(j_{2})",
#               "M_{T}(MET,#mu)",
#               "HT - MT div HT + MT"]
#XVariableName=["MET",
#               "PT1",
#               "PT2",
#               "MT MET MU",
#               "HT - MT div HT+MT"]
#EffFile= ROOT.TFile(PDFNames+".root", "recreate")
# 
#for i in xrange(len(VariablesToCut)):
##    CurCanvScan = rootnotes.canvas("MyPlot", (600, 600)) ##vamos aqui
#    CurCanvScan = YOURcanvas("MyPlot", (600, 600)) ##vamos aqui
# 
#    #Constructing efficiency histograms
#    Var=i
#    SignalMETEffHisto = GetEffHisto(VariablesToCut[Var][0],
#                                VariablesToCut[Var][1],
#                                SigChain,
#                                "Signal",
#                                VariablesToCut[Var][2],
#                                VariablesToCut[Var][3],
#                                VariablesToCut[Var][4])
# 
#    SingleTMETEffHisto = GetEffHisto(VariablesToCut[Var][0],
#                                VariablesToCut[Var][1],
#                                SingleTChain,
#                                "SingleT",
#                                VariablesToCut[Var][2],
#                                VariablesToCut[Var][3],
#                                VariablesToCut[Var][4])
# 
#    Z1Histo,ZAsimovHisto, SHisto, BHisto, Z3Histo, Z4Histo = GetZHistos(VariablesToCut[Var][0],
#                                VariablesToCut[Var][1],
#                                SigChain, ws,
#                                SingleTChain, wb,
#                                VariablesToCut[Var][2],
#                                VariablesToCut[Var][3],
#                                VariablesToCut[Var][4])
# 
#    METSoverSingleT=SignalMETEffHisto.Clone("METSoverSingleT")
#    METSoverSingleT.Sumw2(); METSoverSingleT.Divide(SingleTMETEffHisto)
#    
#    #Histogram cosmetics
#    SingleTMETEffHisto.SetStats(ROOT.kFALSE)
#    SingleTMETEffHisto.SetLineStyle(7); SignalMETEffHisto.SetLineStyle(9); METSoverSingleT.SetLineStyle(8)
#    Z1Histo.SetLineStyle(6)#; ZAsimovHisto.SetLineStyle(2)
#    SingleTMETEffHisto.SetLineWidth(2); SignalMETEffHisto.SetLineWidth(1); METSoverSingleT.SetLineWidth(2)
#    Z1Histo.SetLineWidth(3); ZAsimovHisto.SetLineWidth(3)
#    SingleTMETEffHisto.SetLineColor(ROOT.kRed); SignalMETEffHisto.SetLineColor(ROOT.kGreen+1); METSoverSingleT.SetLineColor(ROOT.kBlack)
#    Z1Histo.SetLineColor(ROOT.kBlue)#; ZAsimovHisto.SetLineColor(ROOT.kOrange)
#    Z1Histo.SetFillColor(ROOT.kBlue); ZAsimovHisto.SetFillColor(ROOT.kOrange)
#    Z1Histo.SetFillStyle(3004); ZAsimovHisto.SetFillStyle(3005)
#    ############################
#    SHisto.SetStats(ROOT.kFALSE)
#    SHisto.SetLineStyle(1); BHisto.SetLineStyle(2)
#    SHisto.SetLineWidth(2); BHisto.SetLineWidth(1)
#    SHisto.SetLineColor(ROOT.kGreen); BHisto.SetLineColor(ROOT.kRed)
#    
#    #Setting legend
#    LEG=ROOT.TLegend(0.6,0.6,0.9,0.9)
#    LEG.AddEntry(SingleTMETEffHisto, "#varepsilon(SingleT)", "l")
#    LEG.AddEntry(ROOT.TObject(), GetMR(SingleTMETEffHisto), "")
#    LEG.AddEntry(ROOT.TObject(), GetEWI(SingleTMETEffHisto), "")
#    LEG.AddEntry(SignalMETEffHisto, "#varepsilon(S)", "l")
#    LEG.AddEntry(ROOT.TObject(), GetMR(SignalMETEffHisto), "")
#    LEG.AddEntry(ROOT.TObject(), GetEWI(SignalMETEffHisto), "")
#    LEG.AddEntry(METSoverSingleT, "#varepsilon(S)/#varepsilon(SingleT)", "l")
#    #LEG.AddEntry(ROOT.TObject(), GetMR(METSoverZvv), "")
#    #LEG.AddEntry(ROOT.TObject(), GetEWI(METSoverZvv), "")
#    LEG.AddEntry(Z1Histo, "s/#sqrt{b}", "l")
#    #LEG.AddEntry(ZAsimovHisto, "Asimov", "l")
#    LEG.SetFillColor(0)
#    
#    #Setting legend for signal and background histos
#    LEGSB=ROOT.TLegend(0.6,0.6,0.9,0.9)
#    LEGSB.AddEntry(SHisto, "S", "l")
#    LEGSB.AddEntry(ROOT.TObject(), GetMR(SHisto), "")
#    LEGSB.AddEntry(ROOT.TObject(), GetEWI(SHisto), "")
#    LEGSB.AddEntry(BHisto, "SingleT", "l")
#    LEGSB.AddEntry(ROOT.TObject(), GetMR(BHisto), "")
#    LEGSB.AddEntry(ROOT.TObject(), GetEWI(BHisto), "")
#    LEGSB.SetFillColor(0)
#    
#    #Setting maximal value of first plotted histogram
#    Maxima=[SingleTMETEffHisto.GetMaximum(), SignalMETEffHisto.GetMaximum(), METSoverSingleT.GetMaximum()]
#            #Z1Histo.GetMaximum()]#, ZAsimovHisto.GetMaximum()]
#    SingleTMETEffHisto.SetMaximum(1.05*max(Maxima))
#    
#    #Setting maximal value of first plotted histogram
#    MaximaSB=[SHisto.GetMaximum(), BHisto.GetMaximum()]
#    SHisto.SetMaximum(1.05*max(MaximaSB))
#    
#    #Setting axis titles
#    MinX=float(VariablesToCut[Var][3].split(",")[1])
#    MaxX=float(VariablesToCut[Var][3].split(",")[-1][0:-1])
#    Nbins=int(VariablesToCut[Var][3].split(",")[0][1:])
#    SingleTMETEffHisto.SetTitle(";"+XVariableAxis[i]+";A.U./{0:.2f} ".format((MaxX-MinX)/Nbins)+"GeV")
#    #SingleTMETEffHisto.SetTitle(";"+XVariableAxis[i]+"GeV")
#    SingleTMETEffHisto.GetYaxis().SetTitleOffset(1.4)
#    
#    #Setting axis titles
#    SHisto.SetTitle(";"+XVariableAxis[i]+";A.U./{0:.2f} ".format((MaxX-MinX)/Nbins)+"GeV")
#    #SHisto.SetTitle(";"+XVariableAxis[i]+"GeV")
#    SHisto.GetYaxis().SetTitleOffset(1.4)
#    
#    #.GetXaxis().SetRangeUser(0,20)
#    #.GetYaxis().SetRangeUser(0.1,6)
#    #ROOT.gPad.SetLogy()
#    
#    #Plotting
#    SingleTMETEffHisto.Draw("hist e"); SignalMETEffHisto.Draw("hist e same");
#    METSoverSingleT.Draw("E0 same")
#    Z1Histo.Draw("E1 same")
#    #ZAsimovHisto.Draw("E1 same")
#    LEG.Draw()
#    
#    #if i==0:
#    #    CurCanvScan.Print(PDFNames+".pdf(","Title:"+XVariableName[i])        
#    ###elif i==len(VariablesToCut)-1:
#    ###    CurCanvScan.Print(PDFNames+".pdf)","Title:"+XVariableName[i])
#    #else:
#    #    CurCanvScan.Print(PDFNames+".pdf","Title:"+XVariableName[i])
#    #    
#    ##Plotting
#    #SHisto.Draw("hist e"); BHisto.Draw("hist e same")
#    #LEGSB.Draw()
#    #
#    #if i==len(VariablesToCut)-1:
#    #    CurCanvScan.Print(PDFNames+".pdf)","Title:"+XVariableName[i])
#    #else:
#    #    CurCanvScan.Print(PDFNames+".pdf","Title:"+XVariableName[i])
#    
#    SingleTMETEffHisto.Write(); SignalMETEffHisto.Write(); METSoverSingleT.Write(); Z1Histo.Write(); ZAsimovHisto.Write()
#    SHisto.Write(); BHisto.Write(); Z3Histo.Write(); Z4Histo.Write()
# 
#EffFile.Close()




