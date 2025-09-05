import time,sys,os,glob
import numpy as np
import subprocess
from scipy import interpolate
import argparse

'''
 DFT-1/2 ion file generator v1.0

 Developer: Kyuhwan Lee
 Description: Calculate self-energy potential and generate modified ion file for DFT-1/2 calc.
 Usage:
          python gion.py [rcut] [neutral atom ae pot. file] [half-ionized atom ae pot. file] [reference ion file]
 Revised:
          2021.09.02: add comments and fix some notations (Ryong-Gyu Lee)
 Revised:
 	  2024.10.03: without [rcut] calculation for isolated atoms (Kaptan Rajput)
 Revised:
      2025.01.16: generalize the code (Ryong-Gyu Lee)
'''

def write_ion(fae,hae,ion,rin,rout,n,out):

    # read reference ion files
    cond = subprocess.check_output(f'grep -A 1 "Vna" {ion} | grep -v "Vna" | cut -d" " -f11', shell=True)   # Cutoff
    cond1 = subprocess.check_output(f'grep -A 1 "Vna" {ion} | grep -v "Vna" | cut -d" " -f6', shell=True)   # delta
    cond2 = subprocess.check_output(f'grep -A 1 "Vna" {ion} | grep -v "Vna" | cut -d" " -f2', shell=True)   # npts

    vmax = float(cond) # Todo -> vna rc -> Vs rc (will reduce computational cost of SIESTA)
    cnt = int(cond2)
    step = float(cond1)

    f=open(fae,'r')
    g=open(hae,'r')
    ionf = open(ion,'r')


    # calculation of cutted Vs
    list_atm=[]
    for line in f.readlines():
        list_atm.append(line)

    list_hion=[]
    for line in g.readlines():
        list_hion.append(line)

    # number of grid points
    lsize = len(list_atm)

    no_corr = False

    # no correction = DFT
    if abs(rout)<1e-8:
        xnew = np.linspace(0,vmax,cnt)
        ynew = np.zeros(cnt)
        no_corr = True

    # self-energy potential
    else:
        rad = np.zeros(lsize)
        EE = np.zeros(lsize)
        for j in range(lsize):
            atm = list(map(float,list_atm[j].split()))
            hion = list(map(float,list_hion[j].split()))
            rad[j] = atm[0]
            Vs = atm[1]-hion[1]
            EE[j]=Vs

        # interpolation
        x = np.array(rad)
        y = np.array(EE)
        fq = interpolate.splrep(x, y, s=0)
        xnew = np.linspace(0,vmax,cnt)
        ynew = interpolate.splev(xnew, fq, der=0)

        # tailored self-energy potential
        if (rout > 0) and ((rout-rin)>1e-8):
            for i in range(cnt):
                if xnew[i] < rin:
                    ynew[i] = 0
                elif rin <= xnew[i] and xnew[i] <= rout:
                    ynew[i] = ynew[i] * (1-((2*(xnew[i]-rin)/(rout-rin))-1)**n)**3
                else:
                    ynew[i] = 0
        # atomic cases -> no rc
        elif rout < 0:
            pass
        else:
            no_corr = True
            ynew = np.zeros(cnt)

    # ion file generation
    e=open(out,'w')

    ionfs = []
    for i in ionf.readlines():
        ionfs.append(i)

    for i in range(len(ionfs)):
        e.write(str(ionfs[i]))

    if not no_corr:
        e.write('# Vs:__________________________\n')
        e.write(f'{cnt:4d} {step:25.16E} {vmax:21.15f}   # npts, delta, cutoff\n')
        for i in range(cnt):
            ionx = i * step 
            ix = format(ionx, ".17f")
            if abs(ynew[i]) < 0.1:
                iy = format(ynew[i], ".15E")
            else:
                iy = format(ynew[i], ".15f")
            e.write('    ')
            e.write(ix)
            e.write('       ')
            e.write(iy)
            e.write('\n')
        e.close

    else:
        e.close

if __name__=="__main__":


    parser = argparse.ArgumentParser(description='DFT-alpha SIESTA ion generator')

    parser.add_argument('--fae', type=str, default='./FEPOT',
                         help='Sepecify full all-electron potential file')
    parser.add_argument('--hae', type=str, default='./HEPOT',
                         help='Sepecify alpha all-electron potential file')
    parser.add_argument('--ion', type=str, default='./ION',
                         help='Sepecify original SIESTA .ion file')
    parser.add_argument('--rin', type=float, default=0.0,
                         help='Sepecify Rc_in [Bohr]')
    parser.add_argument('--rout', type=float, default=0.0,
                         help='Sepecify Rc_out [Bohr] cf. rc < 0 -> no rc')
    parser.add_argument('--n', type=float, default=8,
                         help='Sepecify N')
    parser.add_argument('--out', type=str, default='./NEW',
                         help='Sepecify output SIESTA .ion file')


    args = parser.parse_args()
    write_ion(**vars(args))
