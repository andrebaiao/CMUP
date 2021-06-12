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

    async function handleSubmit(e){
        e.preventDefault();

        const message = { username, password };
        const url = "http://localhost:9000/login";
        console.log("enviei " + JSON.stringify(message));

        let data = await fetch(url, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"username": "medic1", "password": "medic1"}),
        });

        let response = await data.json();

        if (response.status == 200){
            console.log("Login with success! Token " + response.token);
            localStorage.setItem("token", response.token);
            localStorage.setItem("login", "true");
            window.location.replace("http://localhost:3000/admin/dashboard");
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
                </Col>
                
            </Form>
        </Col>
    </Card>
  )  
}

export default Login;

/*
 <form className={classes.form} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            autoFocus
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Sign In
          </Button>
        </form>
      </div>
      <Box mt={8}>
        <Copyright />
      </Box>
    </Container>
  );
*/