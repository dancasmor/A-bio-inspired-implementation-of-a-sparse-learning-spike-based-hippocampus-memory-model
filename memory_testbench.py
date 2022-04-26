
import math
import configparser
import tools
import time
import numpy as np


def decimal_to_binary(num, list):
    """
    Convert a decimal number to a list of the binary values

    @param num: number to convert to binary
    @param list: list to store the binary sequence
    @return:
    """
    if num >= 1:
        decimal_to_binary(num // 2, list)
    list.append(num % 2)


def decimal_to_binary_list(decimalList):
    """
    Convert a list of decimal numbers to a list of binary numbers, each binary value is a list of 0's and 1's

    @param decimalList:
    @return:
    """
    # Create the list of cues in binary
    binaryValues = [[] for i in range(len(decimalList))]
    for index, value in enumerate(decimalList):
        # Get the binary representation of the current cue
        decimal_to_binary(value, binaryValues[index])
    return binaryValues


def complement_binary_list(binaryList):
    """
    Complement all values in binary list

    @param binaryList:
    @return:
    """
    complementList = [[] for i in range(len(binaryList))]
    for indexNeuron, binValues in enumerate(binaryList):
        for value in binValues:
            if value == 1:
                complementList[indexNeuron].append(0)
            else:
                complementList[indexNeuron].append(1)
    return complementList


def format_cue_vectors(binaryCueValues, cueSizeInBin):
    """
    Format the input list of binary values to have the same size of numbers of neuron in the input cue population

    @param binaryCueValues:
    @param cueSizeInBin:
    @return:
    """
    for index in range(len(binaryCueValues)):
        # Fix it to have cueSizeInBin binary numbers
        if len(binaryCueValues[index]) < cueSizeInBin:
            # If it has less values, fill with 0's at the begining
            binaryCueValues[index] = [0] * (cueSizeInBin - len(binaryCueValues[index])) + binaryCueValues[index]
        elif len(binaryCueValues[index]) > cueSizeInBin:
            binaryCueValues[index] = binaryCueValues[index][len(binaryCueValues[index]) - cueSizeInBin:]
    return binaryCueValues


def create_cue_input_vector(cue, binaryCueValues, currentOperationTime, operationTime, holdingTime, numOperations):
    """
    Take a list of binary values to assign them to the correct cue neuron in the correct time stamp to do the operation

    @param cue:
    @param binaryCueValues:
    @param currentOperationTime:
    @param operationTime:
    @param holdingTime:
    @param numOperations:
    @return:
    """
    # Associate each binary value of each cue as an activation of a neuron input
    for indexCue, inputBinaryCue in enumerate(binaryCueValues):
        for indexValue, binaryValue in enumerate(inputBinaryCue):
            # Only put "active" values (1 in binary)
            if binaryValue == 1:
                # Hold the values as time as the operation need
                for holdingIndex in range(holdingTime):
                    cue[indexValue].append(currentOperationTime + holdingIndex)
        # Add to the current operation time the minimum time to begin the next operation
        currentOperationTime = currentOperationTime + operationTime
        numOperations = numOperations + 1
    return cue, numOperations, currentOperationTime


def create_alternate_cue_input_vector(cue, binaryCueValues, currentOperationTime, operationTime, holdingTime, numOperations):
    """
    Take a list of binary values to assign them to the correct cue neuron in the correct time stamp to do the operation
    adding 2 times the value once for writing and once for reading it

    @param cue:
    @param binaryCueValues:
    @param currentOperationTime:
    @param operationTime:
    @param holdingTime:
    @param numOperations:
    @return:
    """
    # Associate each binary value of each cue as an activation of a neuron input
    for indexCue, inputBinaryCue in enumerate(binaryCueValues):
        # + For the writing operation
        for indexValue, binaryValue in enumerate(inputBinaryCue):
            # Only put "active" values (1 in binary)
            if binaryValue == 1:
                # Hold the values as time as the operation need
                for holdingIndex in range(holdingTime[0]):
                    cue[indexValue].append(currentOperationTime + holdingIndex)
        # Add to the current operation time the minimum time to begin the next operation
        currentOperationTime = currentOperationTime + operationTime[0]
        numOperations = numOperations + 1
        # + For the reading operation
        for indexValue, binaryValue in enumerate(inputBinaryCue):
            # Only put "active" values (1 in binary)
            if binaryValue == 1:
                # Hold the values as time as the operation need
                for holdingIndex in range(holdingTime[1]):
                    cue[indexValue].append(currentOperationTime + holdingIndex)
        currentOperationTime = currentOperationTime + operationTime[1]
        numOperations = numOperations + 1
    return cue, numOperations, currentOperationTime


def create_mem_input_vector(mem, memBinValues, currentOperationTime, operationTime, holdingTime):
    """
        Take a list of binary values to assign them to the correct memory neuron in the correct time stamp to do the operation

        @param mem:
        @param memBinValues:
        @param currentOperationTime:
        @param operationTime:
        @param holdingTime:
        @return:
    """
    # Associate each binary value of each cue as an activation of a neuron input
    for indexMem, memBinValue in enumerate(memBinValues):
        for indexValue, binaryValue in enumerate(memBinValue):
            # Only put "active" values (1 in binary)
            if binaryValue == 1:
                # Hold the values as time as the operation need
                for holdingIndex in range(holdingTime):
                    mem[indexValue].append(currentOperationTime + holdingIndex)
        # Add to the current operation time the minimum time to begin the next operation
        currentOperationTime = currentOperationTime + operationTime
    return mem, currentOperationTime


def create_input_vector_from_operations(mem, cue, operations, memBinValues, binaryCueValues, currentOperationTime, operationTime, holdingTime, numberOfOperations):
    """
    Take a list of binary cue and mem values to assign them to the correct mem and cue neuron in the correct time
    stamp to do the operations passed

    @param mem:
    @param cue:
    @param operations:
    @param memBinValues:
    @param binaryCueValues:
    @param currentOperationTime:
    @param operationTime:
    @param holdingTime:
    @param numberOfOperations:
    @return:
    """
    # For each operation:
    for indexOperation, operation in enumerate(operations):
        # Associate the cue values to neurons
        for indexValue, binaryValue in enumerate(binaryCueValues[indexOperation]):
            # Only put "active" values (1 in binary)
            if binaryValue == 1:
                # Hold the values as time as the operation need
                for holdingIndex in range(holdingTime[operation]):
                    cue[indexValue].append(currentOperationTime + holdingIndex)
        # Associate the memories values to neurons if writing operation
        if operation == 0:
            for indexValue, binaryValue in enumerate(memBinValues[indexOperation]):
                # Only put "active" values (1 in binary)
                if binaryValue == 1:
                    # Hold the values as time as the operation need
                    for holdingIndex in range(holdingTime[operation]):
                        mem[indexValue].append(currentOperationTime + holdingIndex)
        # Add to the current operation time the minimum time to begin the next operation
        currentOperationTime = currentOperationTime + operationTime[operation]
        numberOfOperations = numberOfOperations + 1

    return cue, mem, currentOperationTime, numberOfOperations


def tb_piramidal_sequence(cueSize, memSize, cueSizeInBin, readingOperationTime, readingOperationDataHolding, writingOperationTime, writingOperationDataHolding):
    """
    Create the following sequence: for each cue write the cue as a memory, read all cues, write them
    but complemented, read all cues, write them but complemented again and read all cues.

    @param cueSize:
    @param memSize:
    @param cueSizeInBin:
    @param readingOperationTime:
    @param readingOperationDataHolding:
    @param writingOperationTime:
    @param writingOperationDataHolding:
    @return:
    """
    ## 1) Writing all cues
    #   * Create the empty cue vector
    cue = [[] for i in range(cueSizeInBin)]
    #   * Create the list of cues in decimal
    decimalCue = [i + 1 for i in range(cueSize)]
    #   * Convert the cue from decimal to binary and fix it to the correct input size
    binaryCue = format_cue_vectors(decimal_to_binary_list(decimalCue), cueSizeInBin)
    #   * Assign the binary values to each input cue neuron on the correct timestamp
    currentOperationTime = 1
    numOperations = 0
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime, writingOperationTime,
                                                                       writingOperationDataHolding, numOperations)

    # + Create the input mem activity vector
    #   * Create the empty mem vector
    mem = [[] for i in range(memSize)]
    #   * Create the list of memories in decimal
    numOperationsMem = numOperations
    decimalMem = [(i + 1) % (2 ** memSize) for i in range(numOperationsMem)]
    #   * Convert the mem from decimal to binary and fix it to the correct input size
    binaryMem = format_cue_vectors(decimal_to_binary_list(decimalMem), memSize)
    #   * Generate the data to store
    currentOperationTimeMem = 1
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem, writingOperationTime,
                                                         writingOperationDataHolding)

    ## 2) Reading all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime, readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)

    ## 3) Write the complementary of the current memory
    #   * Cue
    currentOperationTimeMem = currentOperationTime
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       writingOperationTime,
                                                                       writingOperationDataHolding, numOperations)
    #   * Memory (complemented)
    binaryMem = complement_binary_list(binaryMem)
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem, writingOperationTime,
                                                         writingOperationDataHolding)

    ## 4) Read all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)

    ## 5) Write the complementary of the current memory
    #   * Cue
    currentOperationTimeMem = currentOperationTime
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       writingOperationTime,
                                                                       writingOperationDataHolding, numOperations)
    #   * Memory (complemented)
    binaryMem = complement_binary_list(binaryMem)
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                         writingOperationTime,
                                                         writingOperationDataHolding)

    ## 6) Read all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)

    return cue, mem, currentOperationTime, numOperations


