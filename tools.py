
import time
import os
import numpy as np
import json


#####################################
# Input/Output
#####################################

def write_file(basePath, filename, extension, data):
    """
    Generic function to write the data into a file

    :param basePath: directory path where the file will be stored
    :param filename: name of the file
    :param extension: extension of the file
    :param data: data to store in the file
    :return: full path to the file created, name of the file created
    """
    file = open(basePath + filename + extension, "w")
    file.write(str(data))
    file.close()
    return basePath + filename + extension, filename


def write_txt_with_stamp(basePath, baseFilename, data):
    """
    Write the data into a txt file and add the current date and time to the name of the file

    :param basePath: directory path where the file will be stored
    :param baseFilename: base name of the file
    :param data: data to store in the file
    :return: full path to the file created, name of the file created
    """
    # baseFilename_year_month_day_hour_min_seg.txt
    strDate = time.strftime("%Y_%m_%d__%H_%M_%S")
    filename = baseFilename + "_" + strDate
    return write_file(basePath, filename, ".txt", data)


def read_file(fullPath):
    """
    Read the file in fullPath

    :param fullPath: path + filename to the file to read
    :return: data read from the file or False if the file could not be accessed
    """
    try:
        file = open(fullPath, "r")
        return eval(file.read())
    except FileNotFoundError:
        return False


def read_json(fullPath):
    """
    Read the json file in fullPath

    :param fullPath: path + filename to the json file to read
    :return: data read from the json file or False if the json file could not be accessed
    """
    try:
        file = open(fullPath)
        return json.load(file)
    except FileNotFoundError:
        return False


def check_and_create_folder(path):
    """
    Check if a folder exist and, if it does not exist, it creates it

    :param path: path where the folder is located or want to be created
    :return: the path if folder exist or has been created or False if the folder doesn't exist and can't be created
    """
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
            return path
        except OSError as e:
            print("Error to create directory")
            return False
    else:
        return path


#####################################
# Data format
#####################################

def format_neo_data(type, stream, timeStreamParam={}):
    """
    Format the streams of neo data to delete headers and/or make the data structure used in the rest of functions

    :param type: type of neo data ("v", "spikes" and "weights" supported)
    :param stream: data streams to be formated
    :param timeStreamParam: (optional) {"simTime", "timeStep"} necessary to add the time stamp to the weights stream format
    :return: formated stream or Raise an error if is an unsopported type of data
    """
    if timeStreamParam is None:
        timeStream = []
    if type == "v":
        formatStream = format_v_stream(stream)
    elif type == "spikes":
        formatStream = format_spike_stream(stream)
    elif type == "weights":
        formatStream = format_weight_stream(stream, timeStreamParam)
    else:
        raise ValueError("Type of data not supported. Supported types: v, spikes and weights")
    return formatStream


def format_v_stream(vStream):
    """
    Change the format of the neo data streams of membrane potentials and correct nan values

    :param vStream: neo streams of membrane potentials
    :return: v stream formated
    """
    formatV = []
    # Obtain the matrix of values ->
    #   each element represents a time_stamp and the content of that element the value for each neuron
    rawStream = vStream.as_array().tolist()
    # Extract the nnumber of neuron on each time stamp
    numNeurons = len(rawStream[0])
    # Reformat it so each element is a neuron and the content is the values for each time stamp
    for neuron in range(0, numNeurons):
        formatV.append([item[neuron] for item in rawStream])
    # Change nan values for -60 if it is the first value in the stream, the value of the previous instant if it is the
    #  last instant and the average of the instants before and after in another case
    for indexNeuron, neuron in enumerate(formatV):
        for indexTime, timeStamp in enumerate(neuron):
            if str(formatV[indexNeuron][indexTime]) == "nan":
                if indexTime == 0:
                    formatV[indexNeuron][indexTime] = -60.0
                elif indexTime >= len(neuron)-1:
                    formatV[indexNeuron][indexTime] = formatV[indexNeuron][indexTime-1]
                else:
                    formatV[indexNeuron][indexTime] = (formatV[indexNeuron][indexTime-1] +
                                                      formatV[indexNeuron][indexTime+1])/2
    return formatV


