# ml-spp

This project implements a stock prices prediction proposed solution on the following stocks:

* IBM
* Apple
* Amazon
* Google

The project currently supports two different models for stock  Adjusted Close price:
* a Simple Moving Average and
* a DeepAR model.



To run the project, upload it to a SageMaker notebook instance.
To work the SageMaker notebook instance has also to run on:
* on conda_pythorch_p36 kernel (although it could probably run on other kernels that supports pandas too)
* a lifecycle configuration wich includes a [start script](on_start.sh) to install following prerequisites packages:
    * yfinance
    * scikit-learn  


# Project files and folder
The project has the following structure:

0.DataGathering.ipynb\
PositiveReviewExample.png\
SageMaker Project.ipynb\
Web App Diagram.svg\
sentiment_lambda_function.py\
serve/model.py\
serve/predict.py\
serve/requirements.txt\
train/model.py\
train/model_new.py\
train/train.py\
train/train_new.py\
train/requirements.txt\
website/index.html

The notebooks should be run in sequence:
1. [ExploratoryDataAnalysis](1.ExploratoryDataAnalysis.ipynb) should be run re-using the kernel from [0.DataGathering.ipynb]
2. [2.BenchmarkModel.ipynb] should be run re-using the kernel from [1.ExploratoryDataAnalysis.ipynb]
3. [3_A.DeepAR-StockPricesPredictions.ipynb] should be run re-using the kernel from [2.BenchmarkModel.ipynb]

