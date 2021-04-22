function submitForm(oFormElement) {
    var xhr = new XMLHttpRequest();
    var start_date = document.getElementById('start_date_picker');
    // alert(xhr);
    xhr.onload = function () {
        // alert("let's go!");
        /** retrieving POST request response from AWS API Gateway,
        * interrogating the ML Sagemaker Endpoint.
        **/
        var result = xhr.responseText;
        var resultElement = document.getElementById('result');

        // TODO: check if it can be done entirely inside Flask App

        // setting async AJAX in order to wait for POST request to Flask App to return
        $.ajaxSetup({ async: false });
        // POST request to Flask App
        // alert(stock.value);
        var flaskPostRequest;
        // alert(start_date.value)
        if (start_date.value !== "")
        {
            flaskPostRequest = $.post("/predict_future", { start_date: start_date_picker.value, predicted_data: result });
        }
        else
        {
            flaskPostRequest = $.post("/predict", { ticker_name: stock.value, predicted_data: result, dataset: 'valid' });
        }
        // var flaskPostRequest = $.post("/predict", { ticker_name: stock.value, predicted_data: result, dataset: 'valid' });
        
        // writing response data into HTML 
        resultElement.innerHTML = flaskPostRequest.responseText;
    };

    xhr.open(oFormElement.method, oFormElement.action, true);
    let ticker_name = document.getElementById('stock');
    
    // TODO: put an if to control eventual null start date
    var request_body;
    if (start_date !== null)
    {
        request_body = "{\"ticker_name\":\""+String(ticker_name.value)+"\", \"start_date\":\""+String(start_date.value)+"\"}"
    }
    else
    {
        request_body = "{\"ticker_name\":\""+String(ticker_name.value)+"\", \"start_date\":\"\"}"
    }
    
    // alert(request_body)
    // send POST request with requested stock ticker name and requested start date to AWS API Gateway
    xhr.send(request_body)
    return false;
}