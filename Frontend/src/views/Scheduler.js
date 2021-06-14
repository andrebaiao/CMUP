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


const convertIntPartOfDay = {
  1: "BreakFast",
  2: "Lunch",
  3: "Dinner",
  4: "Night"
}

const convertIntDay = {
  1: "Monday",
  2: "Tuesday",
  3: "Wednesday",
  4: "Thrusday",
  5: "Friday",
  6: "Saturday",
  7: "Sunday"
}

export default class BasicTable extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        my_rows: [],
        total_pills: 0,
        total_pills_took: 0,
        total_pills_not_took: 0,
        patients : [],
        pills_not_took: [],
        next_pill: {},
        name_patient: ""
    }

    this.getPatientData = this.getPatientData.bind(this);
    this.createData = this.createData.bind(this);
    this.getPatients = this.getPatients.bind(this);
    this.data = {};
    this.getNextPill = this.getNextPill.bind(this);
    this.newPatient = this.newPatient.bind(this);
    
  }

  componentDidMount() {
    localStorage.setItem("patient_id", 1);
    this.getPatients();
    this.getNextPill();
    this.cleanData();
  }



  createData(part_of_day, monday, tuesday, wednesday, thrusday, friday, saturday, sunday) {
    return { part_of_day, monday, tuesday, wednesday, thrusday, friday, saturday, sunday };
  }


  async getPatients(){

    let url = "http://localhost:9000/patients/medic/" + localStorage.getItem("user_id");

    let data = await fetch(url, {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('token')
      })
    });

    let response = await data.json();
    
    let resp_patients = JSON.parse(response["message"]);


    this.setState({
      patients: resp_patients,
      name_patient: resp_patients[0].name
    });

  }


  async getPatientData(){

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

    

    this.setState({
      pills_not_took: result["pills_not_took"],
      name_patient: response.message.name
    })

    console.log(this.state.name_patient);


    return result;
  };

  async getNextPill(){


    let url = "http://localhost:9000/patients/nextpill/" + localStorage.getItem("patient_id");



    let data = await fetch(url, {
      method: 'GET',
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem('token')
      })
    });


    let response = await data.json();

    response = JSON.parse(response["message"]);
    response.day = convertIntDay[response.day];
    response["part_of_day"] = convertIntPartOfDay[response["part_of_day"]];

    this.setState({
      next_pill: response
    })

  }


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
      this.forceUpdate();

    });


  }

  async newPatient(id){
    localStorage.setItem("patient_id", id);
    this.getNextPill();
    this.cleanData();
  }

  render() {

    return (
      <>
          <div className="content">
          <UncontrolledDropdown group>
                  <DropdownToggle caret>
                      {this.state.name_patient} - Select the patient 
                  </DropdownToggle>
                  <DropdownMenu>
                      {this.state.patients.map( (row) => {
                        return (
                          <DropdownItem onClick={() => {this.newPatient(row.id)}}>{row.id} {row.name}</DropdownItem>
                        )
                      } )}
                  </DropdownMenu>
              </UncontrolledDropdown>
              <Row style={{marginTop:"70px"}}></Row>
              <h3>{this.state.name_patient} - Treatment</h3>
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
            <Col md="7" style={{marginLeft:"20%"}}>
              <h4 style={{color:"red", textAlign:"center"}}><b>Alarms</b></h4>
              <TableContainer component={Paper}>
                <Table aria-label="simple table" >
                <TableHead>
                      <TableRow>
                          <TableCell align="center" >Day</TableCell>
                          <TableCell align="center" >Hour</TableCell>
                      </TableRow>
                      </TableHead>
                      <TableBody>
                    {this.state.pills_not_took.map((row, i)=>{
                      let my_split = row.date.split(" ");
                      let day = my_split[0] + " " + my_split[1] + " " + my_split[2] + " - " + my_split[3];
                      let hour = my_split[(my_split.length - 1)];
                      
                      return(
                        <TableRow key={i}>
                          <TableCell align="center">{day}</TableCell>
                          <TableCell align="center">{hour}</TableCell>
                        </TableRow>
                      )
                    })}          
                  </TableBody>
                </Table>
              </TableContainer>
            </Col>
          </Row>
          <Row style={{marginTop:"70px"}}></Row>
          <Row>
            <Col lg="3" md="6" sm="6" style={{marginLeft: "35%"}}>
                <Card className="card-stats">
                  <CardBody>
                    <Row>
                      <Col md="4" xs="5">
                        <div className="icon-big text-center icon-success" style={{marginTop: "10%"}}>
                          <i className="nc-icon nc-minimal-right text-success" />
                        </div>
                      </Col>
                      <Col md="8" xs="7">
                        <div className="numbers">
                          <p className="card-category"> Next Pill </p>
                          <CardTitle tag="p">{this.state.next_pill.quantity} {this.state.next_pill.name} <br></br> {this.state.next_pill.day} {this.state.next_pill.part_of_day}</CardTitle>
                          <p />
                        </div>
                      </Col>
                    </Row>
                  </CardBody>
                </Card>
              </Col>
          </Row>


          </div>
        
          
        
      </>
    );
  }
  
}
