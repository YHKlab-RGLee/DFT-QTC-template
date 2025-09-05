import os
import numpy as np
import shutil
import glob

def run_atm(exec_atm, input_inp, output_ion):

    os.makedirs('./tmp', exist_ok = True)
    os.chdir('./tmp')
    shutil.copy(input_inp, '.')
    os.system(f'{exec_atm}')
    shutil.move(f'AEPOT', output_ion)
    os.chdir('..')
    shutil.rmtree('./tmp')


if __name__ == '__main__':

    DB = '/home3/DB_psf/04.Alpha/01.LDA/30meV'

    # executable files
    exec_atm = os.path.abspath('./input/atm')
    exec_gion = os.path.abspath('./input/gion.py')
    exec_gatm = os.path.abspath('./input/gatm.py')

    # input files
    name = 'C'
    name_out = 'C'
    occ = '-0.30'
    input_siesta = os.path.abspath('./1.dft/input')
    input_run = os.path.abspath(f'origin/RUN.fdf')
    input_ion = os.path.abspath(f'origin/{name_out}.ion')
    input_slm = os.path.abspath(f'origin/slm_*')

    input_fae = os.path.abspath(f'{DB}/{name}/1.ATOM/input/FEPOT') # optional
    if '-' in name:
        input_hae = os.path.abspath(f'{DB}/{name}/1.ATOM/output_predicted/occ={occ}/HEPOT')
    else:
        input_hae = os.path.abspath(f'{DB}/{name}/1.ATOM/output/occ={occ}/HEPOT')

    input_dft = os.path.abspath(glob.glob(f'./1.dft/OUT/*.RHO')[0])

    # range of rcs
    rcs = np.linspace(0,6,61)

    for irc in range(len(rcs)):

        rc = rcs[irc]
        print(rc)

        # make dirs
        path = os.path.abspath(f'2.alpha/rc={rc:3.2f}')
        os.makedirs(path, exist_ok =True)

        # generate ION
        os.system(f'cp -r {input_siesta} {path}/.')
        os.system(f'cp -r {input_run} {path}/.')
        os.system(f'cp -r {input_slm} {path}/.')
        os.system(f'cp -r {input_dft} {path}/input/DFT.RHO')

        os.system(f'python {exec_gion} --fae {input_fae} --hae {input_hae} --ion {input_ion} --cut {rc} --n 20 --out {path}/input/{name_out}.ion')

        
