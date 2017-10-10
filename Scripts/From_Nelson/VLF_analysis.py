# First import the ROOT Python module.

# In[1]:

import ROOT
import os
import sys
from Generic import *

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
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
ROOT.gSystem.AddDynamicPath("/afs/cern.ch/work/n/nvanegas/public/MG5_aMC_v2_6_0/Delphes")
ROOT.gSystem.AddDynamicPath("/afs/cern.ch/work/n/nvanegas/public/MG5_aMC_v2_6_0/Delphes/external")
ROOT.gSystem.AddDynamicPath("/afs/cern.ch/work/n/nvanegas/public/MG5_aMC_v2_6_0/Delphes/external/ExRootAnalysis")


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

#Signal

SigSamples="/eos/user/j/jruizalv/VLF_Samples/SSSFDM_150Deltam10.root"
SigTSam=1
SigChain=ChainConstructor(SigSamples, TreeName, SigTSam)

#Background

#WjetsSamples="/eos/user/n/nvanegas/VLF_analysis/W+jets/tag_1_delphes_events10.root"
#WjetsTSam=1
#WjetsChain=ChainConstructor(WjetsSamples, TreeName, WjetsTSam)
WjetsChain=ROOT.TChain("Delphes")
#WjetsChain.Add("root://eoscms.cern.ch//eos/cms/store/user/nvanegas/BckgndW+Jets/*2*.root")
#WjetsChain.Add("root://eoscms.cern.ch//eos/cms/store/user/nvanegas/BckgndW+Jets/*3*.root")
#WjetsChain.Add("root://eoscms.cern.ch//eos/cms/store/user/nvanegas/BckgndW+Jets/*4*.root")


# In[8]:

WjetsChain.Add("root://eoscms.cern.ch//eos/cms/store/user/nvanegas/BckgndW+Jets/*18*.root")




# In[13]:

NrWJ = WjetsChain.GetEntries()


# In[14]:

NrSg = SigChain.GetEntries()


# In[ ]:

Trigger="(MissingET.MET>60.)&&(Jet[0].PT>60.)&&(Muon[0].PT>5.)"
Cut0="(Muon_size==1)"

FullCut=Trigger+"&&"+Cut0

TIMEStr=time.strftime("%H_%M_%S_%d_%m_%y")
PDFNames="Plots_Wjets_Signal_150DM10_"+TIMEStr
print "Plotting on:", PDFNames
HistFile= ROOT.TFile(PDFNames+".root", "recreate")

HToExtract=["Jet_size","Jet[0].PT","Jet[1].PT","Muon_size","Muon[0].PT","MissingET.MET",
            "TMath::Sqrt(2*Muon[0].PT*MissingET.MET*(1-TMath::Cos(deltaPhi(MissingET.Phi,Muon[0].Phi))))",#WE NEED TO INCLUDE MT DEFINITION
            "TMath::Abs(Jet[0].PT-MissingET.MET)/(Jet[0].PT+MissingET.MET)",
            "TMath::Abs(ScalarHT.HT-MissingET.MET)/(ScalarHT.HT+MissingET.MET)"]

Binning=["(15,0,15)","(100,0,1000)","(50,0,500)","(5,0,5)","(50,0,100)","(100,0,1000)",
         "(100,0,500)","(200,0,2)","(200,0,2)"]

EntriesListWjets=[]
EntriesListSignal=[]
c = ROOT.TCanvas()
for i in xrange(len(HToExtract)):
    HistName=HToExtract[i].replace("(","").replace(")","").replace("[","").replace("]","").replace(":","").replace(".","").replace("-","m").replace("+","p").replace(" ","_").replace("&&","_and_").replace("&","_and_").replace("*","_").replace(">","g").replace("<","l").replace(",","l").replace("/","d")
    print "Extracting "+HToExtract[i]
    #Extracting Wjets histogram
    HistNameWjets=HistName+"_Wjets"
    WjetsChain.Draw(HToExtract[i]+" >> "+HistNameWjets+Binning[i],FullCut)
    TemHisto1=ROOT.gDirectory.Get(HistNameWjets)
    EntriesListWjets.append(TemHisto1.GetEntries())
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
    print "one step more" #"Wjets entries=", EntriesListWjets[-1]
    #print "Signal entries=", EntriesListSignal[-1]
    print "-----------------------------------------"
    #del(TemHisto2)

print "Wjets cut flow:", EntriesListWjets
print "Signal cut flow:", EntriesListSignal

HistFile.Close()


# In[ ]:




# Cuts optimization

# In[ ]:

VariablesToCut=[['l',"","Muon[0].PT","(500,0,500)",FullCut],
                ['l',"","TMath::Sqrt(2*Muon[0].PT*MissingET.MET*(1-TMath::Cos(deltaPhi(MissingET.Phi,Muon[0].Phi))))","(500,0,500)"
                 ,FullCut+"&&(Muon[0].PT<20)"]] #],
