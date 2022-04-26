
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import tools
from excel_controller import ExcelSpikeTracer


def plot_weight_syn_in_single_neuron(x_neuronId, y_timestamp, z_weight, zlimit, xlimit, colors, xlabel, ylabel, zlabel, figSize, fontsize, figTitle, iSplot, iSsave, saveFigName, saveFigPath):
    """
    Plots the evolution of the weight of all input synapses on a postsynaptic neuron (3D figure). For each synapse 
    (x axis) is represented the weight (z axis) in each time stamp (y axis) during the simulation.

    :param x_neuronId: streams of presynaptic neurons ID with synapses to the same neuron
    :param y_timestamp: streams of time stamps
    :param z_weight: streams of weight for each input synapses
    :param zlimit: list of 2 elements, min and max value to label z axis
    :param xlimit: list of 2 elements, min and max value to label x axis
    :param colors: color list to represent each synapse
    :param xlabel: label for x axis
    :param ylabel: label for y axis
    :param zlabel: label for z axis
    :param figSize: set of 2 values, the size of the figure
    :param fontsize: size of the font used in the figure
    :param figTitle: title of the figure
    :param iSplot: bool, if plot the figure
    :param iSsave: bool, if save the figure in a png file
    :param saveFigName: (optional) name of the output png file
    :param saveFigPath: (optional) path where to store the png file
    :return:
    """
    fig = plt.figure(figsize=figSize)
    ax = plt.axes(projection="3d")

    # For each unique neuron ID, represent the evolution of weight
    xUniqueValues = list(set(x_neuronId))
    for xUniqueValue in xUniqueValues:
        # Extract all x indeces which have the same x value (for the same neuron ID)
        xIndeces = [i for i, value in enumerate(x_neuronId) if value == xUniqueValue]
        # Extract the values for the neuron ID, time stamp and weight information of the unique neuronID-value indeces 
        xForSameX = itemgetter(*xIndeces)(x_neuronId)
        yForSameX = itemgetter(*xIndeces)(y_timestamp)
        zForSameX = itemgetter(*xIndeces)(z_weight)
        ax.plot(xForSameX, yForSameX, zForSameX, color=colors[xUniqueValue], label="Neuron ID " + str(xUniqueValue))

    # Metadata
    ax.set_title(figTitle, fontsize=fontsize)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_zlabel(zlabel, fontsize=fontsize)
    ax.set_xticks(xUniqueValues)
    ax.set_zlim3d(zlimit[0], zlimit[1])
    ax.set_xlim3d(xlimit[0], xlimit[1])
    ax.legend(fontsize=fontsize)

    # Save and/or plot the figure
    if iSsave:
        plt.savefig(saveFigPath + saveFigName + ".png")
    if iSplot:
        plt.show()
    plt.close()


def plot_weight_syn_in_all_neuron(srcNeuronIds, dstNeuronIds, timeStreams, weightsStream, zlimit, colors, baseFigTitle, figSize, fontsize, iSplot, iSsave, saveFigName, saveFigPath):
    """
    Create a 3D graph for each postsynaptic neuron ID showing the evolution of the weight of each input synapse 
    throughout the simulation.

    :param srcNeuronIds: presynaptic neurons ID stream
    :param dstNeuronIds: postsynaptic neurons ID stream
    :param timeStreams: time stamp stream
    :param weightsStream: stream of synapses weight
    :param zlimit: list of 2 elements, min and max value to label z axis (weight)
    :param colors: color list to represent each synapse, it needs a lenght of the max numbers of synapse input
    :param baseFigTitle: base name of the fig title
    :param figSize: set of 2 values, the size of the figure
    :param fontsize: size of the font used in the figure
    :param iSplot: bool, if plot the figure
    :param iSsave: bool, if save the figure in a png file
    :param saveFigName: (optional) base name of the output png file
    :param saveFigPath: (optional) path where to store the png file
    :return:
    """
    # For each postsynaptic neuron ID
    dstUniqueIds = list(set(dstNeuronIds))
    for dstNeuronId in dstUniqueIds:
        # Extract all postsynaptic neuron ID indeces for the same neuron ID
        dstIndeces = [i for i, value in enumerate(dstNeuronIds) if value == dstNeuronId]
        # Extract the values for the neuron ID, time stamp and weight information of the unique neuronID-value indeces 
        srcForSameDst = itemgetter(*dstIndeces)(srcNeuronIds)
        timeForSameDst = itemgetter(*dstIndeces)(timeStreams)
        wForSameDst = itemgetter(*dstIndeces)(weightsStream)

        # Plot it
        plot_weight_syn_in_single_neuron(x_neuronId=srcForSameDst, y_timestamp=timeForSameDst, z_weight=wForSameDst,
                                         zlimit=zlimit, xlimit=[0, len(dstUniqueIds)],
                                         colors=colors, xlabel="Src Neuron", ylabel="Time (ms)", zlabel="Synaptic weight (nA)",
                                         figSize=figSize, fontsize=fontsize, figTitle=baseFigTitle + str(dstNeuronId),
                                         iSplot=iSplot, iSsave=iSsave, saveFigName=saveFigName + "_w_Ni_N" + str(dstNeuronId),
                                         saveFigPath=saveFigPath)


