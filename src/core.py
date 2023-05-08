from xrspatial.focal import focal_stats, apply, _calc_sum
from xrspatial.convolution import circle_kernel
from xarray.core.dataarray import DataArray
from geocube.api.core import make_geocube
import numpy as np
import pandas as pd
import rioxarray
import xarray
import geopandas
import tempfile
from typing import Optional


def experienced_density(raster: DataArray,
                        vector: geopandas.GeoDataFrame,
                        radius: Optional[int] = 10,
                        weighted: Optional[bool] = True):

    # do some sanity checks, such as testing whether
    # both raster and vector have the same crs
    # TODO: crs sanity checks

    # set no data equal to zero
    # DENOMINATOR =====
    raster.values[raster.values == raster.rio.nodata] = 0
    raster = raster.rio.set_nodata(0)

    # KERNEL =======
    # create the area for which we consider the experienced density
    kernel = circle_kernel(1, 1, radius)

    # NEIGHBORS =====
    # compute the sum within the passed kernel
    neigh = apply(raster, kernel, _calc_sum, "neighbors_sum")

    # NUMERATOR =======
    num_raster = neigh * raster

    # TODO: review this
    if raster.rio.crs.linear_units == 'metre':
        pass
    else:
        norm = np.cos(np.deg2rad(raster.y))
        num_raster *= norm

    vector = vector.assign(id=list(range(vector.geometry.shape[0])))

    num_raster = num_raster.rio.clip(vector.geometry.values, vector.crs, from_disk=True).drop("band")
    num_raster.name = 'numerator'
    num_raster_vector = make_geocube(vector_data=vector,
                                     measurements=["id"],
                                     like=num_raster,
                                     fill=0)
    num_raster_vector['pop'] = (num_raster.dims, num_raster.values, num_raster.attrs, num_raster.encoding)
    grouped_num = num_raster_vector.drop("spatial_ref").groupby(
        num_raster_vector.id).sum().rename({"pop": "pop_num"})
    grouped_num = xarray.merge([grouped_num]).to_dataframe()

    den_raster = raster.rio.clip(vector.geometry.values, vector.crs, from_disk=True).drop("band")
    den_raster.name = 'numerator'
    den_raster_vector = make_geocube(vector_data=vector,
                                     measurements=["id"],
                                     like=raster,
                                     fill=0)
    den_raster_vector['pop'] = (raster.dims, raster.values, raster.attrs, raster.encoding)
    grouped_den = den_raster_vector.drop("spatial_ref").groupby(
        den_raster_vector.id).sum().rename({"pop": "pop_den"})
    grouped_den = xarray.merge([grouped_den]).to_dataframe()

    expdendf = pd.concat([grouped_num, grouped_den], axis=1).assign(
        expden=lambda x: x.pop_num / x.pop_den)
    vector = pd.merge(vector, expdendf, on='id').drop(["pop_num", 'pop_den'], axis=1)

    return vector


if __name__ == '__main__':


    """
    grid = rioxarray.open_rasterio(r"../demos/data/esp_ppp_2020_UNadj.tiff", chunks='auto').sel(band=1)
    vector = geopandas.read_file(r"../demos/data/NUTS_RG_01M_2021_3035.geojson")
    vector = vector[(vector.LEVL_CODE == 3) & (vector.CNTR_CODE == 'ES')]
    vector2 = experienced_density(raster=grid, vector=vector, radius=100)
    vector2.to_file(r"exp.geojson")
    """
    df = geopandas.read_file(
        r"/Users/nicoforteza/Desktop/urban_bde/data/secciones-censales/secciones-censales_pop_2020.geojson")
    df= df.drop(['CDIS', 'CMUN', 'CPRO', 'CCA', 'CUDIS',
       'CLAU2', 'NPRO', 'NCA', 'CNUT0', 'CNUT1', 'CNUT2', 'CNUT3', 'NMUN', "mean_pop", "cells_pop", "sum_pop"], axis=1)
    print(df.columns)
    print(df.shape)
    df["density"] = df["density"].astype(np.dtype('float32'))
    df["expden"] = df["expden"].astype(np.dtype('float32'))
    df.to_file(r"/Users/nicoforteza/Desktop/expden/demos/data/secs.geojson")

