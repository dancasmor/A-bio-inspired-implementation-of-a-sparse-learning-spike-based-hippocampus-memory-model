
import random
import tools
import plot
import DG_CA3_CA1_one_hot
import configparser


def processing_data(spikeAmplitude, marginAddLim, fontsize, figSize, figSpikeTitle, figWeightTitle, recordWeight, allTimeStampInTrace,
                    colors, fullPathFile, isPlotShow, isPlotSave, saveFileName, baseSavePath, orientationFormat, excelColors,
                    headers, boxTableSize):
    """
    Processing the data from a simulation to get a visual representation of the result

    @param spikeAmplitude: amplitude of the spike represented in the plot
    @param marginAddLim: margin added to the longitude of the spike representation to make a gap
    @param fontsize: size of the font used in plots
    @param figSize: size of the figure
    @param figSpikeTitle: title of the spikes plots
    @param figWeightTitle: title of the weights plot
    @param recordWeight: if weight information war recorded or not
    @param allTimeStampInTrace: if represent all time stamp in trace files or only time stamps where the network is spiking
    @param colors: dict, colors used to represent information: one for each population of neuron
    @param fullPathFile: the full path to the file with the data recorded from the simulation
    @param isPlotShow: if show the plot in running time
    @param isPlotSave: if store the plots
    @param saveFileName: the base name used to store the generated files (txt, png, ...)
    @param baseSavePath: the base name used to store the generated files (txt, png, ...)
    @param orientationFormat: orientation of the time stamp: "vertical" or "horizontal"
    @param excelColors: colors to use in excel table
    @param headers: headers used in table
    @param boxTableSize: size of box in table
    @return: True if the simulation and/or the creation of the visual representation of the data has been done correctly
            or False in other cases
    """
    # Open data file of the simulation
    data = tools.read_file(fullPathFile)
    if not data:
        print("Error to open data file")
        return False
    # Create folder to store all the generated files
    baseSavePath = tools.check_and_create_folder(baseSavePath + saveFileName + "/")
    if not baseSavePath:
        print("Error to create a folder to store generated files")
        return False

    # Search all variables which are going to be used to create the plots and representations
    vCA3cue, spikesCA3cue, vCA3cont, spikesCA3cont, spikesDG, wCA3cue_CA3cont, spikesInput, spikesCA1, spikesOutput = {}, {}, {}, {}, {}, {}, {}, {}, {}
    for variable in data["variables"]:
        if variable["type"] == "v" and variable["popNameShort"] == "CA3cueL":
            vCA3cue = variable
        elif variable["type"] == "spikes" and variable["popNameShort"] == "CA3cueL":
            spikesCA3cue = variable
        elif variable["type"] == "v" and variable["popNameShort"] == "CA3contL":
            vCA3cont = variable
        elif variable["type"] == "spikes" and variable["popNameShort"] == "CA3contL":
            spikesCA3cont = variable
        elif variable["type"] == "spikes" and variable["popNameShort"] == "DGL":
            spikesDG = variable
        elif variable["type"] == "spikes" and variable["popNameShort"] == "IL":
            spikesInput = variable
        elif variable["type"] == "w" and variable["popNameShort"] == "CA3cueL-CA3contL":
            wCA3cue_CA3cont = variable
        elif variable["type"] == "spikes" and variable["popNameShort"] == "CA1L":
            spikesCA1 = variable
        elif variable["type"] == "spikes" and variable["popNameShort"] == "OL":
            spikesOutput = variable

    # Create the stream of time stamp and format spikes information
    timeStream = tools.generate_time_streams(data["simTime"], data["timeStep"], "ms")
    spikesInfo = {"IN":{"spikeStream":spikesInput["data"], "label":"IN", "sublabels":["INcue", "INcont"], "color":colors["IN"]},
                  "OUT":{"spikeStream":spikesOutput["data"], "label":"OUT", "sublabels":["OUTcue", "OUTcont"], "color":colors["OUT"]}}

    # Create visual plot of sequence of spikes along the network during simulation
    # Only in/out
    plot.plot_spike_sequence(spikesInfo=spikesInfo, timeStream=timeStream, numCueBinaryNeuron=spikesDG["numNeurons"],
                             numContNeuron=data["contSize"], spikeAmplitude=spikeAmplitude, marginAddLim=marginAddLim,
                             fontsize=fontsize, figSize=figSize, figTitle=figSpikeTitle, isPlot=isPlotShow, isSave=isPlotSave,
                             saveFigName=saveFileName+"_in_out_spikes", saveFigPath=baseSavePath)
    # All spikes
    spikesInfo["DG"] = {"spikeStream":spikesDG["data"], "label":"DG", "sublabels":["DG"], "color":colors["DG"]}
    spikesInfo["CA3cue"] = {"spikeStream":spikesCA3cue["data"], "label":"CA3cue", "sublabels":["CA3cue"], "color":colors["CA3cue"]}
    spikesInfo["CA3cont"] = {"spikeStream":spikesCA3cont["data"], "label":"CA3cont", "sublabels":["CA3cont"], "color":colors["CA3cont"]}
    spikesInfo["CA1"] = {"spikeStream": spikesCA1["data"], "label": "CA1", "sublabels": ["CA1"], "color": colors["CA1"]}
    plot.plot_spike_sequence(spikesInfo=spikesInfo, timeStream=timeStream,
                             numCueBinaryNeuron=spikesDG["numNeurons"],
                             numContNeuron=data["contSize"], spikeAmplitude=spikeAmplitude, marginAddLim=marginAddLim,
                             fontsize=fontsize, figSize=figSize, figTitle=figSpikeTitle, isPlot=isPlotShow,
                             isSave=isPlotSave,
                             saveFigName=saveFileName + "_all_spikes", saveFigPath=baseSavePath)

    # Create a txt file with the sequence of spikes formatted
    plot.generate_table_txt(spikesInfo=spikesInfo, timeStream=timeStream,
                            numCueBinaryNeuron=spikesDG["numNeurons"],
                            numCueOneHotNeuron=data["cueSize"], numContNeuron=data["contSize"],
                            endianness=data["endianness"], allTimeStampInTrace=allTimeStampInTrace,
                            iSMetaDataSave=False,
                            fileSavePath=baseSavePath, fileSaveName=saveFileName + "_all_spike", headers=headers,
                            boxTableSize=boxTableSize)
    # Create an excel table with the sequence of spikes formatted
    plot.generate_table_excel(spikesInfo=spikesInfo, timeStream=timeStream,
                              numCueBinaryNeuron=spikesDG["numNeurons"],
                              numCueOneHotNeuron=data["cueSize"], numContNeuron=data["contSize"],
                              endianness=data["endianness"], allTimeStampInTrace=allTimeStampInTrace,
                              iSMetaDataSave=False,
                              fileSavePath=baseSavePath, fileSaveName=saveFileName + "_all_spike",
                              simTime=data["simTime"],
                              colors=excelColors, orientationFormat=orientationFormat, headers=headers,
                              boxTableSize=boxTableSize)

    # Plot weight evolution of the CA3cue-CA3cont layer neurons if applicable
    if recordWeight:
        # Generate as many colors as number of CA3cue neurons
        colors = []
        for i in range(spikesCA3cue["numNeurons"]):
            colors.append('#%06X' % random.randint(0, 0xFFFFFF))
        # Create the weight plots
        plot.plot_weight_syn_in_all_neuron(srcNeuronIds=wCA3cue_CA3cont["data"]["srcNeuronId"], dstNeuronIds=wCA3cue_CA3cont["data"]["dstNeuronId"],
                                           timeStreams=wCA3cue_CA3cont["data"]["timeStamp"], weightsStream=wCA3cue_CA3cont["data"]["w"],
                                           zlimit=[data["synParameters"]["CA3cueL-CA3contL"]["w_min"] - 0.5,
                                         data["synParameters"]["CA3cueL-CA3contL"]["w_max"] + 0.5],
                                           colors=colors, baseFigTitle=figWeightTitle, figSize=figSize, fontsize=fontsize,
                                           iSplot=isPlotShow, iSsave=isPlotSave, saveFigName=saveFileName+"_weight",
                                           saveFigPath=baseSavePath)
    return True