def tb_piramidal_reinforced(cueSize, memSize, cueSizeInBin, readingOperationTime, readingOperationDataHolding, writingOperationTime, writingOperationDataHolding):
    """
    Create the following sequence: for each cue write the cue as a memory and read it at the same time (reinforced writing),
    read all cues, reinforced write them but complemented, read all cues, reinforced write them but complemented again
    and read all cues.

    @param cueSize:
    @param memSize:
    @param cueSizeInBin:
    @param readingOperationTime:
    @param readingOperationDataHolding:
    @param writingOperationTime:
    @param writingOperationDataHolding:
    @return:
    """
    # 1) Write and read all memories alternatively
    # + Create the input cue activity vector
    #   * Create the empty cue vector
    cue = [[] for i in range(cueSizeInBin)]
    #   * Create the list of cues in decimal
    decimalCue = [i + 1 for i in range(cueSize)]
    #   * Convert the cue from decimal to binary and fix it to the correct input size
    binaryCue = format_cue_vectors(decimal_to_binary_list(decimalCue), cueSizeInBin)
    #   * Assign the binary values to each input cue neuron on the correct timestamp
    currentOperationTime = 1
    numOperations = 0
    cue, numOperations, currentOperationTime = create_alternate_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                                 [writingOperationTime,
                                                                                  readingOperationTime],
                                                                                 [writingOperationDataHolding,
                                                                                  readingOperationDataHolding],
                                                                                 numOperations)

    # + Create the input mem activity vector
    #   * Create the empty mem vector
    mem = [[] for i in range(memSize)]
    #   * Create the list of memories in decimal
    numOperationsMem = int(numOperations / 2)
    decimalMem = [(i + 1) % (2 ** memSize) for i in range(numOperationsMem)]
    #   * Convert the mem from decimal to binary and fix it to the correct input size
    binaryMem = format_cue_vectors(decimal_to_binary_list(decimalMem), memSize)
    #   * Generate the data to store
    currentOperationTimeMem = 1
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                         writingOperationTime + readingOperationTime,
                                                         writingOperationDataHolding)

    # 2) Read all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)

    # 3) Write and read the complementary
    #   * Cue
    currentOperationTimeMem = currentOperationTime
    cue, numOperations, currentOperationTime = create_alternate_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                                 [writingOperationTime,
                                                                                  readingOperationTime],
                                                                                 [writingOperationDataHolding,
                                                                                  readingOperationDataHolding],
                                                                                 numOperations)
    #   * Memories (complemented)
    binaryMem = complement_binary_list(binaryMem)
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                         writingOperationTime + readingOperationTime,
                                                         writingOperationDataHolding)

    # 4) Read all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)

    # 5) Write and read the complementary
    #   * Cue
    currentOperationTimeMem = currentOperationTime
    cue, numOperations, currentOperationTime = create_alternate_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                                 [writingOperationTime,
                                                                                  readingOperationTime],
                                                                                 [writingOperationDataHolding,
                                                                                  readingOperationDataHolding],
                                                                                 numOperations)
    #   * Memories (complemented)
    binaryMem = complement_binary_list(binaryMem)
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                         writingOperationTime + readingOperationTime,
                                                         writingOperationDataHolding)

    # 6) Read all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)
    return cue, mem, currentOperationTime, numOperations


