// Text in begging 
let st_text = `
    <p>The lockdown and related measures implemented by many countries to stop the spread of COVID-19 have led to a sudden decrease in 
    economic activities. To assess how this has affected concentrations of air pollution, this tool is developed to help user to track
    daily average concentration of nitrogen dioxide (NO2), particulate matter (PM2.5 and PM10) and weather changes during 2019-2020. 
    Data source: aqicn.org </p>
`;
 let st_text1 = `<p>Any suggestions are welcomed to improve this tool. Please send me an <a href="mailto:n.wang@abmsystems.com">email</a></p>`;

$('#text1').append(st_text);
$('#text1').append(st_text1);

let labels = [];
let data = [];
var ctx = $('#myChart');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            {
            label: 'Selected City',
            data: data,
            borderColor: [
                'red'
            ],
            borderWidth: 1,
            fill: false
            }
    ]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        legend: {
            display:false,
            // label:{
            //     boxWidth: 200
            // }
        },
        animation: {
        },
        title : {
            display:true,
            text: 'Global AQI 2019-2020',
            fontSize: 20,
            fontStyle: 'normal',
            fontColor: 'black'
        }

    }
});

$("#submit").click((e)=>{
    let val_countries = $("#countries").val();
    let val_cities = $("#cities").val();
    let val_pollutants = $("#pollutants").val();
    let data_tosend = {
        country: val_countries,
        city: val_cities,
        pollutant: val_pollutants
    };
    
    $.get('/plot',data_tosend,function(data_resp,status){
       
      updateData (myChart,arrayJump(data_resp.date,1),arrayJump(data_resp.median,1));
        //} 
       //draw_chart(passed_data.labels,passed_data.value);
    });
    let loadingText = `<div class='status_text'><h5>Program is loading...(Slow response may be experienced due to the limit budgeted cloud resources. Some cities may not have available data)</h5></div>`;
    let finishloadingText = `<div class='status_text'><h5>New chart is successful loaded</h5></div>`;
    $('#myBar').html(loadingText);
    $(document).ajaxStart(function() {
    }).ajaxSuccess(function() {
       $('#myBar').html(finishloadingText);
    });
});

var display_data = {};
$.get('/load',{},function(data_resp,status){
    let jo = JSON.parse(data_resp);
    display_data = jo;
    let country_dropdown = $('#countries');
    let city_dropdown = $('#cities');
    country_dropdown.empty();

    country_dropdown.append('<option selected="true" disabled>Choose Country</option>');
    city_dropdown.append('<option selected="true" disabled>Choose City</option>');
    country_dropdown.prop('selectedIndex', 0);
    country_dropdown.prop('selectedIndex', 0);
    let ctris = Object.keys(display_data).sort();
    ctris.forEach(key=>{
        country_dropdown.append($('<option></option>').attr('value', key).text(key));
    })
});

function fillSelect(selected_value, area_update){
    if(area_update == "cities"){
        $('#cities').empty();
        for (var key in display_data[selected_value]) {
            $('#cities').append($('<option></option>').attr('value', key).text(key));
        }
    }

  }


function updateData(chart, label, data) {
    chart.data.labels = label;
    chart.data.datasets.forEach((dataset) => {
        dataset.data = data;
    });
    chart.update();
}


function arrayJump (ar,jumpover_number) {
  let newar = [];
  for(i=0; i<ar.length; i = i+jumpover_number ){
      newar.push(ar[i]);
 }
   return newar;
}

function arraySort (ar, order){


}
// function removeData(chart) {
//     // chart.data.labels.pop();
//     // chart.data.datasets.forEach((dataset) => {
//     //     dataset.data.pop();
//     // });
//     // chart.update();
//     chart.data.labels = [];
//     chart.data.datasets.forEach((dataset) => {
//         dataset.data = [];
//     });
//     chart.update();
// }