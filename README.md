# A bio-inspired implementation of a sparse-learning spike-based hippocampus memory model

<h2 name="Description">Description</h2>
<p align="justify">
Code on which the paper entitled "A bio-inspired implementation of a sparse-learning spike-based hippocampus memory model" is based, sent to a journal and awaiting review.
</p>
<p align="justify">
A fully functional hippocampal bio-inspired memory model implemented on the <a href="https://apt.cs.manchester.ac.uk/projects/SpiNNaker/">SpiNNaker</a> hardware platform using the technology of the Spiking Neuronal Network (SNN) is presented. The code is written in Python and makes use of the PyNN library and their adaptation for SpiNNaker called <a href="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjaxOCWhrn3AhVL1BoKHVtQDvsQFnoECAkQAQ&url=https%3A%2F%2Fgithub.com%2FSpiNNakerManchester%2FsPyNNaker&usg=AOvVaw3e3TBMJ-08yBqtsKza_RiE">sPyNNaker</a>. In addition, the necessary scripts to replicate the tests and plots carried out in the paper are included, together with data and plots of the first tests.
</p>
<p align="justify">
Please go to section <a href="#CiteThisWork">cite this work</a> to learn how to properly reference the works cited here.
</p>


<h2>Table of contents</h2>
<p align="justify">
<ul>
<li><a href="#Description">Description</a></li>
<li><a href="#Article">Article</a></li>
<li><a href="#Instalation">Instalation</a></li>
<li><a href="#Usage">Usage</a></li>
<li><a href="#RepositoryContent">Repository content</a></li>
<li><a href="#CiteThisWork">Cite this work</a></li>
<li><a href="#Credits">Credits</a></li>
<li><a href="#License">License</a></li>
</ul>
</p>


<h2 name="Article">Article</h2>
<p align="justify">
<strong>Title</strong>: A bio-inspired implementation of a sparse-learning spike-based hippocampus memory model

<strong>Abstract</strong>: The nervous system, more specifically, the brain, is capable of solving complex problems simply and efficiently, far surpassing modern computers. In this regard, neuromorphic engineering is a research field that focuses on mimicking the basic principles that govern the brain in order to develop systems that achieve such computational capabilities. Within this field, bio-inspired learning and memory systems are still a challenge to be solved, and this is where the hippocampus is involved. It is the region of the brain that acts as a short-term memory, allowing the learning and unstructured and rapid storage of information from all the sensory nuclei of the cerebral cortex and its subsequent recall. In this work, we propose a novel bio-inspired memory model based on the hippocampus with the ability to learn memories, recall them from a cue (a part of the memory associated with the rest of the content) and even forget memories when trying to learn others with the same cue. This model has been implemented on the SpiNNaker hardware platform using Spiking Neural Networks, and a set of experiments and tests were performed to demonstrate its correct and expected operation. The proposed spike-based memory model generates spikes only when it receives an input, being energy efficient, and it needs 7 timesteps for the learning step and 6 timesteps for recalling a previously-stored memory. This work presents the first hardware implementation of a fully functional bio-inspired spike-based hippocampus memory model, paving the road for the development of future more complex neuromorphic systems.

<strong>Keywords</strong>: Hippocampus model, spiking neural networks, Neuromorphic engineering, CA3, DG, CA1, SpiNNaker, spike-based memory

<strong>Author</strong>: Daniel Casanueva-Morato

<strong>Contact</strong>: dcasanueva@us.es
</p>


<h2 name="Instalation">Instalation</h2>
<p align="justify">
<ol>
	<li>Have or have access to the SpiNNaker hardware platform. In case of local use, follow the installation instructions available on the <a href="http://spinnakermanchester.github.io/spynnaker/6.0.0/index.html">official website</a></li>
	<li>Python version 3.8.10</li>
	<li>Python libraries:</li>
	<ul>
		<li><strong>sPyNNaker8</strong>: last stable version <a href="http://spinnakermanchester.github.io/development/gitinstall.html">compiled from source</a></li>
		<li><strong>numpy</strong> 1.21.4</li>
		<li><strong>matplotlib</strong> 3.5.0</li>
		<li><strong>xlsxWriter</strong> 3.0.2</li>
		<li><strong>sPyBlocks</strong>: 0.0.1</li>
	</ul>
</ol>
</p>
<p align="justify">
To run any script, follow the python nomenclature: 
<code>
python script.py
</code>
</p>