def tb_stress_reinforced(cueSize, memSize, cueSizeInBin, readingOperationTime, readingOperationDataHolding, writingOperationTime, writingOperationDataHolding):
    """
    Create the same sequence that tb_piramidal_reinforced but adding at the end 3 reading of all cues and 3 reinforced
    writings operations to try to stress the network

    @param cueSize:
    @param memSize:
    @param cueSizeInBin:
    @param readingOperationTime:
    @param readingOperationDataHolding:
    @param writingOperationTime:
    @param writingOperationDataHolding:
    @return:
    """
    # 1) Write and read all memories alternatively
    # + Create the input cue activity vector
    #   * Create the empty cue vector
    cue = [[] for i in range(cueSizeInBin)]
    #   * Create the list of cues in decimal
    decimalCue = [i + 1 for i in range(cueSize)]
    #   * Convert the cue from decimal to binary and fix it to the correct input size
    binaryCue = format_cue_vectors(decimal_to_binary_list(decimalCue), cueSizeInBin)
    #   * Assign the binary values to each input cue neuron on the correct timestamp
    currentOperationTime = 1
    numOperations = 0
    cue, numOperations, currentOperationTime = create_alternate_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                                 [writingOperationTime, readingOperationTime],
                                                                                 [writingOperationDataHolding,readingOperationDataHolding], numOperations)

    # + Create the input mem activity vector
    #   * Create the empty mem vector
    mem = [[] for i in range(memSize)]
    #   * Create the list of memories in decimal
    numOperationsMem = int(numOperations/2)
    decimalMem = [(i + 1) % (2 ** memSize) for i in range(numOperationsMem)]
    #   * Convert the mem from decimal to binary and fix it to the correct input size
    binaryMem = format_cue_vectors(decimal_to_binary_list(decimalMem), memSize)
    #   * Generate the data to store
    currentOperationTimeMem = 1
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                         writingOperationTime + readingOperationTime,
                                                         writingOperationDataHolding)

    # 2) Read all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)

    # 3) Write and read the complementary
    #   * Cue
    currentOperationTimeMem = currentOperationTime
    cue, numOperations, currentOperationTime = create_alternate_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                                 [writingOperationTime, readingOperationTime],
                                                                                 [writingOperationDataHolding,readingOperationDataHolding], numOperations)
    #   * Memories (complemented)
    binaryMem = complement_binary_list(binaryMem)
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                         writingOperationTime + readingOperationTime,
                                                         writingOperationDataHolding)

    # 4) Read all cues
    cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding, numOperations)

    # 5) Write and read the complementary
    #   * Cue
    currentOperationTimeMem = currentOperationTime
    cue, numOperations, currentOperationTime = create_alternate_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                                 [writingOperationTime, readingOperationTime],
                                                                                 [writingOperationDataHolding,readingOperationDataHolding], numOperations)
    #   * Memories (complemented)
    binaryMem = complement_binary_list(binaryMem)
    mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                         writingOperationTime + readingOperationTime,
                                                         writingOperationDataHolding)

    # 6) Read all cues 3 times
    for i in range(3):
        cue, numOperations, currentOperationTime = create_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                           readingOperationTime,
                                                                           readingOperationDataHolding, numOperations)

    # 7) Write and read all memories alternatively and complemented 3 times
    for i in range(3):
        #   * Cue
        currentOperationTimeMem = currentOperationTime
        cue, numOperations, currentOperationTime = create_alternate_cue_input_vector(cue, binaryCue, currentOperationTime,
                                                                                     [writingOperationTime,
                                                                                      readingOperationTime],
                                                                                     [writingOperationDataHolding,
                                                                                      readingOperationDataHolding],
                                                                                     numOperations)
        #   * Memories (complemented)
        binaryMem = complement_binary_list(binaryMem)
        mem, currentOperationTime = create_mem_input_vector(mem, binaryMem, currentOperationTimeMem,
                                                             writingOperationTime + readingOperationTime,
                                                             writingOperationDataHolding)

    return cue, mem, currentOperationTime, numOperations