def format_spike_stream(spikesStream):
    """
    Change the format of the neo data streams of spikes generated by neurons

    :param spikesStream: neo stream of spikes
    :return: spikes stream formated
    """
    formatSpikes = []
    for neuron in spikesStream:
        formatSpikes.append(neuron.as_array().tolist())
    return formatSpikes


def format_weight_stream(weightsStream, timeStreamParam):
    """
    Change the format of the streams of weights recorded

    :param weightsStream: weight stream
    :param timeStreamParam: temporal parameters of the simulation -> {"simTime", "timeStep"}
    :return: formated weight stream -> {"srcNeuronId", "dstNeuronId", "w", "timeStamp"}
    """
    srcNeuronId, dstNeuronId, w, timeStampStream = [], [], [], []

    # Generate time stream in ms
    timeStream = generate_time_streams(timeStreamParam["simTime"], timeStreamParam["timeStep"], "ms", endPlus=True)

    # For each time stamp:
    for indexStep, step in enumerate(weightsStream):
        # For each synapse:
        for indexSyn, synapse in enumerate(step):
            srcNeuronId.append(synapse[0])
            dstNeuronId.append(synapse[1])
            w.append(synapse[2])
            timeStampStream.append(timeStream[indexStep])
    return {"srcNeuronId": srcNeuronId, "dstNeuronId": dstNeuronId, "w": w, "timeStamp": timeStampStream}


def get_spikes_per_timestamp(spikesInfo, timeStream, numCueBinaryNeuron, numContNeuron, endianness, isSave, fileSavePath="", fileSaveName=""):
    """
    Order distint streams of spikes by the time stamp when it were fired

    @param spikesInfo: dictionary with as keys as population which values are the spike stream and label of that population
        {"population_i":{"spikeStream":spikeStream, "label":label, "sublabels": sublabel}:, ...}
    @param timeStream: time stamp stream
    @param numCueBinaryNeuron: number of neurons used to address in the input array
    @param numContNeuron: number of neurons used to store content of memories
    @param endianness: type of codification of the information stored in memory: "little endian" or "big_endian"
    @param isSave: bool, if save the information in a txt file
    @param fileSavePath: (optional) path where to store the txt file
    @param fileSaveName: (optional) base name of the output txt file
    @return: the dictionary where the spikes are timestamp-ordered: {stamp: spikesCurrTimeStamp}
        spikesCurrTimeStamp is: {"hasSpike":hasSpike, "population_i": spikesOfPopiInCurrStamp, ...}
    """

    spikesOrderedByTimeStamp = {}

    # Crete a list or reorder indeces for the spikes of INPUT neurons to support endianness codifications
    if endianness == "little_endian":
        indexInputSpike = np.flip(range(numCueBinaryNeuron)).tolist() + list(range(numContNeuron))
    elif endianness == "big_endian":
        indexInputSpike = list(range(numCueBinaryNeuron)) + list(range(numContNeuron))
    else:
        raise ValueError("Endianness code not supported. Supported: little_endian and big_endian")

    # Check what neurons had fired in each time stamp to store them ordered in the dictionary
    for stamp in timeStream:
        hasSpike = False
        spikesCurrTimeStamp = {}
        # For each population of neuron:
        for spikesInfoSinglePop in spikesInfo.values():
            label = spikesInfoSinglePop["label"]
            spikesCurrTimeStampPopulation_i = []
            spikesCurrTimeStampPopulation_j = [] # Only for IN or OUT population case
            # For each neuron of the current population
            for indexNeuron, spikeStream in enumerate(spikesInfoSinglePop["spikeStream"]):
                # Check DG population special case
                if label == "DG" and indexNeuron == 0:
                    continue
                # Only if the current neuron has fired in the current time stamp, it is added
                if stamp in spikeStream:
                    if label == "IN" or label == "OUT" or label == "CA1":
                        # Special case for IN and OUT population: separate IN/OUT cue (True) and IN/OUT cont (False)
                        if indexNeuron < numCueBinaryNeuron:
                            spikesCurrTimeStampPopulation_i.append(indexInputSpike[indexNeuron])
                        else:
                            spikesCurrTimeStampPopulation_j.append(indexInputSpike[indexNeuron])
                    else:
                        # Base case
                        spikesCurrTimeStampPopulation_i.append(indexNeuron)
            # Add to the current time stamp the spikes of the current population
            if label == "IN" or label == "OUT":
                spikesCurrTimeStamp[spikesInfoSinglePop["sublabels"][0]] = spikesCurrTimeStampPopulation_i
                spikesCurrTimeStamp[spikesInfoSinglePop["sublabels"][1]] = spikesCurrTimeStampPopulation_j
            else:
                spikesCurrTimeStamp[label] = spikesCurrTimeStampPopulation_i
            # Check if there are spikes in the current time stamp and current population
            hasSpike = hasSpike or spikesCurrTimeStampPopulation_i
            if label == "IN" or label == "OUT":
                hasSpike = hasSpike or spikesCurrTimeStampPopulation_j
        # Add the emptiness of information of the current timestamp
        spikesCurrTimeStamp["hasSpike"] = hasSpike
        # Store all the information using time stamp as a key for the dictionary
        spikesOrderedByTimeStamp.update({stamp: spikesCurrTimeStamp})

    # Store the data if applicable
    if isSave:
        write_file(fileSavePath, fileSaveName + "_spikes_ordered_by_timestamp", "txt", spikesOrderedByTimeStamp)

    return spikesOrderedByTimeStamp


