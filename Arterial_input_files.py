# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 16:24:03 2021

@author: uxowin10
"""

import os, glob, ntpath, shutil
import arcpy
#import geopandas as gpd
#from shapely.geometry import Point,Polygon,mapping
#from fiona.crs import from_epsg  
#from osgeo import gdal, ogr, os
import pandas as pd

input_data = r"J:\#UK_Pact_Project\Phase_I\Output"
output = r"J:\#UK_Pact_Project\PHASE_II\Arterial_input_files"
arcpy.env.scratchWorkspace = "J:\#UK_Pact_Project\PHASE_II\Arterial_input_files"
for cities in os.listdir(input_data):
    city = ntpath.basename(cities)
    print (city)
    for i in  range(4,5):
        for xx in glob.glob(r"%s\%s\urban_edge_t%s.*" %(input_data,city,i)):
            print (xx)
            src = xx
            #file_name = ntpath.basename(xx)[:-4]
            folder_path = r"%s\%s\Urban_edge" %(output, city)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            dest = shutil.copy(src, folder_path)
    for i in  range(4,5):
        for xx in glob.glob(r"%s\%s\urban_edge_t%s.shp" %(input_data,city,i)):
            print (xx)      
        
            city_b= r"%s\%s\Buffer" %(output, city)
            if not os.path.exists(city_b):
                os.makedirs(city_b)
        
            ue_buffer = r"%s\%s_urban_edge_t4_buffer.shp" %(city_b, city)
                
            arcpy.Buffer_analysis(xx, ue_buffer, "1000 METERS","FULL", "ROUND", "ALL")

            desc = arcpy.Describe(ue_buffer)
            sr = desc.spatialReference
            
            out_grid = r"%s\%s_urban_edge_t4_buffer_1km_grid.shp" %(city_b,city)
            
            arcpy.CreateFishnet_management(out_grid,str(desc.extent.lowerLeft),str(desc.extent.XMin) + " " + str(desc.extent.YMax),"1000","1000","0","0",str(desc.extent.upperRight),"NO_LABELS","#","POLYGON")
            arcpy.DefineProjection_management(out_grid, sr)
            print("%s_grid_done" % city)
        
            Art_grid= r"%s\Final_grid\%s" %(output, city)
            if not os.path.exists(Art_grid):
                os.makedirs(Art_grid)
                    

            grid_f = r"%s\%s_New_Arterial_study_area.shp" %(Art_grid, city) 
            arcpy.Clip_analysis(out_grid,ue_buffer,grid_f)

            arcpy.AddField_management(grid_f, "City", "TEXT", "", "","50")
            arcpy.CalculateField_management(grid_f, "City","'" + city + "'" , "PYTHON")
            print ("%s_done" % city)
