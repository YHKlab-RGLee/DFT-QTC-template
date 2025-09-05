import os, glob
import numpy as np
import shutil
import subprocess
import siestagap


if __name__ == '__main__':

    # input files
    input_scf_alpha = os.path.abspath('./2.alpha') # alpha results

    # occ lists
    occs  = os.listdir(input_scf_alpha)

    # total energy lists
    with open('total.txt', 'w') as f:
        for occ in occs:
            path = glob.glob(os.path.join(input_scf_alpha,occ)+'/OUT/*.bands')[0] 
            ef, homo, lumo = siestagap.get_bands(path)
            gap = lumo - homo
            f.write(f'{occ} \t HOMO = {homo:5.4f} eV \t LUMO = {lumo:5.4f} \t GAP = {gap:5.4f}\n')

