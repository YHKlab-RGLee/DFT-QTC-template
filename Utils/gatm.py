import os
import numpy as np
import io_atm
import argparse


def modify_atm(atm, orb, occ, out):

    # read atm file
    calc_info, occ_info = io_atm.read_atm(atm) 

    # modify occ info
    nv = calc_info['nv']
    for iv in range(nv):
        if occ_info[iv]['iql'] == orb:
            occ_info[iv]['occ1'] = occ_info[iv]['occ1'] + occ

    # write atm file
    io_atm.write_atm(out, calc_info, occ_info)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='DFT-alpha atm inp generator')

    parser.add_argument('--atm', type=str, default='./INP',
                         help='Sepecify atm input file')
    parser.add_argument('--orb', type=int, default=0,
                         help='Select the orbital channel to be corrected')
    parser.add_argument('--occ', type=float, default=0.0,
                         help='Select alpha value (min,max) = (-1.0,1.0)')
    parser.add_argument('--out', type=str, default='./NEW',
                         help='Sepecify atm output file')

    args = parser.parse_args()

    modify_atm(**vars(args))