def test(isPlotShow, isPlotSave, colors, spikeAmplitude, marginAddLim, fontsize, figSize, figSpikeTitle, figWeightTitle,
         baseSavePath, allTimeStampInTrace, executeSim, recordWeight, fullPathFile, saveFileName, orientationFormat, excelColors,
         headers, boxTableSize):
    """
    Execute the simulation of the network and/or create a visual representation of the data recorded

    @param isPlotShow: if show the plot in running time
    @param isPlotSave: if store the plots
    @param colors: dict, colors used to represent information: one for each population of neuron
    @param spikeAmplitude: amplitude of the spike represented in the plot
    @param marginAddLim: margin added to the longitude of the spike representation to make a gap
    @param fontsize: size of the font used in plots
    @param figSize: size of the figure
    @param figSpikeTitle: title of the spikes plots
    @param figWeightTitle: title of the weights plot
    @param baseSavePath: base path where the plot will be saved
    @param allTimeStampInTrace: if represent all time stamp in trace files or only time stamps where the network is spiking
    @param executeSim: if execute the network or take already generated data
    @param recordWeight: if execute, if record weight information or not
    @param fullPathFile: if not execute, the full path to the file with the data recorded from the simulation
    @param saveFileName: if not execute, the base name used to store the generated files (txt, png, ...)
    @param orientationFormat: orientation of the time stamp: "vertical" or "horizontal"
    @param excelColors: colors to use in excel table
    @param headers: headers used in table
    @param boxTableSize: size of box in table
    @return: True if the simulation and/or the creation of the visual representation of the data has been done correctly
            or False in other cases
    """
    # Execute the model if applicable
    if executeSim:
        fullPathFile, filename = DG_CA3_CA1_one_hot.main(recordWeight)
        saveFileName = filename
    # Check and/or create the base folder to store all the plot
    checkStatus = tools.check_and_create_folder(baseSavePath)
    if not checkStatus:
        print("Error to create a folder to store generated files")
        return False
    # Processing the data to plot it
    exitStatus = processing_data(spikeAmplitude, marginAddLim, fontsize, figSize, figSpikeTitle, figWeightTitle,
                                 recordWeight, allTimeStampInTrace, colors, fullPathFile, isPlotShow, isPlotSave, saveFileName,
                                 baseSavePath, orientationFormat, excelColors, headers, boxTableSize)
    return exitStatus