def get_format_spike_info(spikesInfo, timeStream, numCueBinaryNeuron, numContOneHotNeuron, numContNeuron,
                          endianness, iSMetaDataSave, isSave, allTimeStampInTrace, fileSavePath="", fileSaveName=""):
    """
    Format all the spikes information along the network to create a readable data structure where the spikes are
    ordered by time stamp

    @param spikesInfo: dictionary with as keys as population which values are the spike stream and label of that population
        {"population_i":{"spikeStream":spikeStream, "label":label, "sublabels": sublabel}:, ...}
    @param timeStream: time stamp stream
    @param numCueBinaryNeuron: number of neurons used to address in the input array
    @param numContOneHotNeuron: number of neurons used to address in One-hot
    @param numContNeuron: number of neurons used to store content of memories
    @param endianness: type of codification of the information stored in memory: "little endian" or "big_endian"
    @param iSMetaDataSave: bool, if save the middle information in a txt file (all spikes data ordered but not formatted)
    @param isSave: bool, if save the information in a txt file
    @param allTimeStampInTrace: if represent all time stamp in trace files or only time stamps where the network is spiking
    @param fileSavePath: (optional) path where to store the txt file
    @param fileSaveName: (optional) base name of the output txt file
    @return: the dictionary where the spikes are timestamp-ordered and formatted: {stamp: spikesCurrTimeStamp}
        spikesCurrTimeStamp is: {"population_i": spikesOfPopiInCurrStampFormatted, ...}
    """
    spikesOrderedByTimeStampFormatted = {}

    # Get the spikes ordered by time stamp when they were fired
    spikesOrderedByTimeStamp = get_spikes_per_timestamp(spikesInfo, timeStream, numCueBinaryNeuron, numContNeuron, endianness,
                                                        iSMetaDataSave, fileSavePath=fileSavePath, fileSaveName=fileSaveName)

    # Crete a list or reorder indeces for the spikes of INPUT neurons to support endianness codifications
    if endianness == "little_endian":
        indexInputSpike = np.flip(range(numCueBinaryNeuron)).tolist()
    elif endianness == "big_endian":
        indexInputSpike = range(numCueBinaryNeuron)
    else:
        raise ValueError("Endianness code not supported. Supported: little_endian and big_endian")

    # Take each time stamp and format the spike information to a more readable one
    for stamp, spikesOrderedInfo in spikesOrderedByTimeStamp.items():
        hasSpike = False
        # For each population in the current time stamp:
        spikesCurrTimeStamp = {}
        for label, spikeStream in spikesOrderedInfo.items():
            formatSpikes = None
            if label == "hasSpike":
                # spikeStream denote if there is any spike in the current time stamp
                hasSpike = spikeStream
                continue
            elif (label == "INcue" or label == "CA1" or label == "OUTcue") and spikeStream:
                # INcue, CA1 and OUTcue: from binary to decimal (if it is not empty)
                formatSpikes = 0
                for spike in spikeStream:
                    formatSpikes = formatSpikes + pow(2, indexInputSpike[spike])
            elif label == "DG" and spikeStream:
                # DG: substract 1 to work in 1-n interval, marking which position is set to 1
                formatSpikes = spikeStream[0] - 1
            elif label == "CA3cue" and spikeStream:
                # CA3cue: add 1 to use cues from 1 to n, and not begin in 0
                formatSpikes = spikeStream[0] + 1
            elif spikeStream:
                # Base format information: dont do anything, pass as is
                formatSpikes = spikeStream
            else:
                continue
            spikesCurrTimeStamp[label] = formatSpikes
        # Only take time stamp if there are spikes
        if allTimeStampInTrace or hasSpike:
            spikesOrderedByTimeStampFormatted.update({stamp: spikesCurrTimeStamp})
    # Store the data if applicable
    if isSave:
        write_file(fileSavePath, fileSaveName + "_spikes_ordered_by_timestamp_formated", "txt", spikesOrderedByTimeStampFormatted)
    return spikesOrderedByTimeStampFormatted


