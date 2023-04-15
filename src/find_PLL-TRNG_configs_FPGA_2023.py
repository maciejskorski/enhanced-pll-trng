# -*- coding: utf-8 -*-
from functools import lru_cache
from math import sqrt, floor, ceil, gcd
from time import process_time

from constraint import Problem, BacktrackingSolver
import numpy as np
from numpy import mod, arange, hstack, abs
from sympy import mod_inverse

def round_up_to_odd(n):
    if n & 1 == 0:
        return n+1
    return n

@lru_cache(maxsize=None)

# NB 03/2023 : nouveau calcul des distances qui ne prend plus uniquement la valeur min mais l'ensemble des contributeurs
# on ne fait plus la recherche sur une plage autour du front (tolérance sur le dc) mais pour une valeur arbitraire de dc
# le nb de points par fronts est calculé en fonction du jitter

def distances(jit, KM, KD):
    # pts per edge = 3.3*KD*sig/T1)
    # for a 2/1000 jitter # = 3.3*KD*2/1000 par front
    NP = int(3.3*KD*jit)

    # index of rising edges and falling edges
    Ri = np.arange(1,NP+1)
    Fi = np.arange(int(KD/2),int(KD/2)+NP+1)
    # vector of contributors indexes
    K = np.concatenate([Ri, Fi])
    # indexes after reconstruction
    kinvKM = (K*mod_inverse(KM,KD)) % KD
    kinvKM.sort()
    # distances between contributors
    d = kinvKM[1:] - kinvKM[:-1]
    #return d.mean()
    return d
    

def rs_product(m_product, n_c_product):
    return 0.015625 * m_product / n_c_product


def get_physical_contraints(family):
    physical_constraints = {
        "Xilinx_S6":
        {
            "fpfd_min": 19,
            "fpfd_max": 500,
            "fpll0_min": 3.125,
            "fpll0_max": 400,
            "fpll1_min": 3.125,
            "fpll1_max": 400,
            "fvco_min": 400,
            "fvco_max": 1080,
            "nmin": 1,
            "nmax": 52,
            "mmin": 1,
            "mmax": 64,
            "cmin": 1,
            "cmax": 128,
            "pvcomin": 1,
            "pvcomax": 1
        },
        "Xilinx_S7":
        {
            "fpfd_min": 19,
            "fpfd_max": 500,
            "fpll0_min": 6.25,
            "fpll0_max": 800,
            "fpll1_min": 6.25,
            "fpll1_max": 800,
            "fvco_min": 800,
            "fvco_max": 1866,
            "nmin": 1,
            "nmax": 56,
            "mmin": 2,
            "mmax": 64,
            "cmin": 1,
            "cmax": 128,
            "pvcomin": 1,
            "pvcomax": 1
        },
        # xilinx Kintex Ultrascale XQRKU060
        "Xilinx_KUS":
        {
            "fpfd_min": 70,
            "fpfd_max": 600,
            "fpll0_min": 4.69,
            "fpll0_max": 630,
            "fpll1_min": 4.69,
            "fpll1_max": 630,
            "fvco_min": 600,
            "fvco_max": 1200,
            "nmin": 1,
            "nmax": 15,
            "mmin": 1,
            "mmax": 19,
            "cmin": 1,
            "cmax": 128,
            "pvcomin": 1,
            "pvcomax": 1
        },
        "Intel_CV":
        {
            "fpfd_min": 5,
            "fpfd_max": 325,
            "fpll0_min": 1,
            "fpll0_max": 460,
            "fpll1_min": 1,
            "fpll1_max": 460,
            "fvco_min": 600,
            "fvco_max": 1300,
            "nmin": 1,
            "nmax": 512,
            "mmin": 1,
            "mmax": 512,
            "cmin": 1,
            "cmax": 512,
            "pvcomin": 1,
            "pvcomax": 2
        },
        "Intel_C10":
        {
            "fpfd_min": 5,
            "fpfd_max": 325,
            "fpll0_min": 5,
            "fpll0_max": 472.5,
            "fpll1_min": 5,
            "fpll1_max": 472.5,
            "fvco_min": 600,
            "fvco_max": 1300,
            "nmin": 1,
            "nmax": 512,
            "mmin": 1,
            "mmax": 512,
            "cmin": 1,
            "cmax": 512,
            "pvcomin": 1,
            "pvcomax": 2
        },
##        "Microsemi_SF2":
##        {
##            "fpfd_min": 1,
##            "fpfd_max": 200,
##            "fpll0_min": 20,
##            "fpll0_max": 400,
##            "fpll1_min": 20,
##            "fpll1_max": 400,
##            "fvco_min": 500,
##            "fvco_max": 1000,
##            "nmin": 1,
##            "nmax": 256,
##            "mmin": 1,
##            "mmax": 16384,
##            "cmin": 1,
##            "cmax": 32
##        }
        "Microsemi_SF2":
        {
            "fpfd_min": 1,
            "fpfd_max": 200,
            "fpll0_min": 20,
            "fpll0_max": 400,
            "fpll1_min": 20,
            "fpll1_max": 400,
            "fvco_min": 500,
            "fvco_max": 1000,
            "nmin": 1,
            "nmax": 256,
            "mmin": 1,
            "mmax": 1024,
            "cmin": 1,
            "cmax": 128,
            "pvcomin": 1,
            "pvcomax": 4
        }
    }
    return (physical_constraints[family].values())


