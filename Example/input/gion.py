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

def write_ion(fae,hae,ion,cut,n,out):

    # read reference ion files
    cond = subprocess.check_output(f'grep -A 1 "Vna" {ion} | grep -v "Vna" | cut -d" " -f11', shell=True)   # Cutoff
    cond1 = subprocess.check_output(f'grep -A 1 "Vna" {ion} | grep -v "Vna" | cut -d" " -f6', shell=True)   # delta
    cond2 = subprocess.check_output(f'grep -A 1 "Vna" {ion} | grep -v "Vna" | cut -d" " -f2', shell=True)   # npts

    vmax = float(cond)
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


    # no correction = DFT
    if abs(cut)<1e-8:
        xnew = np.linspace(0,vmax,cnt)
        ynew = np.zeros(cnt)

    # cutoff radius for the solid cases
    elif cut >= 0:
        newrcut = int((cut/step)+1)
        rc = 1
        for i in range(lsize):
            rr = list_atm[i]
            rr = rr.split()
            u = float(rr[0])
            if(u <= cut):
                rc = rc + 1
            else:
                rcut = rc
                break

        rrc = rcut
        rad = np.zeros(rrc)
        EE = np.zeros(rrc)
        for j in range(0,rrc):
            atm = list_atm[j]
            atm = atm.split()
            hion = list_hion[j]
            hion = hion.split()
            rad[j] = atm[0]
            Vs = (float(atm[1])-float(hion[1]))*(1-(float(atm[0])/cut)**n)**3
            EE[j]=Vs

        # interpolation
        x = np.array(rad)
        y = np.array(EE)
        fq = interpolate.splrep(x, y, s=0)
        xnew = np.linspace(0,vmax,cnt)
        xnewc = xnew[0:newrcut:1]
        ynewc = np.zeros(cnt-newrcut)
        ynew = interpolate.splev(xnewc, fq, der=0)
        ynew = np.hstack((ynew,ynewc))

    # self-energy for the atomic cases
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


    # ion file generation
    e=open(out,'w')

    ionfs = []
    for i in ionf.readlines():
        ionfs.append(i)

    for i in range(len(ionfs)):
        e.write(str(ionfs[i]))

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


if __name__=="__main__":


    parser = argparse.ArgumentParser(description='DFT-alpha SIESTA ion generator')

    parser.add_argument('--fae', type=str, default='./FEPOT',
                         help='Sepecify full all-electron potential file')
    parser.add_argument('--hae', type=str, default='./HEPOT',
                         help='Sepecify alpha all-electron potential file')
    parser.add_argument('--ion', type=str, default='./ION',
                         help='Sepecify original SIESTA .ion file')
    parser.add_argument('--cut', type=float, default=0.0,
                         help='Sepecify Rc [Bohr] cf. rc < 0 -> no rc')
    parser.add_argument('--n', type=float, default=8,
                         help='Sepecify N')
    parser.add_argument('--out', type=str, default='./NEW',
                         help='Sepecify output SIESTA .ion file')

    args = parser.parse_args()
    write_ion(**vars(args))
