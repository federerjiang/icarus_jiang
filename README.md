# This program will be runned in the server.

# Icarus ICN caching simulator
Icarus is a Python-based discrete-event simulator for evaluating caching
performance in Information Centric Networks (ICN).

Icarus is not bound to any specific ICN architecture. Its design allows users
to implement and evalute new caching policies or caching and routing strategy
with few lines of code.

This document explains how to configure and run the simulator.


## Usage

### Run simulations

To use Icarus with the currently implemented topologies and models of caching policies and strategies you need to do the following.

First, create a configuration file with all the desired parameters of your
simulation. You can modify the file `config.py`, which is a well documented
example configuration. You can even use the configuration file as it is just
to get started. Alternatively, have a look at the `examples` folder which
contains examples of configuration files for various use cases.

Second, run Icarus by running the script `icarus.py` using the following syntax

    $ python icarus.py --results RESULTS_FILE CONF_FILE

where:

 * `RESULTS_FILE` is the [pickle](http://docs.python.org/3/library/pickle.html) file in which results will be saved,
 * `CONF_FILE` is the configuration file

Example usage could be:

    $ python icarus.py --results results.pickle config.py

After saveing the results in pickle format you can extract them in a human
readable format using the `printresults.py` script from the `scripts` folder. Example usage could be:

    $ python scripts/printresults.py results.pickle > results.txt

Icarus also provides a set of helper functions for plotting results. Have a look at the `examples`
folder for plot examples.

By executing the steps illustrated above it is possible to run simulations using the
topologies, cache policies, strategies and result collectors readily available on
Icarus. Icarus makes it easy to implement new models to use in simulations.

To implement new models, please refer to the description of the simulator 
provided in this paper:

L.Saino, I. Psaras and G. Pavlou, Icarus: a Caching Simulator for Information Centric
Networking (ICN), in Proc. of SIMUTOOLS'14, Lisbon, Portugal, March 2014.
\[[PDF](http://www.ee.ucl.ac.uk/~lsaino/publications/icarus-simutools14.pdf)\],
\[[Slides](http://www.ee.ucl.ac.uk/~lsaino/publications/icarus-simutools14-slides.pdf)\],
\[[BibTex](http://www.ee.ucl.ac.uk/~lsaino/publications/icarus-simutools14.bib)\]

Otherwise, please browse the source code. It is very well documented and easy to
understand.

### Modelling tools
Icarus provides utilities for modelling the performance of caches and
work with traffic traces. The code is included in the `icarus.tools` package.
These tools are described in detail in [this paper](http://www.ee.ucl.ac.uk/~lsaino/publications/icarus-simutools14.pdf).

### Run tests
To run the unit test cases you can use the `test.py` script located in the directory of
this README file.

    $ python test.py