def add_variables(problem, family, nb_PLLS, fixed_m0=0, fixed_n0=0, fixed_c0=0, fixed_pvco0=0):
    # Get PLL Physical constraints
    (fpfd_min, fpfd_max, fpll0_min, fpll0_max,
     fpll1_min, fpll1_max, fvco_min, fvco_max,
     nmin, nmax, mmin, mmax, cmin, cmax,
     pvcomin, pvcomax) = get_physical_contraints(family)

    nmin = max(nmin, int(ceil(fref/fpfd_max)))
    nmax = min(nmax, int(floor(fref/fpfd_min)))
    mmin = max(mmin, int(ceil(fvco_min*nmin/(fref*pvcomax))))
    mmax = min(mmax, int(floor(fvco_max*nmax/(fref*pvcomin))))
    cmin = max(cmin, int(ceil(fref*mmin/(nmax*fpll0_max))))
    cmax = min(cmax, int(floor(fref*mmax/(nmin*fpll0_min))))

    problem.addVariable("n1", range(round_up_to_odd(nmin), nmax+1, 2))
    problem.addVariable("m1", range(mmin, mmax+1))
    problem.addVariable("c1", range(round_up_to_odd(cmin), cmax+1, 2))
    problem.addVariable("pvco1", range(pvcomin, pvcomax+1))
    if nb_PLLs == 2:
        if fixed_n0:
            problem.addVariable("n0", [fixed_n0])
        else:
            problem.addVariable("n0", range(nmin, nmax+1))
        if fixed_m0:
            problem.addVariable("m0", [fixed_m0])
        else:
            problem.addVariable("m0", range(round_up_to_odd(mmin), mmax+1, 2))
        if fixed_c0:
            problem.addVariable("c0", [fixed_c0])
        else:
            problem.addVariable("c0", range(cmin, cmax+1))
        if fixed_pvco0:
            problem.addVariable("pvco0", [fixed_pvco0])
        else:
            problem.addVariable("pvco0", range(pvcomin, pvcomax+1))
    elif nb_PLLs == 1:
        problem.addVariable("n0", [1])
        problem.addVariable("m0", [1])
        problem.addVariable("c0", [1])
        problem.addVariable("pvco0", [1])
    return problem


def add_physical_constraints(problem, family, nb_PLLs):
    # Get PLL Physical constraints
    (fpfd_min, fpfd_max, fpll0_min, fpll0_max,
     fpll1_min, fpll1_max, fvco_min, fvco_max,
    nmin, nmax, mmin, mmax, cmin, cmax,
     pvcomin, pvcomax) = get_physical_contraints(family)

    constraints = [
        # Phase-frequency detector 1
        (lambda n1: fpfd_min <= fref/n1 <= fpfd_max, ("n1",)),
        # Voltage-controlled oscillator 1
        (lambda m1, n1, pvco1: fvco_min <= fref*m1*pvco1/n1 <= fvco_max, ("m1", "n1", "pvco1")),
        # Output frequency of PLL1
        (lambda m1, n1, c1, pvco1: fpll1_min <= fref*m1*pvco1/(n1*c1) <= fpll1_max, ("m1", "n1", "c1", "pvco1"))
    ]
    if nb_PLLs == 2:
        # Physical constraints
        constraints += [
            # Phase-frequency detector 0
            (lambda n0: fpfd_min <= fref/n0 <= fpfd_max, ("n0",)),
            # Voltage-controlled oscillator 0
            (lambda m0, n0, pvco0: fvco_min <= fref*m0*pvco0/n0 <= fvco_max, ("m0", "n0", "pvco0")),
            # Output frequency of PLL0
            (lambda m0, n0, c0, pvco0: fpll0_min <= fref*m0*pvco0/(n0*c0) <= fpll0_max, ("m0", "n0", "c0", "pvco0")),
        ]
    return problem, constraints


