var options = {
    responsive:true
};

var data = {
    labels: ["Hoje"],
    datasets: [
        {
            label: "Dados primários",
            fillColor: "rgba(0,100,0,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: [getTotaisDiaReceita()]
        },
        {
            label: "Dados secundários",
            fillColor: "rgba(139,0,0,0.5)",
            strokeColor: "rgba(151,187,205,0.8)",
            highlightFill: "rgba(151,187,205,0.75)",
            highlightStroke: "rgba(151,187,205,1)",
            data: [getTotaisDiaDespesa()]
        }
    ]
};                

window.onload = function(){
    var ctx = document.getElementById("GraficoBarra").getContext("2d");
    var BarChart = new Chart(ctx).Bar(data, options);
}           