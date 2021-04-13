import React from 'react';
import './App.css';

import Card from 'react-bootstrap/Card'
import CardDeck from 'react-bootstrap/CardDeck'
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Modal from 'react-bootstrap/Modal'
import Form from 'react-bootstrap/Form'

import LoadingOverlay from 'react-loading-overlay';
import CanvasJSReact from './canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;


function ListWebsites(props) {

  if (Object.keys(props.cards).length === 0) {
    return null
  }
  
  let card = props.cards.map((cards) =>
  
      <Card style={{ width: '25rem' }}>
        <Card.Img variant="top" src={cards.img} />
          <Card.Body className='cards'>
          <Card.Title > <a href={cards.domain} className='card-title'> {cards.title} </a> </Card.Title>
          <Card.Text className='card-text'>
          <p>{cards.desc}</p>
          <span className="text-muted">{cards.domain.split('/', 3).slice(1)}</span>
          </Card.Text>
          <Button variant="default" className='card-button' href={cards.domain}>Go to Article</Button>
          </Card.Body>
      </Card>
      )
  
  
    return( 
      <CardDeck>{card}</CardDeck>
    )
    
}

function ErrorModal (props) {
  return (
    <Modal
      {...props}
      size="lg"
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          <h1>Error!</h1>
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h4>Oops, something went wrong! Please try again.</h4>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="default" className='modalButton' onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  )
}

class App extends React.Component {

  constructor() {
    super()
    this.state = {
      company: '',
      loading: false,
      cardLoading: false,
      stock: {},
      sites: [],
      card_info1: {},
      card_info2: {},
      date: '',
      dataPs: [],
      webSites: [],
      modalShow: false,
    }
    this.onClick = this.onClick.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  handleChange(e) {
    this.setState({company: e.target.value})
  }

  /*
  componentDidMount() {
      this.setState({
        loading:true,
        dataPoints: [],
        websites: []
      })
      var dataPoints = []
      var websites = []
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
      .catch(this.setState({modalShow: true}))
      .then(() =>{
        for (let key of Object.keys(this.state.stock)) {
          let stock = this.state.stock
          if (stock[key].Spikes === 1.0) {
            let point =
            {
              x: new Date(stock[key].Date),
              y: stock[key].Close,
              click: this.onClick,
              color: '#0F1531',
              markerSize: 8
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
        this.setState({
          dataPs: dataPoints,
          webSites: websites,
          card_info: {}
        })
          
        }
        chart.render()
      })
      
    }
*/


  handleSubmit(e) {
    this.setState({
      loading:true,
      dataPoints: [],
      websites: [],
      card_info1: {},
      card_info2: {},
      dataPs: [],
      date: ''
    })
    var dataPoints = []
    var websites = []
    var chart = this.chart
    fetch('/_update_stocks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.state.company)
    })
    .then(res => res.json())
    .then(data => {
      //console.log(data)
      data = JSON.parse(data)
      this.setState({
        stock: data,
        loading: false
      })
    })
    .catch(error => {console.log(error)
      this.setState({
        modalShow: true,
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
            color: '#0F1531',
            markerSize: 8
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
      this.setState({
        dataPs: dataPoints,
        webSites: websites,
        card_info: {}
      })
        
      }
      chart.render()
    })
    e.preventDefault()
    
  }

  onClick(e) {
    for (let key of Object.keys(this.state.webSites)) {
      if (this.state.webSites[key].x.getTime() === e.dataPoint.x.getTime()){
        this.setState({
          sites: this.state.webSites[key].sites,
          date: this.state.webSites[key].x.toDateString().split(' ').slice(1).join(' ')
        })
        break
      }
    }

  fetch('/_link_prev', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(this.state.sites)
  })
  .then(this.setState({
    cardLoading: true
  }))
  .then(response => response.json())
  .catch(error => {
    console.log(error)
    this.setState({
        modalShow: true,
        cardLoading:false
      })
    })
  .then(data => {
    data = JSON.stringify(data)
  this.setState({
    card_info1: JSON.parse(data).slice(0,4),
    card_info2: JSON.parse(data).slice(4),
    cardLoading: false
  })
  })

  }
   

  render() {

    var titleText = this.state.company + " Stock History"

    const options = {
      backgroundColor: '#f1efee',
			title: {
				text: titleText
			},
			axisY: {
				title: "Stock Price",
				prefix: "$"
      },
      animationEnabled: true,
      zoomEnabled: true,
      zoomType: "xy",
			data: [{
        type: "line",
        markerType: "circle",
        markerSize: 5,
        color: '#3D96D0',
				xValueFormatString: "MMM DD YYYY",
				yValueFormatString: "$###,###.00",
				dataPoints: this.state.dataPs
			}]
		}
    
    return (
      
        <div className="App">
          
          <LoadingOverlay
            active={this.state.loading}
            spinner
            text='Loading may take about a minute or so, please wait...'
            >
          <LoadingOverlay
            active={this.state.cardLoading}
            spinner
            text='Loading articles...'
            >
            
            <Container fluid>
            <ErrorModal
              show={this.state.modalShow}
              onHide={() => this.setState({modalShow: false})}
            />
          
            <Row className='chart'>
            <CanvasJSChart options = {options} 
          onRef={ref => this.chart = ref}
          />
            </Row>
            <Form>
              <Form.Row className="justify-content-md-center">
                <Form.Group>
                <Form.Control size='lg' placeholder='Company to search for...' onChange={this.handleChange} />
                <Form.Text className="company-warning">
                  Please make sure company is publicly traded and spelled correctly
                </Form.Text>
                </Form.Group>
                <Form.Group>
                <Button variant="default" className='company-button' type='submit' size='lg' onClick={this.handleSubmit}>Get History</Button>
                </Form.Group>
              </Form.Row>
            </Form>
            
            {!this.state.loading ?  <div> <Row className='justify-content-md-center'> <h1 className='date-chosen'>{this.state.date}</h1> </Row>
            <Row className='card-row justify-content-md-center'> <ListWebsites cards={this.state.card_info1}/></Row>
            <Row className='card-row justify-content-md-center'> <ListWebsites cards={this.state.card_info2}/></Row>
            </div>: null} 
            
            
            
            </Container>
          </LoadingOverlay>
          </LoadingOverlay>
           
      </div>
     
    )
  }
}

export default App;
