from osgeo import gdal, osr
from gdal import gdalconst
filename = "F:\HOUDINI_14_playground\geo\geographics_DATA\L1-5 MSS\LM51960282013003NSG00.tif"
dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
print dataset

geotransform = dataset.GetGeoTransform()
originX = geotransform[0]
originY = geotransform[3]
srs = osr.SpatialReference()
srs.ImportFromWkt(dataset.GetProjection())

srsLatLong = srs.CloneGeogCS()
ct = osr.CoordinateTransformation(srs,srsLatLong)
print ct.TransformPoint(originX,originY)
"""
    adfGeoTransform[0] /* top left x */
    adfGeoTransform[1] /* w-e pixel resolution */
    adfGeoTransform[2] /* rotation, 0 if image is "north up" */
    adfGeoTransform[3] /* top left y */
    adfGeoTransform[4] /* rotation, 0 if image is "north up" */
    adfGeoTransform[5] /* n-s pixel resolution */ 


"""