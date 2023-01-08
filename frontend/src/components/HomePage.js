import React, { Component, useEffect } from "react";
import { Grid, Button, ButtonGroup, Typography, RaisedButton } from "@material-ui/core";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect,
  useNavigate,
} from "react-router-dom";
import SearchIcon from "@material-ui/icons/Search"
import CreateIcon from "@material-ui/icons/Create"

export default function HomePage(props){
    return(
        <Grid container align = "center" spacing={6}>
            <Grid item xs = {12}>
                <Typography align="center" variant="h2" >
                    What's Up Next?
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <ButtonGroup variant="contained" color="primary">
                    <Button color="secondary" component={Link} to="/create">
                        <CreateIcon/>Create New Party
                    </Button>
                    <Button color="primary" component={Link} to="/join">
                        <SearchIcon/>   Join Existing Party 
                    </Button>
                </ButtonGroup>
            </Grid>
        </Grid>
    );
}