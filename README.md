[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/static/v1?message=Python&color=3776AB&logo=Python&logoColor=FFFFFF&label=)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-276DC3?&logo=r&logoColor=white)](https://www.r-project.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?logo=docker&logoColor=white)](https://www.docker.com/)
[![MLflow](https://img.shields.io/static/v1?message=MLflow&color=0194E2&logo=MLflow&logoColor=FFFFFF&label=)](https://mlflow.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Google Colab](https://img.shields.io/static/v1?message=Google+Colab&color=222222&logo=Google+Colab&logoColor=F9AB00&label=)](https://colab.research.google.com/)
<a id="binder_link">[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maciejskorski/enhanced-pll-trng/v0.0.4)</a>

# Enhancing Quality and Security of the PLL-TRNG

## :star: Authors

<p align="center">
    <a href="https://skorski.lu"><strong>Maciej Skórski</strong></a>,
    <a href="mailto:quentin.dallison@thalesgroup.com"><strong>Quentin Dallison</strong></a>,
    <a href="mailto:nathalie.bochard@univ-st-etienne.fr"><strong>Nathalie Bochard</strong></a>,
    <a href="mailto:florent.bernard@univ-st-etienne.fr"><strong>Florent Bernard</strong></a>,
    <a href="mailto:fischer@univ-st-etienne.fr"><strong>Viktor Fisher</strong></a>
</p>

## :memo: About

This repository contains supplementary material (data and code) to reproduce the evaluation of a true random number generator presented in :open_book: "Enhancing Quality and Security of the PLL-TRNG" at TCHES 2023.

<figure>
<img src="images/pll_trng_new.jpg" style="display:block; margin:auto"/>
<figcaption style="text-align:center">Figure: PLL-TRNG Architecture</figcaption>
</figure>

## :file_folder: Data

All necessary data can be found under the `data` directory.
The zipped data are available to download from [releases](https://github.com/maciejskorski/enhanced-pll-trng/releases).

<details>
  <summary>Read more about data structure</summary>
  
Data used in experiments are stored under the `data` directory.
Sub-directories at the first level group experiments according to the environmental conditions (regular conditions, corner values and a temperature attack scenario).
- The file in `data/CornerAnalysis` regroups all results accross all cards, configurations and external conditions;
- The temperature attack was executed on a single Spartan device, and its results are in `data/TemperatureAttack`;
- Further sub-directories in `data/Regular` group acquired data according to the FPGA card family (CV - Cyclone®V, S6 - Spartan™6, SF - SmartFusion2®), in which we find all configurations as described in the paper (A, B, or C with one or two PLL outputs as indicated by the suffix, e.g. A_1 vs A_2).
Note that two Spartan devices were tested, both placed on the cards version 11, cards #2 and #8 marked S6v11_2 and S6v11_8.
For each experiment, the data file contains the bitstream available at the sampler output, i.e. the D flip-flop output marked dff_out in Figure 3. The binary files end in `_dff.bin` and the associated metadata files have extension `.log`.

```
├───📁 CornerAnalysis/
│   └───📄 corner_values.xlsx
├───📁 TemperatureAttack/
│   └───📄 S6_C_freezing attack_km476_kd495_dff.bin
├───📁 Regular/
│   ├───📁 CVv12_4/
│   │   ├───📁 A_1/
│   │   │   └───...
│   │   ├───📁 A_2/
│   │   │   └───...
│   │   ├───📁 B_1/
│   │   │   └───...
│   │   ├───📁 B_2/
│   │   │   └───...
│   │   ├───📁 C_1/
│   │   │   └───...
│   │   └───📁 C_2/
│   │       └───...
│   ├───📁 S6v11_2/
│   │   ├───📁 A_1/
│   │   │   └───...
│   │   ├───📁 A_2/
│   │   │   └───...
│   │   ├───📁 B_1/
│   │   │   └───...
│   │   ├───📁 B_2/
│   │   │   └───...
│   │   ├───📁 C_1/
│   │   │   └───...
│   │   └───📁 C_2/
│   │       └───...
│   ├───📁 S6v11_8/
│   │   ├───📁 A_1/
│   │   │   └───...
│   │   ├───📁 A_2/
│   │   │   └───...
│   │   ├───📁 B_1/
│   │   │   └───...
│   │   ├───📁 B_2/
│   │   │   └───...
│   │   ├───📁 C_1/
│   │   │   └───...
│   │   ├───📁 C_2/
│   │   │   └───...
│   │   └───📄 .DS_Store
│   └───📁 SF2v11_11/
│       ├───📁 A_1/
│       │   └───...
│       ├───📁 A_2/
│       │   └───...
│       ├───📁 B_1/
│       │   └───...
│       ├───📁 B_2/
│       │   └───...
│       ├───📁 C_1/
│       │   └───...
│       └───📁 C_2/
│           └───...
└───📄 data.zip
```

</details>

## 🖥 Code execution

The code is available in form of Python and R notebooks under the `src` directory. 
The notebooks run interactively under the customized [Docker Image of Jupyter](https://jupyter-docker-stacks.readthedocs.io/en/latest/).
For convenience, [the image](Dockerfile) provides the user with both software and data.

### Run Online with Docker

<!-- markdown-link-check-disable -->
For a single-click online access use  <a href="#binder_link">the Binder link at the top</a>.
<!-- markdown-link-check-enable -->

### Run Locally with Docker

On a machine with Docker (local computer, virtual machine on cloud) run this image
```console
docker run -it --rm -p 8888:8888 ghcr.io/maciejskorski/enhanced-pll-trng:latest
```
and follow instructions to access the repository via Jupyter. 

<details>
  <summary>See a snapshot </summary>
The Jupyter server will be available through a web browser, under http://127.0.0.1:8888/lab?token=...
![Jupyter Start](images/jupyter_start.png)
</details>



## :bar_chart: Scripts Overview

The code can be found under the `src` directory, as Python scripts and Python or R notebooks.

### ⚙ Generating configurations

[find_PLL-TRNG_configs.py](src/find_pll_trng_configs.py) is the Python script that generates the list of all possible configurations, along with the list of time distances between contributing bits. [The main code block](https://github.com/maciejskorski/new_pll_trng/blob/main/src/find_pll_trng_configs.py#L474-L494) contains the constraints of the state-space to explore. First developed by <a href="mailto:brice.colombier@univ-st-etienne.fr">Brice Colombier</a>, the authors modified this script to compute the time distances between contributing bits.

### 🏁 Data Basics

The notebook [raw_data_processing.ipynb](src/raw_data_processing.ipynb) shows how to process and visualize data samples. It reproduces Figures 10 and 11 from the paper.

### 💻 Theoretical Model Properties

The R notebook [stochastic_model.ipynb](src/stochastic_model.ipynb) explains in detail how to use the theoretical model. It reproduces Figures 4, 5, 6 and 7 from the paper.

### 🔬 Statistical Analysis under Regular Conditions

The notebook [model_analysis.ipynb](src/model_analysis.ipynb) runs the statistical analysis of the acquired data to validate empirically all of the model assumptions. It reproduces Table 4, Figure 12 and Figure 13 from the paper.

### 🌡️🔌 Analysis under Corner Values

The notebook [corner_values.ipynb](src/corner_values.ipynb) analyzes the data aquired under corner values of temperature and voltage.

### ❄️ Temperature Attack

A temperature attack was executed during acquisition and the results are shown in the animation below. As the TRNG was online, we blew cold air (around -40°C) directly on the chip to influence the jitter and the performance of the TRNG. Plotted are consecutive values of the empirical variance of the counter estimated on 4096 counter values (left) and the reconstructed period of the sampled PLL (right).
During the first 80 to 90 estimations of the counter variance, we see that it remains constant to 0.92-0.98. However, with a sudden drop in temperature, the samples seem to shift along the reconstructed period. We also observe a sharp increase in the estimated variance on the left panel to about 1.15.
In addition to the lower bound for counter variance that we defined in the paper, the experiment suggests that an embedded test dedicated to detecting a sudden change in counter variance could address third-party attacks.

![Temperature Attack](images/pll_trng_temperature_attack.gif)

## Links

- For random number generator standards, see [AIS-31 (New Draft)](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Certification/Interpretations/AIS_31_Functionality_classes_for_random_number_generators_e.pdf?__blob=publicationFile&v=5)
- For more about stochastic models for PLL-based designs, see ["Modern Random Number Generator Design - Case Study on a Secured PLL-based TRNG"](https://www.degruyter.com/document/doi/10.1515/itit-2018-0025/html?lang=en)
