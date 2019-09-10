#coding=utf8
import arcpy
from arcpy import env
import datetime

in_GDBPaths =arcpy.GetParameterAsText(0)

saveGDBDir =arcpy.GetParameterAsText(1)
save_spatialReference=arcpy.GetParameterAsText(2)

gdbPathList=in_GDBPaths.split(';')

pFeaDsName=[]  #dataset name list
pFeaClsPathList=[]
pFeaName=[]

for gdbPath in gdbPathList:
    env.workspace =gdbPath
    dsList=arcpy.ListDatasets() 
    for ds in dsList:
        pFeaDsName.append(ds)   #get dataset name list
          
        FeaClsList=arcpy.ListFeatureClasses(feature_dataset=ds)
        for lis in FeaClsList:
            pFeaClsPathList.append(gdbPath+"\\"+ds+"\\"+lis)    #get featureClass path list
            pFeaName.append(lis)    # get featureClass name list
arcpy.AddMessage("Get Datasets and FeatureClasses  SuccessFully!")

pFeaName=list(set(pFeaName))
pFeaDsName=list(set(pFeaDsName))

#create db and dataset
time=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
dbName="MegerDB_"+time
arcpy.CreateFileGDB_management(saveGDBDir,dbName)
arcpy.AddMessage("Create db SuccessFully!")
dbpath=saveGDBDir+"\\"+dbName+".gdb"

for dsname1 in pFeaDsName:
    arcpy.CreateFeatureDataset_management(dbpath,dsname1,save_spatialReference)

arcpy.AddMessage("Create  Datasets SuccessFully!")

for dsname in pFeaDsName:
    for name in pFeaName:
        MegerList = []
        for pFeaPath in pFeaClsPathList:
            spList=pFeaPath.split('\\')

            if spList[-1]==name and spList[-2]==dsname:
                MegerList.append(pFeaPath)

        if len(MegerList)>1:
            try:
                arcpy.Merge_management(MegerList, dbpath + '\\' +dsname+"\\"+ name)
                #message="FeatureClass：{0} SuccessFully!".format(name)
                arcpy.AddMessage(name+":SuccessFully!")
            except Exception as e:
                arcpy.AddError("These is an error:")
                arcpy.AddError(e)
        elif len(MegerList)==1:
            try:
                arcpy.FeatureClassToFeatureClass_conversion(MegerList[0],dbpath + '\\' +dsname,name)

            except Exception as e:
                arcpy.AddError("These is an error:")
                arcpy.AddError(e)

arcpy.AddMessage('All Finish!')

