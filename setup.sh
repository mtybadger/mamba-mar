#!/bin/bash

# Install Miniconda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash

# Add conda to PATH for this session
export PATH="$HOME/miniconda3/bin:$PATH"

# Reload bash configuration to apply changes
source ~/.bashrc

cd /workspace/mar
conda env create -f environment.yaml
conda activate mar

# Install system dependencies
apt update && apt install -y libsm6 libxext6 libxrender-dev

# Navigate to Bi-Mamba2 directory and install
cd /workspace/mar/models/Bi-Mamba2
pip install -e .

# Return to mar directory
cd /workspace/mar

pip install einops mamba_ssm causal_conv1d wandb



wandb login --relogin

curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs
git lfs install







vvhf_nCNsjQeYLJDcQHLSZmbnUPfqmhDIKWzyGz
