/*!

=========================================================
* Paper Dashboard React - v1.3.0
=========================================================

* Product Page: https://www.creative-tim.com/product/paper-dashboard-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com)

* Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard-react/blob/main/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";
import "assets/scss/paper-dashboard.scss?v=1.3.0";
import "assets/demo/demo.css";
import "perfect-scrollbar/css/perfect-scrollbar.css";

import AdminLayout from "layouts/Admin.js";
import LoginLayout from "layouts/LoginPage.js";



if(localStorage.getItem("login") == "true"){

  ReactDOM.render(
    <BrowserRouter>
      <Switch>
        <Route path="/admin" render={(props) => <AdminLayout {...props} />} />
        <Redirect to="/admin/patient/scheduler" />
        
      </Switch>
    </BrowserRouter>,
    document.getElementById("root")
  );

} else {
  ReactDOM.render(
    <BrowserRouter>
      <Switch>
        <Route path="/page" render={(props) => <LoginLayout {...props} />} />
        <Redirect to="/page/login" />
        
      </Switch>
    </BrowserRouter>,
    document.getElementById("root")
  );
}


