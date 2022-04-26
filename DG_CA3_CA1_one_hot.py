
import spynnaker8 as sim
import tools
import math
import numpy as np
import configparser
import os
import sys
import inspect
parent_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
neural_decoder_path = os.path.join(parent_dir_path, "neural_blocks")
sys.path.insert(0, neural_decoder_path)
from neural_decoder import NeuralDecoder
from neural_encoder import NeuralEncoder
from constant_spike_source import ConstantSpikeSource
from connection_functions import truth_table_column


"""
DG-CA3-CA1 one-hot network

+ Population:
    + Input: pattern input
    + DG: one-hot codification of direction of the pattern
    + CA3cue: store direction/cue of patterns
    + CA3mem: store content/memories of patterns
    + CA1: recode the direction of the pattern to make it binary again in the output
    + Output: output of the network

+ Synapses: 
    + Input-DG: 1 to 1 excitatory and static (first n bits: corresponding to the direction of patterns)
    + Input-CA3mem: 1 to 1 excitatory and static (the rest of the bits)
    + DG-CA3cue: 1 to 1 excitatory and static
    + CA3cue-CA3mem: all to all excitatory and dinamic (STDP).
    + CA3cue-CA1: 1 to 1 excitatory and static
    + CA1-Output: 1 to 1 excitatory and static
    + CA3mem-Output: 1 to 1 excitatory and static
"""

# Open configparser object interface to read config files
config = configparser.ConfigParser()

# + Check the active config file directory
config.read("config_files/configFileParameters.ini")
activeConfigFilePath = "config_files/" + eval(config["configFileParameters"]["activeConfigFiles"]) + "/"


# + Input memory parameters
config.read(activeConfigFilePath + "memory_config.ini")

# Max number of patterns to store
cueSize = eval(config["memory"]["cueSize"])
# Size of patterns to store (number of bits)
memSize = eval(config["memory"]["memSize"])
# Codification of information: "little_endian" o "big_endian"
endianness = eval(config["memory"]["endianness"])

# + Calculated memory parameters
# Input size of DG population (decoder)
dgInputSize = math.ceil(math.log2(cueSize+1))
# Size of CA3 network in number of neurons neccesary to store the direction/cue and content/memories of patterns
networkSize = cueSize + memSize
# Size of IN population
ilInputSize = dgInputSize + memSize
# Number of neurons for each population
popNeurons = {"ILayer": ilInputSize, "DGLayer": dgInputSize, "CA3cueLayer": cueSize, "CA3memLayer": memSize, "CA1Layer": cueSize, "OLayer": ilInputSize}


# + Network components parameters
network_config = tools.read_json(activeConfigFilePath + "network_config.json")

# Neurons paramaters
neuronParameters = network_config["neuronParameters"]
# Initial neuron parameters
initNeuronParameters = network_config["initNeuronParameters"]
# Synapses parameters
synParameters = network_config["synParameters"]


# + Simulation parameters: simulation time, time step and network/memory name
config.read(activeConfigFilePath + "simulation_config.ini")
simulationParameters = {"simTime": eval(config["simulationParameters"]["simTime"]), "timeStep": eval(config["simulationParameters"]["timeStep"]),
                        "networkName": eval(config["simulationParameters"]["networkName"])}


# + IN input spikes
config.read(activeConfigFilePath + "input_spikes.ini")
# CUE
InputSpikesCue = eval(config["input_cue"]["InputSpikesCue"])
# MEM
InputSpikesMem = eval(config["input_mem"]["InputSpikesMem"])
# Endianess format
if endianness == "little_endian":
    InputSpikesCue = np.flip(InputSpikesCue).tolist()
    InputSpikesMem = np.flip(InputSpikesMem).tolist()
# Full pattern
InputSpikes = InputSpikesCue + InputSpikesMem


