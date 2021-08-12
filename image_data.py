# -*- coding: utf-8 -*-
"""
Tweak the calibration and clean parameters in the run.json file
for an imaging run of the sky.

To run (in terminal):
casa -c casa_image_ms.py <run paramters>.json <measurement sets>.ms
"""

from casa import *
import numpy as np
import os
import collections
import json
import argparse

from casa_imaging.imaging_utils import *
from casa_imaging.process_ms import CASA_Imaging


if __name__ == "__main__":
    args = sys.argv[3:]
    folders = [folder for folder in args if folder.endswith("ms")]
    folders.sort()

    config = [arg for arg in args if arg.endswith("json")][0]

    with open(config) as f:
        config_data = convert_json(json.load(f))

    ci = CASA_Imaging(config_data)

    if config_data["new_calibration"] == "True":
        cal_params = config_data["new_cal_params"]
        infile = cal_params["file_to_calibrate"]
        model_name = os.path.join(
            config_data["data_path"]["run_folder"], cal_params["model_name"]
        )
        cal_sources = cal_params["cal_sources"]
        if type(cal_sources.values()[0]) is not dict:
            with open(cal_sources.values()[0], "r") as fp:
                cal_sources = convert_json(json.load(fp))
        create_model(infile, cal_sources, model_name)
        ci.create_cal_files()

    sources_file = config_data["clean_mask_sources"]["file_name"]
    mask_dec = config_data["base_mask_params"]["dec"]
    mask_radius = config_data["base_mask_params"]["radius"]

    with open(sources_file) as f:
        sources = json.load(f)

    for folder in folders:
        ra, _ = find_ra_dec(folder)
        mask = set_mask(
            ra, mask_dec, sources, path=ci.run_folder, mask_size=mask_radius
        )

        if mask.endswith("rgn"):
            print mask
            ci.final_clean_params["mask"] = mask
        else:
            print mask
            ci.final_clean_params["mask"] = mask

        ci.make_image(folder)
