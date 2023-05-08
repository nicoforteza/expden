
# ☢️ WORK IN PROGRESS ❗️

# About

`expden` is a library that provides functions to calculate the 
experienced density, using a modern stack of GIS libraries in Python.

#### What is Experienced Density?

As described by [Diego Puga](https://diegopuga.org/papers/Duranton_Puga_JEP_2020.pdf):


_"Population or employment density is often used as a summary statistic to describe the spatial concentration of economic activity. In this context, density is commonly defined as the number of individuals per unit geographic area. Such "naive density" is easy to calculate. However, it may not appropriately reflect the density actually faced by the individual or firm at hand. One problem is that economic units are traditionally defined as aggregates of administrative units: for example, us metropolitan areas are defined based on counties. However, if a metro area includes some counties with substantial rural portions, such calculation will understate the density experienced by most economic actors. In particular, the match between urban and county boundaries is systematically looser for younger and less dense metropolitan areas in the West. De la Roca and Puga (2017) and and Henderson, Kriticos, and Nigmatulina (2020) have proposed measuring "experienced density" by counting population within a given radius around each individual. Such experienced density, in addition to dealing with the uneven tightness of area boundaries, captures better how close the typical individual is to other people when population is unevenly distributed. To give an illustrative example at the level of countries, where boundaries are given, the United States has nearly nine times the population of Canada with a slightly smaller surface area, so its naive density is ten times higher. And yet walking around cities and towns in both countries, one likely perceives similar concentrations of people nearby."_


#### How is it calculated?

Experienced density can be defined as population within K kilometres of the
average resident in a given area. To calculate it, we need a grid or raster and a vector file 
delineating the areas of interest:

 - Measure the number of people within a K kilometres 
radius of each cell in a population grid for given population grid. 
 - Compute, for all grid cells in area, the population-weighted average of this count of people within K kilometres.
Weighting by population is important, since otherwise we would be 
calculating population within K kilometres of the average place 
instead of within K kilometres of the average person.

You can use rasters of different nature. For example, rasters with data on pollution or particulate matter.
Go and see the docs for more!

# Installation and Requirements

For the installation of the package, you need a `Python >= 3.9.16` version. 
Please, take into account that you may need to install other GIS libraries in your system, such as GDAL or PROJ4.

To install the latest stable version of the library, please use `pip:

```
pip install expden
```

# References

This library abstracts the functionality needed to perform the experienced density calculations that 
you can see in the economic academic literature. Some references:

De la Roca, Jorge and Diego Puga. 2017. Learning by 
working in big cities. Review of Economic Studies 84(1): 
106-142.

Duranton, Gilles and Diego Puga. 2020. The economics
of urban density. Journal of Economic Perspectives 34(3): 
3-26.

Henderson, J. Vernon, Sebastian Kriticos, and Jamila 
Nigmatulina. 2020. Measuring urban economic density. 
Journal of Urban Economics (forthcoming).

