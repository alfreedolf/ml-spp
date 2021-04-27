import torch.nn as nn

class LSTM_Predictor(nn.Module):
    """
    This is the RNN model we will be using to perform Stock Prices prediction.
    """

    def __init__(self, units, hidden_dim, layers, dropout, prediction_length):
        """
        Initialize the model by setting up layers.
        """
        self.prediciton_length = prediction_length
        super(LSTM_Predictor, self).__init__()
        self.lstm = nn.LSTM(input_size=units, hidden_size=hidden_dim, num_layers=layers, dropout=dropout)
        self.dense = nn.Linear(in_features=hidden_dim, out_features=1)
        self.relu = nn.ReLU()

        

    def forward(self, x):
        """
        Perform a forward pass of our model on some input.
        """
        lstm_out, _ = self.lstm(x)
        out = self.dense(lstm_out)
        out = out[self.prediction_length - 1, range(self.prediction_length)]
        return self.relu(out.squeeze())
    