from casa import *
import numpy as np
import os
import collections
import json
import argparse
from process_ms import CASA_Imaging


def create_model(infile, cal_sources, model_name):
    for _, params in cal_sources.iteritems():
        cl.addcomponent(**params)
    cl.rename(model_name)
    cl.close()
    ft(infile, complist=model_name, usescratch=True)


def convert_json(data):
    if isinstance(data, basestring):
        return data.encode("utf-8")
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_json, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_json, data))
    else:
        return data


def rad_to_hms(angle):
    """
    Converts an angle in radians to a right ascension

    Parameters
    ----------
    angle : float
        angle to be converted in radians

    Returns
    -------
    ra : string
        right ascension calculated from the angle given in hours, minutes, and seconds
    """
    if angle < 0:
        angle += 2 * np.pi
    time = (angle / (2 * np.pi)) * 24
    hours = int(time)
    time = (time % 1) * 60
    mins = int(time)
    secs = (time % 1) * 60
    ra = str(hours) + "h" + str(mins) + "m" + str(secs) + "s"
    return ra


def dd_to_dms(degs):
    """
    Converts an angle in decimal degrees to a degrees, minutes, and seconds

    Parameters
    ----------
    angle : float
        angle to be converted in decimal degrees

    Returns
    -------
    ra : string
        right ascension calculated from the angle given in degrees, minutes, and seconds
    """
    neg = degs < 0
    degs = (-1) ** neg * degs
    degs, d_int = np.modf(degs)
    mins, m_int = np.modf(60 * degs)
    secs = 60 * mins
    if neg:
        return str(int(-d_int)) + "d" + str(int(m_int)) + "m" + str(secs) + "s"
    return str(int(d_int)) + "d" + str(int(m_int)) + "m" + str(secs) + "s"


def find_ra_dec(folder):
    tb.open(os.path.join(folder, "SOURCE"))
    angle_ra = tb.getcol("DIRECTION")[0][0]
    angle_dec = tb.getcol("DIRECTION")[1][0]
    tb.close()
    return angle_ra, angle_dec


def set_mask(ra, dec, srcs, path, mask_size="32000arcsec", imsize=512, cell_size=250):
    """
    Sets an cleaning mask over a specified region given and array of sources

    Parameters
    ----------
    ra : float (or list)
        Right ascension of the masked source
    dec : float (or list)
        Declination of the masked source
    srcs : dict
        Dictionary containing source metadata
    path : str
        Filename of the mask

    Returns
    -------
    ra : string
        right ascension calculated from the angle given in degrees, minutes, and seconds
    """
    fov = np.deg2rad((imsize * cell_size) / 3600)
    mask = "circle[[" + rad_to_hms(ra) + ", " + dec + "], " + mask_size + "]"
    final_srcs = {
        k: src
        for k, src in srcs.iteritems()
        if ra - fov / 2 <= src["RA"] <= ra + fov / 2
    }  # check if sources cross into the FOV
    if len(final_srcs) > 0:
        fname = "mask.rgn"
        fname = os.path.join(path, fname)
        with open(fname, "w") as f:
            f.write("#CRTFv0\n")
            f.write(mask + "\n")
            for _, v in final_srcs.iteritems():
                f.write(
                    "circle[["
                    + rad_to_hms(v["RA"])
                    + ", "
                    + dd_to_dms(v["DEC"])
                    + "], 2000arcsec]\n"
                )
        mask = fname
    return mask