def tb_random_operations(cueSize, memSize, cueSizeInBin, readingOperationTime, readingOperationDataHolding, writingOperationTime, writingOperationDataHolding, numberOfOperations):
    """
    Generate a random sequence of reading and writing operations with random cues and memories values in the limits
    of the network parameters

    @param cueSize:
    @param memSize:
    @param cueSizeInBin:
    @param readingOperationTime:
    @param readingOperationDataHolding:
    @param writingOperationTime:
    @param writingOperationDataHolding:
    @param numberOfOperations:
    @return:
    """
    # Create the vector of random operations: 0 = learning and 1 = recalling
    operations = np.random.randint(0, 2, numberOfOperations)
    numLearning = np.count_nonzero(operations==0)
    numRecalling = np.count_nonzero(operations==1)
    # Create the vector of random operations and memories values
    decimalCue = np.random.randint(1, cueSize + 1, numberOfOperations)
    decimalMem = np.random.randint(1, 2 ** memSize, numberOfOperations)

    # Convert the memories and cue from decimal to binary and fix it to the correct input size
    binaryCue = format_cue_vectors(decimal_to_binary_list(decimalCue), cueSizeInBin)
    binaryMem = format_cue_vectors(decimal_to_binary_list(decimalMem), memSize)

    # Create the empty cue and mem vector
    cue = [[] for i in range(cueSizeInBin)]
    mem = [[] for i in range(memSize)]

    # Associate values to neurons
    currentOperationTime = 1
    numOperations = 0
    cue, mem, currentOperationTime, numOperations = create_input_vector_from_operations(mem, cue, operations, binaryMem,
                                                                                              binaryCue, currentOperationTime,
                                                                                              [writingOperationTime,
                                                                                               readingOperationTime],
                                                                                              [writingOperationDataHolding,
                                                                                               readingOperationDataHolding],
                                                                                              numOperations)
    return cue, mem, currentOperationTime, numOperations, numLearning, numRecalling