def add_TRNG_setting_constraints(problem, constraints, family, nb_PLLs, s_m, s_d):
    # Get PLL Physical constraints
    (fpfd_min, fpfd_max, fpll0_min, fpll0_max,
     fpll1_min, fpll1_max, fvco_min, fvco_max,
     nmin, nmax, mmin, mmax, cmin, cmax,
     pvcomin, pvcomax) = get_physical_contraints(family)

    constraints += [
        # Km range
        (lambda m1, n0, c0: m1*n0*c0 <= s_m, ("m1", "n0", "c0")),
        # Kd range
        (lambda m0, n1, c1: m0*n1*c1 <= s_d, ("m0", "n1", "c1")),
        # Km and Kd should be coprime
        (lambda m0, n0, c0, m1, n1, c1: gcd(m0*n1*c1, m1*n0*c0) == 1, ("m0", "n0", "c0", "m1", "n1", "c1"))
    ]
    return problem, constraints


def add_application_requirements(problem, constraints, family, nb_PLLs, f_max_design, s_min, s_max, r_min, r_max, d_min, d_max, rs_min, rs_max, f_min_pll0=0, f_max_pll0=float("inf")):
    # Get PLL Physical constraints
    (fpfd_min, fpfd_max, fpll0_min, fpll0_max,
     fpll1_min, fpll1_max, fvco_min, fvco_max,
     nmin, nmax, mmin, mmax, cmin, cmax,
     pvcomin, pvcomax) = get_physical_contraints(family)

    constraints += [
        # Design fmax
        (lambda m0, n0, c0: fref*m0/(c0*n0) <= f_max_design, ("m0", "n0", "c0"))
    ]
    if nb_PLLs == 2:
        if f_min_pll0 != 0:
            constraints += [
                # Design fmax
                (lambda m0, n0, c0: f_min_pll0 <= fref*m0/(c0*n0), ("m0", "n0", "c0")),
            ]
        if f_max_pll0 != float("inf"):
            constraints += [
                # Design fmax
                (lambda m0, n0, c0: fref*m0/(c0*n0) <= f_max_pll0, ("m0", "n0", "c0")),
            ]

    if d_min != 1 or d_max != float("inf"):
        constraints += [(lambda m0, n0, c0, m1, n1, c1: d_min <= distances(jit, m1*n0*c0, m0*n1*c1) <= d_max, ("m0", "n0", "c0", "m1", "n1", "c1"))]
    if rs_min != 0 or rs_max != float("inf"):
        constraints += [(lambda m0, n0, c0, m1, n1, c1: rs_min <= rs_product(m0*m1, n0*n1*c1*c0) <= rs_max, ("m0", "n0", "c0", "m1", "n1", "c1"))]
    if r_min != 0 or r_max != float("inf"):
        constraints += [(lambda n0, n1, c0, c1: r_min <= fref/(n0*n1*c1*c0) <= r_max, ("n0", "n1", "c0", "c1"))]
    if s_min != 0 or s_max != float("inf"):
        constraints += [(lambda m0, m1, c1: s_min <= fref*m0*m1/1000000 <= s_max, ("m0", "m1", "c1"))]

    constraints.sort(key=lambda tup: len(tup[1]), reverse=True)

    for constraint in constraints:
        problem.addConstraint(*constraint)
    return problem


def extend_solutions(solutions, fref):
    for solution in solutions:
        solution["Km"] = solution["m1"]*solution["n0"]*solution["c0"]
        solution["Kd"] = solution["m0"]*solution["n1"]*solution["c1"]
        solution["f0"] = round(fref*solution["m0"]/(solution["n0"]*solution["c0"]), 3)
        solution["f1"] = round(fref*solution["m1"]/(solution["n1"]*solution["c1"]), 3)
        solution["fpfd0"] = round(fref/solution["n0"], 3)
        solution["fpfd1"] = round(fref/solution["n1"], 3)
        solution["fvco0"] = round(solution["fpfd0"]*solution["m0"]*solution["pvco0"], 3)
        solution["fvco1"] = round(solution["fpfd1"]*solution["m1"]*solution["pvco1"], 3)
        solution["R"] = round(fref/(solution["n0"]*solution["c0"]*solution["n1"]*solution["c1"]), 5)
        solution["S"] = round(fref*solution["m1"]*solution["m0"]/(1e6), 5)
        d = distances(jit, solution["m1"]*solution["n0"]*solution["c0"],
                           solution["m0"]*solution["n1"]*solution["c1"])
        solution["#pts"] = len(d)
        solution["#sup20"] = sum(d>20)
        solution["#sup30"] = sum(d>30)
        solution["#sup40"] = sum(d>40)
        solution["#sup50"] = sum(d>50)
        solution["dmean"] = d.mean()
        solution["d"] = d
    return solutions


