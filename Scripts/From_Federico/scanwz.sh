if (("$#" != 2)); 
    then echo " illegal number of parameters ("$#"): ifilenum ffilenum"
else
 make compile_ROOT_Delphes
 typeset -i start=$1
 typeset -i end=$2

 for ((j=$start;j<=$end;j++))
        do
	      #ln -sf /DiscoB/temp/temp_cavila/wz/results/wz$j.txt OUTFILE.TXT
	      ln -sf wz/results/wz$j.txt OUTFILE.TXT
       ./scan /DiscoB/temp/temp_cavila/wz/tag_1_delphes_events$j.root  
 done
fi


   