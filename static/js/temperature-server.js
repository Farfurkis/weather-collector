function update_weather(temperature_element_id, humidity_element_id, source) {
    jQuery.ajax({
        url: source,
        success: function(data) {
            jQuery("#" + humidity_element_id).html(data["humidity"])
            jQuery("#" + temperature_element_id).html(data["temperature"])
        }
    });
    //setTimeout(update_weather_periodically(temperature_element_id, humidity_element_id, update_period, source), update_period);
}

function prepareFlot(data, placeholderId) {
    var plot_conf = {
        series: {
            lines: {
                show: true,
                lineWidth: 2
            }
        },
        xaxis: {
            mode: "time",
//            minTickSize: [1, "day"],
            timeformat: "%d %b %y"
        }
    };
    jQuery.plot(jQuery("#" + placeholderId), data, plot_conf);
}

function retrieveFlotData(source, placeholderId) {
    jQuery.ajax({
        url: source,
        dataType: 'json'
    }).success(
        function (data) {
            prepareFlot(prepareFlotData(data), placeholderId);
        }
    );
}

function prepareFlotData(data) {
    var plot_row_temperature = {
        label: "Temperature",
        color: 1,
        data: new Array()
    }
    var plot_row_humidity = {
        label: "Humidity",
        color: 2,
        data: new Array()
    }
    for(var i in data.measurements) {
        var measurementDate = Date.parse(data.measurements[i].datetime);
        plot_row_temperature.data[i] = [measurementDate, data.measurements[i].temperature];
        plot_row_humidity.data[i] = [measurementDate, data.measurements[i].humidity];
    }
    return [plot_row_temperature, plot_row_humidity];
}
