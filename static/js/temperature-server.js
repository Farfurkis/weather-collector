function retrieveMeasurers() {
    jQuery.ajax({
        url: '/measurers',
        success: function(data) {
            const baseElement = jQuery("#measurers");
            for (var i in data.measurers) {
                var id = data.measurers[i].id
                var code = data.measurers[i].code
                var name = data.measurers[i].name
                var description = data.measurers[i].description
                var element_id = id + "_" + code
                baseElement.append("<div id='" + element_id + "' class='measurer measurer-enabled'>"
                    + "<div class='measurer-name'>" + name + "</div>"
                    + "<div class='measurer-description'>" + description + "</div>"
                    + "<div class='current-temperature'><span id='" + element_id + "_current_temperature'></span>&nbsp;&deg;C</div>"
                    + "<div class='current-humidity'><span id='" + element_id + "_current_humidity'></span>&nbsp;%</div>"
                    + "</div>");
                update_weather(element_id + '_current_temperature',
                               element_id + '_current_humidity',
                               '/temperature/current/' + id);
                setInterval(
                    function() {
                        update_weather(element_id + '_current_temperature',
                                       element_id + '_current_humidity',
                                       '/temperature/current/' + id);
                    },
                    60000);
                var measurer_element = jQuery("#" + element_id);
                measurer_element.click(
                    function () {
                        jQuery(this).toggleClass("measurer-enabled");
                    }
                );
            }
        }
    });
}

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