def testbench(cueSize, memSize, cueSizeInBin, readingOperationTime, readingOperationDataHolding, writingOperationTime, writingOperationDataHolding, tbPath, numberOfOperations):
    """
    Call a battery of memory testbench to generate the input sequence to the spike memory

    @param cueSize: Max number of patterns to store
    @param memSize: Size of patterns to store (number of bits)
    @param cueSizeInBin: input cue size in binary
    @param readingOperationTime: Time to begin the next operation after a read operation
    @param readingOperationDataHolding: Data holding time at the input for a reading operation
    @param writingOperationTime: Time to begin the next operation after a write operation
    @param writingOperationDataHolding: Data holding time at the input for a writing operation
    @param tbPath: path to store the testbench
    @param numberOfOperations: number of random operation for the random test
    @return:
    """

    # Create the directory to store the tb if it isn't exist
    tools.check_and_create_folder(tbPath)
    tbBasePath = tools.check_and_create_folder(tbPath + "tb_" + time.strftime("%Y_%m_%d__%H_%M_%S") + "/")

    # Testbench 1 -> create a piramidal sequence of input
    cue_seq, mem_seq, minTimeSim, numOperations = tb_piramidal_sequence(cueSize, memSize, cueSizeInBin, readingOperationTime, readingOperationDataHolding, writingOperationTime, writingOperationDataHolding)
    print("Testbench 1: piramidal sequence")
    print("Min simulation time to simulate all operations = " + str(minTimeSim) + " ms")
    print("Num of operations = " + str(numOperations))
    # Write the results
    tb_data = "[input_cue]\nInputSpikesCue = " + str(cue_seq) + "\n[input_mem]\nInputSpikesMem = " + str(mem_seq)
    tbFullPath = tools.check_and_create_folder(tbBasePath + "tb1_piramidal/")
    path, filename = tools.write_file(tbFullPath, "input_spikes", ".ini", tb_data)
    print(path + "\n\n")

    # Testbench 2 -> create a piramidal sequence of input with reinforced writing (write and read in the same cue at the same time)
    cue_seq, mem_seq, minTimeSim, numOperations = tb_piramidal_reinforced(cueSize, memSize, cueSizeInBin,
                                                                          readingOperationTime,
                                                                          readingOperationDataHolding,
                                                                          writingOperationTime,
                                                                          writingOperationDataHolding)
    print("Testbench 2: piramidal sequence with reinforced writing")
    print("Min simulation time to simulate all operations = " + str(minTimeSim) + " ms")
    print("Num of operations = " + str(numOperations))
    # Write the results
    tb_data = "[input_cue]\nInputSpikesCue = " + str(cue_seq) + "\n[input_mem]\nInputSpikesMem = " + str(mem_seq)
    tbFullPath = tools.check_and_create_folder(tbBasePath + "tb2_piramidal_reinforced/")
    path, filename = tools.write_file(tbFullPath, "input_spikes", ".ini", tb_data)
    print(path + "\n\n")

    # Testbench 3 -> create alternate operation in memory (write and read in the same cue)
    cue_seq, mem_seq, minTimeSim, numOperations = tb_stress_reinforced(cueSize, memSize, cueSizeInBin,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding,
                                                                       writingOperationTime,
                                                                       writingOperationDataHolding)
    print("Testbench 3: stress the network with reinforced writing")
    print("Min simulation time to simulate all operations = " + str(minTimeSim) + " ms")
    print("Num of operations = " + str(numOperations))
    # Write the results
    tb_data = "[input_cue]\nInputSpikesCue = " + str(cue_seq) + "\n[input_mem]\nInputSpikesMem = " + str(mem_seq)
    tbFullPath = tools.check_and_create_folder(tbBasePath + "tb3_stress_reinforced/")
    path, filename = tools.write_file(tbFullPath, "input_spikes", ".ini", tb_data)
    print(path + "\n\n")

    # Testbench 4 -> random operations
    cue_seq, mem_seq, minTimeSim, numOperations, numLearning, numRecalling = tb_random_operations(cueSize, memSize, cueSizeInBin,
                                                                       readingOperationTime,
                                                                       readingOperationDataHolding,
                                                                       writingOperationTime,
                                                                       writingOperationDataHolding, numberOfOperations)
    print("Testbench 4: random operations")
    print("Min simulation time to simulate all operations = " + str(minTimeSim) + " ms")
    print("Num of operations = " + str(numOperations))
    print(" - Learning = " + str(numLearning))
    print(" - Recalling = " + str(numRecalling))
    # Write the results
    tb_data = "[input_cue]\nInputSpikesCue = " + str(cue_seq) + "\n[input_mem]\nInputSpikesMem = " + str(mem_seq)
    tbFullPath = tools.check_and_create_folder(tbBasePath + "tb4_random_operations/")
    path, filename = tools.write_file(tbFullPath, "input_spikes", ".ini", tb_data)
    print(path + "\n\n")