# Execute the simulation and store the parameters in a file: weight if load/store weight along the simulation time
def main(weight):

    ######################################
    # Simulation parameters
    ######################################
    # El paso de tiempo de cada iteración en ms
    sim.setup(timestep=simulationParameters["timeStep"])

    ######################################
    # Create neuron population
    ######################################
    # IL
    ILayer = sim.Population(popNeurons["ILayer"], sim.SpikeSourceArray(spike_times=InputSpikes), label="ILayer")
    # CA3cue
    CA3cueLayer = sim.Population(popNeurons["CA3cueLayer"], sim.IF_curr_exp(**neuronParameters["CA3cueL"]), label="CA3cueLayer")
    CA3cueLayer.set(v=initNeuronParameters["CA3cueL"]["vInit"])
    # CA3mem
    CA3memLayer = sim.Population(popNeurons["CA3memLayer"], sim.IF_curr_exp(**neuronParameters["CA3memL"]), label="CA3memLayer")
    CA3memLayer.set(v=initNeuronParameters["CA3memL"]["vInit"])
    # DG (decoder)
    DGLayer = NeuralDecoder(popNeurons["DGLayer"], sim, {"min_delay":synParameters["IL-DGL"]["delay"]},
                            neuronParameters["DGL"], sim.StaticSynapse(weight=synParameters["IL-DGL"]["initWeight"],
                                              delay=synParameters["IL-DGL"]["delay"]))
    # Necessary for the Decoder
    constant_spike_source = ConstantSpikeSource(sim, {"min_delay": synParameters["IL-DGL"]["delay"]},
                                                neuronParameters["DGL"],
                                                sim.StaticSynapse(weight=synParameters["IL-DGL"]["initWeight"],
                                                                  delay=synParameters["IL-DGL"]["delay"]))
    # CA1 (encoder)
    CA1Layer = NeuralEncoder(2**dgInputSize, sim, {"min_delay":synParameters["CA3cueL-CA1L"]["delay"]},
                             neuronParameters["CA1L"], sim.StaticSynapse(weight=synParameters["CA3cueL-CA1L"]["initWeight"],
                                              delay=synParameters["CA3cueL-CA1L"]["delay"]))

    # OL
    OLayer = sim.Population(popNeurons["OLayer"], sim.IF_curr_exp(**neuronParameters["OL"]), label="OLayer")
    OLayer.set(v=initNeuronParameters["OL"]["vInit"])

    ######################################
    # Create synapses
    ######################################

    # IL-DG -> 1 to 1, excitatory and static (first dgInputSize bits/neurons)
    DGLayer.connect_inputs(sim.PopulationView(ILayer, range(dgInputSize)), ini_pop_indexes=[[i] for i in range(dgInputSize)])
    # DG-CA3cueL -> 1 to 1, excitatory and static
    DGLayer.connect_outputs(CA3cueLayer, end_pop_indexes=[[i] for i in range(cueSize)], and_indexes=range(1, cueSize+1),
                            conn=sim.StaticSynapse(weight=synParameters["DGL-CA3cueL"]["initWeight"],
                                                   delay=synParameters["DGL-CA3cueL"]["delay"]))
    DGLayer.connect_constant_spikes([constant_spike_source.set_source, constant_spike_source.flip_flop.output_neuron])

    # IL-CA3mem -> 1 to 1, excitatory and static (last m neurons of DG: only the number of directions to use)
    IL_CA3memL_conn = sim.Projection(sim.PopulationView(ILayer, range(dgInputSize, ilInputSize, 1)), CA3memLayer, sim.OneToOneConnector(),
                                          synapse_type=sim.StaticSynapse(weight=synParameters["IL-CA3memL"]["initWeight"],
                                                                         delay=synParameters["IL-CA3memL"]["delay"]),
                                          receptor_type=synParameters["IL-CA3memL"]["receptor_type"])

    # CA3cue-CA3mem -> all to all STDP
    # + Time rule
    timing_rule = sim.SpikePairRule(tau_plus=synParameters["CA3cueL-CA3memL"]["tau_plus"], tau_minus=synParameters["CA3cueL-CA3memL"]["tau_minus"],
                                    A_plus=synParameters["CA3cueL-CA3memL"]["A_plus"], A_minus=synParameters["CA3cueL-CA3memL"]["A_minus"])
    # + Weight rule
    weight_rule = sim.AdditiveWeightDependence(w_max=synParameters["CA3cueL-CA3memL"]["w_max"], w_min=synParameters["CA3cueL-CA3memL"]["w_min"])
    # + STDP model
    stdp_model = sim.STDPMechanism(timing_dependence=timing_rule, weight_dependence=weight_rule,
                                   weight=synParameters["CA3cueL-CA3memL"]["initWeight"], delay=synParameters["CA3cueL-CA3memL"]["delay"])
    # + Create the STDP synapses
    CA3cueL_CA3memL_conn = sim.Projection(CA3cueLayer, CA3memLayer, sim.AllToAllConnector(allow_self_connections=True), synapse_type=stdp_model)

    # CA3cue-CA1 -> 1 to 1 excitatory and static
    input_indexes = range(cueSize)
    or_indexes = range(CA1Layer.n_outputs)
    for i in or_indexes:
        selected_inputs = list(set(np.array(truth_table_column(CA1Layer.n_inputs, i, select=1)) - 1).intersection(input_indexes))
        CA1Layer.connect_inputs(CA3cueLayer, ini_pop_indexes=selected_inputs, or_indexes=[i])
    # CA1-Output -> 1 to 1 excitatory and static
    CA1Layer.connect_outputs(sim.PopulationView(OLayer, range(dgInputSize)), end_pop_indexes=[[i] for i in range(dgInputSize)],
                             conn=sim.StaticSynapse(weight=synParameters["CA1L-OL"]["initWeight"],
                                                    delay=synParameters["CA1L-OL"]["delay"]))

    # CA3mem-Output -> 1 to 1 excitatory and static
    CA3memL_OL_conn = sim.Projection(CA3memLayer, sim.PopulationView(OLayer, range(dgInputSize, ilInputSize, 1)),
                                      sim.OneToOneConnector(),
                                      synapse_type=sim.StaticSynapse(weight=synParameters["CA3memL-OL"]["initWeight"],
                                                                     delay=synParameters["CA3memL-OL"]["delay"]),
                                      receptor_type=synParameters["CA3memL-OL"]["receptor_type"])

    ######################################
    # Parameters to store
    ######################################
    CA3cueLayer.record(["spikes", "v"])
    CA3memLayer.record(["spikes", "v"])
    OLayer.record(["spikes"])
    for gate in DGLayer.and_gates.and_array:
        gate.output_neuron.record(("spikes"))
    for gate in CA1Layer.or_gates.or_array:
        gate.output_neuron.record(("spikes"))

    ######################################
    # Execute the simulation
    ######################################
    # The simulation is execute in time intervals to store the weight of synapses if applicable
    if weight:
        w_CA3cueL_CA3memL = []
        w_CA3cueL_CA3memL.append(CA3cueL_CA3memL_conn.get('weight', format='list', with_address=True))  # Instante 0
        for n in range(0, int(simulationParameters["simTime"]), int(simulationParameters["timeStep"])):
            sim.run(simulationParameters["timeStep"])
            w_CA3cueL_CA3memL.append(CA3cueL_CA3memL_conn.get('weight', format='list', with_address=True))
    else:
        sim.run(simulationParameters["simTime"])

    ######################################
    # Retrieve output data
    ######################################
    # Get the data from CA3
    CA3cueData = CA3cueLayer.get_data(variables=["spikes", "v"])
    CA3memData = CA3memLayer.get_data(variables=["spikes", "v"])

    # Get data from Output
    OLData = OLayer.get_data(variables=["spikes"])

    # Separate for each type of data (each segment = 1 execution/run)
    spikesCA3cue = CA3cueData.segments[0].spiketrains
    vCA3cue = CA3cueData.segments[0].filter(name='v')[0]
    spikesCA3mem = CA3memData.segments[0].spiketrains
    vCA3mem = CA3memData.segments[0].filter(name='v')[0]
    spikesDG = []
    for gate in DGLayer.and_gates.and_array:
        spikesDG.append(gate.output_neuron.get_data(variables=["spikes"]).segments[0].spiketrains[0])
    spikesCA1 = []
    for gate in CA1Layer.or_gates.or_array:
        spikesCA1.append(gate.output_neuron.get_data(variables=["spikes"]).segments[0].spiketrains[0])
    spikesOut = OLData.segments[0].spiketrains

    ######################################
    # End simulation
    ######################################
    sim.end()

    ######################################
    # Processing and store the output data
    ######################################
    # Format the retrieve data
    formatVCA3cue = tools.format_neo_data("v", vCA3cue)
    formatSpikesCA3cue = tools.format_neo_data("spikes", spikesCA3cue)
    formatVCA3mem = tools.format_neo_data("v", vCA3mem)
    formatSpikesCA3mem = tools.format_neo_data("spikes", spikesCA3mem)
    if weight:
        formatWeightPCcueL_PCmemL = tools.format_neo_data("weights", w_CA3cueL_CA3memL,
                                                           {"simTime": simulationParameters["simTime"],
                                                            "timeStep": simulationParameters["timeStep"]})
    formatSpikeDG = tools.format_neo_data("spikes", spikesDG)
    formatSpikeCA1 = tools.format_neo_data("spikes", spikesCA1)
    formatSpikeOut = tools.format_neo_data("spikes", spikesOut)

    # Show some of the data
    # print("Spikes Input = " + str(InputSpikes) + "\n")
    # print("Spikes DG = " + str(formatSpikeDG) + "\n")
    # print("V CA3cueLayer = " + str(formatVCA3cue) + "\n")
    # print("Spikes CA3cueLayer = " + str(formatSpikesCA3cue) + "\n")
    # print("V CA3memLayer = " + str(formatVCA3mem) + "\n")
    # print("Spikes CA3memLayer = " + str(formatSpikesCA3mem) + "\n")
    # print("Weight CA3cueL-CA3memL = " + str(formatWeightCA3cueL_CA3memL) + "\n")
    # print("Spikes CA1 = " + str(formatSpikeCA1) + "\n")
    # print("Spikes Out = " + str(formatSpikeOut) + "\n")

    # Create a dictionary with all the information and headers
    dataOut = {"networkName": simulationParameters["networkName"], "timeStep": simulationParameters["timeStep"],
               "simTime": simulationParameters["simTime"], "synParameters": synParameters,
               "neuronParameters": neuronParameters, "initNeuronParameters": initNeuronParameters,
               "cueSize": cueSize, "memSize": memSize, "endianness": endianness, "variables": []}
    dataOut["variables"].append(
        {"type": "spikes", "popName": "CA3cue Layer", "popNameShort": "CA3cueL", "numNeurons": popNeurons["CA3cueLayer"],
         "data": formatSpikesCA3cue})
    dataOut["variables"].append(
        {"type": "v", "popName": "CA3cue Layer", "popNameShort": "CA3cueL", "numNeurons": popNeurons["CA3cueLayer"],
         "data": formatVCA3cue})
    dataOut["variables"].append(
        {"type": "spikes", "popName": "CA3mem Layer", "popNameShort": "CA3memL", "numNeurons": popNeurons["CA3memLayer"],
         "data": formatSpikesCA3mem})
    dataOut["variables"].append(
        {"type": "v", "popName": "CA3mem Layer", "popNameShort": "CA3memL", "numNeurons": popNeurons["CA3memLayer"],
         "data": formatVCA3mem})
    if weight:
        dataOut["variables"].append({"type": "w", "popName": "CA3cueL-CA3memL", "popNameShort": "CA3cueL-CA3memL",
                                     "data": formatWeightCA3cueL_CA3memL})
    dataOut["variables"].append(
        {"type": "spikes", "popName": "DG Layer", "popNameShort": "DGL", "numNeurons": popNeurons["DGLayer"],
         "data": formatSpikeDG})
    dataOut["variables"].append(
        {"type": "spikes", "popName": "Input Layer", "popNameShort": "IL", "numNeurons": popNeurons["ILayer"],
         "data": InputSpikes})
    dataOut["variables"].append(
        {"type": "spikes", "popName": "CA1 Layer", "popNameShort": "CA1L", "numNeurons": popNeurons["CA1Layer"],
         "data": formatSpikeCA1})
    dataOut["variables"].append(
        {"type": "spikes", "popName": "Output Layer", "popNameShort": "OL", "numNeurons": popNeurons["OLayer"],
         "data": formatSpikeOut})

    # Store the data in a file
    tools.check_and_create_folder("data/")
    fullPath, filename = tools.write_txt_with_stamp("data/", simulationParameters["networkName"], dataOut)
    print("Data stored in: " + fullPath)
    return fullPath, filename

