import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { Line } from "react-chartjs-2";
import { UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col,
} from "reactstrap";


const convertDayInt = {
  "Monday": 0,
  "Tuesday": 1,
  "Wednesday": 2,
  "Thrusday": 3,
  "Friday": 4,
  "Saturday": 5,
  "Sunday": 6

}

const dashboardChart = {
  data: {
      labels: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thrusday",
        "Friday",
        "Saturday",
        "Sunday",
      ],
      datasets: [
        {
          data: [, , , , , , ,],
          fill: false,
          borderColor: "transparent",
          backgroundColor: "transparent",
          pointBorderColor: "#b03217",
          pointRadius: 4,
          pointHoverRadius: 4,
          pointBorderWidth: 8,
          tension: 0.4,
        }
      ],
    },
  options: {
    plugins: {
      legend: { display: false },
    },
  },
};


export default class BasicTable extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        my_rows: [],
        total_pills: 0,
        total_pills_took: 0,
        total_pills_not_took: 0,
        data_chart: {

          data: {
            labels: [
              "Monday",
              "Tuesday",
              "Wednesday",
              "Thrusday",
              "Friday",
              "Saturday",
              "Sunday",
            ],
            datasets: [
              {
                data: [, , , , , , ,],
                fill: false,
                borderColor: "transparent",
                backgroundColor: "transparent",
                pointBorderColor: "#b03217",
                pointRadius: 3,
                pointHoverRadius: 4,
                pointBorderWidth: 8,
                tension: 0.4,
              }
            ],
          },
        options: {
          plugins: {
            legend: { display: false },
          },
        },

        }
    }

    this.getPatientData = this.getPatientData.bind(this);
    this.createData = this.createData.bind(this)
    this.data = {}
    
  }

  componentDidMount() {

    this.cleanData();
  }



  createData(part_of_day, monday, tuesday, wednesday, thrusday, friday, saturday, sunday) {
    return { part_of_day, monday, tuesday, wednesday, thrusday, friday, saturday, sunday };
  }

  async getPatientData(){

    console.log("Chamei funçao getPatientData");

    localStorage.setItem("patient_id", 1);
    let patient_id = localStorage.getItem("patient_id");

    let url = "http://localhost:9000/patients/" + patient_id;

    let data = await fetch(url, {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('token')
      })
    });


    let result = {};

    let response = await data.json();
    
    result["pills_not_took"] = JSON.parse(response.message.pills_not_took);
    result["treatment"] = JSON.parse(response.message.treatment);
    result["total_pills_not_took"]  = result["pills_not_took"].length;
    result["total_pills_took"] = JSON.parse(response.message.total_pills_took);

    this.setState({
      total_pills: result["total_pills_not_took"] + result["total_pills_took"],
      total_pills_not_took: result["total_pills_not_took"],
      total_pills_took: result["total_pills_took"]
    })

    
    result["pills_not_took"].map((p) => {

      let pill_split = p.date.split(" ");
      let partofday = pill_split[3];
      partofday = convertDayInt[partofday];
      let hour = pill_split[4].split(":")[0];
      dashboardChart.data.datasets[0].data[partofday] = hour;
      
    })

    this.setState({
      data_chart: dashboardChart
    })


    return result;
  };


  async cleanData(){

    let my_data = [];

    this.getPatientData().then((res)=>{

      this.data = res;


      let parts_of_day = ["BreakFast", "Lunch", "Dinner", "Night"];

      for(var i = 0; i < 4; i++){
        
        let parameters = [parts_of_day[i], "", "", "", "", "", "", ""];
      
        this.data["treatment"].map((p)=>{
          if(p.part_of_day == i + 1){
            parameters[p.day] = parameters[p.day] + " "+  p.quantity + " " +p.name;
          }
        });

        my_data.push(this.createData(parameters[0], parameters[1],parameters[2],parameters[3],parameters[4],parameters[5],parameters[6], parameters[7], parameters[8]))
      }

      this.setState({
        my_rows: my_data
      })

      console.log(this.data)

    });


  }

  render() {

    return (
      <>
          <div className="content">
          <UncontrolledDropdown>
                  <DropdownToggle caret>
                      Patient1 Luis
                  </DropdownToggle>
                  <DropdownMenu>
                      <DropdownItem>Patient2 Andre</DropdownItem>
                      <DropdownItem>Patient3 Joao</DropdownItem>
                      <DropdownItem>Something Jose</DropdownItem>
                  </DropdownMenu>
              </UncontrolledDropdown>
              <Row style={{marginTop:"70px"}}></Row>
              <TableContainer component={Paper}>
              <Table aria-label="simple table" style={{minWidth: 650}}>
                  <TableHead>
                  <TableRow>
                      <TableCell></TableCell>
                      <TableCell align="center">Monday</TableCell>
                      <TableCell align="center">Tuesday</TableCell>
                      <TableCell align="center">Wednesday</TableCell>
                      <TableCell align="center">Thursday</TableCell>
                      <TableCell align="center">Friday</TableCell>
                      <TableCell align="center">Saturday</TableCell>
                      <TableCell align="center">Sunday</TableCell>
                  </TableRow>
                  </TableHead>
                  <TableBody>
                  {this.state.my_rows.map((row) => {


                    return (
                      <TableRow key={row.part_of_day}>
                      <TableCell >
                          {row.part_of_day}
                      </TableCell>
                      <TableCell align="center">{row.monday}</TableCell>
                      <TableCell align="center">{row.tuesday}</TableCell>
                      <TableCell align="center">{row.wednesday}</TableCell>
                      <TableCell align="center">{row.thrusday}</TableCell>
                      <TableCell align="center">{row.friday}</TableCell>
                      <TableCell align="center">{row.saturday}</TableCell>
                      <TableCell align="center">{row.sunday}</TableCell>
                      </TableRow>
                    )         
                  })}
                  </TableBody>
              </Table>
              </TableContainer>
              <Row style={{marginTop:"70px"}}></Row>
              <Row>
                <Col lg="3" md="6" sm="6" style={{marginLeft: "5%"}}>
                  <Card className="card-stats">
                    <CardBody>
                      <Row>
                        <Col md="4" xs="5">
                          <div className="icon-big text-center icon-info">
                            <i className="nc-icon nc-globe text-info" />
                          </div>
                        </Col>
                        <Col md="8" xs="7">
                          <div className="numbers">
                            <p className="card-category">Total Pills </p>
                            <CardTitle tag="p">{this.state.total_pills}</CardTitle>
                            <p />
                          </div>
                        </Col>
                      </Row>
                    </CardBody>
                  </Card>
                </Col>
                <Col lg="3" md="6" sm="6" style={{marginLeft: "5%"}}>
                  <Card className="card-stats">
                    <CardBody>
                      <Row>
                        <Col md="4" xs="5">
                          <div className="icon-big text-center icon-success">
                            <i className="nc-icon nc-check-2 text-success" />
                          </div>
                        </Col>
                        <Col md="8" xs="7">
                          <div className="numbers">
                            <p className="card-category">Total Pills Took </p>
                            <CardTitle tag="p">{this.state.total_pills_took}</CardTitle>
                            <p />
                          </div>
                        </Col>
                      </Row>
                    </CardBody>
                  </Card>
                </Col>
                <Col lg="3" md="6" sm="6" style={{marginLeft: "5%"}}>
                  <Card className="card-stats">
                    <CardBody>
                      <Row>
                        <Col md="4" xs="5">
                          <div className="icon-big text-center icon-danger">
                            <i className="nc-icon nc-simple-remove text-danger" />
                          </div>
                        </Col>
                        <Col md="8" xs="7">
                          <div className="numbers">
                            <p className="card-category">Total Pills Not Took </p>
                            <CardTitle tag="p">{this.state.total_pills_not_took}</CardTitle>
                            <p />
                          </div>
                        </Col>
                      </Row>
                    </CardBody>
                  </Card>
                </Col>
            </Row>
            <Row style={{marginTop:"70px"}}></Row>
            <Row>
            <Col md="8" style={{marginLeft:"15%"}}>
            <Card className="card-chart">
              <CardHeader>
                <CardTitle tag="h5">Last Week</CardTitle>
                <p className="card-category">Alerts by pill not taken</p>
              </CardHeader>
              <CardBody>
                <Line
                  data={this.state.data_chart.data}
                  options={this.state.data_chart.options}
                  width={400}
                  height={100}
                />
              </CardBody>
        
            </Card>
          </Col>
            </Row>
          </div>
        
          
        
      </>
    );
  }
  
}
