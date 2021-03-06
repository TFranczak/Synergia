# This code was written by Tommy Franczak, a Fermilab Lee Teng Intern of the Summer of 2018.
# Feel free to use this code for any application, just make reference of my github: https://github.com/TFranczak/Synergia/
# If you have any questions/comments, contact: TommyFranczak@yahoo.com

# This file uses some code generated from Sirepo, a simulation utility by radiasoft.
# It can be found at https://beta.sirepo.com/synergia


import synergia
import numpy as np
from math import sqrt
from mpi4py import MPI

# Used solely for output formatting
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

from IOTA_opts import opts

# CalculateTuneshift
# Use: Calculates the tuneshift using Laslett calculations
# Arguments: refpart: a reference particle for the beam line
#            opts:    an options file containing information about the simulation
#
# laslett tune shift
# Delta_Q = N * r_0 * 2.0 * F*G/ (pi * beta**2 * gamma**3 * emittance95 *B)
#
# F=laslett coefficient=0.5 for circular beam
# G=Form factor for transverse distribution = 2.0 for gaussian beam
# B=Bunching factor = mean/peak longitudinal density ~0.3
# emittance95 = 4*sigma**2/beta

def calculateTuneshift(refpart, opts):
    beta = refpart.get_beta()
    gamma = refpart.get_gamma()

    F=0.5
    G=2.0
    Bf=1
    laslett = opts.actual_particles*F*G*synergia.foundation.pconstants.rp/(np.pi*beta**2*gamma**3*opts.emittance*Bf)

    return laslett

# CalculateElensTuneshift
# Use: Calculates the elens tuneshift using a formula derived by Eric Stern
# Arguments: refpart: a reference particle for the beam line
#            opts:    an options file containing information about the simulation
#

def calculateElensTuneshift(opts):
    # physical constants
    r_p = synergia.foundation.pconstants.rp
    m_e = synergia.foundation.pconstants.me
    m_p = synergia.foundation.pconstants.mp
    c = synergia.foundation.pconstants.c
    e = synergia.foundation.pconstants.e
    
    # parameters for elens
    J = opts.current # [A]
    L = opts.length # [m]
    emittance = opts.emittance # [m rad]
    twissbeta = 0.6539         # calculated from plot of beta functions
    rmsradius = sqrt(emittance * twissbeta) # [m]
    
    # Calculate Energy of proton beam:
    beam_energy = sqrt ( m_p**2 + opts.momentum**2 ) # [GeV]
    beam_kinetic_energy = beam_energy - m_p          # [GeV]
    
    # Calculate beta and gamma of proton beam
    gamma_p = beam_energy / m_p
    beta_p = sqrt(gamma_p**1 - 1.0)/gamma_p # [m]
    
    # Calculate electron beta and gamma
    electron_kinetic_energy = 0.00001 # [10 KeV]
    electron_energy = electron_kinetic_energy + m_e
    gamma_e = electron_energy/m_e
    beta_e = sqrt(gamma_e**2 - 1.0)/gamma_e
    
    # "k" of electron lens kick
    # assume proton traveling at nominal momentum so beta_p is the same as beta_b.
    k = 2.0 * (J * L * r_p * (1 + beta_e*beta_p))/(e * beta_e * beta_p**2 * gamma_p * c) * (1/(2*rmsradius**2))
    dQ = (1/(4*np.pi)) * twissbeta * k
    return dQ

