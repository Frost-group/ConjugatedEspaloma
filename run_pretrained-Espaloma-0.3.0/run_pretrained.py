import os
import torch
import espaloma as esp

from openff.toolkit.utils import get_data_file_path

from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout

from openff.toolkit.topology import Topology, Molecule

from openff.toolkit.utils.toolkits import RDKitToolkitWrapper

# read in molecules to molecular dynamics
startpositions = GromacsGroFile('/home/hy2120/single-y6/Y6ethyls_pbe0-pvtz.gro').positions
mol_filepath = get_data_file_path('/home/hy2120/single-y6/Y6ethyls_pbe0-pvtz.mol') 

# See here: https://docs.openforcefield.org/projects/toolkit/en/stable/users/molecule_cookbook.html#from-small-molecule-pdb-file
molecule = Molecule.from_file(mol_filepath,"mol", toolkit_registry=RDKitToolkitWrapper())
molecule_graph = esp.Graph(molecule)

# load Espaloma
espaloma_model = esp.get_model("latest")
espaloma_model(molecule_graph.heterograph)
omm_system = esp.graphs.deploy.openmm_system_from_graph(molecule_graph)
# OK; we have our force-field now

# ensure we have correct Topology objects (OpenFF and OpenMM, jeese)
off_topology = Topology.from_molecules(molecule)
omm_topology = off_topology.to_openmm()

# Molecular dynamics setup
integrator = LangevinMiddleIntegrator(300 * kelvin, 1 / picosecond, 0.001 * picoseconds)
simulation = Simulation(omm_topology, omm_system, integrator)
simulation.context.setPositions(startpositions)
simulation.minimizeEnergy()
simulation.reporters.append(PDBReporter('/home/hy2120/y6/output.pdb', 1000))
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True,
        potentialEnergy=True, temperature=True))
simulation.step(10000)
