import csv
import urllib
import urllib2
#this function receives a sequence and returns the reverse complement of the sequence.
def revcom(seq):
    answer=''
    for i in range(0,len(seq)):       
        if seq[i]== 'A':
            answer ='T'+answer
        elif seq[i]=='C':
            answer ='G'+answer
        elif seq[i]=='G':
           answer ='C'+answer
        elif seq[i]=='T':
            answer ='A'+answer
    return answer
#This code gets files containing masked sequences, finds crRNA in the unmasked regions, designs the homology arms and primers for genotyping that region
Number_of_Sequences=1
for k in range(0,Number_of_Sequences):
    address='Sequences/'+str(k)+'.txt'
    f = open(address, 'r')
    lines = f.readlines()
    lines = '\t'.join([line.strip() for line in lines])	
    gene = ''.join([line.strip() for line in lines])	
    url = 'http://crispr.dbcls.jp/'
    start=gene.find('N')+2
    nonmasked=''
    target_regions=[]
    for i in gene[start:len(gene)-1]:
    	if i=='N':
    		if len(nonmasked)>100:
    			target_regions.append(nonmasked)
    		nonmasked=''
    	else:
    		nonmasked=nonmasked+i

    finallist=[]
    # The script below subits each target region to the CRISPRdirect website and receives a response that is later saved in a file called crna_file.txt
    for i in target_regions:

        values = {'userseq' :i,
                  'format' : 'txt',
                  'download':'download'
                  }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        page = response.read()
        with open('crna_file.txt', 'w') as f:
            f.write(page)
        f.close
       
        #############################################################################################################################################################################
        # This part gets the crRNA in a file called crna_file.txt or a variable called temp and then screens it.
        # This secondary read and write was used to interface with other modules not used in this publication.
        ###############################################################################################################################################################################

        with open('crna_file.txt','r') as f:
            reader = csv.reader(f, delimiter="\t")
            temp = list(reader)
        f.close
        crRNA=[]
        
        for i in range(6,len(temp)-2):
            seq=temp[i][3]
            if int(temp[i][9])<10:                
                if int(temp[i][0])>50:
            		if int(temp[i][6])==0:
            			if int(temp[i][8])==1:
            				finallist.append(temp[i])

    #This section of the code saves the list of best cRNAs in a separate folder in csv format for the user to use.
    address2='crna/crna'+str(k)+'.csv'
    print finallist
    with open(address2, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(finallist)
    f.close 


