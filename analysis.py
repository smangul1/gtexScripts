import argparse
import csv
import sys
import os

csv.field_size_limit(sys.maxsize)


ap=argparse.ArgumentParser()
ap.add_argument('geneCounts',help='file with thegene Counts downlaod from GTEX portal')
ap.add_argument('metadata',help='metadata')
ap.add_argument('metadata2',help='metadata with details causeOfDeathDetailed.csv')
ap.add_argument('out',help='save to ')



args=ap.parse_args()




#filename <->sample

fileName_sampleName_d={}

#updated_manifest.csv:SRR1396057,G61971.K-562.2,RNA-Seq,GRCh37,SAMN02792987,BI,150,PAIRED,Solexa-230208,04-Oct-14,5895,2749,14-Jun-14,SRS637628,K-562-SM-5LZWR,RNA:Total RNA,Cells - Leukemia cell line (CML),1273876,590982,Bone Marrow,Yes,RNA_Seq (NGS),female,K-562-SM-5LZWR,K-562,PRJNA75899,GRU,Homo sapiens,ILLUMINA,SRP012682,<not provided>,<not provided>,phs000424,1,<not provided>,Cross-Sectional,Genotype-Tissue Expression (GTEx),GTEx

f=open("/u/home/s/serghei/collab/metadata/updated_manifest.csv")
csv_f=csv.reader(f)
next(csv_f,None)

for row in csv_f:
    fileName_sampleName_d[row[1]]=row[14]



sampleName={}
geneCounts={}

dict={}





sample_namesSet=set()

samplesSet=set()
indSet=set()

#-------------

#metadata
#SUBJID,sample,Assay_Type_s,InsertSize_l,MBases_l,MBytes_l,ReleaseDate_s,analyte_type_s,body_site_s,histological_type_s,molecular_data_type_s,sex_s
#GTEX-XUYS,GTEX-XUYS-0226-SM-47JX1,RNA-Seq,400,5122,2324,04-Jan-14,RNA:Total RNA,Adipose - Subcutaneous,Adipose Tissue,RNA_Seq (NGS),male

print "Open",args.metadata

f = open(args.metadata)
csv_f = csv.reader(f)
next(csv_f, None)  # skip the headers


dictHeader={}


samples=[]

for row in csv_f:
    dict[row[1]]=[ [],"","","","",[],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],0]
    sample_namesSet.add(row[1])




#1 - gene count for ENSG00000167286.5 TCR CD3D(TCR)
#2 - ENSG00000110448.6 TCR CD5(TCR)
#3 - ENSG00000081237.14 BCR B220(BCR)
#4 - ENSG00000177455.7 BCR CD19(BCR)
#5 - detailed metadata
#6 -IGH
#7 IGK
#8 - IGL
#9 - TRA
#10 - TRB
#11 -TRD
#12 - TRG
#13 - igblast exist


f.close()


f = open(args.metadata)
csv_f = csv.reader(f)
next(csv_f, None)  # skip the headers

for row in csv_f:
        samplesSet.add(row[1])
        indSet.add(row[0])
        dict[row[1]][0]=row




#------
#gene counts

print "Open ",args.geneCounts

f = open(args.geneCounts)
csv_f = csv.reader(f, delimiter="\t")
next(csv_f, None)  # skip the headers
next(csv_f, None)  # skip the headers



dictTemp={}

print 'GTEX-OHPJ-0006-SM-3LK6G' in sample_namesSet

sampleNamesCounts=set()



for row in csv_f:
    if row[0]=="Name":
        for i in range(2,len(row)):
            sampleNamesCounts.add(row[i])
            dictTemp[i]=row[i]

        print sample_namesSet.difference(sampleNamesCounts)
        print len(sample_namesSet.difference(sampleNamesCounts))


    if row[0]=="ENSG00000167286.5":

        for i in range(2,len(row)):
            if dictTemp[i] in sample_namesSet:
                
                dict[dictTemp[i]][1]=row[i]
            else:
                print dictTemp[i]
                print dict[dictTemp[i]]

    elif row[0]=="ENSG00000110448.6":
        for i in range(2,len(row)):
            if dictTemp[i] in sample_namesSet:
                dict[dictTemp[i]][2]=row[i]
    elif row[0]=="ENSG00000081237.14":
        for i in range(2,len(row)):
            if dictTemp[i] in sample_namesSet:
                dict[dictTemp[i]][3]=row[i]
    elif row[0]=="ENSG00000177455.7":
        for i in range(2,len(row)):
            if dictTemp[i] in sample_namesSet:
                dict[dictTemp[i]][4]=row[i]




sys.exit(1)





print "Number of individuals", len(indSet)





#------
#detailed metadata


print "Open ",args.metadata2

f = open(args.metadata2)
csv_f = csv.reader(f, delimiter="\t")
next(csv_f, None)  # skip the headers




for row in csv_f:
    if row[0]=="dbGaP_Subject_ID":
        header_detailedMetadata=row
    if row[1] in indSet:
        
        for key,val in dict.items():
            if val[0][0]==row[1]:
                
                
                dict[val[0][1]][5]=row






#6 -IGH
#7 IGK
#8 - IGL
#9 - TRA
#10 - TRB
#11 -TRD
#12 - TRG


#------
#alpha BCR TCR

#alpha diversity

