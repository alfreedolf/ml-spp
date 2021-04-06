######################################################################
# This file contains utility functions to load test data from file,  #
# and invoke DeepAR predictor and plot the observed and target data. #
######################################################################

import io
import os
import json
import pandas as pd
import sagemaker


# * new function
# TODO check for start value usage
def series_to_json_obj(ts, target_column, dyn_feat, start=None):
    """Returns a dictionary of values in DeepAR, JSON format.
       :param dyn_feat: array of dynamic features
       :param ts: A time series dataframe containing stock prices data features.
       :param target_column: A single feature time series to be predicted.
       :param start: A datetime start value to be used as beginning of time series used as prediction context
       :return: A dictionary of values with "start", "target" and "dynamic_feat" keys if any
       """
    # get start time and target from the time series, ts
    if start is not None:
        start_index = start
        ts = ts.loc[start_index:]

        if not dyn_feat:

            json_obj = {"start": str(pd.to_datetime(start_index)),
                        "target": list(ts.loc[:, target_column])}
        else:
            # populating dynamic features array
            df_dyn_feat = ts.loc[:, dyn_feat]
            dyn_feat_list = []
            for feat in df_dyn_feat:
                dyn_feat_list.append(list(df_dyn_feat[feat]))

            # creating json object    
            json_obj = {"start": str(pd.to_datetime(start_index)),
                        "target": list(ts.loc[:, target_column]),
                        "dynamic_feat": list(dyn_feat_list)}

    else:
        if not dyn_feat:
            json_obj = {"start": str(ts.index[0]),
                        "target": list(ts.loc[:, target_column])}

        else:
            # populating dynamic features array
            df_dyn_feat = ts.loc[:, dyn_feat]
            dyn_feat_list = []
            for feat in df_dyn_feat:
                dyn_feat_list.append(list(df_dyn_feat[feat]))

            # creating json object
            json_obj = {"start": str(ts.index[0]), "target": list(ts.loc[:, target_column]),
                        "dynamic_feat": list(dyn_feat_list)}

    return json_obj


# TODO check for start value usage
def future_date_to_json_obj(start_date):
    """Returns a dictionary of values in DeepAR, JSON format.
       :param start_date: start date of the json to be produced
       :return: A json dictionary of values with "start" date and an empty "target" value list.
       """

    json_obj = {
        "start": pd.to_datetime(start_date).strftime(format="%Y-%m-%d"),
        "target": []
    }

    return json_obj


def ts2dar_json(ts, saving_path, file_name, dyn_feat=[], start=None):
    """
    Serializes a dataframe containing time series data into a json ready
    to be processed by DeepAR
    """
    json_obj = series_to_json_obj(ts=ts, target_column='Adj Close',
                                  dyn_feat=dyn_feat, start=start)
    with open(os.path.join(saving_path, file_name), 'w') as fp:
        json.dump(json_obj, fp)


