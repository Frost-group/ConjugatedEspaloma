
# Hello! Many thanks for the reply. I'm trying to build a box of small molecules only. So I've allowed the topology to be the same as my 'molecule'. If there is only one molecule it works (sure) but if it's >1 the problem remains. My .py now looks something like this. My workflow begins with packmol'ing two small molecules and that is the Y6_2_out.mol/.gro

import os
pwd=os.getcwd()

import torch
import espaloma as esp
from openmmforcefields.generators import EspalomaTemplateGenerator

from openff.toolkit.utils import get_data_file_path

from openmm import *
from sys import stdout

from openff.toolkit.topology import Topology, Molecule
from openff.toolkit.utils.toolkits import RDKitToolkitWrapper

# read in molecules + positions
gro=app.GromacsGroFile(pwd+'/single-y6/espaloma_on_single_y6/dimer/Y6_2_out.gro')
positions = gro.getPositions(asNumpy=True)

mol_filepath = get_data_file_path(pwd+'/single-y6/espaloma_on_single_y6/dimer/Y6_2_out.mol') 

# See here: https://docs.openforcefield.org/projects/toolkit/en/stable/users/molecule_cookbook.html#from-small-molecule-pdb-file
# molecule is just the connectivity, used to build the topology, it has no positions
molecule = Molecule.from_file(mol_filepath,"mol", toolkit_registry=RDKitToolkitWrapper())
molecule_graph = esp.Graph(molecule)

# load Espaloma
espaloma_model = esp.get_model("0.3.1")
espaloma_model(molecule_graph.heterograph)
openmm_system = esp.graphs.deploy.openmm_system_from_graph(molecule_graph)
# OK; we have our force-field now

# ensure we have correct Topology objects (OpenFF and OpenMM, jeese)
openff_topology = Topology.from_molecules(molecule)
openmm_topology = openff_topology.to_openmm()

espaloma_generator = EspalomaTemplateGenerator(molecules=molecule, forcefield='espaloma-0.3.1')

openmm_topology = molecule.to_topology().to_openmm()
openmm_positions =  molecule.conformers[0].to_openmm()

forcefield=app.forcefield.ForceField() # empty, to hold Espaloma generator
forcefield.registerTemplateGenerator(espaloma_generator.generator)

modeller = app.Modeller(openmm_topology, positions)
print('System has %d atoms' % modeller.topology.getNumAtoms())
# this bit not currently working...
#modeller.add(openmm_topology, positions[561:561+561])
#print('System has %d atoms' % modeller.topology.getNumAtoms())

# The topology is described in the openforcefield API
# print('Adding ligand...')
# lig_top = ligand_mol.to_topology()
# modeller.add(lig_top.to_openmm(), lig_top.get_positions().to_openmm())

print("Creating system... Espaloma final model has %d atoms" % modeller.topology.getNumAtoms())
system=forcefield.createSystem(modeller.topology,
    nonbondedCutoff=0.9*unit.nanometer,hydrogenMass=1.5*unit.amu)
print(system)

print("Attempting minimization...")
simulation = app.Simulation(modeller.topology, system, openmm.VerletIntegrator(1.0*unit.femtoseconds))
simulation.context.setPositions(openmm_positions)
simulation.minimizeEnergy(maxIterations=5000)
print(simulation)

# approach using the standard OFFs
#forcefield = app.ForceField('openff-2.1.0.offxml')
#system = forcefield.createSystem(omm_topology, nonbondedMethod=app.PME, nonbondedCutoff=1*unit.nanometer, constraints=app.HBonds)

print("Computing potential energy...")
# Compute the potential energy
def compute_potential(system, positions):
    """Print the potential energy given a System and positions."""
    integrator = openmm.VerletIntegrator(1.0 * unit.femtoseconds)
    context = openmm.Context(system, integrator)
    context.setPositions(positions)
    print('Potential energy: %s' % context.getState(getEnergy=True).getPotentialEnergy())
    # Clean up
    del context, integrator

compute_potential(system, openmm_positions)

print("Attempting Langevin dynamics...")
# Molecular dynamics setup
integrator = LangevinMiddleIntegrator(300 * unit.kelvin, 1 / unit.picosecond, 0.001 * unit.picoseconds)
simulation = app.Simulation(openmm_topology, openmm_system, integrator)
simulation.context.setPositions(openmm_positions)
simulation.minimizeEnergy()
simulation.reporters.append(app.pdbreporter.PDBReporter('output.pdb', 1000))
#simulation.reporters.append(StateDataReporter(stdout, 1000, step=True,
#        potentialEnergy=True, temperature=True))
simulation.step(10000)

print(simulation)

