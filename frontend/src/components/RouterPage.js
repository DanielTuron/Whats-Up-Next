import React, { Component, useEffect} from "react";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Routes,
  Link,
  Redirect,
  useNavigate,
} from "react-router-dom";
import HomePage from "./HomePage";
import CreatePage from "./CreatePage";
import PartyPage from "./PartyPage";
import JoinPage from "./JoinPage";

export default function RouterPage(props){
    return(
                <Routes>
                    <Route exact path="/" element={<HomePage/>}/>
                    <Route path="/create" element={<CreatePage/>}/>
                    <Route path="/join" element={<JoinPage/>}/>
                    <Route path="/party" element={<PartyPage/>}/>
                </Routes>
    );
}
            

            