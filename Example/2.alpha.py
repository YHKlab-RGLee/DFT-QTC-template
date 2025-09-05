import os
import numpy as np
import shutil
import glob
from omegaconf import DictConfig, OmegaConf


def run_atm(exec_atm, input_inp, output_ion):

    os.makedirs('./tmp', exist_ok = True)
    os.chdir('./tmp')
    shutil.copy(input_inp, '.')
    os.system(f'{exec_atm}')
    shutil.move(f'AEPOT', output_ion)
    os.chdir('..')
    shutil.rmtree('./tmp')


if __name__ == '__main__':

    input_config = OmegaConf.load('input.yaml')

    # Input files =========================

    # All-electron Vs potential
    name = input_config['Species']['DB']
    ion_name = input_config['Species']['ION']
    occ = input_config['Occupation']
    DB = input_config['VS_DB']

    # Rc range
    rc_max = input_config['Rc']['Max']
    rc_min = input_config['Rc']['Min']
    rc_npt = input_config['Rc']['Npt']

    # =======================================


    # executable files
    exec_atm = os.path.abspath('./input/atm')
    exec_gion = os.path.abspath('./input/gion.py')
    exec_gatm = os.path.abspath('./input/gatm.py')

    # reference input
    input_siesta = os.path.abspath('./1.dft/input')
    input_run = os.path.abspath(f'origin/RUN.fdf')
    input_slm = os.path.abspath(f'origin/slm_*')

    input_ions = glob.glob('origin/*.ion')
    input_target_ion = os.path.abspath(f'./1.dft/OUT/{ion_name}.ion') # to be corrected


    input_fae = os.path.abspath(f'{DB}/{name}/1.ATOM/input/FEPOT') # optional
    if '-' in name:
        input_hae = os.path.abspath(f'{DB}/{name}/1.ATOM/output_predicted/occ={occ}/HEPOT')
    else:
        input_hae = os.path.abspath(f'{DB}/{name}/1.ATOM/output/occ={occ}/HEPOT')

    input_dft = os.path.abspath(glob.glob(f'./1.dft/OUT/*.RHO')[0])

    # range of rcs
    rcs = np.linspace(rc_min,rc_max,rc_npt)

    for irc in range(len(rcs)):

        rc = rcs[irc]
        print(rc)

        # make dirs
        path = os.path.abspath(f'2.alpha/rc={rc:3.2f}')
        os.makedirs(path, exist_ok =True)

        # copy reference input files
        os.system(f'cp -r {input_siesta} {path}/.')
        os.system(f'cp -r {input_run} {path}/.')
        os.system(f'cp -r {input_slm} {path}/.')
        os.system(f'cp -r {input_dft} {path}/input/DFT.RHO')

        # copy reference ion
        for ion in input_ions:
            os.system('cp {input_ion} {path}/input/.')

        # generate ion
        os.system(f'python {exec_gion} --fae {input_fae} --hae {input_hae} --ion {input_target_ion} --rout {rc} --n 20 --out {path}/input/{ion_name}.ion')

        
