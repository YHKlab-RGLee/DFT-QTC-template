#!/usr/bin/env python
import os, sys, glob

def read_atm(fname):

    calc_info = {}
    occ_info = {}

    with open(fname, 'r') as f:

        lines = f.readlines()
        element, xc = lines[1].split()

        # calculation
        calc_info['element'] = element
        calc_info['xc'] = xc

        # core/valence shell info
        nc, nv = map(int, lines[3].split())
        calc_info['nc'] = nc
        calc_info['nv'] = nv

        # valence configurations
        for iv in range(nv):
            iqn, iql, occ1, occ2 = lines[4+iv].split()[:4]

            # occupation information
            occ_info[iv] = {}
            occ_info[iv]['iqn'] = int(iqn)
            occ_info[iv]['iql'] = int(iql)
            occ_info[iv]['occ1'] = float(occ1)
            occ_info[iv]['occ2'] = float(occ2)

    return calc_info, occ_info

def write_atm(fname, calc_info, occ_info):

    element = calc_info['element']
    xc = calc_info['xc']
    nc = calc_info['nc']
    nv = calc_info['nv']

    with open(fname, 'w') as f:
        f.write("   ae                 -- file generated from atm_io\n")
        if xc[-1] == 'r':
            f.write(f"{element:>5}{xc:>6}\n")
        else:
            f.write(f"{element:>5}{xc:>5}\n")
        f.write("     0.000     0.000     0.000     0.000     0.000     0.000\n")
        f.write(f"{nc:>5}{nv:>5}\n")

        for iv in range(nv):

            iqn = str(occ_info[iv]['iqn'])
            iql = str(occ_info[iv]['iql'])
            occ1 = f"{occ_info[iv]['occ1']:4.3f}"
            occ2 = f"{occ_info[iv]['occ2']:4.3f}"

            f.write(f"{iqn:>5}{iql:>5}{occ1:>10}{occ2:>10}\n")
        f.write("100 maxit")

