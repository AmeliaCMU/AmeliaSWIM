# AmeliaSWIM

This repository contains the raw dataset download scripts as well as scripts to preprocess and filter the data:

### Amelia: A Large Dataset and Model for Airport Surface Movement Forecasting [[paper](todo)]

[Ingrid Navarro](https://navars.xyz) *, [Pablo Ortega-Kral](https://paok-2001.github.io) *, [Jay Patrikar](https://www.jaypatrikar.me) *, Haichuan Wang,
Zelin Ye, Jong Hoon Park, [Jean Oh](https://cmubig.github.io/team/jean_oh/) and [Sebastian Scherer](https://theairlab.org/team/sebastian/)

*Equal contribution

## Overview

**Amelia-48** 

[Amelia-48](https://ameliacmu.github.io/amelia-dataset/) dataset contains the trajectory as well .




## Pre-requisites

### Installation

#### Basic Setup

Install and activate the environment:
```bash
conda activate swim
```
#### Download raw files:

The raw SWIM .njson.gz files can be downloaded using the following scripts:

Download the GitHub repository and install requirements:

```bash
git clone git@github.com:AmeliaCMU/AmeliaTF.git
cd AmeliaTF
pip install -e .
```

#### Full Setup

If you're interested in using all of our [tools](https://ameliacmu.github.io/amelia-dataset/), you can install our framework through this [script](https://github.com/AmeliaCMU/AmeliaScenes/install.sh).

### Dataset

To run this repository, you first need to download the amelia dataset. Follow the instructions [here](https://github.com/AmeliaCMU/AmeliaScenes/DATASET.md) to download and setup the dataset.

Once downloaded, create a symbolic link into  ```datasets```:

```bash
cd datasets
ln -s /path/to/the/amelia/dataset .
```

### Scenario Pre-processing

Once you've downloaded the dataset and installed the required modules. You need to post-process the dataset. Follow the instructions [here](https://github.com/AmeliaCMU/AmeliaScenes/README.md).

### Additional Notes

Our repository's structure is based on this [template](https://github.com/ashleve/lightning-hydra-template), which uses Hydra and Pytorch Lightning. We recommend going through their [README](https://github.com/ashleve/lightning-hydra-template?tab=readme-ov-file#your-superpowers) for further details into the code's functionalities.

## How to use

Activate your amelia environment (**Please make sure to follow the pre-requisites guidelines above above**):

```bash
conda activate amelia
```

### Training a Model

The general format for running a training experiment is:

```bash
python src/train.py data=[data_config] model=[model_config] trainer=[trainer_config]
```

where:

- ```[data_config]```, represents a dataset configuration specified under ```./configs/data```
- ```[model_config]```, represents a model configuration specified under ```./configs/model```
- ```[trainer_config]```, represents the trainer to be used, (e.g., CPU, GPU, DDP, etc), specified under ```./configs/trainer```

For example, to train our model on GPU using all of our currently supported airports, you would run:

```bash
python src/train.py data=seen-all model=marginal trainer=gpu
```

### Evaluating a Model

If you already have a pre-trained checkpoint you can run evaluation only using `eval.py` and following a similar format as above. However, you need to provide the path to the pre-trained weights. For example,

`bash
python src/eval.py data=seen-all model=marginal trainer=gpu ckpt_path=/path/to/pretrained/weights.ckpt
`

### Our experiments

We provide the configuration combination to run our experiments, as well as our pre-trained weights.

#### Single-Airport Experiments (Table 5 in our paper)

The model configuration used for all of these experiments was `marginal.yaml`.

| Airport                                   | Airport ICAO | Data Config | ADE@20 | FDE@20 | ADE@50 | FDE@50 | Weights  |
|:-----------------------------------------:|:------------:|:-----------:|:------:| :----: | :----: | :----: | :------: |
| Ted Stevens Anchorage Intl. Airport       |      PANC    | `panc.yaml` | 10.11  | 20.87  | 38.84  | 101.89 | [panc](todo) |
| Boston-Logan Intl. Airport                |      KBOS    | `kbos.yaml` |  5.58  | 10.90  | 21.34  |  53.76 | [kbos](todo) |
| Ronald Reagan Washington Natl. Airport    |      KDCA    | `kdca.yaml` |  4.74  |  9.22  | 16.42  |  40.57 | [kdca](todo) |
| Newark Liberty Intl. Airport              |      KEWR    | `kewr.yaml` |  6.61  | 12.92  | 23.68  |  57.63 | [kewr](todo) |
| John F. Kennedy Intl. Airport             |      KJFK    | `kjfk.yaml` |  4.58  |  9.52  | 17.11  |  41.19 | [kjfk](todo) |
| Los Angeles Intl. Airport                 |      KLAX    | `klax.yaml` | 11.36  | 20.63  | 36.08  |  88.25 | [klax](todo) |
| Chicago-Midway Intl. Airport              |      KMDW    | `kmdw.yaml` |  3.30  |  6.12  | 11.50  |  28.80 | [kmdw](todo) |
| Louis Armstrong New Orleans Intl. Airport |      KMSY    | `kmsy.yaml` |  2.73  |  5.12  |  9.89  |  25.68 | [kmsy](todo) |
| Seattle-Tacoma Intl. Airport              |      KSEA    | `ksea.yaml` |  9.76  | 18.35  | 29.94  |  65.82 | [ksea](todo) |
| San Francisco Intl. Airport               |      KSFO    | `ksfo.yaml` |  5.06  |  9.82  | 17.05  |  40.23 | [ksfo](todo) |

<hr>

#### Multi-Airport Experiments (Table 6 and 8 in our paper)

The model configuration used for all of these experiments was also `marginal.yaml`.

| Seen Airport(s)                                            | Unseen Airport(s)                                    | Data Config     | Avg. ADE@20 | Avg. FDE@20 | Avg. ADE@50 | Avg. FDE@50 | Weights |
| :--------------------------------------------------------: | :--------------------------------------------------: | :-------------: | :---------: | :---------: | :---------: | :---------: | :-----: |
| KMDW                                                       | KEWR, KBOS, KSFO, KSEA, KDCA, PANC, KLAX, KJFK, KMSY | `seen-1.yaml`   |     3.30    |     6.12    |    11.50    |    28.80    | [seen-1](todo) |
| KMDW, KEWR                                                 | KBOS, KSFO, KSEA, KDCA, PANC, KLAX, KJFK, KMSY       | `seen-2.yaml`   |     3.31    |     6.23    |    11.84    |    28.89    | [seen-2](todo) |
| KMDW, KEWR, KBOS                                           | KSFO, KSEA, KDCA, PANC, KLAX, KJFK, KMSY             | `seen-3.yaml`   |     3.26    |     6.59    |    12.46    |    31.81    | [seen-3](todo) |
| KMDW, KEWR, KBOS, KSFO                                     | KSEA, KDCA, PANC, KLAX, KJFK, KMSY                   | `seen-4.yaml`   |     3.52    |     6.74    |    12.71    |    31.64    | [seen-4](todo) |
| KMDW, KEWR, KBOS, KSFO, KSEA, KDCA, PANC                   | KLAX, KJFK, KMSY                                     | `seen-7.yaml`   |     3.59    |     7.03    |    14.35    |    38.62    | [seen-7](todo) |
| KMDW, KEWR, KBOS, KSFO, KSEA, KDCA, PANC, KLAX, KJFK, KMSY | -                                                    | `seen-all.yaml` |     3.88    |     7.70    |    15.30    |    40.91    | [seen-all](todo) |

<hr>

#### Other Experiments

- We trained our models under a **marginal** prediction setting, but we have support for training models on a **joint** prediction setting. To change the prediction paradigm, change the model parameter to `joint`. For example:

```bash
python src/train.py data=seen-all model=joint trainer=gpu
```

- Our model can be trained with and without context (maps). To train the trajectory-only model, use either `marginal_traj` or `joint_traj` configurations. For example,

```bash
python src/train.py data=seen-all model=marginal_traj trainer=gpu
```

<hr>

## BibTeX

If you find our work useful in your research, please cite us!

```bibtex
@article{navarro2024amelia,
  title={Amelia: A Large Model and Dataset for Airport Surface
Movement Forecasting},
  author={Navarro, Ingrid and Ortega-Kral, Pablo and Patrikar, Jay, and Haichuan, Wang and Park, Jong Hoon and Oh, Jean and Scherer, Sebastian},
  journal={arXiv preprint arXiv:2309.08889},
  year={2024}
}
```