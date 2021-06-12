import React from "react";
import PerfectScrollbar from "perfect-scrollbar";
import { Route, Switch, useLocation } from "react-router-dom";


import Footer from "components/Footer/Footer.js";


import routes from "routes.js";

var ps;

export default function LoginPage(props) {
   
    return (
        <div className="wrapper">

          <div >
            <Switch>
              {routes.map((prop, key) => {
                return (
                  <Route
                    path={prop.layout + prop.path}
                    component={prop.component}
                    key={key}
                  />
                );
              })}
            </Switch>
       
          </div>
          
        </div>
      );
}