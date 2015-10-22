# -*- coding: utf-8 -*-

"""
Spatial analysis utilities
"""

from shapely.wkt import loads
import pyproj
from shapely.ops import transform
from functools import partial


def get_xy_geo_object(geo_object):
    """
    returns the xy coordinates of a geo object
    """

    return loads(geo_object).xy


def get_wkt_length(geo_wkt):
    """
    :param geo_wkt: wkt string that represents a geometrical object like line
    example:
    'LINESTRING (8.6933590400000007 50.1097593399999965, 8.6857207800000005 50.1053506599999992)'
    :returns : the length of the object
    """

    return loads(geo_wkt).length


def geo_geodetic_to_cartesian(geo_wkt):
    """
    Transforms a wkt string of geodetic coordinates to cartesian coordinates
    :param geo_wkt: wkt string of geodetic coordinates
    :returns : wkt string object of cartesian coordinates
    - - - Transformation information - - -
    'EPSG:4326': LatLon with WGS84 datum used by GPS units and Google Earth
    'aea': 'Albers Equal Area is a conic, equal area map projection that uses
    two standard parallels. Although scale and shape are not preserved,
    distortion is minimal between the standard parallels.
    """

    geo = loads(geo_wkt)
    lon_vec = geo.xy[0]
    lat_vec = geo.xy[1]
    geo_transformed = transform(
        partial(pyproj.transform,
                pyproj.Proj(init='EPSG:4326'),
                pyproj.Proj(proj='aea',
                            lon=lon_vec,
                            lat=lat_vec)
            ),
        geo)

    return geo_transformed.wkt


def get_length_of_geo_object_array(geo_object_array):
    """
    :param geo_object_array: an numpy array of string, which of the represents
        an geo object
    example:
    array(['LINESTRING (8.69335904 50.10975934, 8.69335904 50.10975934)',
           'LINESTRING (8.69335904 50.10975934, 8.68572078 50.10535066)',
           'LINESTRING (8.68572078 50.10535066, 8.69335904 50.10975934)'])
    :returns: the total lenght of this object
    """

    total_length = 0
    for geo_object in geo_object_array:
        total_length += get_wkt_length(geo_object)

    return total_length
