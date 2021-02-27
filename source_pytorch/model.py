import torch.nn as nn

class LSTM_Predictor(nn.Module):
    """
    This is the RNN model we will be using to perform Stock Prices prediction.
    """

    def __init__(self, units, hidden_dim, layers, dropout):
        """
        Initialize the model by setting up layers.
        """
        super(LSTM_Predictor, self).__init__()ì
        self.lstm = nn.LSTM(input_size=units, hidden_size=hidden_dim, num_layers=layers, dropout=dropout)
        self.dense = nn.Linear(in_features=hidden_dim, out_features=1)
        self.relu = nn.ReLU()
        

    def forward(self, x):
        """
        Perform a forward pass of our model on some input.
        """
        lstm_out, _ = self.lstm(x)
        out = self.dense(lstm_out)
        out = out[lengths - 1, range(len(lengths))]
        return self.relu(out.squeeze())
    