if __name__ == "__main__":
    # Open configparser object interface to read config files
    config = configparser.ConfigParser()
    # + Check the active config file directory
    config.read("config_files/configFileParameters.ini")
    activeConfigFilePath = "config_files/" + eval(config["configFileParameters"]["activeConfigFiles"]) + "/"

    # + Simulation parameters
    config.read(activeConfigFilePath + "simulation_config.ini")

    # Plot and execution parameters
    # + If show the plot in running time
    isPlotShow = eval(config["testParameters"]["isPlotShow"])
    # + If store the plots
    isPlotSave = eval(config["testParameters"]["isPlotSave"])
    # + Base path where store the plot
    baseSavePath = eval(config["testParameters"]["baseSavePath"])
    # + If represent all time stamp in trace files or only time stamps where the network is spiking
    allTimeStampInTrace = eval(config["testParameters"]["allTimeStampInTrace"])
    # + If execute the network or take already generated data
    executeSim = eval(config["testParameters"]["executeSim"])
    # + If execute, if record weight information or not
    recordWeight = eval(config["testParameters"]["recordWeight"])
    # + If not execute, the full path to the file with the data recorded from the simulation and the base name used to store
    #   the generated files (txt, png, ...)
    fullPathFile = eval(config["testParameters"]["fullPathFile"])
    saveFileName = eval(config["testParameters"]["saveFileName"])

    # Meta info parameters
    # + Colors used to represent information: as many as there are different populations
    colorsPopName = eval(config["testParameters"]["colorsPopName"])
    colorsPopType = eval(config["testParameters"]["colorsPopType"])
    colors = {}
    [colors.update({colorsPopName[i]:colorsPopType[i]})  for i in range(len(colorsPopName))]
    # + Amplitude of the spike represented in the plot
    spikeAmplitude = eval(config["testParameters"]["spikeAmplitude"])
    # + Margin added to the longitude of the spike representation to make a gap
    marginAddLim = eval(config["testParameters"]["marginAddLim"])
    # + Size of the font used in plots
    fontsize = eval(config["testParameters"]["fontsize"])
    # + Size of the figure
    figSize = eval(config["testParameters"]["figSize"])
    # + Title of the spikes plots
    figSpikeTitle = eval(config["testParameters"]["figSpikeTitle"])
    # + Title of the weights plot
    figWeightTitle = eval(config["testParameters"]["figWeightTitle"])
    # + Orientation of the time stamp: "vertical" or "horizontal", in the excel file
    orientationFormat = eval(config["testParameters"]["orientationFormat"])
    # + Colors to use in excel table
    colorsPopName = eval(config["testParameters"]["excelColorsPopName"])
    colorsPopType = eval(config["testParameters"]["excelColorsPopType"])
    excelColors = {}
    [excelColors.update({colorsPopName[i]: colorsPopType[i]}) for i in range(len(colorsPopName))]
    # Headers used in excel and txt table
    headers = eval(config["testParameters"]["headers"])
    # Size of box in table
    boxTableSize = eval(config["testParameters"]["boxTableSize"])

    # Simulation and/or representation
    exisStatus = test(isPlotShow, isPlotSave, colors, spikeAmplitude, marginAddLim, fontsize, figSize, figSpikeTitle, figWeightTitle,
                      baseSavePath, allTimeStampInTrace, executeSim, recordWeight, fullPathFile, saveFileName, orientationFormat,
                      excelColors, headers, boxTableSize)
    if exisStatus:
        print("Finished without problems")
    else:
        print("Problems during execution")
