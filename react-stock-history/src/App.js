import React from 'react';
import './App.css';

import Card from 'react-bootstrap/Card'
import CardDeck from 'react-bootstrap/CardDeck'
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
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
          <Card.Body>
          <Card.Title> <a href={cards.domain}> {cards.title} </a> </Card.Title>
          <Card.Text>
          <p>{cards.desc}</p>
          <span>{cards.domain.split('/', 3).slice(1)}</span>
          </Card.Text>
          <Button href={cards.domain} variant="primary">Go to Article</Button>
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
        <Button variant='secondary' onClick={props.onHide}>Close</Button>
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
      stock: {},
      sites: [],
      card_info: {},
      date: '',
      dataPs: [],
      webSites: [],
      modalShow: false,
    }
    this.onClick = this.onClick.bind(this)
    //this.handleSubmit = this.handleSubmit.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  handleChange(e) {
    this.setState({company: e.target.value})
  }

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
        this.setState({
          dataPs: dataPoints,
          webSites: websites,
          card_info: {}
        })
          
        }
        chart.render()
      })
      
    }


  /*
  handleSubmit(e) {
    this.setState({
      loading:true,
      dataPoints: [],
      websites: []
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
  */
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
    loading: true
  }))
  .then(response => response.json())
  .then(data => {
    data = JSON.stringify(data)
  this.setState({
    card_info: JSON.parse(data),
    loading: false
  })
  })

  }
   

  render() {

    var titleText = this.state.company + " Stock History"

    const options = {
			theme: "dark2",
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
            text='Loading your content...'
            >
            
            <Container fluid>
            <ErrorModal
              show={this.state.modalShow}
              onHide={() => this.setState({modalShow: false})}
            />
          
            <Row>
            <CanvasJSChart options = {options} 
          onRef={ref => this.chart = ref}
          />
            </Row>
            {/*
            <form onSubmit={this.handleSubmit}>
            <input 
            type='text' 
            onChange={this.handleChange}
            />
            
            <input 
            type='button'
            value='Get History'
            onClick={this.handleSubmit}
            />
            </form>
            */}
            <Form>
              <Form.Row className="justify-content-md-center">
                <Form.Group>
                <Form.Control size='lg' placeholder='Company to search for...' onChange={this.handleChange} />
                <Form.Text className="text-muted">
                  Please make sure company is publicly traded and spelled correctly
                </Form.Text>
                </Form.Group>
                <Form.Group>
                <Button type='submit' size='lg' onClick={this.handleSubmit}>Get History</Button>
                </Form.Group>
              </Form.Row>
            </Form>

            {!this.state.loading ? <div> <Row> <h1>{this.state.date}</h1> </Row>
            <Row> <ListWebsites cards={this.state.card_info}/></Row></div> : null} 
            
            
            
            </Container>
          </LoadingOverlay>
           
      </div>
     
    )
  }
}

export default App;
