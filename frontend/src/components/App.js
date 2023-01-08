import React, { Component } from "react";
import { 
  render,
} from "react-dom";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Routes,
  Link,
  Redirect,
  useNavigate,
} from "react-router-dom";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import RouterPage from "./RouterPage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="center">
        <Grid>
          <Router>
            <RouterPage />
          </Router>
        </Grid>
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);