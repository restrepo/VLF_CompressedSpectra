#include <iostream>
#include <stdlib.h> 
#include <sstream>
#include <fstream>
#include <cmath>
#ifndef _significance10095_H_
#define _significanca10095_H_
using namespace std;
#endif

int main(int argc, char *argv[])
{

  ifstream sgnal,mcw,mctop,mcwz;
 ofstream ssb;
 int ndt=72000;
 
 sgnal.open("signal10095total.dat");
 mcw.open("wjetstotal.dat");
 mctop.open("singletoptotal.dat");
 mcwz.open("wztotal.dat");
 ssb.open("significance10095.dat");
// read list of cuts to be applied
  ifstream cuts;
  char cname[10];
  string str;
  int nmuonpt,njets,nljetpt,nmet,nmt,ndphi;
  double muonptcut[20];
  double njetscut[20];
  double ljetptcut[20];
  double metcut[20];
  double mtcut[20];
  double dphicut[20];

  cuts.open("CUTSINFO.DAT");
  std::getline(cuts,str);  
  cuts>>cname>>nmuonpt;
  for (int i=0;i<nmuonpt;i++) cuts>>muonptcut[i];
  cuts>>cname>>njets;
  for (int i=0;i<njets;i++) cuts>>njetscut[i];
  cuts>>cname>>nljetpt;
  for (int i=0;i<nljetpt;i++) cuts>>ljetptcut[i];
  cuts>>cname>>nmet;
  for (int i=0;i<nmet;i++) cuts>>metcut[i];
  cuts>>cname>>nmt;
  for (int i=0;i<nmt;i++) cuts>>mtcut[i];
  cuts>>cname>>ndphi;
  for (int i=0;i<ndphi;i++) cuts>>dphicut[i];
  cuts.close();

  ndt=nmuonpt*njets*nljetpt*nmet*nmt*ndphi;

 double lumi=100.0; // projected lumi in fb-1
 double lumisignal, lumiw,lumitop, lumiwz;
 double xs_wjets=3091500.0; //fb
 double xs_top=288170.0; //fb
 double xs_wz=22820.0; //fb
 double xs_signal=331.0;//fb

 double scale_signal,scale_w,scale_top,scale_wz;

 int sval[25000][16], wval[25000][16], tval[25000][16], wzval[25000][16];;
 double s_sb[25000][16];
 for (int i=0;i<ndt;i++){
   sgnal>>sval[i][0]>>sval[i][1]>>sval[i][2]>>sval[i][3]>>sval[i][4]>>sval[i][5]>>sval[i][6]>>sval[i][7]>>sval[i][8]>>sval[i][9]>>sval[i][10]>>sval[i][11]>>sval[i][12]>>sval[i][13]>>sval[i][14]>>sval[i][15];

 mcw>>wval[i][0]>>wval[i][1]>>wval[i][2]>>wval[i][3]>>wval[i][4]>>wval[i][5]>>wval[i][6]>>wval[i][7]>>wval[i][8]>>wval[i][9]>>wval[i][10]>>wval[i][11]>>wval[i][12]>>wval[i][13]>>wval[i][14]>>wval[i][15];

 mctop>>tval[i][0]>>tval[i][1]>>tval[i][2]>>tval[i][3]>>tval[i][4]>>tval[i][5]>>tval[i][6]>>tval[i][7]>>tval[i][8]>>tval[i][9]>>tval[i][10]>>tval[i][11]>>tval[i][12]>>tval[i][13]>>tval[i][14]>>tval[i][15];

mcwz>>wzval[i][0]>>wzval[i][1]>>wzval[i][2]>>wzval[i][3]>>wzval[i][4]>>wzval[i][5]>>wzval[i][6]>>wzval[i][7]>>wzval[i][8]>>wzval[i][9]>>wzval[i][10]>>wzval[i][11]>>wzval[i][12]>>wzval[i][13]>>wzval[i][14]>>wzval[i][15];

 lumisignal=sval[i][6]/xs_signal;
 lumiw=wval[i][6]/xs_wjets;
 lumiwz=wzval[i][6]/xs_wz;
 lumitop=tval[i][6]/xs_top;
 scale_signal= lumi/lumisignal;
 scale_w= lumi/lumiw;
 scale_wz= lumi/lumiwz;
 scale_top= lumi/lumitop;
 for (int j=6;j<16;j++){
   s_sb[i][j]=0.0;
   if (sval[i][j]>0) {
     s_sb[i][j]=sval[i][j]*scale_signal/(sqrt(sval[i][j]*scale_signal+wval[i][j]*scale_w+tval[i][j]*scale_top+wzval[i][j]*scale_wz));
   }
 }
 for (int j=0;j<6;j++){s_sb[i][j]=sval[i][j];}  
 }
 sgnal.close();
 mcw.close();
 mctop.close();
 // sort the significance array from higher to lower significance
 double temp;
 double itemp;
 for (int i=0;i<ndt;i++){
   for (int j=i+1;j<ndt;j++){
     if (s_sb[j][15]>s_sb[i][15]){
       for (int k=0;k<16;k++){
	 temp=s_sb[i][k];
	 s_sb[i][k]=s_sb[j][k];
	 s_sb[j][k]=temp;
	 itemp=sval[i][k];
	 sval[i][k]=sval[j][k];
	 sval[j][k]=itemp;
	 itemp=wval[i][k];
	 wval[i][k]=wval[j][k];
	 wval[j][k]=itemp;
	 itemp=tval[i][k];
	 tval[i][k]=tval[j][k];
	 tval[j][k]=itemp;	 
	 itemp=wzval[i][k];
	 wzval[i][k]=wzval[j][k];
	 wzval[j][k]=itemp;
       }
     }
   }
 }

for (int i=0;i<ndt;i++){
if ((wval[i][15]+tval[i][15])<1) continue;
  ssb<<"mupt"<<muonptcut[int(s_sb[i][0])]<<" "<<"njets"<<njetscut[int(s_sb[i][1])]<<" "<<"ljetpt"<<ljetptcut[int(s_sb[i][2])]<<" "
     <<"met"<<metcut[int(s_sb[i][3])]<<" "<<"mt"<<mtcut[int(s_sb[i][4])]<<" "<<"dphi-pi"<<dphicut[int(s_sb[i][5])]<<" ";
  for (int j=6;j<15;j++){
    ssb<<s_sb[i][j]<<" ";

  }
  ssb<<"s/sqrt(s+b)="<<s_sb[i][15]<<" ";
  ssb<<"nsignal="<<sval[i][15]<<"; nwjets="<<wval[i][15]<<" ; ntop="<<tval[i][15]<<" ; nwz="<<wzval[i][15]<<endl;
 } 
 ssb.close();
}
