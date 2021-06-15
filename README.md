## Paper Title

M. E. Gursoy, L. Liu, S. Truex and L. Yu, "Differentially Private and Utility Preserving Publication of Trajectory Data," in *IEEE Transactions on Mobile Computing*, vol. 18, no. 10, pp. 2315-2329, 1 Oct. 2019, doi: 10.1109/TMC.2018.2874008.

## Introduction

This repo is the simulation of DP-Star. DP-Star is a methodical framework for publishing trajectory data with differential privacy guarantee as well as high utility preservation.

### Installation

none

### Usage

#### overall call files

The files for call is **config.py** and **main.py**

In **config.py**, you can set the parmeter to set the middlewave file paths, privacy budget and etc.

In **main.py**, you can call the func in dpstar and utils modules.

### DP-Star components

- Adaptive Grid Construction；

- Trip Distribution Extraction；

- Mobility Model Construction；

- Route Length Estimation；

- Synthetic Trajectory Generation；