#                ['l',"","TMath::Abs(ScalarHT.HT-MissingET.MET)/(ScalarHT.HT+MissingET.MET)","(200,0,2)"
#                 ,FullCut+"&&(Muon[0].PT<20)"+"&&(TMath::Sqrt(2*Muon[0].PT*MissingET.MET*(1-TMath::Cos(deltaPhi(MissingET.Phi,Muon[0].Phi))))<50)"]
#               ]

XSWjets=3091.5; # pb
XSSig=0.100 #0.008599; # pb
lumi=100 # fb-1
ws=(lumi*XSSig*1000.)/NrSg
wb=(lumi*XSWjets*1000.)/NrWJ
print "Signal weight =", ws
print "Signal events =", NrSg
print "Wjets weight = ", wb
print "Wjets events = ", NrWJ
print "Number of variables = ", len(VariablesToCut)


# In[ ]:

TIMEStr=time.strftime("%H_%M_%S_%d_%m_%y")
PDFNames="Varibl_Eff_WJet_DeltM10_"+TIMEStr
print "Plotting on:", PDFNames

XVariableAxis=["MET",
               "p_{T}(j_{1})",
               "p_{T}(j_{2})",
               "M_{T}(MET,#mu)",]
XVariableName=["MET",
               "PT1",
               "PT2",
               "MT MET MU"]
EffFile= ROOT.TFile(PDFNames+".root", "recreate")

