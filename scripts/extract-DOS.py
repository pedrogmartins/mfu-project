import matplotlib.pyplot as plt
import numpy as np

#This script extracts the output from a VASP local orbital projection
#   calculation. The total density of states (DOS) is extracted as well    
#   as the atomic DOS and the specific orbital projection on each atom.

# Define a function to parse the DOSCAR file
def parse_doscar_file(filename):

    #Read data
    data = {}
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Get e_min, e_max, n_atoms and NEDOS for parsing, e_fermi for plotting
    n_atoms = int(lines[0].split()[0])
    e_min = float(lines[5].split()[0])
    e_max = float(lines[5].split()[1])
    NEDOS = int(lines[5].split()[2])
    e_fermi = float(lines[5].split()[3])

    #Find indices starting DOS
    initial_DOS_index = []
    for i, line in enumerate(lines):
        if line.strip() and line.split()[0].replace('.', '', 1).isdigit():
            if float(line.split()[0]) == e_min:
                #We have found the start line of some DOS for an atom
                initial_DOS_index.append(i)

    #Extract Total DOS
    total_DOS_energy = []
    total_DOS_density = []
    total_DOS_int_den = []

    for i in range(initial_DOS_index[0] + 1, int(initial_DOS_index[0] + NEDOS + 1), 1):
        total_DOS_energy.append(float(lines[i].split()[0]))
        total_DOS_density.append(float(lines[i].split()[1]))
        total_DOS_int_den.append(float(lines[i].split()[2]))

    total_DOS = [total_DOS_energy, total_DOS_density, total_DOS_int_den]

    #Check if TDOS matches the result from pymatgen, in DOS.ipynb in parent folder
    #plt.plot(np.asarray(total_DOS_energy)-e_fermi, total_DOS_density)
    #plt.xlim(-3, 3)
    #plt.axvline(x=0, color='k', linestyle='--')
    #plt.xlabel("Energy (eV)")
    #plt.ylabel("Density")

    #Extract Local DOS

    atomic_DOS = []

    for n in range(0, n_atoms, 1):
        atomic_energy = []
        atomic_s = []
        atomic_py = []
        atomic_pz = []
        atomic_px = []
        atomic_dxy = []
        atomic_dyz = []
        atomic_dz2mr2 = []
        atomic_dxz = []
        atomic_dx2my2 = []

        for i in range(initial_DOS_index[n+1] + 1, int(initial_DOS_index[n+1] + NEDOS + 1), 1):
            atomic_energy.append(float(lines[i].split()[0]))
            atomic_s.append(float(lines[i].split()[1]))
            atomic_py.append(float(lines[i].split()[2]))
            atomic_pz.append(float(lines[i].split()[3]))
            atomic_px.append(float(lines[i].split()[4]))
            atomic_dxy.append(float(lines[i].split()[5]))
            atomic_dyz.append(float(lines[i].split()[6]))
            atomic_dz2mr2.append(float(lines[i].split()[7]))
            atomic_dxz.append(float(lines[i].split()[8]))
            atomic_dx2my2.append(float(lines[i].split()[9]))


        a = [atomic_energy, atomic_s, atomic_py, atomic_pz, atomic_px, atomic_dxy,
            atomic_dyz, atomic_dz2mr2, atomic_dxz, atomic_dx2my2]

        atomic_DOS.append(a)

    return [total_DOS, atomic_DOS, e_fermi]

#Extract output from CO in a box vibrational calculation
filename = "./co-bound/DOSCAR"
cdCO_total, cdCO_atomic, cdCO_efermi = parse_doscar_file(filename)