# Class that allows making requests using pandas Series objects rather than raw JSON strings
class DeepARPredictor(sagemaker.predictor.Predictor):
    def __init__(self, endpoint_name, sagemaker_session):
        super().__init__(endpoint_name=endpoint_name, sagemaker_session=sagemaker_session)
        self.__freq = 'D'
        self.__prediction_length = 20

    def set_prediction_parameters(self, freq, prediction_length):
        """
        Set the time frequency and prediction length parameters. This method **must** be called
        before being able to use `predict`, otherwise, default values of 'D' and `20` wil be used.

        Parameters:
        freq -- string indicating the time frequency
        prediction_length -- integer, number of predicted time points

        Return value: none.
        """
        self.__freq = freq
        self.__prediction_length = prediction_length

    def predict(self, ts, cat=None, encoding="utf-8", num_samples=100, quantiles=["0.1", "0.5", "0.9"],
                content_type="application/json"):
        """Requests the prediction of for the time series listed in `ts`, each with the (optional)
        corresponding category listed in `cat`.

        Parameters:
        ts -- Time series to predict from. Can be either a list of dataframes,
        a single dataframe or a json S3 file path.
        cat -- list of integers (default: None)
        encoding -- string, encoding to use for the request (default: "utf-8")
        num_samples -- integer, number of samples to compute at prediction time (default: 100)
        quantiles -- list of strings specifying the quantiles to compute (default: ["0.1", "0.5", "0.9"])

        Return value: list of `pandas.DataFrame` objects, each containing the predictions
        """
        if isinstance(ts, list):
            prediction_times = [x.index[-1] + pd.Timedelta(1, unit=self.__freq) for x in ts]
            req = self.__encode_request(ts, cat, encoding, num_samples, quantiles)
        elif isinstance(ts, pd.DataFrame):
            prediction_times = ts.index[-1] + pd.Timedelta(1, unit=self.__freq)
            req = self.__encode_request(ts, cat, encoding, num_samples, quantiles)
        elif isinstance(ts, str):
            # TODO add code to process ts as an S3 path to a json file coded time series
            if ts.upper() == 'IBM':
                # TODO add code to feed predictor with IBM data starting from last value of test set
                pass
            elif ts.upper() == 'AAPL':
                # TODO add code to feed predictor with AAPL data starting from last value of test set
                pass
            elif ts.upper() == 'AMZN':
                # TODO add code to feed predictor with AMZN data starting from last value of test set
                pass
            elif ts.upper() == 'GOOGL':
                # TODO add code to feed predictor with GOOGL data starting from last value of test set
                pass
            else:
                pass
            req = None
        else:
            # TODO add code to handle error in input format
            req = None

        res = super(DeepARPredictor, self).predict(req, initial_args={"ContentType": content_type})
        return self.__decode_response(res, prediction_times, encoding)

    @staticmethod
    def __encode_request(ts, cat, encoding, num_samples, quantiles) -> object:
        """
        This function encodes a json request for the endpoint, that accepts
        :param ts: time series to be predicted
        :param cat: categorical features
        :param encoding: encoding to be used
        :param num_samples: number of samples to be used by DeepAR
        :param quantiles: list of quantiles to be used by
        :return:
        """
        instances = [series_to_json_obj(ts[k], target_column='Adj Close',
                                        dyn_feat=[], start=None) for k in range(len(ts))]
        configuration = {
            "num_samples": num_samples,
            "output_types": ["quantiles"],
            "quantiles": quantiles,
        }
        http_request_data = {"instances": instances, "configuration": configuration}
        return json.dumps(http_request_data).encode(encoding)

    @staticmethod
    def __encode_future_request(start_times, cat, encoding, num_samples, quantiles):
        instances = [{"start": st.strftime(format="%Y-%m-%d"), "target": []} for k, st in enumerate(start_times)]

        configuration = {
            "num_samples": num_samples,
            "output_types": ["quantiles"],
            "quantiles": quantiles,
        }
        http_request_data = {"instances": instances, "configuration": configuration}
        return json.dumps(http_request_data).encode(encoding)

    def __decode_response(self, response, prediction_times, encoding):
        response_data = json.loads(response.decode(encoding))
        list_of_df = []
        for k in range(len(prediction_times)):
            prediction_index = pd.date_range(
                start=prediction_times[k], freq=self.__freq, periods=self.__prediction_length
            )
            list_of_df.append(
                pd.DataFrame(data=response_data["predictions"][k]["quantiles"], index=prediction_index)
            )
        return list_of_df

    def predict_future(self, start_times, cat=None, encoding="utf-8",
                       num_samples=100, quantiles=["0.1", "0.5", "0.9"], content_type="application/json") -> list:
        """Requests the prediction of future time series values for the time series from `start_date`, each with the (optional)
        corresponding category listed in `cat`.

        Parameters:
        start_times -- start date of the future prediction
        cat -- list of integers (default: None)
        encoding -- string, encoding to use for the request (default: "utf-8")
        num_samples -- integer, number of samples to compute at prediction time (default: 100)
        quantiles -- list of strings specifying the quantiles to compute (default: ["0.1", "0.5", "0.9"])

        Return value: list of `pandas.DataFrame` objects, each containing the predictions
        """
        prediction_times = [st + pd.Timedelta(1, unit=self.__freq) for st in start_times]
        req = self.__encode_future_request(start_times, cat, encoding, num_samples, quantiles)
        res = super(DeepARPredictor, self).predict(req, initial_args={"ContentType": content_type})
        return self.__decode_response(res, prediction_times, encoding)