def prune_repeated(solutions, nb_reps, feature):

    different_values = {}
    pruned_solutions = []
    try:
        for solution in sorted(solutions, key=lambda d: d[feature]):
            if solution[feature] in different_values:
                different_values[solution[feature]] += 1
            else:
                different_values[solution[feature]] = 1
            if different_values[solution[feature]] <= nb_reps:
                pruned_solutions.append(solution)
        return pruned_solutions
    except KeyError as e:
        print("Solutions were not pruned since feature {} is unknown".format(e))
        return solutions


def pretty_print_solutions(solutions, nb_PLLs):
    if nb_PLLs == 2:
        for index, solution in enumerate(solutions):
            if index%30 == 0:
                if index == 0:
                    print("┌───┬───┬───┬─────┬───┬───┬───┬─────┬────┬────┬───────┬───────┬──────────┬──────────┬──────────┬──────────┬───────┬───────┬─────┐")
                else:
                    print("├───┼───┼───┼─────┼───┼───┼───┼─────┼────┼────┼───────┼───────┼──────────┼──────────┼──────────┼──────────┼───────┼───────┼─────┤")
                print("│m0 │n0 │c0 │pvco0│m1 │n1 │c1 │pvco1│Km  │Kd  │f0[MHz]│f1[MHz]│fPFD0[MHz]│fPFD1[MHz]│fVCO0[MHz]│fVCO1[MHz]│R[Mb/s]│S[ps-1]│d_min│")
                print("├───┼───┼───┼─────┼───┼───┼───┼─────┼────┼────┼───────┼───────┼──────────┼──────────┼──────────┼──────────┼───────┼───────┼─────┤")
            print("│{m0:<3}│{n0:<3}│{c0:<3}│{pvco0:<5}│{m1:<3}│{n1:<3}│{c1:<3}│{pvco1:<5}│{Km:<4}"
                  "│{Kd:<4}│{f0:<7}│{f1:<7}│{fpfd0:<10}│{fpfd1:<10}│{fvco0:<10}│{fvco1:<10}│{R:<7}│{S:<7}│{d:<5}│".format(**solution))
        print("└───┴───┴───┴─────┴───┴───┴───┴─────┴────┴────┴───────┴───────┴──────────┴──────────┴──────────┴──────────┴───────┴───────┴─────┘")
    elif nb_PLLs == 1:
        for index, solution in enumerate(solutions):
            if index%30 == 0:
                if index == 0:
                    print("┌───┬───┬───┬─────┬────┬────┬───────┬───────┬──────────┬──────────┬──────────┬──────────┬───────┬───────┬─────┐")
                else:
                    print("├───┼───┼───┼─────┼────┼────┼───────┼───────┼──────────┼──────────┼──────────┼──────────┼───────┼───────┼─────┤")
                print("│m1 │n1 │c1 │pvco1│Km  │Kd  │f0[MHz]│f1[MHz]│fPFD0[MHz]│fPFD1[MHz]│fVCO0[MHz]│fVCO1[MHz]│R[Mb/s]│S[ps-1]│d_min│")
                print("├───┼───┼───┼─────┼────┼────┼───────┼───────┼──────────┼──────────┼──────────┼──────────┼───────┼───────┼─────┤")
            print("│{m1:<3}│{n1:<3}│{c1:<3}│{pvco1:<5}│{Km:<4}"
                  "│{Kd:<4}│{f0:<7}│{f1:<7}│{fpfd0:<10}│{fpfd1:<10}│{fvco0:<10}│{fvco1:<10}│{R:<7}│{S:<7}│{d:<5}│".format(**solution))
        print("└───┴───┴───┴─────┴────┴────┴───────┴───────┴──────────┴──────────┴──────────┴──────────┴───────┴───────┴─────┘")


