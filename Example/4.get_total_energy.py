import os, glob, sys
import numpy as np
import shutil
import subprocess

def get_total_energy(path):

    etot = subprocess.run(f"grep 'Total =' {path}/OUT/stdout.txt | awk '{{print $NF}}'", 
                          shell=True,
                          capture_output=True,
                          text=True)
    return float(etot.stdout.strip())

def get_es(path):

    etot = subprocess.run(f"grep '(RHO_SIC - RHO_DFT)  =' {path}/OUT/stdout.txt | tail -n 1 | awk '{{print $NF}}'",
                          shell=True,
                          capture_output=True,
                          text=True)
    print(etot.stdout.strip())
    return float(etot.stdout.strip())



if __name__ == '__main__':

    # input files
    input_dft = os.path.abspath(f'1.dft') 
    input_scf_alpha = os.path.abspath(f'2.alpha') # alpha results

    # occ lists
    occs  = sorted(os.listdir(input_scf_alpha))

    etot0 = get_total_energy(input_dft)

    # total energy lists
    with open('total.txt', 'w') as f:
        data = {}
        for occ in occs:
            etot1 = get_total_energy(os.path.join(input_scf_alpha,occ))
            etot2 = get_es(os.path.join(input_scf_alpha,occ))
            etot = 2*etot1 + etot2 - etot0

            occ_val = float(occ.split('=')[-1])
            data[occ_val] = etot

        data = dict(sorted(data.items()))
        for key, value in data.items():
            f.write(f'{key} \t {value:17.15f}\n')


