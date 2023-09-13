# ConjugatedEspaloma

Extending the Espaloma 3.0 Graph Neural Netowkr Force-Field for conjugated electronic materials. 

you wait long enough and some drug-design samaritan will solve all your molecular dynamics challenges: https://github.com/choderalab/espaloma

Espaloma is a Graph Neural Network that parameterises a classical force field from learned embeddings. This makes it 2-3 orders of magnitude faster than directly predicting force and energy with a GNN, which is the current state of the art. 

Espaloma has a pretrained ff (espaloma-0.3.0), based in quantum chemical energies and forces with a standarised `B3LYP-D3BJ/DZVP` method in the XXX open-sourfce code. The dataset is available to download from  https://github.com/choderalab/download-qca-datasets. The comprehensive list can be read pp17-18 (https://arxiv.org/abs/2307.07085).

Follow Espaloma/run_pretrained README and download the dependencies required to run the script, run_pretrained.sh

You can also train your own espaloma ff by feeding it .xyz of optimised molecules and its energy.
