import React from 'react';
import './App.css';

import CanvasJSReact from './canvasjs.react';
var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
 

var dataPoints = []
var websites = []

class App extends React.Component {

  constructor() {
    super()
    this.state = {
      loading: false,
      stock: {}
    };
  };

  componentDidMount() {
    this.setState({loading:true})
    var chart = this.chart
    fetch('/stocks')
    .then(res => res.json())
    .then(data => {
      data = JSON.parse(data)
      this.setState({
        stock: data,
        loading: false
      })
    })
    .then(() =>{
      for (let key of Object.keys(this.state.stock)) {
        let stock = this.state.stock
        if (stock[key].Spikes === 1.0) {
          let point =
          {
            x: new Date(stock[key].Date),
            y: stock[key].Close,
            click: this.onClick,
            color: 'LightSeaGreen'
        }
        dataPoints.push(point)
        websites.push({
          x: new Date(stock[key].Date),
          sites: stock[key].Websites
        })
      } else {
        let point = {
          x: new Date(stock[key].Date),
          y: stock[key].Close,
        }
        dataPoints.push(point)
      }
        
      }
      chart.render()
      console.log(websites)
    })
  }
  
  onClick(e) {

    for (let key of Object.keys(websites)) {
      if (websites[key].x.getTime() === e.dataPoint.x.getTime()){
        console.log(websites[key].sites)
        break
      }
    }
    
  }
   

  render() {

    

    const options = {
			theme: "light1",
			title: {
				text: "Stock History"
			},
			axisY: {
				title: "Stock Price",
				prefix: "$"
      },
      width:1500,
      zoomEnabled: true,
      zoomType: "xy",
			data: [{
        type: "line",
        markerType: "circle",
        markerSize: 5,
				xValueFormatString: "MMM DD YYYY",
				yValueFormatString: "$###,###.00",
				dataPoints: dataPoints
			}]
		}
    
    return (
      <div className="App">
        <div>
          <CanvasJSChart options = {options} 
				 onRef={ref => this.chart = ref}
			/>
          </div>
          <button onClick={this.handleClick}>Call API</button>
      </div>
    )
  }
}

export default App;