if __name__ == "__main__":
    # * Open configparser object interface to read config files
    config = configparser.ConfigParser()
    #   + Check the active config file directory
    config.read("config_files/configFileParameters.ini")
    activeConfigFilePath = "config_files/" + eval(config["configFileParameters"]["activeConfigFiles"]) + "/"
    #   + Input memory parameters
    config.read(activeConfigFilePath + "memory_config.ini")
    #       - Max number of patterns to store
    cueSize = eval(config["memory"]["cueSize"])
    #       - Size of patterns to store (number of bits)
    memSize = eval(config["memory"]["memSize"])
    #       - Calculate the input cue size in binary
    cueSizeInBin = math.ceil(math.log2(cueSize + 1))
    #   + Memory times
    config.read(activeConfigFilePath + "simulation_config.ini")
    #       - Time to begin the next operation after a read operation
    readingOperationTime = eval(config["testbench"]["readingOperationTime"])
    #       - Time to begin the next operation after a write operation
    writingOperationTime = eval(config["testbench"]["writingOperationTime"])
    #   + Data holding time at the input
    #       - Read
    readingOperationDataHolding = eval(config["testbench"]["readingOperationDataHolding"])
    #       - Write
    writingOperationDataHolding = eval(config["testbench"]["writingOperationDataHolding"])
    #   + Path to store the testbench txt
    tbPath = eval(config["testbench"]["tbPath"])
    #   + Number of randoms operations for the random testbench
    numberOfOperations = eval(config["testbench"]["numberOfOperations"])

    # * Create battery of test input sequence
    testbench(cueSize, memSize, cueSizeInBin, readingOperationTime, readingOperationDataHolding, writingOperationTime,
              writingOperationDataHolding, tbPath, numberOfOperations)
