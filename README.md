# A bio-inspired implementation of a sparse-learning spike-based hippocampus memory model

<h2 name="Description">Description</h2>
<p align="justify">
Code on which the paper entitled "A bio-inspired implementation of a sparse-learning spike-based hippocampus memory model" is based, sent to a journal and awaiting review.
</p>
<p align="justify">
A fully functional hippocampal bio-inspired memory model implemented on the <a href="https://apt.cs.manchester.ac.uk/projects/SpiNNaker/">SpiNNaker</a> hardware platform using the technology of the Spiking Neuronal Network (SNN) is presented. The code is written in Python and makes use of the PyNN library and their adaptation for SpiNNaker called <a href="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjaxOCWhrn3AhVL1BoKHVtQDvsQFnoECAkQAQ&url=https%3A%2F%2Fgithub.com%2FSpiNNakerManchester%2FsPyNNaker&usg=AOvVaw3e3TBMJ-08yBqtsKza_RiE">sPyNNaker</a>. In addition, the necessary scripts to replicate the tests and plots carried out in the paper are included, together with data and plots of the first tests.
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

<strong>Abstract</strong>: 

<strong>Keywords</strong>: 

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
		<li><strong>neural blocks</strong> last repository version (link to be uploaded)</li>
		<li><strong>numpy</strong> 1.21.4</li>
		<li><strong>matplotlib</strong> 3.5.0</li>
		<li><strong>xlsxWriter</strong> 3.0.2</li>
		<li><strong>sPyBlocks</strong>: version (pending)</li>
	</ul>
</ol>
</p>


<h2 name="RepositoryContent">Repository content</h3>
<p align="justify">
<ul>
	<li><a href="DG_CA3_CA1_one_hot.py">DG_CA3_CA1_one_hot.py</a>: script responsible for building and simulating the oscillating memory model, as well as storing the simulation data in a file in the <a href="data/">data</a> folder, according to the configuration specified in the selected <a href="config_files/">config_files</a> folder.</li>
	<li><a href="test_DG_CA3_CA1_one_hot.py">test_DG_CA3_CA1_one_hot.py</a>: script in charge of carrying out the simulation of the memory model and the plotting of the necessary graphics of the simulation. The conditions of the simulation are as indicated in the configuration specified in the selected <a href="config_files/">config_files</a> folder.</li>
	<li><a href="memory_testbench.py">memory_testbench.py</a>: script in charge of generating the file with the input spikes of the memory model (in <a href="tb/">tb</a> folder) needed to perform the different tests.</li>
	<li><a href="tools.py">tools.py</a>,<a href="plot.py">plot.py</a> and <a href="excel_controller.py">excel_controller.py</a>: set of functions used as a tool for data processing, graphical representation of the data and generation of excel files summarising the result of the experimentation respectively.</li>
	<li><a href="data/">data</a> and <a href="plot/">plot</a>: folders where the data files from the network simulation are stored and where the plots of these data are stored respectively.</li>
	<li><a href="config_files/">config_files</a> folder: contains different folders, one for each desired configuration of the memory model. The <a href="config_files/configFileParameters.ini">configFileParameters.ini</a> file indicates which of all the configurations are to be used. Within each configuration there are 4 files:</li>
		<ul>
			<li><a href="config_files/test_01/input_spikes.ini">input_spikes.ini</a>: input spikes to the memory model.</li>
			<li><a href="config_files/test_01/memory_config.ini">memory_config.ini</a>: parameters shaping the memory model.</li>
			<li><a href="config_files/test_01/network_config.json">network_config.json</a>: construction parameters of the neuron and synapse models of the network (it is advisable not to modify them).</li>
			<li><a href="config_files/test_01/simulation_config.ini">simulation_config.ini</a>: all parameters related to the simulation and graphical representation of the results.</li>
		</ul>
</ul>
</p>


<h2 name="Usage">Usage</h2>
<p align="justify">
Still under construction.
</p>
<p align="justify">

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
