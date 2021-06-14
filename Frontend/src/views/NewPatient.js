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
  Form,
  Input,
  Button,
  Row,
  Col,
} from "reactstrap";


const convertPartOfDayInt = {
    "BreakFast" : 1,
    "Lunch" : 2,
    "Dinner" : 3,
    "Night" : 4
  }
  
  const convertDayInt = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thrusday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
  }



export default class NewPatient extends React.Component {

    constructor(props) {
      super(props);
      this.state = {
          my_rows: [{"name": "", "quantity": 0, "day": "Select Day of Week", "part_of_day": "Select Part Of  Day"}],
          name: "",
          age: "",
          message_success: "Created with success!",
          success: false
      }

      this.addRow = this.addRow.bind(this);
      this.removeRow = this.removeRow.bind(this);
      this.createPatient = this.createPatient.bind(this);
      this.insertDay = this.insertDay.bind(this);
      this.insertPartOfDay = this.insertPartOfDay.bind(this);
      this.insertNamePill = this.insertNamePill.bind(this);
      this.insertQuantityPill = this.insertQuantityPill.bind(this);

    }


    addRow(){
        let rows = this.state.my_rows;
        rows.push({"name": "", "quantity": 0, "day": "Select Day of Week", "part_of_day": "Select Part Of  Day"});

        this.setState({
            my_rows: rows
        })
    }

    removeRow(){
        let rows = this.state.my_rows;
        rows.pop();
        this.setState({
            my_rows: rows
        })
    }

    async createPatient(){
        
        let url = "http://localhost:9000/new_patient";


        let pills = this.state.my_rows;

        pills.map( (row, i) => {
            row.day = convertDayInt[row.day];
            row.part_of_day = convertPartOfDayInt[row.part_of_day];
        })

        let data = await fetch(url, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('token')
            },
            body: JSON.stringify(
                    {
                        "user_id" : localStorage.getItem("user_id"),
                        "name": this.state.name,
                        "age": this.state.age,
                        "pills": pills
                    }
                    ),
        });

        let response = await data.json();

        if(response.status == 200){
            console.log("Created with success!");
            this.setState({
                my_rows: [{"name": "", "quantity": 0, "day": "Select Day of Week", "part_of_day": "Select Part Of  Day"}],
                name: "",
                age: "",
                success: true
        })
        }
    }

    insertDay(index, day){
        
        let rows = this.state.my_rows;
        rows[index].day = day;

        this.setState({
            my_rows: rows
        });

    }

    insertPartOfDay(index, part_of_day){

        let rows = this.state.my_rows;
        rows[index].part_of_day = part_of_day;

        this.setState({
            my_rows: rows
        });
    }

    insertNamePill(event){
        let rows = this.state.my_rows;
        rows[event.target.id].name = event.target.value;

        this.setState({
            my_rows: rows
        });
    }

    insertQuantityPill(event){
        let rows = this.state.my_rows;
        rows[event.target.id].quantity = event.target.value;

        this.setState({
            my_rows: rows
        });
    }


    render() {

        return (
            <>
                <div className="content">
                    <Row>
                        <Col md="3"  form >
                            {/* UserName */}
                            <h4> Information about Patient </h4>
                                <label htmlFor="feFirstName" style={{marginTop: "5%"}}>Name</label>
                                <Input
                                    id="feFirstName"
                                    placeholder=""
                                    name="name"
                                    value={this.state.name}
                                    onChange={ (e)=> this.setState({ name: e.target.value}) } 
                                />
                            
                            {/* PassWord */}
                            
                                <label htmlFor="feLastName" style={{marginTop:"30px"}}>Age</label>
                                <Input
                                    id="feLastName"
                                    placeholder=""
                                    type="number"
                                    name="age"
                                    onChange={ (e)=>  this.setState({ age: e.target.value}) }
                                />

                            
                            <Row>
                            <Button theme="accent"  style={{ marginTop:"10%", marginLeft:"5%"}} onClick={this.createPatient}>Create</Button>
                            { this.state.success && <h6 style={{color:"green", marginTop:"12%", marginLeft:"5%"}}>{this.state.message_success}</h6>}
                            </Row>
                            
                        
                        </Col>
                        <Col  md="4" style={{marginLeft:"10%"}}>
                        
                        <h4>Treatment - Pills </h4> <br></br>
                            {this.state.my_rows.map( (row, i) => {

                                return (
                                    <span>
                                        <label >Name</label>
                                        <Input
                                        id={i}
                                        placeholder=""
                                        type="text"
                                        name="name_pill"
                                        value={this.state.my_rows[i].name}
                                        onChange={ (e)=> { this.insertNamePill(e) } }
                                        />
                                        <label style={{marginTop: "5%"}}>Quantity</label>
                                        <Input
                                        id={i}
                                        placeholder=""
                                        type="number"
                                        value={this.state.my_rows[i].age}
                                        name="pill_quantity"
                                        onChange={ (e)=> { this.insertQuantityPill(e) } }
                                        />
                                        <Row style={{marginBottom: "5%", marginTop: "5%" }}>
                                            <Col style={{alignSelf:"right"}}>
                                            <label>Day</label> <br></br>
                                            <UncontrolledDropdown group>
                                            <DropdownToggle caret>
                                                {this.state.my_rows[i].day}
                                            </DropdownToggle>
                                            <DropdownMenu>
                                                <DropdownItem id={i} onClick={(e) => {this.insertDay(e.target.id, "Monday")}}>Monday</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertDay(e.target.id, "Tuesday")}}>Tuesday</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertDay(e.target.id, "Wednesday")}}>Wednesday</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertDay(e.target.id, "Thrusday")}}>Thrusday</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertDay(e.target.id, "Friday")}}>Friday</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertDay(e.target.id, "Saturday")}}>Saturday</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertDay(e.target.id, "Sunday")}}>Sunday</DropdownItem>
                                            </DropdownMenu>
                                            </UncontrolledDropdown>
                                            </Col>
                                            <Col >
                                            <label>Part of Day</label> <br></br>
                                            <UncontrolledDropdown group>
                                            <DropdownToggle caret>
                                                {this.state.my_rows[i]["part_of_day"]}
                                            </DropdownToggle>
                                            <DropdownMenu>
                                                <DropdownItem id={i} onClick={(e) => {this.insertPartOfDay(e.target.id, "BreakFast")}}>BreakFast</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertPartOfDay(e.target.id, "Lunch")}}>Lunch</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertPartOfDay(e.target.id, "Dinner")}}>Dinner</DropdownItem>
                                                <DropdownItem id={i} onClick={(e) => {this.insertPartOfDay(e.target.id, "Night")}}>Night</DropdownItem>
                                            </DropdownMenu>
                                            </UncontrolledDropdown>
                                            </Col>
                                        </Row>
                                        

                                    </span>
                                    
                                )

                            } )}

                            <Button theme="accent" color="success" style={{ marginLeft: "0" ,marginTop:"30px"}} onClick={this.addRow}>
                                <i className="nc-icon nc-simple-add" />
                            </Button>
                            <Button theme="accent" color="danger"  style={{marginLeft: "70px", marginTop:"30px"}} onClick={this.removeRow}>
                                <i className="nc-icon nc-box" />
                            </Button>

                        </Col>
                            
                     
                    </Row>
                </div>
            </> 
            )
    }
}  