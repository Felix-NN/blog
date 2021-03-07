import React from 'react';
import './App.css';

import CanvasJSReact from './canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

var dataPoints = []
var websites = []

function ListWebsites(props) {
  
    
    return( 
      null
      
      //<span key={props.key}>
      //  <a href={props.sites}> {props.sites} </a>
      //</span>
    )
}

class App extends React.Component {

  constructor() {
    super()
    this.state = {
      loading: false,
      stock: {},
      sites: [],
      card_info: {},
      date: ''
    }
    this.onClick = this.onClick.bind(this)
  }

  componentDidMount() {
    this.setState({loading:true})
    var chart = this.chart
    fetch('/stocks')
    .then(res => res.json())
    .then(data => {
      //console.log(data)
      //data = JSON.parse(data)
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
    })
  }
  
  onClick(e) {
    for (let key of Object.keys(websites)) {
      if (websites[key].x.getTime() === e.dataPoint.x.getTime()){
        this.setState({
          sites: websites[key].sites,
          date: websites[key].x.toDateString().split(' ').slice(1).join(' ')
        })
        break
      }
    }
    
    console.log(this.state.sites)
  fetch('/_link_prev', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(this.state.sites)
  })
  .then(response => response.json())
  .then(data => {
  this.setState({
    card_info: data
  })
  console.log(this.state.card_info)
  })

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
          <p>{this.state.date}</p>
          <button onClick={this.handleClick}>Call API</button>
          
          <ListWebsites key={this.state.sites.x} sites={this.state.sites}/>
          
      </div>
    )
  }
}

export default App;