def plot_spike_sequence(spikesInfo, timeStream, numCueBinaryNeuron, numMemNeuron, spikeAmplitude, marginAddLim, fontsize, figSize, figTitle, isPlot, isSave, saveFigName, saveFigPath):
    """
    Plot all spikes of population of neuron given throughout the simulation.

    @param spikesInfo: data structure that contains all information needed about spikes. Example:
    {"population_i":{"spikeStream":spikeStream, "label":label, "sublabels": sublabels, "color":color}:, ...}
    @param timeStream: time stamp stream
    @param numCueBinaryNeuron: number of neurons used to address in the input array
    @param numMemNeuron: number of neurons used to store memories
    @param spikeAmplitude: amplitude of the representation of the spikes in the sequence
    @param marginAddLim: additional margin to the spike amplitude to mark the begin and end of the representation view
    @param fontsize: size of the fonts for the figure
    @param figSize: set of 2 values, the size of the figure
    @param fonsize: size of the font used in the figure
    @param iSplot: bool, if plot the figure
    @param iSsave: bool, if save the figure in a png file
    @param saveFigName: (optional) base name of the output png file
    @param saveFigPath: (optional) path where to store the png file
    @return: full path (path + fig name) where the figure has been stored, if isSave is True
    """
    plt.figure(figsize=figSize)
    
    # Add spikes for each population of neuron that has been passed
    listXticks = [0, max(timeStream) + 1]
    for spikesInfoSinglePop in spikesInfo.values():
        label = spikesInfoSinglePop["label"]
        for indexNeuron, spikeStream in enumerate(spikesInfoSinglePop["spikeStream"]):
            if label == "DG" and indexNeuron == 0:
                continue
            plt.vlines(spikeStream, ymin=0, ymax=spikeAmplitude, color=spikesInfoSinglePop["color"], label=label)
            label = "_nolegend_"
            # List of values to mark in axis
            listXticks = listXticks + spikeStream

    # Create custom labels for each time stamp where all neuron that spikes in each time stamp are grouped
    for stamp in timeStream:
        labelTimeStamp = ""
        # Check what population of neurons fires in the current time stamp
        for spikesInfoSinglePop in spikesInfo.values():
            # Get labels and sublabel strings
            labelSpike = spikesInfoSinglePop["label"]
            sublabel = " " + spikesInfoSinglePop["sublabels"][0] + "="
            if labelSpike == "IN" or labelSpike == "OUT":
                sublabelCue = " " + spikesInfoSinglePop["sublabels"][0] + "="
                sublabelMem = " " + spikesInfoSinglePop["sublabels"][1] + "="
            # For each population of neuron:
            for indexNeuron, spikeStream in enumerate(spikesInfoSinglePop["spikeStream"]):
                # If the neuron of the current population of neuron fires in the current time stamp:
                if stamp in spikeStream:
                    # Check restriction with DG neuron
                    if labelSpike == "DG":
                        if indexNeuron == 0:
                            continue
                        indexNeuron = indexNeuron - 1
                    # Check label restriction with IN and OUT neuron, difference between IN cue and IN mem
                    if labelSpike == "IN" or labelSpike == "OUT":
                        if indexNeuron < numCueBinaryNeuron:
                            sublabel = sublabelCue
                            sublabelCue = "-"
                        else:
                            sublabel = sublabelMem
                            sublabelMem = "-"
                            indexNeuron = indexNeuron - numCueBinaryNeuron
                    # Add new information to the label of the current time stamp
                    labelTimeStamp = labelTimeStamp + sublabel + str(indexNeuron)
                    sublabel = "-"
        # Realizamos la anotación sobre el instante temporal actual
        plt.annotate(labelTimeStamp, xy=(stamp + 0.1, 0.01), rotation=90, fontsize=fontsize)
    
    # Metadata
    plt.xlabel("Simulation time (ms)", fontsize=fontsize)
    plt.ylabel("Spikes", fontsize=fontsize)
    plt.title(figTitle, fontsize=fontsize)
    plt.ylim([-marginAddLim, spikeAmplitude + marginAddLim])
    plt.xlim(-0.5, max(timeStream) + 1.5)
    listXticks = list(set(listXticks))
    plt.xticks(listXticks, fontsize=fontsize)
    plt.yticks([])
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left', fontsize=fontsize)
    plt.xticks(rotation=90)

    # Save and/or plot the figure
    if isSave:
        plt.savefig(saveFigPath + saveFigName + ".png")
    if isPlot:
        plt.show()
    plt.close()

    return saveFigPath + saveFigName + ".png"