def get_string_format_spike_info_each_timestamp(spikes, numCueOneHotNeuron, numContNeuron, operationCountBegin, operationCountEnd):
    """
    Given spike information of neurons at a specific time stamp, format it to a more friendly-redable format

    @param spikes: spikes information at a specific time stamp: {"population_i": spikesOfPopiInCurrStampFormatted, ...}
    @param numCueOneHotNeuron: number of neurons used to address in One-hot
    @param numContNeuron: number of neurons used to store content of memories
    @param operationCountBegin: index of the next operation to begin
    @param operationCountEnd: index of the next operation to end
    @return: a list with the spike stream formated for each population in the current time stamp
                [inCue, inContBin, dgOneHot, ca3Cue, ca3ContBin, ca1bin, outCue, outCont, operationName]
    """

    # + Reformat spike information to string
    # + Change False and [] values for - char to indicate that there is no relevant information

    # INcue
    inCue = spikes["INcue"] if ("INcue" in spikes) and not (spikes["INcue"] == []) and (
            spikes["INcue"] is not False) else "-"

    # INcont: represent the content of memories in binary and in neurons activated
    if ("INcont" in spikes) and not (spikes["INcont"] == []) and (spikes["INcont"] is not False):
        inContBin = ""
        for index in range(numContNeuron):
            if index in spikes["INcont"]:
                inContBin = "1" + inContBin
            else:
                inContBin = "0" + inContBin
        spikes["INcont"].reverse()
        inContBin = inContBin + " " + str(spikes["INcont"])
    else:
        inContBin = "-"

    # DG: one-hot representation
    if ("DG" in spikes) and not (spikes["DG"] == []) and (spikes["DG"] is not False):
        dgOneHot = ""
        for index in range(numCueOneHotNeuron):
            if index == spikes["DG"]:
                dgOneHot = dgOneHot + "1"
            else:
                dgOneHot = dgOneHot + "0"
    else:
        dgOneHot = "-"
    dgOneHot = dgOneHot[::-1]

    # CA3cue
    ca3Cue = spikes["CA3cue"] if ("CA3cue" in spikes) and not (spikes["CA3cue"] == []) and (
            spikes["CA3cue"] is not False) else "-"

    # CA3cont: represent the content of memories in binary and in neurons activated
    if ("CA3cont" in spikes) and not (spikes["CA3cont"] == []) and (spikes["CA3cont"] is not False):
        ca3ContBin = ""
        for index in range(numContNeuron):
            if index in spikes["CA3cont"]:
                ca3ContBin = "1" + ca3ContBin
            else:
                ca3ContBin = "0" + ca3ContBin
        spikes["CA3cont"].reverse()
        ca3ContBin = ca3ContBin + " " + str(spikes["CA3cont"])
    else:
        ca3ContBin = "-"

    # CA1
    ca1bin = spikes["CA1"] if ("CA1" in spikes) and not (spikes["CA1"] == []) and (
            spikes["CA1"] is not False) else "-"

    # OUTcue
    outCue = spikes["OUTcue"] if ("OUTcue" in spikes) and not (spikes["OUTcue"] == []) and (
            spikes["OUTcue"] is not False) else "-"

    # OUTcont: represent the content of memories in binary and in neurons activated
    if ("OUTcont" in spikes) and not (spikes["OUTcont"] == []) and (spikes["OUTcont"] is not False):
        outContBin = ""
        for index in range(numContNeuron):
            if index in spikes["OUTcont"]:
                outContBin = "1" + outContBin
            else:
                outContBin = "0" + outContBin
        spikes["OUTcont"].reverse()
        outContBin = outContBin + " " + str(spikes["OUTcont"])
    else:
        outContBin = "-"

    # Check if a operation is begining: write = full input (cue and cont), read = cue input only
    operationNameBegin = "-"
    if not (inCue == "-") and not (inContBin == "-"):
        operationNameBegin = "Learn " + str(operationCountBegin)
    elif not (inCue == "-"):
        operationNameBegin = "Recall " + str(operationCountBegin)

    # Check if a operation is ending: write = full output (cue and cont), read = cue output only
    operationNameEnd = "-"
    if not (outCue == "-") and not (outContBin == "-"):
        operationNameEnd = "Learn " + str(operationCountEnd)
    elif not (outContBin == "-"):
        operationNameEnd = "Recall " + str(operationCountEnd)

    return [inCue, inContBin, dgOneHot, ca3Cue, ca3ContBin, ca1bin, outCue, outContBin, operationNameBegin, operationNameEnd]


