import pandas
import sys
import csv
import os
import argparse


ap = argparse.ArgumentParser()
ap.add_argument('csv1', help='csv1')
ap.add_argument('merged', help='merged csv')

args = ap.parse_args()





csv1 = pandas.read_csv(args.csv1)

#SUBJID,sample,Assay_Type_s,InsertSize_l,MBases_l,MBytes_l,ReleaseDate_s,analyte_type_s,body_site_s,histological_type_s,molecular_data_type_s,sex_s,CD3D(TCR),CD5(TCR),B220(BCR),CD19(BCR),-,IGH_richness_VJ,IGH_Shannon_VJ,IGH_InverseSimpson_VJ,-,IGH_richness_V,IGH_Shannon_V,IGH_InverseSimpson_V,-,IGH_nV,IGH_nVJ,-,IGK_richness_VJ,IGK_Shannon_VJ,IGK_InverseSimpson_VJ,-,IGK_richness_V,IGK_Shannon_V,IGK_InverseSimpson_V,-,IGK_nV,IGK_nVJ,-,IGL_richness_VJ,IGL_Shannon_VJ,IGL_InverseSimpson_VJ,-,IGL_richness_V,IGL_Shannon_V,IGL_InverseSimpson_V,-,IGL_nV,IGL_nVJ,-,TRA_richness_VJ,TRA_Shannon_VJ,TRA_InverseSimpson_VJ,-,TRA_richness_V,TRA_Shannon_V,TRA_InverseSimpson_V,-,TRA_nV,TRA_nVJ,-,TRB_richness_VJ,TRB_Shannon_VJ,TRB_InverseSimpson_VJ,-,TRB_richness_V,TRB_Shannon_V,TRB_InverseSimpson_V,-,TRB_nV,TRB_nVJ,-,TRD_richness_VJ,TRD_Shannon_VJ,TRD_InverseSimpson_VJ,-,TRD_richness_V,TRD_Shannon_V,TRD_InverseSimpson_V,-,TRD_nV,TRD_nVJ,-,TRG_richness_VJ,TRG_Shannon_VJ,TRG_InverseSimpson_VJ,-,TRG_richness_V,TRG_Shannon_V,TRG_InverseSimpson_V,-,TRG_nV,TRG_nVJ


list=['SUBJID','sample','Assay_Type_s','InsertSize_l','MBases_l','MBytes_l','ReleaseDate_s','analyte_type_s','body_site_s','histological_type_s','molecular_data_type_s','sex_s','CD3D-TCR','CD5-TCR','B220-BCR','CD19-BCR','-']



#merged['TotalSingle'] = merged.total*2



csv1['TotalSingle']=(csv1.MBases_l/150)*1000000*2





for column in csv1:
    name=csv1[column].name
    print name
    if "_prc" in name:
        csv1.drop(column, axis=1, inplace=True)





for column in csv1:
    name=csv1[column].name
    print name
    
    if name not in list and "-." not in name:
        print "|",name,"|"
        if "_prc" not in name:
            print "name,csv1[column]",name,csv1[column]
            newName=name+"_prc"
            ratio=int(csv1[column])/csv1.TotalSingle
            print newName,ratio
            csv1[newName] = ratio


csv1.to_csv(args.merged, index=False)


