function controlCalendar() {
    // Get the checkbox
    var checkBox = document.getElementById("predict_from_date");
    // Get the output text
    var calendar = document.getElementById("start_date_picker");

    // If the checkbox is checked, display the calendar
    if (checkBox.checked == true) {
        calendar.style.display = "block";
    } else {
        calendar.style.display = "none";
    }
}