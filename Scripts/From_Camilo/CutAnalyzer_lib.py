
# coding: utf-8

# Import from Python

# In[1]:

import pickle
import ROOT


# Import from ROOT

# In[2]:


#delphes should be on the system paths
ROOT.gSystem.Load("libDelphes");


# In[ ]:

def save_obj(obj, name):
    """
    To sabe objets in binary format
    """
    with open(name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
    To load objets from binary formats
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def CutMaker(Chain,LsOfCuts,LsOfPOandVOI,OutputPath):
    """
    Chain:
    
    LsOfCuts = {Physic_Objet:{VariableOfInteres:[(#Which_one,cut1),cut2,...]}}
        Physic_Objet: See final
        VariablesOfInteres(VOI): See final
        cut: String of a condition for the VOI
        #Which_one: To whom aply the cuts, if there is more than the leading one or aply.
                    If do not use a tuple is asumed that the cut is aplied to the leading one
                EJE:
                   LsOfCuts={
                                "Jet":
                                    {
                                    #Leading Jet PT greater than 60GeV
                                        "PT":[(0,">60")]
                                    },
                                "Muon":
                                    {
                                        #Leading Muon PT greater than 5GeV
                                        "PT":[(0,">5")],
                                        #number of Muon equal to one
                                        "Entries":["==1"]
                                    },
                                "MissingET":
                                    {
                                        #
                                        "MET":[">60"]
                                    }
                            }
                    
                    
    LsOfPOandVOI:[Physic_Objet,VariablesOfInteres] 
        Physic_Objet                         
        Jet,
            Entries	Number of jets in the event
            PT	jet transverse momentum
            Eta	jet pseudorapidity
            Phi	jet azimuthal angle
            Mass	jet invariant mass
            Flavor	jet flavor
            FlavorAlgo	jet flavor
            FlavorPhys	jet flavor
            BTag	0 or 1 for a jet that has been tagged as containing a heavy quark
            BTagAlgo	0 or 1 for a jet that has been tagged as containing a heavy quark
            BTagPhys	0 or 1 for a jet that has been tagged as containing a heavy quark
            TauTag	0 or 1 for a jet that has been tagged as a tau
            Charge	tau charge
            EhadOverEem	ratio of the hadronic versus electromagnetic energy deposited in the calorimeter
            NCharged	number of charged constituents
            NNeutrals	number of neutral constituents   
        Muon,
            Entries	Number of Muons in the event
            PT	muon transverse momentum
            Eta	muon pseudorapidity
            Phi	muon azimuthal angle
            T	particle arrival time of flight
            Charge	muon charge
            Particle	reference to generated particle
            IsolationVar	isolation variable
            IsolationVarRhoCorr	isolation variable
            SumPtCharged	isolation variable
            SumPtNeutral	isolation variable
            SumPtChargedPU	isolation variable
            SumPt	isolation variable
        Electron,
            Same as Muon
        
        Photon  
            Same as Muon
            Charge	DO NOT HAVE 
            E	photon energy
        
        ScalarHT
            HT	scalar sum of transverse momenta
            
        MissingET 
            MET	mising transverse energy
            Eta	mising energy pseudorapidity
            Phi	mising energy azimuthal angle
            
    VariablesOfInteres:
        One, or more than one of the propreties of the Physic Object
                        
    """
    #The ExRootTreeReader objet
    treeReader = ROOT.ExRootTreeReader(Chain)
    numberOfEntries = treeReader.GetEntries()

    # Counters to 0
    #No tiene en cuenta las variables de los multiparticulas (varios jets)
    #Y crea una variable que no se va a usar
    counts={}
    PhOb=LsOfCuts.keys()
    Branches=[]
    #If is empty return error
    for i in PhOb:
        #List to get branches
        Branches.append(i)
        VaOfIn=LsOfCuts[i]
        #If is empty return error
        Cuts=VaOfIn.keys()
        #If is empty return error
        for j in Cuts:
            cut_base=VaOfIn[j]
            for cut_ in cut_base:
                if isinstance(cut_, tuple):
                    counts["Count_"+i+"["+str(cut_[0])+"]"+j+cut_[1]] = 0
                else:
                    counts["Count_"+i+j+cut_]=0
        
    #get the branches I am going to use
    PhyObj={}
    #Branches=["Jet","Muon","MissingET","ScalarHT","Photon","Electron"]
    for branch in Branches:
        PhyObj[branch] = treeReader.UseBranch(branch)
        
    # Loop over events
    for entry in range(0, numberOfEntries):
        #Get the entry
        treeReader.ReadEntry(entry)
        
        # Cuts over jets
        if LsOfCuts.has_key('Jet'):                         #Cuts over Jets?
            if PhyObj["Jet"].GetEntries() > 0:              #There are any Jets in the data
                VaOfIn=LsOfCuts['Jet']                      #Which cuts over jets
                
                if VaOfIn.has_key('Entries'):
                    Cuts=VaOfIn['Entries']
                    for cut_ in Cuts:               #run over all the Entries cuts 
                        flag=False
                        filt=cut_
                        #Evaluate the condition
                        mycode="flag = True if PhyObj['Jet'].GetEntries() "+filt+" else False" 
                        exec(mycode)
                        if flag:                    #Counts
                            name="Count_JetEntries"+filt
                            counts[name] += 1
                        
                    
                if VaOfIn.has_key('PT') and PhyObj["Jet"].GetEntries() > 0:                    #If ther are cut over PT
                    Cuts=VaOfIn['PT']
                    for cut_ in Cuts:               #run over all the PT cuts 
                        if isinstance(cut_, tuple):     #See if is tuple
                            flag=False
                            filt=cut_[1]
                            #See if there are enough entries to evaluate
                            if(PhyObj["Jet"].GetEntries() <= cut_[0]):
                                jet= PhyObj["Jet"].At(cut_[0])
                                #Evaluate the condition
                                mycode="flag = True if jet.PT "+filt+" else False" 
                                exec(mycode)
                            if flag:                    #Counts
                                name="Count_Jet["+str(cut_[0])+"]PT"+cut_[1]
                                counts[name] += 1
                        else:           #Evaluate the condition for the avaible jets 
                            for l in range(0, PhyObj["Jet"].GetEntries() ):
                                jet = PhyObj["Jet"].At(l)
                                flag=False
                                filt=cut_
                                #Evaluate the condition
                                mycode="flag = True if jet.PT "+filt+" else False" 
                                exec(mycode)
                                if flag:                    #Counts
                                    name="Count_Jet["+str(l)+"]PT"+filt
                                    if counts.has_key(name):
                                        counts[name] += 1
                                    else:
                                        counts[name] = 1
                
                if VaOfIn.has_key('Eta'):
                    print "Jet Eta Not implementet yet"
                if VaOfIn.has_key('Phi'):
                    print "Jet Phi Not implementet yet"
                if VaOfIn.has_key('Mass'):
                    print "Jet Mass Not implementet yet"
                if VaOfIn.has_key('Flavor'):
                    print "Jet Flavor Not implementet yet"
                if VaOfIn.has_key('FlavorAlgo'):
                    print "Jet FlavorAlgo Not implementet yet"
                if VaOfIn.has_key('FlavorPhys'):
                    print "Jet FlavorPhys Not implementet yet"
                if VaOfIn.has_key('BTag'):
                    print "Not BTag implementet yet"
                if VaOfIn.has_key('BTagAlgo'):
                    print "Jet BTagAlgo Not implementet yet"
                if VaOfIn.has_key('BTagPhys'):
                    print "Jet BTagPhys Not implementet yet"
                if VaOfIn.has_key('TauTag'):
                    print "Jet TauTag Not implementet yet"
                if VaOfIn.has_key('Charge'):
                    print "Jet Charge Not implementet yet"
                if VaOfIn.has_key('EhadOverEem'):
                    print "Jet EhadOverEem Not implementet yet"
                if VaOfIn.has_key('NCharged'):
                    print "Jet NCharged Not implementet yet"
                if VaOfIn.has_key('NNeutrals'):
                    print "Jet NNeutrals Not implementet yet"
            #END IF JETS >0
        #END IF JET KEY

        
        # Cuts over Leptons and Photons
        # Made general
        #creo una lista de keys de leptones y corro sobre la lista
        """
        Entries	Number of Muons in the event
        PT	muon transverse momentum
        Eta	muon pseudorapidity
        Phi	muon azimuthal angle
        T	particle arrival time of flight
        Charge	muon charge
        Particle	reference to generated particle
        IsolationVar	isolation variable
        IsolationVarRhoCorr	isolation variable
        SumPtCharged	isolation variable
        SumPtNeutral	isolation variable
        SumPtChargedPU	isolation variable
        SumPt	isolation variable
        """
        if LsOfCuts.has_key('Muon'): 
            VaOfIn=LsOfCuts['Muon']                      #Which cuts over jets
            if VaOfIn.has_key('Entries'):
                Cuts=VaOfIn['Entries']
                for cut_ in Cuts:               #run over all the Entries cuts 
                    flag=False
                    filt=cut_
                    #Evaluate the condition
                    mycode="flag = True if PhyObj['Muon'].GetEntries() "+filt+" else False" 
                    exec(mycode)
                    if flag:                    #Counts
                        name="Count_MuonEntries"+filt
                        counts[name] += 1
                    
                
            if VaOfIn.has_key('PT') and PhyObj["Muon"].GetEntries() > 0:        #If ther are cut over PT
                Cuts=VaOfIn['PT']
                for cut_ in Cuts:               #run over all the PT cuts 
                    if isinstance(cut_, tuple):     #See if is tuple
                        flag=False
                        filt=cut_[1]
                        #See if there are enough entries to evaluate
                        if(PhyObj["Muon"].GetEntries() <= cut_[0]):
                            muon= PhyObj["Muon"].At(cut_[0])
                            #Evaluate the condition
                            mycode="flag = True if muon.PT "+filt+" else False" 
                            exec(mycode)
                        if flag:                    #Counts
                            name="Count_Muon["+str(cut_[0])+"]PT"+cut_[1]
                            counts[name] += 1
                    else:           #Evaluate the condition for the avaible jets 
                        for l in range(0, PhyObj["Muon"].GetEntries() ):
                            muon = PhyObj["Muon"].At(l)
                            flag=False
                            filt=cut_
                            #Evaluate the condition
                            mycode="flag = True if muon.PT "+filt+" else False" 
                            exec(mycode)
                            if flag:                    #Counts
                                name="Count_Muon["+str(l)+"]PT"+filt
                                if counts.has_key(name):
                                    counts[name] += 1
                                else:
                                    counts[name] = 1

            
            
            
            
            if VaOfIn.has_key('Eta'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('Phi'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('T'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('Charge'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('Particle'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('IsolationVar'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('IsolationVarRhoCorr'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('SumPtCharged'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('SumPtNeutral'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('SumPtChargedPU'):
                print "Muon  Not implementet yet"
            if VaOfIn.has_key('SumPt'):
                print "Muon  Not implementet yet"
         
        
        # Cuts over MET
        """ 
        MET	mising transverse energy
        Eta	mising energy pseudorapidity
        Phi	mising energy azimuthal angle
        """
        if LsOfCuts.has_key('MissingET'):                   #Cuts over MissingET?
            VaOfIn=LsOfCuts['MissingET']                      #Which cuts over jets
            if VaOfIn.has_key('MET') and PhyObj["MissingET"].GetEntries() > 0:        #If ther are cut over PT
                Cuts=VaOfIn['MET']
                for cut_ in Cuts:               #run over all the PT cuts 
                    flag=False
                    filt=cut_
                    met= PhyObj["MissingET"].At(0)
                    #Evaluate the condition
                    mycode="flag = True if met.MET "+filt+" else False" 
                    exec(mycode)
                    if flag:                    #Counts
                        name="Count_MissingETMET"+filt
                        counts[name] += 1    
                
                
                
                
                
            if VaOfIn.has_key('Eta'):
                print "MissingET Eta Not implementet yet"
            if VaOfIn.has_key('Phi'):
                print "MissingET Phi Not implementet yet"
