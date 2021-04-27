# ml-spp

This project implements a stock prices prediction on the following stocks:

* IBM
* Apple
* Amazon
* Google

Using two different models:
* a Simple Moving Average and
* a DeepAR model from Amazon SageMaker

Prerequisites are:
* yfinance and
* scikit-learn

The notebooks should be run in sequence:
1. [1.ExploratoryDataAnalysis.ipynb] should be run re-using the kernel from [0.DataGathering.ipynb]
2. [2.BenchmarkModel.ipynb] should be run re-using the kernel from [1.ExploratoryDataAnalysis.ipynb]
3. [3_A.DeepAR-StockPricesPredictions.ipynb] should be run re-using the kernel from [2.BenchmarkModel.ipynb]

