import React from "react";
import { useState } from "react";
// reactstrap components
import {
  Button,
  Card,
  CardHeader,

  CardTitle,
  Form,
  Input,

  Col,

} from "reactstrap";


function Login() {

    const[ username, setUsername ] = useState('');
    const[ password, setPassword ] = useState('');


    const [msg, setMsg] = useState('')

    async function handleSubmit(e){
        e.preventDefault();

        const message = { username, password };
        const url = "http://localhost:9000/login";
        

        let data = await fetch(url, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"username": username, "password": password}),
        });

        let response = await data.json();

        if (response.status == 200){
            console.log("Login with success! Token " + response.token);
            localStorage.setItem("token", response.token);
            localStorage.setItem("user_id", response["user_id"]);
            localStorage.setItem("login", "true");
            window.location.replace("http://localhost:3000/admin/patient/scheduler");
        } else {
          setMsg('Credentials invalid! Try Again...');
        }

        
    }

  return (
    <Card style={{width: "400px", margin: "0 auto", marginTop:"10%"}}>
        <CardHeader>
        <CardTitle tag="h4" style={{textAlign:"center"}}>SignIn</CardTitle>
        </CardHeader>
        <Col >
            <Form onSubmit={handleSubmit}>
                <Col md="12"  form>
                    {/* UserName */}
                    
                        <label htmlFor="feFirstName">Username</label>
                        <Input
                            id="feFirstName"
                            placeholder=""
                            name="username"
                            onChange={(e)=>setUsername(e.target.value)}
                        />
                    
                    {/* PassWord */}
                    
                        <label htmlFor="feLastName" style={{marginTop:"30px"}}>Password</label>
                        <Input
                            id="feLastName"
                            type="password"
                            placeholder=""
                            name="password"
                            onChange={(e)=>setPassword(e.target.value)}
                        />
                    
                    <Button theme="accent"  style={{marginLeft: "70px", marginTop:"30px"}}>Log in</Button>
                
                    <Button theme="accent" style={{marginLeft: "20px", marginTop:"30px"}}>Sign Out</Button>

                    <p style={{color:"red", marginTop: "5%px", marginLeft: "5%"}}>{msg}</p>
                </Col>
                
            </Form>
        </Col>
    </Card>
  )  
}

export default Login;