#####################################
# Generation of data
#####################################

def generate_time_streams(simTime, timeStep, unit, endPlus=False):
    """
    Generates a time sequence in s or ms of the simulation duration using the timestep of the simulation

    :param simTime: duration of the simulation in ms
    :param timeStep: time step used in simulation in ms
    :param unit: time unit of the sequence: ms or s
    :param endPlus: (optional) bool to indicate if include the simTime stamp at the end of the sequence
    :return: temporal sequence
    """
    # Add the last time stamp of the time sequence or not
    if endPlus:
        endCount = 1
    else:
        endCount = 0

    # Generated time sequence in s o ms
    if unit == "s":
        timeStream = generate_sequence(0, simTime + endCount, timeStep, 1000)
    elif unit == "ms":
        timeStream = generate_sequence(0, simTime + endCount, timeStep, 1)
    else:
        raise ValueError("Not supported units. Supported time units: ms and s")
    return timeStream


def generate_sequence(start, stop, step, divisor):
    """
    Generate a sequence of numbers with the input conditions (start included, stop not included)

    :param start: start of sequence (included)
    :param stop: stop value of the sequence (non included)
    :param step: increment in each iteration
    :param divisor: value by which to divide the counting when storing it
    :return: sequence of generated values
    """
    sequence = []
    count = start
    while count < stop:
        sequence.append(float(count)/divisor)
        count = count + step
    return sequence


def calculate_index_operation(operationNameBegin, sameOperationBeginCount, operationCountBegin, operationNameEnd, sameOperationEndCount, operationCountEnd, beginingOperations):
    """
    Determine the index of the operation which is begining or ending

    @param operationNameBegin: name of the operation begining
    @param sameOperationBeginCount: index that count the occurrence of the same operation begining
    @param operationCountBegin: index of the operation begining
    @param operationNameEnd: name of the operation ending
    @param sameOperationEndCount: index that count the occurrence of the same operation ending
    @param operationCountEnd: index of the operation ending
    @param beginingOperations: list of begining operations along the simulation
    @return: the same input params
    """
    if not (operationNameBegin == "-"):
        if "Recall" in operationNameBegin:
            operationCountBegin = operationCountBegin + 1
            beginingOperations.append("recall")
        else:
            if sameOperationBeginCount == 0:
                operationCountBegin = operationCountBegin + 1
                sameOperationBeginCount = 2
                beginingOperations.append("learn")
            else:
                sameOperationBeginCount = sameOperationBeginCount - 1
                operationNameBegin = "-"
    if not (operationNameEnd == "-"):
        if "Recall" in operationNameEnd:
            if beginingOperations[operationCountEnd] == "recall":
                operationCountEnd = operationCountEnd + 1
            else:
                operationNameEnd = "-"
        else:
            if sameOperationEndCount == 1:
                if beginingOperations[operationCountEnd] == "learn":
                    operationCountEnd = operationCountEnd + 1
                    sameOperationEndCount = 0
            else:
                sameOperationEndCount = sameOperationEndCount + 1
                operationNameEnd = "-"

    return operationNameBegin, sameOperationBeginCount, operationCountBegin, operationNameEnd, sameOperationEndCount, operationCountEnd, beginingOperations