<h2 name="RepositoryContent">Repository content</h3>
<p align="justify">
<ul>
	<li><p align="justify"><a href="DG_CA3_CA1_one_hot.py">DG_CA3_CA1_one_hot.py</a>: script responsible for building and simulating the oscillating memory model, as well as storing the simulation data in a file in the <a href="data/">data</a> folder, according to the configuration specified in the selected <a href="config_files/">config_files</a> folder.</p></li>
	<li><p align="justify"><a href="test_DG_CA3_CA1_one_hot.py">test_DG_CA3_CA1_one_hot.py</a>: script in charge of carrying out the simulation of the memory model and the plotting of the necessary graphics of the simulation. The conditions of the simulation are as indicated in the configuration specified in the selected <a href="config_files/">config_files</a> folder and the generated graphics are stored in <a href="plot/">plot</a>.</p></li>
	<li><p align="justify"><a href="memory_testbench.py">memory_testbench.py</a>: script in charge of generating the file with the input spikes of the memory model (in <a href="tb/">tb</a> folder) needed to perform the different tests.</p></li>
	<li><p align="justify"><a href="tools.py">tools.py</a>,<a href="plot.py">plot.py</a> and <a href="excel_controller.py">excel_controller.py</a>: set of functions used as a tool for data processing, graphical representation of the data and generation of excel files summarising the result of the experimentation respectively.</p></li>
	<li><p align="justify"><a href="data/">data</a> and <a href="plot/">plot</a>: folders where the data files from the network simulation are stored and where the plots of these data are stored respectively.</p></li>
	<li><p align="justify"><a href="config_files/">config_files</a> folder: contains different folders, one for each desired configuration of the memory model. The <a href="config_files/configFileParameters.ini">configFileParameters.ini</a> file indicates which of all the configurations are to be used. Within each configuration there are 4 files:</p></li>
		<ul>
			<li><p align="justify"><a href="config_files/test_01/input_spikes.ini">input_spikes.ini</a>: input spikes to the memory model. For learning operations, spikes need to be held for 3 time units at the input of the memory and no further operation can be performed until 7 time units later. In the case of recall operations, spikes must be displayed for a single time unit and 6 time units must be waited until the next operation. For more information, read the paper.</p></li>
			<li><p align="justify"><a href="config_files/test_01/memory_config.ini">memory_config.ini</a>: parameters shaping the memory model.</p></li>
			<li><p align="justify"><a href="config_files/test_01/network_config.json">network_config.json</a>: construction parameters of the neuron and synapse models of the network (it is advisable not to modify them).</p></li>
			<li><p align="justify"><a href="config_files/test_01/simulation_config.ini">simulation_config.ini</a>: all parameters related to the simulation and graphical representation of the results.</p></li>
		</ul>
</ul>
</p>


<h2 name="Usage">Usage</h2>
<p align="justify">
To perform memory tests, run <a href="test_DG_CA3_CA1_one_hot.py">test_DG_CA3_CA1_one_hot.py</a>. This script is in charge of building the memory model, i.e. calling <a href="DG_CA3_CA1_one_hot.py">DG_CA3_CA1_one_hot.py</a>, run the simulation and create the necessary visual resources on the simulation result.
</p>
<p align="justify">
In order to define the parameters of the memory model to be built and the conditions of the simulation to be run, it is necessary to create or modify a set of configuration files located in the folder <a href="config_files/">config_files</a>. You can have as many configurations of models and simulations as you want, each one must be contained in a different folder, and is the file <a href="config_files/configFileParameters.ini">configFileParameters.ini</a> in which you indicate which of all the configurations you want to use. The configuration must consist of 4 files, the contents of which are specified in <a href="#RepositoryContent">Repository content</a> section.
</p>
<p align="justify">
In case you want to try some of the tests discussed in the paper such as the stress test or the random access test, you can use <a href="memory_testbench.py">memory_testbench.py</a>. It generates the input_spikes.ini necessary to carry out the test, as well as indicating the simulation time required and the number of operations performed.
</p>
<p align="justify">
Finally, in order to be able to use the memory model as a module within a larger SNN network, we have developed a python package that includes this memory model (among others): sPyMem. You can install sPyMem via pip thanks to its <a href="https://pypi.org/project/sPyMem/">PyPi</a> distribution: <code>pip install sPyMem</code> or download it from source on their <a href="https://github.com/dancasmor/sPyMem/">github repository</a>. In this package, the memory model presented in this paper would be called <strong>hippocampus_with_forgetting</strong>.
</p>


<h2 name="CiteThisWork">Cite this work</h2>
<p align="justify">
Sent to a journal and awaiting review.
</p>


<h2 name="Credits">Credits</h2>
<p align="justify">
The author of the original idea is Daniel Casanueva-Morato while working on a research project of the <a href="http://www.rtc.us.es/">RTC Group</a>.

This research was partially supported by the Spanish grant MINDROB (PID2019-105556GB-C33/AEI/10.13039/501100011033). 

D. C.-M. was supported by a "Formación de Profesor Universitario" Scholarship from the Spanish Ministry of Education, Culture and Sport.
</p>


<h2 name="License">License</h2>
<p align="justify">
This project is licensed under the GPL License - see the <a href="https://github.com/dancasmor/A-bio-inspired-implementation-of-a-sparse-learning-spike-based-hippocampus-memory-model/blob/main/LICENSE">LICENSE.md</a> file for details.
</p>
<p align="justify">
Copyright © 2022 Daniel Casanueva-Morato<br>  
<a href="mailto:dcasanueva@us.es">dcasanueva@us.es</a>
</p>

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
