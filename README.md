# Espaloma
you wait long enough and some drug-design samaritan will do it for you.
https://github.com/choderalab/espaloma

Espaloma is an ML algorithm that learns the parameters from a classical force field perspective instead of QM (speeds things up by 2,3 orders of mag. from current ML SOTA).

Made atom-typing continuous with Graph Neural Networks (no need to table look-up).

Espaloma has a pretrained ff (espaloma-0.3.0). Its been trained directly from quantum chemical energies computed with B3LYP-D3BJ/DZVP. The dataset is available to download from  https://github.com/choderalab/download-qca-datasets. The comprehensive list can be read pp17-18 (https://arxiv.org/abs/2307.07085).

Follow Espaloma/run_pretrained README and download the dependencies required to run the script, run_pretrained.sh

You can also train your own espaloma ff by feeding it .xyz of optimised molecules and its energy.
