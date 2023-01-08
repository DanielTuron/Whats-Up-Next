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
import LoginIcon from '@mui/icons-material/Login';



export default function JoinPage(props){
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [usernameError, setUsernameError] = useState("");
    const [partyCode, setPartyCode] = useState('');
    const [partyCodeError, setPartyCodeError] = useState("");

    function handleUserNameChange(e) {
        e.target.value=e.target.value.toLowerCase();
        setUsername(
            e.target.value
        );
    }

    function handlePartyCodeChange(e) {
        e.target.value=e.target.value.toLowerCase();
        setPartyCode(
            (e.target.value).toLowerCase()
        );
    }

    async function handleJoinButtonPressed() {
        let bad = false;
        if(username === ""){
            setUsernameError("Username CANNOT be blank");
            bad = true;
        }

        await fetch("/api/taken-username?code=" + partyCode + "&username=" + username)
            .then((response) => {
                if(response.status!=204){
                    setUsernameError("Username already exists in party, choose another");
                    bad=true;
                }
            }
        );

        await fetch("/api/get-party" + "?code=" + partyCode)
            .then((response) => {
                if(!response.ok){
                    setPartyCodeError("No party matching this code");
                    bad = true;
                }
            });
        
        if(!bad){
            const addUserRequestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  username: username,
                  is_host: false,
                  party_code: partyCode,
                }),
            };
    
            fetch("/api/add-user", addUserRequestOptions)
                .then((response) => {
                    if(response.ok){
                        navigate('/party');
                    }
                }
            );
        }
    }

    function renderPartyCodeError(){
        return(
            <Collapse in={partyCodeError != ""}>
                <Alert 
                    severity="error" 
                    onClose={() => {setPartyCodeError("");}
                }>
                    {partyCodeError}
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
                    Joining Party ...
                </Typography>
            </Grid>
            <Grid item xs = {12} align="center">
                <FormControl>
                    <TextField 
                        required={true} 
                        inputProps={{
                            style: {textAlign: 'center'},
                            maxLength: 4
                        }}
                        label="Enter Party Code"
                        variant="filled"
                        size="small"
                        onChange={handlePartyCodeChange}
                    />

                    <FormHelperText>
                        <div align="center">
                            The party code is visible on the hosts screen
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>
            <Grid item xs = {12} align="center">
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
                    <Button color="primary" onClick={handleJoinButtonPressed}>
                        <LoginIcon/>Join Party
                    </Button>
                </ButtonGroup>
            </Grid>
            <Grid item xs={12} align="center">
                {renderPartyCodeError()}
            </Grid>
            <Grid item xs={12} align="center">
                {renderUsernameError()}
            </Grid>
        </Grid>
    );
}