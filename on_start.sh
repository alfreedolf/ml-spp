#!/bin/bash

set -e

# OVERVIEW
# This script installs the following packages in pythorch3_6 SageMaker conda environment:
# - yfinance for stock prices gathering
# - scikit-learn for performance metrics and othe utilities
sudo -u ec2-user -i <<'EOF'
# PARAMETERS

# packages to be installed
YFINANCE=yfinance
SKLEARN=scikit-learn


# selected environment
ENVIRONMENT=pytorch_p36
 

# operation to be run on notebook starts
source /home/ec2-user/anaconda3/bin/activate "$ENVIRONMENT"

# install required packages
pip install --upgrade "$YFINANCE"
pip install -U "$SKLEARN"
# deactivating the environment before quit
conda deactivate
EOF

initctl restart jupyter-server --no-wait