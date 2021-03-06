#!/usr/bin/env python

import synergia_workflow

opts = synergia_workflow.Options("foo")

# beam
opts.add("momentum", 0.07, "Momentum of particle")
opts.add("emittance", 1e-5, "Emittance of beam")
opts.add("actual_particles", 2.25e10, "Phyiscal particles in beam")
opts.add("longrms", 1.7, "Bunch length of beam")
opts.add("dp_over_p", 0.001, "delta p / p")

# simulation options
opts.add("macro_particles", 100000, "Particles in PIC sim")
opts.add("turns", 1000, "Amount of turns around lattice")
opts.add("verbosity", 1, "Verbosity")
opts.add("spacecharge", True, "Toggles between no space charge and 2D open hockney")
opts.add("nonLinearLattice", False, "Toggles between T:chef_propagate and F:chef_map; chef_map forces linear elements (except for elens)")
opts.add("showTuneInfo", True, "Shows tune and tuneshift")

# e lens
opts.add("elens", True, "Use Elens?")
opts.add("current", 0.5, "Current of Elens")
opts.add("length", 0.7, "Physical length of Elens")

# output options
opts.add("particles_tracked", 16, "Number of particles for track diagnostic tool (shows particles in phase space)")
opts.add("output_frequency", "Turn", "Frequency of diagnostic output; 'Turn', 'Step', or 'Mark'")
opts.add("checkpoint_period", 0, "Number of turns between checkpoints. 0 for no checkpoints")
opts.add("output_flags", "Turn", "Append a custom flag to output name. Empty string for no flag")
