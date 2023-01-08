import React, { Component, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Grid, Button, ButtonGroup, Typography, TextField, FormControl, FormHelperText, Collapse } from "@material-ui/core";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import Alert from "@material-ui/lab/Alert";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";
import CreateIcon from "@material-ui/icons/Create";
import CelebrationIcon from '@mui/icons-material/Celebration';

var ESCAPE_KEY = 27;


export default function CreatePage(props){
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [maxQueues, setMaxQueues] = useState(3);
    const [queueError, setQueueError] = useState("");
    const [usernameError, setUsernameError] = useState("");
      
    
    function handleMaxQueuesChange(e) {
        setMaxQueues(
            e.target.value
        );
    }

    function handleUserNameChange(e) {
        e.target.value=e.target.value.toLowerCase();
        setUsername(
            e.target.value
        );
    }

    function handleCreateButtonPressed() {
        let bad = false;

        if(username === ""){
            setUsernameError("Username CANNOT be blank");
            bad = true;
        }

        if(maxQueues < 1){
            setQueueError("Max Queues MUST be 1 or greater");
            bad = true;
        }
        
        if(!bad){
            const createPartyRequestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  max_queues: maxQueues,
                }),
            };
    
            fetch("/api/create-party", createPartyRequestOptions)
            .then((response) => response.json())
            .then((data) => {
                const addUserRequestOptions = {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      username: username,
                      is_host: true,
                      party_code: data.code,
                    }),
                };
                fetch("/api/add-user", addUserRequestOptions)
                .then((response) => {
                    if(response.ok){
                        navigate('/party');
                    }
                });
            });
        }
        
    }

    function renderQueueError(){
        return(
            <Collapse in={queueError != ""}>
                <Alert 
                    severity="error" 
                    onClose={() => {setQueueError("");}
                }>
                    {queueError}
                </Alert>
            </Collapse>
        );
    }

    function renderUsernameError(){
        return(
            <Collapse in={usernameError != ""}>
                <Alert 
                    severity="error" 
                    onClose={() => {setUsernameError("");}
                }>
                    {usernameError}
                </Alert>
            </Collapse>
        );
    }

    return(
        <Grid container align = "center" spacing={4}>
            <Grid item xs = {12}>
                <Typography align="center" variant="h2" >
                    Creating Party ...
                </Typography>
            </Grid>
            <Grid item xs = {6} align="center">
                <FormControl>
                    <TextField 
                        required={true} 
                        type = "number" 
                        defaultValue={3}
                        inputProps={{
                            min: 1,
                            style: {textAlign: 'center'}
                        }}
                        onChange={handleMaxQueuesChange}
                    />

                    <FormHelperText>
                        <div align="center">
                            Max queue's per user at a time
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>
            <Grid item xs = {6} align="center">
                <FormControl>
                    <TextField 
                        required={true} 
                        inputProps={{
                            style: {textAlign: 'center'},
                            maxLength: 12
                        }}
                        label="Enter Username"
                        variant="filled"
                        size="small"
                        onChange={handleUserNameChange}
                    />

                    <FormHelperText>
                        <div align="center">
                            Username
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <ButtonGroup variant="contained" color="primary">
                    <Button color="secondary" component={Link} to="/">
                        <ArrowBackIcon/>
                    </Button>
                    <Button color="primary" onClick={handleCreateButtonPressed}>
                        <CelebrationIcon/> Create Party
                    </Button>
                </ButtonGroup>
            </Grid>
            <Grid item xs={12} align="center">
                {renderQueueError()}
            </Grid>
            <Grid item xs={12} align="center">
                {renderUsernameError()}
            </Grid>
        </Grid>
    );
}