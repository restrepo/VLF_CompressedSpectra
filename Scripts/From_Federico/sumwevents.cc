#include <iostream>
#include <stdlib.h> 
#include <sstream>
#include <fstream>
#ifndef _sumwevents_H_
#define _sumwevents_H_
using namespace std;
#endif

int main(int argc, char *argv[]) {

 int cutflow[10]={10*0};

 int scan[80000][16]={80000*16*0};
 ifstream datos;
 ofstream datostotal;
 std::string filename;
 int ndt=0;
 

 for (int i=1;i<184;i++) {
   cout<<" beginning to read file # "<<i<<endl;
   std::string sint; 
   ostringstream temp;  //temporal to convert integer to string
   temp<<i;
   sint=temp.str();
   filename= "wjets/results/wjets"+sint+".txt"; //putting together filename     
   cout<<"filename = "<<filename<<endl;
   const char* strname= filename.c_str();
   datos.open(strname);
   ndt=0;
   int ivalue[16];
   //  while (!datos.eof()) {
   // cout<<"reading line = "<<ndt<<endl;
   
   while(datos>>ivalue[0]>>ivalue[1]>>ivalue[2]>>ivalue[3]>>ivalue[4]>>ivalue[5]>>ivalue[6]>>ivalue[7]>>ivalue[8]>>ivalue[9]>>ivalue[10]>>ivalue[11]>>ivalue[12]>>ivalue[13]>>ivalue[14]>>ivalue[15]) { 
       //for (j=0;j<16;j++){
       //datos>>ivalue;
       //cout<<"ivalue ="<<ivalue<<endl;
     for (int j=0;j<16;j++){
      if (j>5) {
	 scan[ndt][j]=scan[ndt][j]+ivalue[j];
       }
       else {
	 scan[ndt][j]=ivalue[j];
       }
     }
     //     cout<<scan[ndt][0]<<" ... "<<scan[ndt][15]<<endl;
     ndt++;
   }
   datos.close();
 }

 cout<<" ndt ="<<ndt<<endl; 
 datostotal.open("wjetstotal.dat");
 for (int i=0;i<ndt;i++){
   for (int j=0;j<16;j++){
     datostotal<<scan[i][j]<<" ";
     //cout<<"scan("<<i<<","<<j<<")="<<scan[i][j]<<endl;
   }
   datostotal<<endl;
 }
 datostotal.close();
} //end program