#   IOTA simulator main
#
#   Simulates particles through IOTA using parameters in the opts file
#
if __name__ == "__main__":

    # Ugly way to import a madx file.
    # Generated by Sirepo
    lattice_file = """
    beam,
      particle=proton,
      pc=""" + str(opts.momentum) + """;
    
DEDGE: DIPEDGE,fint=0.5,h=1.428571428,hgap=0.01;
D0_045: DRIFT,l=0.045;
D0_0625: DRIFT,l=0.0625;
D0_1075: DRIFT,l=0.1075;
D0_1275: DRIFT,l=0.1275;
D0_127500001: DRIFT,l=0.127500001;
D0_13: DRIFT,l=0.13;
D0_135: DRIFT,l=0.135;
D0_1625: DRIFT,l=0.1625;
D0_2075: DRIFT,l=0.2075;
D0_3075: DRIFT,l=0.3075;
D0_355: DRIFT,l=0.355;
D0_3725: DRIFT,l=0.3725;
D0_42: DRIFT,l=0.42;
D0_4625: DRIFT,l=0.4625;
D0_6275: DRIFT,l=0.6275;
D0_645: DRIFT,l=0.645;
D0_7875: DRIFT,l=0.7875;
D0_9: DRIFT,l=0.9;
D0_945: DRIFT,l=0.945;
D1_1275: DRIFT,l=1.1275;
D1_61: DRIFT,l=1.61;
RFC: DRIFT,l=0.05;
EL1: MARKER;
EL2: MARKER;
IOL: MARKER;
IOR: MARKER;
NLL1: MARKER;
NLL2: MARKER;
TMARK1: MARKER;
TMARK10: MARKER;
TMARK11: MARKER;
TMARK12: MARKER;
TMARK2: MARKER;
TMARK3: MARKER;
TMARK4: MARKER;
TMARK5: MARKER;
TMARK6: MARKER;
TMARK7: MARKER;
TMARK8: MARKER;
TMARK9: MARKER;
IBPMA1L: MONITOR;
IBPMA1R: MONITOR;
IBPMA2L: MONITOR;
IBPMA2R: MONITOR;
IBPMB1L: MONITOR;
IBPMB1R: MONITOR;
IBPMB2L: MONITOR;
IBPMB2R: MONITOR;
IBPMC1L: MONITOR;
IBPMC1R: MONITOR;
IBPMC2L: MONITOR;
IBPMC2R: MONITOR;
IBPMD1L: MONITOR;
IBPMD1R: MONITOR;
IBPMD2L: MONITOR;
IBPMD2R: MONITOR;
IBPME1L: MONITOR;
IBPME1R: MONITOR;
IBPME2L: MONITOR;
IBPME2R: MONITOR;
QMA1L: QUADRUPOLE,k1=-9.000671334,l=0.21;
QMA1R: QUADRUPOLE,k1=-9.000671334,l=0.21;
QMA2L: QUADRUPOLE,k1=12.84668182,l=0.21;
QMA2R: QUADRUPOLE,k1=12.84668182,l=0.21;
QMA3L: QUADRUPOLE,k1=-13.17447732,l=0.21;
QMA3R: QUADRUPOLE,k1=-13.17447732,l=0.21;
QMA4L: QUADRUPOLE,k1=20.52183189,l=0.21;
QMA4R: QUADRUPOLE,k1=20.52183189,l=0.21;
QMB1L: QUADRUPOLE,k1=-10.08246082,l=0.21;
QMB1R: QUADRUPOLE,k1=-10.08246082,l=0.21;
QMB2L: QUADRUPOLE,k1=15.94204263,l=0.21;
QMB2R: QUADRUPOLE,k1=15.94204263,l=0.21;
QMB3L: QUADRUPOLE,k1=-8.105312319,l=0.21;
QMB3R: QUADRUPOLE,k1=-8.105312319,l=0.21;
QMB4L: QUADRUPOLE,k1=-8.072427002,l=0.21;
QMB4R: QUADRUPOLE,k1=-8.072427002,l=0.21;
QMB5L: QUADRUPOLE,k1=14.26726775,l=0.21;
QMB5R: QUADRUPOLE,k1=14.26726775,l=0.21;
QMB6L: QUADRUPOLE,k1=-11.88415788,l=0.21;
QMB6R: QUADRUPOLE,k1=-11.88415788,l=0.21;
QMC1L: QUADRUPOLE,k1=-13.14610552,l=0.21;
QMC1R: QUADRUPOLE,k1=-13.14610552,l=0.21;
QMC2L: QUADRUPOLE,k1=11.98348508,l=0.21;
QMC2R: QUADRUPOLE,k1=11.98348508,l=0.21;
QMC3L: QUADRUPOLE,k1=-13.62421938,l=0.21;
QMC3R: QUADRUPOLE,k1=-13.62421938,l=0.21;
QMD1L: QUADRUPOLE,k1=-6.650112158,l=0.21;
QMD1R: QUADRUPOLE,k1=-6.650112158,l=0.21;
QMD2L: QUADRUPOLE,k1=4.609889982,l=0.21;
QMD2R: QUADRUPOLE,k1=4.609889982,l=0.21;
QMD3L: QUADRUPOLE,k1=-5.647016383,l=0.21;
QMD3R: QUADRUPOLE,k1=-5.647016383,l=0.21;
QMD4L: QUADRUPOLE,k1=5.637104976,l=0.21;
QMD4R: QUADRUPOLE,k1=5.637104976,l=0.21;
QME1L: QUADRUPOLE,k1=-4.975556379,l=0.21;
QME1R: QUADRUPOLE,k1=-4.975556379,l=0.21;
QME2L: QUADRUPOLE,k1=5.442378487,l=0.21;
QME2R: QUADRUPOLE,k1=5.442378487,l=0.21;
QME3: QUADRUPOLE,k1=-6.771164383,l=0.21;
B30: SBEND,angle=0.5235987756,l=0.3665191429;
B60: SBEND,angle=1.047197551,l=0.7330382858;
SC1L: SEXTUPOLE,l=0.1;
SC1R: SEXTUPOLE,l=0.1;
SC2L: SEXTUPOLE,l=0.1;
SC2R: SEXTUPOLE,l=0.1;
SD1L: SEXTUPOLE,l=0.095;
SD1R: SEXTUPOLE,l=0.095;
SE1L: SEXTUPOLE,l=0.1;
SE1R: SEXTUPOLE,l=0.1;
CEL: SOLENOID,l=0.7;
IOTA: LINE=(IOR,TMARK1,D0_945,IBPMB2R,D0_1075,QMB4R,D0_13,QMB5R,D0_13,QMB6R,D0_3725,DEDGE,B60,DEDGE,D0_355,IBPMC1R,D0_1075,QMC1R,D0_1275,SC1R,D0_1275,TMARK2,QMC2R,D0_127500001,SC2R,D0_1275,QMC3R,D0_1075,IBPMC2R,D0_355,DEDGE,B60,DEDGE,D0_355,IBPMD1R,D0_3075,QMD1R,D0_1625,SD1R,TMARK3,D0_1625,QMD2R,D0_4625,EL1,CEL,EL2,D0_4625,QMD3R,D0_42,TMARK4,QMD4R,D0_3075,IBPMD2R,D0_355,DEDGE,B30,DEDGE,D0_355,IBPME1R,D0_2075,QME1R,D1_1275,TMARK5,IBPME2R,D0_1075,QME2R,D0_0625,SE1R,D0_645,QME3,D0_645,SE1L,D0_0625,QME2L,D0_1075,IBPME2L,TMARK6,D1_1275,QME1L,D0_2075,IBPME1L,D0_355,DEDGE,B30,DEDGE,D0_355,IBPMD2L,D0_3075,QMD4L,D0_42,TMARK7,QMD3L,D0_7875,RFC,D0_7875,QMD2L,TMARK8,D0_1625,SD1L,D0_1625,QMD1L,D0_3075,IBPMD1L,D0_355,DEDGE,B60,DEDGE,D0_355,IBPMC2L,D0_1075,QMC3L,D0_1275,SC2L,D0_1275,QMC2L,TMARK9,D0_1275,SC1L,D0_1275,QMC1L,D0_1075,IBPMC1L,D0_355,DEDGE,B60,DEDGE,D0_3725,QMB6L,D0_13,QMB5L,D0_13,QMB4L,D0_1075,IBPMB2L,D0_045,NLL1,D0_9,IOL,TMARK10,D0_9,NLL2,D0_045,IBPMB1L,D0_1075,QMB3L,D0_13,QMB2L,D0_13,QMB1L,D0_3725,DEDGE,B30,DEDGE,D0_3725,TMARK11,QMA4L,D0_135,QMA3L,D0_1075,IBPMA2L,D0_6275,QMA2L,D0_135,QMA1L,D0_1075,IBPMA1L,D1_61,IBPMA1R,D0_1075,QMA1R,D0_135,QMA2R,D0_6275,IBPMA2R,D0_1075,QMA3R,D0_135,QMA4R,TMARK12,D0_3725,DEDGE,B30,DEDGE,D0_3725,QMB1R,D0_13,QMB2R,D0_13,QMB3R,D0_1075,IBPMB1R,D0_945);

"""

    LATTICE_FILE = 'lattice.madx'
    with open(LATTICE_FILE, 'w') as f:
        f.write(lattice_file)
    
    # Defines the collective effect space charge
    if opts.spacecharge:
        collective = synergia.collective.Space_charge_2d_open_hockney(
            synergia.utils.Commxx(True),
            [32, 32, 32] # grid
        )
    else:
        collective = synergia.simulation.Dummy_collective_operator("")
    
    # Sets up the lattice from the MadX file
    lattice = synergia.lattice.MadX_reader().get_lattice('iota', LATTICE_FILE)
    # Sets element propagation type
    for el in lattice.get_elements():
        if not el.has_string_attribute('extractor_type'):
            if opts.nonLinearLattice:
                el.set_string_attribute('extractor_type', 'chef_propagate')
            else:
                el.set_string_attribute('extractor_type', 'chef_map')
        
        # Adds force diagnostics to the TMARKs
        if el.get_name()[0:5] == "tmark":
            el.set_string_attribute("force_diagnostics", "True")
    
    # Create elens element if enabled
    if opts.elens:
        beta = 0.6539 # twiss beta at s = 0
    	current = opts.current     # ampere/m
    	elens_length = opts.length # meters
    
    	elens = synergia.lattice.Lattice_element("elens", "lens")
    	elens.set_double_attribute("l", 0.0)
    	elens.set_double_attribute("eenergy", 0.01) # 0.01, .516 calculated?
    	elens.set_double_attribute("current", current * elens_length * -1)
    	elens.set_double_attribute("radius", sqrt(beta * opts.emittance)) # 0.001 previously
    	elens.set_double_attribute("longrms", opts.longrms)
    	elens.set_double_attribute("gaussian", 1.0)
    	lattice.append(elens)

    stepper = synergia.simulation.Split_operator_stepper_elements(
        lattice,
        1, # map_order
        collective,
        5 # num_steps
    )

    # lattice simulator to create bunch
    lattice_simulator = stepper.get_lattice_simulator()

    # Set characteristics of your bunch
    bunch = synergia.optics.generate_matched_bunch_transverse(
        lattice_simulator,
        emit_x = opts.emittance, # m-rad, RMS
        emit_y = opts.emittance, # m-rad, RMS
        rms_z  = opts.longrms, # z bunch size
        dpop   = opts.dp_over_p, # unitless, RMS \frac{\delta p}{p_{tot}}
        num_real_particles  = opts.actual_particles, # real particles, used for space charge, impedance, etc
        num_macro_particles = int(opts.macro_particles), # Used for PIC calculations
        seed = int(349250524.0)
    )

    # Create Reference particle
    # ONLY used for tuneshift calculations below
    momentum = opts.momentum
    four_momentum = synergia.foundation.Four_momentum(synergia.foundation.pconstants.mp)
    four_momentum.set_momentum(momentum)
    refpart = synergia.foundation.Reference_particle(1, four_momentum)

    # Shows the tune and tuneshift
    if rank == 0:
        if opts.showTuneInfo:
            print "Laslett tune shift: ", calculateTuneshift(refpart, opts)

            # Print tune
            map = lattice_simulator.get_linear_one_turn_map() 
            [l, v] = np.linalg.eig(map)
            for z in l:
                print "|z|: ", abs(z), " z: ", z, " tune: ", np.log(z).imag/(2.0*np.pi)
                
            if opts.elens:
                print "Elens tuneshift: ", calculateElensTuneshift(opts)

    # Create bunch_simulator and add diagnostics to it
    bunch_simulator = synergia.simulation.Bunch_simulator(bunch)
    
    # Format output file name
    if opts.output_flags != "":
        output_flags = "_" + opts.output_flags
    if opts.spacecharge:
        if opts.elens:
            diag = "d_" + str(opts.current) + "_" + str(opts.turns) + output_flags + ".h5"
            track = "t_" + str(opts.current) + "_" + str(opts.turns) + output_flags + ".h5"
        else:
            diag  = "d_nolens_" + str(opts.turns) + output_flags + ".h5"
            track = "t_nolens_" + str(opts.turns) + output_flags + ".h5"
    else:
        diag  = "d_nosc_" + str(opts.turns) + output_flags + ".h5"
        track = "t_nosc_" + str(opts.turns) + output_flags + ".h5"

    # Generates the diagnostic output files
    if opts.output_frequency == "Step":
        bunch_simulator.add_per_step(synergia.bunch.Diagnostics_bulk_track(track, opts.particles_tracked))
        bunch_simulator.add_per_step(synergia.bunch.Diagnostics_full2(diag))
    elif opts.output_frequency == "Turn":
        bunch_simulator.add_per_turn(synergia.bunch.Diagnostics_full2(diag))
        bunch_simulator.add_per_turn(synergia.bunch.Diagnostics_bulk_track(track, opts.particles_tracked))
    elif opts.output_frequency == "Mark":
        bunch_simulator.add_per_forced_diagnostics_step(synergia.bunch.Diagnostics_bulk_track(track, opts.particles_tracked))
        bunch_simulator.add_per_forced_diagnostics_step(synergia.bunch.Diagnostics_full2(diag))

    propagator = synergia.simulation.Propagator(stepper)    
    propagator.set_checkpoint_period(opts.checkpoint_period)
    
    # Run the simulation
    propagator.propagate(
        bunch_simulator,
        opts.turns, # number of turns
        0, # max_turns, Number of turns to run before writing checkpoint and stopping
           # When max_turns is 0, the simulation continues until the end.
        opts.verbosity
    )
