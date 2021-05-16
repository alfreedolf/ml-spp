# ml-spp

This project explores a set of models for stock prices predictions.
Repository implemented solutions aim to predict following stocks Adjusted Close value:

* IBM
* Apple
* Amazon
* Google

The project currently supports two different models for stock  Adjusted Close price:
* a Simple Moving Average and
* a DeepAR model.


Most of the project could be run locally, but the DeepAR based model needs to be run in a SageMaker notebook instance.
When run on SageMaker, in order to work, notebook has also to comply the following prerequisites:
* conda_pytorch_p36 kernel (although it could probably run on other kernels that supports pandas too)
* a lifecycle configuration which includes a [start script](on_start.sh) to install following prerequisites packages:
    * yfinance
    * scikit-learn  

The project contains a web application to interrogate SageMaker define endpoint.
The web application is based on Flask framework and interrogates the endpoint through a REST API, defined by means of
AWS API Gateway.
The AWS API Gateway interrogated the endpoint through an AWS Lambda function. For more details, look ad the ProjectReport.pdf


# Project files and folder
Here follows project structure:

## License file
Currently, under MIT license.\
[LICENSE](LICENSE)

## Project report
[ProjectReport.pdf](ProjectReport.pdf)

## Jupyter Notebooks
[0.DataGathering.ipynb](0.DataGathering.ipynb)\
[1.ExploratoryDataAnalysis.ipynb](1.ExploratoryDataAnalysis.ipynb)\
[2.BenchmarkModel.ipynb](2.BenchmarkModel.ipynb)\
[3.DeepAR-StockPricesPredictions.ipynb](3.DeepAR-StockPricesPredictions.ipynb) (relies on AWS SageMaker DeepAR implementation)

The notebooks should be run in sequence:
1. [1.ExploratoryDataAnalysis](1.ExploratoryDataAnalysis.ipynb) should be run re-using the kernel from [0.DataGathering](0.DataGathering.ipynb)
2. [2.BenchmarkModel](2.BenchmarkModel.ipynb) should be run re-using the kernel from [1.ExploratoryDataAnalysis](1.ExploratoryDataAnalysis.ipynb)
3. [3.DeepAR-StockPricesPredictions](3.DeepAR-StockPricesPredictions.ipynb) should be run re-using the kernel from [2.BenchmarkModel](2.BenchmarkModel.ipynb)

## AWS SageMaker notebook instance lifecycle script
[on_start.sh](on_start.sh)

## DeepAR model related code
This folder has been created to host files needed to interface with SageMaeker DeepAR model,
and to plot results from there.\
[source_deepar/deepar_utils.py](source_deepar/deepar_utils.py)\
[source_deepar/display_quantiles.py](source_deepar/display_quantiles.py)\
[source_deepar/lambda_stock_prediction.py](source_deepar/lambda_stock_prediction.py)

## Pytorch model related code
This folder has been created to host files of a future Pytorch based prediction implementation.
This is a very interesting future development thread. Any help would be welcome.\
[source_pytorch/model.py](source_pytorch/model.py)

## Utility code
This folder contains a few scripts to manage and prepare data for model preprocessing.
It currently contains:
* data splitting [utils/data_prepare.py](utils/data_prepare.py) and
* some technical indicators computation [utils/technical_indicators.py](utils/technical_indicators.py).

## Web application code
This folder contains the implementation of a Flask and JavaScript based web app to interrogate model endpoint.\
This part of the project has been just sketched for quick presentation purposes but could be an interesting future development thread. Any help would be welcome.\
[website/static/formControl.js](website/static/formControl.js)\
[website/static/sbtStockPredReq.js](website/static/sbtStockPredReq.js)\
[website/templates/base.html](website/templates/base.html)\
[website/app.py](website/app.py)