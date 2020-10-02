function generateChart(customData,customLabels){
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: customLabels,
        datasets: [{
            label: 'Last 6 Months',
            data: customData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
       title:{
           display:true,
           text: "Expense By Category"
       }
    }
});
}

const getChartData=()=>{
    fetch('/expense_summary').then(res=>res.json()).then(results=>{
        let customLabels = []
        for(let k in results) customLabels.push(k);

        let customValues = []
        for(let k in results) customValues.push(results[k]);

        generateChart(customValues,customLabels);
    });
};

document.onload = getChartData();