def generate_table_txt(spikesInfo, timeStream, numCueBinaryNeuron, numCueOneHotNeuron, numMemNeuron,
                       endianness, allTimeStampInTrace, iSMetaDataSave, fileSavePath, fileSaveName, headers,
                       boxTableSize):
    """
    Create a table with all spike information formatted and store in a txt file

    @param spikesInfo: dictionary with as keys as population which values are the spike stream and label of that population
        {"population_i":{"spikeStream":spikeStream, "label":label, "sublabels": sublabel}:, ...}
    @param timeStream: time stamp stream
    @param numCueBinaryNeuron: number of neurons used to address in the input array
    @param numCueOneHotNeuron: number of neurons used to address in One-hot
    @param numMemNeuron: number of neurons used to store memories
    @param endianness: type of codification of the information stored in memory: "little endian" or "big_endian"
    @param allTimeStampInTrace: if represent all time stamp in trace files or only time stamps where the network is spiking
    @param iSMetaDataSave: bool, if save the middle information in a txt file (all spikes data ordered but not formatted)
    @param fileSavePath: (optional) path where to store the txt file
    @param fileSaveName: (optional) base name of the output txt file
    @param headers: headers used in table
    @param boxTableSize: size of box in table
    @return: the full path to the txt file
    """

    # Check if folder path exist and create in other case
    tools.check_and_create_folder(fileSavePath)

    # Get the spikes ordered by time stamp when they were fired and formatted to a more readable style
    spikesOrderedByTimeStampFormatted = tools.get_format_spike_info(spikesInfo, timeStream, numCueBinaryNeuron,
                                                                    numCueOneHotNeuron, numMemNeuron,
                                                                    endianness, iSMetaDataSave, iSMetaDataSave, allTimeStampInTrace,
                                                                    fileSavePath=fileSavePath, fileSaveName=fileSaveName)


    # Create header
    tableFormatString = "\t {:{}} {:{}} {:{}} {:{}} {:{}} {:{}}" \
                        " {:{}} {:{}} {:{}} {:{}} {:{}} \n".format(headers[0], boxTableSize, headers[1], boxTableSize,
                                         headers[2], boxTableSize, headers[3], boxTableSize,
                                         headers[4], boxTableSize, headers[5], boxTableSize,
                                         headers[6], boxTableSize, headers[7], boxTableSize,
                                         headers[8], boxTableSize, headers[9], boxTableSize,
                                         headers[10], boxTableSize)
    tableFormatString = tableFormatString + "--------" + "-" * len(headers) * boxTableSize + "\n"

    # Add rows to the table, each row is a different time stamp:
    operationCountBegin = 0
    operationCountEnd = 0
    sameOperationBeginCount = 0
    sameOperationEndCount = 0
    beginingOperations = []
    for stamp, spikes in spikesOrderedByTimeStampFormatted.items():
        [inCue, inMemBin, dgOneHot, ca3Cue, ca3MemBin, ca1bin, outCue, outMem, operationNameBegin, operationNameEnd] = tools.get_string_format_spike_info_each_timestamp(
            spikes, numCueOneHotNeuron, numMemNeuron, operationCountBegin, operationCountEnd)

        # Update the count of operations
        operationNameBegin, sameOperationBeginCount, operationCountBegin, operationNameEnd, sameOperationEndCount, operationCountEnd, beginingOperations = \
            tools.calculate_index_operation(operationNameBegin, sameOperationBeginCount, operationCountBegin, operationNameEnd,
                                  sameOperationEndCount, operationCountEnd, beginingOperations)

        # Add separation between rows
        tableFormatString = tableFormatString + "\t {:{}} {:{}} {:{}} {:{}} {:{}} {:{}}" \
                                                " {:{}} {:{}} {:{}} {:{}} {:{}} \n".format(str(stamp), boxTableSize,
                                                                  str(inCue), boxTableSize,
                                                                  str(inMemBin), boxTableSize,
                                                                  str(dgOneHot), boxTableSize,
                                                                  str(ca3Cue), boxTableSize,
                                                                  str(ca3MemBin), boxTableSize,
                                                                  str(ca1bin), boxTableSize,
                                                                  str(outCue), boxTableSize,
                                                                  str(outMem), boxTableSize,
                                                                  operationNameBegin, boxTableSize,
                                                                  operationNameEnd, boxTableSize)
        tableFormatString = tableFormatString + "--------" + "-" * len(headers) * boxTableSize + "\n"

    # Store in a txt file
    fullFilePath, _ = tools.write_file(fileSavePath, fileSaveName + "_table", ".txt", tableFormatString)
    return fullFilePath


