function submitForm(oFormElement) {
    var xhr = new XMLHttpRequest();
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
        var flaskPostRequest = $.post("/predict", { ticker_name: stock.value, predicted_data: result, dataset: 'valid' });
        // writing response data into HTML 
        resultElement.innerHTML = flaskPostRequest.responseText;
    };

    xhr.open(oFormElement.method, oFormElement.action, true);
    var stock = document.getElementById('stock');
    // send POST request with requested stock ticket to AWS API Gateway
    xhr.send(stock.value);
    return false;
}