def save_solutions_to_csv(solutions, csv_filename, fref, nb_PLLs):
    if nb_PLLs == 2:
        with open(csv_filename, "w") as csv_file:
            csv_file.write("fref,m0,n0,c0,pvco0,m1,n1,c1,pvco1,Km,Kd,f0,f1,fpfd0,fpfd1,fvco0,fvco1,R,S,#pts,#>20,#>30,#>40,#>50,dmean,d\n")
            for solution in solutions:
                csv_file.write("{},{m0},{n0},{c0},{pvco0},{m1},{n1},{c1},{pvco1},{Km},{Kd},{f0},{f1},{fpfd0},"
                               "{fpfd1},{fvco0},{fvco1},{R},{S},{#pts},{#sup20},{#sup30},{#sup40},{#sup50},{dmean},{d}\n".format(fref, **solution))
    elif nb_PLLs == 1:
        with open(csv_filename, "w") as csv_file:
            csv_file.write("fref,m1,n1,c1,pvco1,Km,Kd,f0,f1,fpfd0,fpfd1,fvco0,fvco1,R,S\n")
            for solution in solutions:
                csv_file.write("{},{m1},{n1},{c1},{pvco1},{Km},{Kd},{f0},{f1},{fpfd0},"
                               "{fpfd1},{fvco0},{fvco1},{R},{S},{#pts},{#sup20},{#sup30},{#sup40},{#sup50},{dmean},{d}\n".format(fref, **solution))


def convert_csv_to_Excel(csv_filename):
    with open(csv_filename, "r") as csv_file:
        with open(csv_filename.replace(".csv", "_for_Excel.csv"), "w") as Excel_file:
            for ligne in csv_file:
                #Excel_file.write(ligne.replace(",", ";").replace(".", ","))
                Excel_file.write(ligne.replace(",", ";"))


if __name__ == "__main__":

    # Mandatory parameters

    # FPGA family
    family = "Intel_CV"  # "Intel_CV" or "Xilinx_S6" or "Microsemi_SF2" or "Intel_C10" or "Xilinx_KUS", Xilinx_S7
    # Reference frequency of the PLLs
    fref = 125
    # Maximum frequency of the design
    f_max_design = 250
    # Throughput range
    r_min, r_max = 0.28, float("inf")
    # Sensitivity range
    s_min, s_max = 0.03, float("inf")
    # Min distance between points in the reconstructed waveform
    d_min, d_max = 1, float("inf")
    # Km and Kd max values
    s_m, s_d = 1000, 500
    # Number of PLLs: 1 or 2
    nb_PLLs = 2
    # jitter per period
    jit = 2.5/1000

    # Optional parameters

    # Throughput sensitivity product
    rs_min, rs_max = 0, float("inf")
    # Output frequency range for PLL0
    f_min_pll0, f_max_pll0 = 150, 250
    # PLL0 parameters
    fixed_m0, fixed_n0, fixed_c0 = 15, 2, 4

    t0 = process_time()
    # Instantiate the problem to solve
    print("Starting configurations search")
    problem = Problem(BacktrackingSolver())

##    # No constraints on PLL0
##    problem = add_variables(problem, family, nb_PLLs)
##    problem, constraints = add_physical_constraints(problem, family, nb_PLLs)
##    problem, constraints = add_TRNG_setting_constraints(problem, constraints, family, nb_PLLs, s_m, s_d)
##    problem = add_application_requirements(problem, constraints, family, nb_PLLs, f_max_design, s_min, s_max, r_min, r_max, d_min, d_max, rs_min, rs_max)

    # Constraints on PLL0 fmin and fmax
    problem = add_variables(problem, family, nb_PLLs)
    problem, constraints = add_physical_constraints(problem, family, nb_PLLs)
    problem, constraints = add_TRNG_setting_constraints(problem, constraints, family, nb_PLLs, s_m, s_d)
    problem = add_application_requirements(problem, constraints, family, nb_PLLs, f_max_design, s_min, s_max, r_min, r_max, d_min, d_max, rs_min, rs_max, f_min_pll0, f_max_pll0)

    # Constraints on PLL0 coefficients
    # problem = add_variables(problem, family, nb_PLLs, fixed_m0, fixed_n0, fixed_c0)
    # problem, constraints = add_physical_constraints(problem, family, nb_PLLs)
    # problem, constraints = add_TRNG_setting_constraints(problem, constraints, family, nb_PLLs, s_m, s_d)
    # problem = add_application_requirements(problem, constraints, family, nb_PLLs, f_max_design, s_min, s_max, r_min, r_max, d_min, d_max, rs_min, rs_max)

    solutions = problem.getSolutions()

    outfilename = family + "_solutions.csv"

    if solutions:
        init_nb_solutions = len(solutions)
        solutions = extend_solutions(solutions, fref)
        # solutions = prune_repeated(solutions, 1, "d")
        # pretty_print_solutions(solutions, nb_PLLs)        
        save_solutions_to_csv(solutions, outfilename, fref, nb_PLLs)
        convert_csv_to_Excel(outfilename)
        print(family)
        print("{} solutions found in {}s".format(init_nb_solutions, round(process_time() - t0, 3)))
    else:
        print(family)
        print("No solution found in {}s".format(round(process_time() - t0, 3)))
