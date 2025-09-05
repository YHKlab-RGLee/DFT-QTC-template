# README

## (0) Setup Environment
- Copy the executable program and the codes in the **`Utils`** directory.  
- Paste them into your **`bin`** directory.

## (1) Setup Calculation (using `Example`)
1. Copy the original DFT calculation directory into **`Example/1.dft`**.  
2. Modify **`origin/RUN.fdf`** to be comparable with **`1.dft/RUN.fdf`** (note: keep the `DFT-half` option) 
3. Paste all **`.ion`** files into the **`original`** directory (note: some may already be corrected).  
4. Edit **`2.python.py`** to update the following:  
   - `DB`: path of all-electron potential  
   - `name`: species  
   - `name_output`: output name  
5. Execute:  
   ```bash
   python 2.alpha.py
   ```

## (2) Run Calculation
Submit the job with:
```bash
python qsub.py 2.alpha
```

## (3) Obtain Results
1. Get band information:  
   ```bash
   python 3.get_bands
   ```  
   → Generates **`total.txt`** with:  
   - 1st row: `rc` (Bohr)
   - 2nd row: HOMO (eV)
   - 3rd row: LUMO (eV)
   - 4th row: band gap (eV) 

2. Get total energy (run in the previous directory of `Example`):  
   ```bash
   python 1.get_total_energy
   ```  
   → Generates **`total`** file with:  
   - 1st row: `rc` (Bohr)
   - 2nd row: total energy (eV)  

3. The **optimal `rc`** is the value that minimizes the total energy.