#sample,richness,Shannon,InverseSimpson
#G62242.GTEX-14BIM-1226.2.unmapped_after_rRNA_lostHuman.fasta_TCRB_igblast.,0,0.0,0.0

for i in ('IGH',6), ('IGK',7),('IGL',8),('TRA',9),('TRB',10),('TRD',11),('TRG',12):
    print i[0]


    f=open('/u/home/s/serghei/collab/gtex_immune_newJune7/rop/alpha/alpha%s_VJ.csv' %(i[0]))
    csv_f=csv.reader(f)
    next(csv_f,None)
    for row in csv_f:
        fileName=row[0].split(".unmapped_")[0]
        sample=fileName_sampleName_d[fileName]
        if sample in samplesSet:
            dict[sample][i[1]][0]=row
            #file exist
            if os.path.exists('/u/home/s/serghei/collab/gtex_immune_newJune7/rop/alpha/alpha%s_VJ.csv' %(i[0])):
                dict[sample][13]=1
        else:
            print sample, "ERROR"
            sys.exit(1)
    f.close()
    f=open('/u/home/s/serghei/collab/gtex_immune_newJune7/rop/alpha/alpha%s_V.csv' %(i[0]))
    csv_f=csv.reader(f)
    next(csv_f,None)
    for row in csv_f:
        fileName=row[0].split(".unmapped_")[0]
        sample=fileName_sampleName_d[fileName]
        if sample in samplesSet:
            dict[sample][i[1]][1]=row
        else:
            print sample, "ERROR"
            sys.exit(1)
    f.close()
    f=open('/u/home/s/serghei/collab/gtex_immune_newJune7/rop2/%s.stat' %(i[0]))
    csv_f=csv.reader(f)
    next(csv_f,None)
    for row in csv_f:
        fileName=row[0].split(".unmapped_")[0]
        sample=fileName_sampleName_d[fileName]
        if sample in samplesSet:
            dict[sample][i[1]][2]=row
        else:
            print sample, "ERROR"
            sys.exit(1)
f.close()



out=open(args.out,'w')


header1=['SUBJID','sample','Assay_Type_s','InsertSize_l','MBases_l','MBytes_l','ReleaseDate_s','analyte_type_s','body_site_s','histological_type_s','molecular_data_type_s','sex_s']




headerImmuneIGH=['-','IGH_richness_VJ','IGH_Shannon_VJ','IGH_InverseSimpson_VJ','-','IGH_richness_V','IGH_Shannon_V','IGH_InverseSimpson_V','-','IGH_nV','IGH_nVJ']
headerImmuneIGK=['-','IGK_richness_VJ','IGK_Shannon_VJ','IGK_InverseSimpson_VJ','-','IGK_richness_V','IGK_Shannon_V','IGK_InverseSimpson_V','-','IGK_nV','IGK_nVJ']
headerImmuneIGL=['-','IGL_richness_VJ','IGL_Shannon_VJ','IGL_InverseSimpson_VJ','-','IGL_richness_V','IGL_Shannon_V','IGL_InverseSimpson_V','-','IGL_nV','IGL_nVJ']

headerImmuneTRA=['-','TRA_richness_VJ','TRA_Shannon_VJ','TRA_InverseSimpson_VJ','-','TRA_richness_V','TRA_Shannon_V','TRA_InverseSimpson_V','-','TRA_nV','TRA_nVJ']
headerImmuneTRB=['-','TRB_richness_VJ','TRB_Shannon_VJ','TRB_InverseSimpson_VJ','-','TRB_richness_V','TRB_Shannon_V','TRB_InverseSimpson_V','-','TRB_nV','TRB_nVJ']
headerImmuneTRD=['-','TRD_richness_VJ','TRD_Shannon_VJ','TRD_InverseSimpson_VJ','-','TRD_richness_V','TRD_Shannon_V','TRD_InverseSimpson_V','-','TRD_nV','TRD_nVJ']
headerImmuneTRG=['-','TRG_richness_VJ','TRG_Shannon_VJ','TRG_InverseSimpson_VJ','-','TRG_richness_V','TRG_Shannon_V','TRG_InverseSimpson_V','-','TRG_nV','TRG_nVJ']




#out.write(','.join(header1+['CD3D(TCR)','CD5(TCR)','B220(BCR)','CD19(BCR)']+header_detailedMetadata+headerImmune))
out.write(','.join(header1+['CD3D-TCR','CD5-TCR','B220-BCR','CD19-BCR']+headerImmuneIGH+headerImmuneIGK+headerImmuneIGL+headerImmuneTRA+headerImmuneTRB+headerImmuneTRD+headerImmuneTRG))



for key,val in dict.items():
    if val[13]==1:
        out.write('\n')

#out.write(','.join(val[0]+val[1:4]+val[5]+val[6][0]+val[6][1]+val[6][2])) # 5 needs to be fixed
        temp=[]
        temp=val[0]+val[1:5]
        for i in [6,7,8,9,10,11,12]:
            temp+=val[i][0]+val[i][1]+val[i][2]
    
        out.write(','.join(temp))

    #print ','.join(val[0]+val[1:4]+val[5]+val[6][0]+val[6][1]+val[6][2])
    #print ','.join(val[1:4])
    #print ','.join(val[5])
    #print ', '.join(val[6][0]+val[6][1]+val[6][2])
    
    
    


print "DONE!"




