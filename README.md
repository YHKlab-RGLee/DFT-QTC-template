# README

## (0) Setup Environment
- Copy the executable program and the codes in the **`Utils`** directory.  
- Paste them into your **`bin`** directory.

## (1) Setup Calculation (using `Example`)
1. Copy the original DFT calculation directory into **`Example/1.dft`**.  

2. Modify **`origin/RUN.fdf`** to be comparable with **`1.dft/RUN.fdf`** (note: keep the `DFT-half` option) 

3. Paste all **`.ion`** files into the **`original`** directory (note: some may already be corrected).  

4. Modify the YAML input file **`input.yaml`**. The input file is structured as follows:

   - **`VS_DB`**:  
     Path to the database of all-electron potentials.  
     Example:  
     ```yaml
     VS_DB: "/home3/DB_psf/04.Alpha/01.LDA/30meV"
     ```

   - **`Species`**:  
     Information about the target species. This section includes:
       - **`DB`**: Name of the species in the database (used to locate potential files).  
       - **`ION`**: Name of the ion file to be used for calculation.  
       - **`Occupation`**: Occupation number correction (usually a fractional value, e.g., `-0.30`).  
     Example:  
     ```yaml
     Species:
       DB: "C"
       ION: "C"
       Occupation: -0.30
     ```

   - **`Rc`**:  
     Defines the cutoff radius scan range. This is used to search for the optimal cutoff parameter.  
       - **`Min`**: Minimum cutoff radius.  
       - **`Max`**: Maximum cutoff radius.  
       - **`Npt`**: Number of sampling points between Min and Max.  
     Example:  
     ```yaml
     Rc:
       Min: 0.0
       Max: 6.0
       Npt: 61
     ```
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