for i in xrange(len(VariablesToCut)):
#    CurCanvScan = rootnotes.canvas("MyPlot", (600, 600)) ##vamos aqui
    CurCanvScan = YOURcanvas("MyPlot", (600, 600)) ##vamos aqui

    #Constructing efficiency histograms
    Var=i
    SignalMETEffHisto = GetEffHisto(VariablesToCut[Var][0],
                                VariablesToCut[Var][1],
                                SigChain,
                                "Signal",
                                VariablesToCut[Var][2],
                                VariablesToCut[Var][3],
                                VariablesToCut[Var][4])

    WjetsMETEffHisto = GetEffHisto(VariablesToCut[Var][0],
                                VariablesToCut[Var][1],
                                WjetsChain,
                                "Wjets",
                                VariablesToCut[Var][2],
                                VariablesToCut[Var][3],
                                VariablesToCut[Var][4])

    Z1Histo,ZAsimovHisto, SHisto, BHisto, Z3Histo, Z4Histo = GetZHistos(VariablesToCut[Var][0],
                                VariablesToCut[Var][1],
                                SigChain, ws,
                                WjetsChain, wb,
                                VariablesToCut[Var][2],
                                VariablesToCut[Var][3],
                                VariablesToCut[Var][4])

    METSoverWjets=SignalMETEffHisto.Clone("METSoverWjets")
    METSoverWjets.Sumw2(); METSoverWjets.Divide(WjetsMETEffHisto)
    
    #Histogram cosmetics
    WjetsMETEffHisto.SetStats(ROOT.kFALSE)
    WjetsMETEffHisto.SetLineStyle(7); SignalMETEffHisto.SetLineStyle(9); METSoverWjets.SetLineStyle(8)
    Z1Histo.SetLineStyle(6)#; ZAsimovHisto.SetLineStyle(2)
    WjetsMETEffHisto.SetLineWidth(2); SignalMETEffHisto.SetLineWidth(1); METSoverWjets.SetLineWidth(2)
    Z1Histo.SetLineWidth(3); ZAsimovHisto.SetLineWidth(3)
    WjetsMETEffHisto.SetLineColor(ROOT.kRed); SignalMETEffHisto.SetLineColor(ROOT.kGreen+1); METSoverWjets.SetLineColor(ROOT.kBlack)
    Z1Histo.SetLineColor(ROOT.kBlue)#; ZAsimovHisto.SetLineColor(ROOT.kOrange)
    Z1Histo.SetFillColor(ROOT.kBlue); ZAsimovHisto.SetFillColor(ROOT.kOrange)
    Z1Histo.SetFillStyle(3004); ZAsimovHisto.SetFillStyle(3005)
    ############################
    SHisto.SetStats(ROOT.kFALSE)
    SHisto.SetLineStyle(1); BHisto.SetLineStyle(2)
    SHisto.SetLineWidth(2); BHisto.SetLineWidth(1)
    SHisto.SetLineColor(ROOT.kGreen); BHisto.SetLineColor(ROOT.kRed)
    
    #Setting legend
    LEG=ROOT.TLegend(0.6,0.6,0.9,0.9)
    LEG.AddEntry(WjetsMETEffHisto, "#varepsilon(W+jets)", "l")
    LEG.AddEntry(ROOT.TObject(), GetMR(WjetsMETEffHisto), "")
    LEG.AddEntry(ROOT.TObject(), GetEWI(WjetsMETEffHisto), "")
    LEG.AddEntry(SignalMETEffHisto, "#varepsilon(S)", "l")
    LEG.AddEntry(ROOT.TObject(), GetMR(SignalMETEffHisto), "")
    LEG.AddEntry(ROOT.TObject(), GetEWI(SignalMETEffHisto), "")
    LEG.AddEntry(METSoverWjets, "#varepsilon(S)/#varepsilon(W+jets)", "l")
    #LEG.AddEntry(ROOT.TObject(), GetMR(METSoverZvv), "")
    #LEG.AddEntry(ROOT.TObject(), GetEWI(METSoverZvv), "")
    LEG.AddEntry(Z1Histo, "s/#sqrt{b}", "l")
    #LEG.AddEntry(ZAsimovHisto, "Asimov", "l")
    LEG.SetFillColor(0)
    
    #Setting legend for signal and background histos
    LEGSB=ROOT.TLegend(0.6,0.6,0.9,0.9)
    LEGSB.AddEntry(SHisto, "S", "l")
    LEGSB.AddEntry(ROOT.TObject(), GetMR(SHisto), "")
    LEGSB.AddEntry(ROOT.TObject(), GetEWI(SHisto), "")
    LEGSB.AddEntry(BHisto, "Wjets", "l")
    LEGSB.AddEntry(ROOT.TObject(), GetMR(BHisto), "")
    LEGSB.AddEntry(ROOT.TObject(), GetEWI(BHisto), "")
    LEGSB.SetFillColor(0)
    
    #Setting maximal value of first plotted histogram
    Maxima=[WjetsMETEffHisto.GetMaximum(), SignalMETEffHisto.GetMaximum(), METSoverWjets.GetMaximum()]
            #Z1Histo.GetMaximum()]#, ZAsimovHisto.GetMaximum()]
    WjetsMETEffHisto.SetMaximum(1.05*max(Maxima))
    
    #Setting maximal value of first plotted histogram
    MaximaSB=[SHisto.GetMaximum(), BHisto.GetMaximum()]
    SHisto.SetMaximum(1.05*max(MaximaSB))
    
    #Setting axis titles
    MinX=float(VariablesToCut[Var][3].split(",")[1])
    MaxX=float(VariablesToCut[Var][3].split(",")[-1][0:-1])
    Nbins=int(VariablesToCut[Var][3].split(",")[0][1:])
    WjetsMETEffHisto.SetTitle(";"+XVariableAxis[i]+";A.U./{0:.2f} ".format((MaxX-MinX)/Nbins)+"GeV")
    WjetsMETEffHisto.GetYaxis().SetTitleOffset(1.4)
    
    #Setting axis titles
    SHisto.SetTitle(";"+XVariableAxis[i]+";A.U./{0:.2f} ".format((MaxX-MinX)/Nbins)+"GeV")
    SHisto.GetYaxis().SetTitleOffset(1.4)
    
    #.GetXaxis().SetRangeUser(0,20)
    #.GetYaxis().SetRangeUser(0.1,6)
    #ROOT.gPad.SetLogy()
    
    #Plotting
    WjetsMETEffHisto.Draw("hist e"); SignalMETEffHisto.Draw("hist e same");
    METSoverWjets.Draw("E0 same")
    Z1Histo.Draw("E1 same")
    #ZAsimovHisto.Draw("E1 same")
    LEG.Draw()
    
    #if i==0:
    #    CurCanvScan.Print(PDFNames+".pdf(","Title:"+XVariableName[i])        
    ###elif i==len(VariablesToCut)-1:
    ###    CurCanvScan.Print(PDFNames+".pdf)","Title:"+XVariableName[i])
    #else:
    #    CurCanvScan.Print(PDFNames+".pdf","Title:"+XVariableName[i])
    #    
    ##Plotting
    #SHisto.Draw("hist e"); BHisto.Draw("hist e same")
    #LEGSB.Draw()
    #
    #if i==len(VariablesToCut)-1:
    #    CurCanvScan.Print(PDFNames+".pdf)","Title:"+XVariableName[i])
    #else:
    #    CurCanvScan.Print(PDFNames+".pdf","Title:"+XVariableName[i])
    
    WjetsMETEffHisto.Write(); SignalMETEffHisto.Write(); METSoverWjets.Write(); #Z1Histo.Write()#; ZAsimovHisto.Write()
    SHisto.Write(); BHisto.Write()#; Z3Histo.Write(); Z4Histo.Write()

EffFile.Close()


h = ROOT.TH1F("TracksPt","Tracks;Pt [GeV/c];#",128,0,64)
for event in f.events:
    for track in event.tracks:
        h.Fill(track.Pt())
c = ROOT.TCanvas()
h.Draw()
c.Draw()