def generate_table_excel(spikesInfo, timeStream, numCueBinaryNeuron, numCueOneHotNeuron, numMemNeuron,
                         endianness, allTimeStampInTrace, iSMetaDataSave, fileSavePath, fileSaveName, simTime, colors,
                         orientationFormat, headers, boxTableSize):
    """
        Create an excel table with all spike information formatted

        @param spikesInfo: dictionary with as keys as population which values are the spike stream and label of that population
            {"population_i":{"spikeStream":spikeStream, "label":label, "sublabels": sublabel}:, ...}
        @param timeStream: time stamp stream
        @param numCueBinaryNeuron: number of neurons used to address in the input array
        @param numCueOneHotNeuron: number of neurons used to address in One-hot
        @param numMemNeuron: number of neurons used to store memories
        @param endianness: type of codification of the information stored in memory: "little endian" or "big_endian"
        @param allTimeStampInTrace: if represent all time stamp in trace files or only time stamps where the network is spiking
        @param iSMetaDataSave: bool, if save the middle information in a txt file (all spikes data ordered but not formatted)
        @param fileSavePath: (optional) path where to store the txt file
        @param fileSaveName: (optional) base name of the output txt file
        @param simTime: time duration in ms of the simulation
        @param colors: colors to use in excel table
        @param orientationFormat: orientation of the time stamp: "vertical" or "horizontal"
        @param headers: headers used in table
        @param boxTableSize: size of box in table
        @return: the full path to the txt file
    """

    # Check if folder path exist and create in other case
    tools.check_and_create_folder(fileSavePath)

    # Get the spikes ordered by time stamp when they were fired and formatted to a more readable style
    spikesOrderedByTimeStampFormatted = tools.get_format_spike_info(spikesInfo, timeStream, numCueBinaryNeuron,
                                                                    numCueOneHotNeuron, numMemNeuron,
                                                                    endianness, iSMetaDataSave, iSMetaDataSave,
                                                                    allTimeStampInTrace,
                                                                    fileSavePath=fileSavePath,
                                                                    fileSaveName=fileSaveName)

    # Create matrix of information whose rows is the spike information formatted at a specific time stamp and
    #  columns represent the values for a specific population of neuron along the simulation time
    matrixSpikeInfo = []
    operationCountBegin = 0
    operationCountEnd = 0
    sameOperationBeginCount = 0
    sameOperationEndCount = 0
    beginingOperations = []
    for stamp, spikes in spikesOrderedByTimeStampFormatted.items():
        [inCue, inMemBin, dgOneHot, ca3Cue, ca3MemBin, ca1bin, outCue, outMem, operationNameBegin, operationNameEnd] = tools.get_string_format_spike_info_each_timestamp(
            spikes, numCueOneHotNeuron, numMemNeuron, operationCountBegin, operationCountEnd)

        # Update the count of operations
        operationNameBegin, sameOperationBeginCount, operationCountBegin, operationNameEnd, sameOperationEndCount, operationCountEnd, beginingOperations = \
            tools.calculate_index_operation(operationNameBegin, sameOperationBeginCount, operationCountBegin,
                                      operationNameEnd,
                                      sameOperationEndCount, operationCountEnd, beginingOperations)

        matrixSpikeInfo.append([inCue, inMemBin, dgOneHot, ca3Cue, ca3MemBin, ca1bin, outCue, outMem, operationNameBegin, operationNameEnd])


    # Excel file creation
    excelFile = ExcelSpikeTracer(fileSavePath, fileSaveName, simTime, len(matrixSpikeInfo[0]), colors["bgColor"], colors["hdColor"],
                                 orientationFormat, boxTableSize)

    # Add the headers to the excel table depend on the orientation
    if orientationFormat == "horizontal":
        excelFile.print_column(0, True, headers, colors["hdColor"])
    else:
        excelFile.print_row(0, True, headers, colors["hdColor"])

    # Add the format spike information to the excel table depend on the orientation
    indexCount = 1
    cellColor = [colors["IN"], colors["IN"], colors["DG"], colors["CA3"], colors["CA3"], colors["CA1"], colors["OUT"],
                 colors["OUT"], colors["operation"], colors["operation"]]
    for spikePop in matrixSpikeInfo:
        if orientationFormat == "horizontal":
            excelFile.print_column(indexCount, False, spikePop, cellColor)
        else:
            excelFile.print_row(indexCount, False, spikePop, cellColor)
        indexCount = indexCount + 1

    # Close and save file
    excelFile.closeExcel()
    return excelFile.fullPath
