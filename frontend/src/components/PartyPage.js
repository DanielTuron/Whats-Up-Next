import React, { Component, useState, useEffect } from "react";
import { 
    Grid, 
    Button, 
    ButtonGroup, 
    Typography, 
    List, 
    ListItem, 
    ListItemAvatar, 
    ListItemIcon,
    ListSubheader,
    ListItemText, 
    } from "@material-ui/core";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect,
  useLocation,
  useNavigate,
} from "react-router-dom";
import HomeIcon from '@mui/icons-material/Home';
import Playback from "./Playback";
import SearchBar from "./SearchBar";
import TopDJCard from "./TopDJCard";


let ISH = false;
export default function PartyPage(props){
    const [badState, setBadState] = useState(false);
    const [wasGoodState, setWasGoodState] = useState(false);
    const [code, setCode] = useState(null);
    const [isHost, setHost] = useState(false);
    const [maxQueues, setMaxQueues] = useState(null);
    const [keepCalling, setKeepCalling] = useState(true);
    const navigate = useNavigate();

    function handleUserLeave(){ 
        const RequestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        };

        fetch("/api/leave-party", RequestOptions)
            .then((response) => {
                if(response.ok){
                    navigate('/');
                }
            }
        );
    }

    async function authenticateSpotify() {
        await fetch("/spotify/check-auth")
            .then((response) => response.json())
            .then((data) => {
                let is_auth = data.is_authenticated;
                if (!is_auth) {
                    fetch("/spotify/get-auth-url")
                    .then((response) => response.json())
                    .then((data) => {
                        window.location.replace(data.url);
                    });
                } 
            });
            
    };

    function setPlayback(){
        fetch("/spotify/current-song");
    }

    async function checkState(){
        //keepCalling not working, gets reset to true somehow
        if(keepCalling){
            await fetch("/api/user-party")
            .then((response) => {
                if (!response.ok) {
                    setBadState(true);
                    }
                return response.json();
            })
            .then((data) => {
                if(!badState)
                    setCode(data.code);
                    setHost(data.is_host);
                    ISH = data.is_host
                    setMaxQueues(data.max_queues);
                    setWasGoodState(true);
            });
        }
    }

    function cleanQueue(){
        const RequestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        };
        fetch("/spotify/clean-queue", RequestOptions);
    }

    useEffect(() => {
        checkState();
        const authenticateInterval = setInterval(() => {
            if(ISH){
                authenticateSpotify();
            }
          }, 1000 * 60);

        const checkStateInterval = setInterval(() => {
          checkState();
        }, 1000);
        const setPlaybackInterval = setInterval(() => {
            if(ISH){
                setPlayback();
            }
        }, 1000);

        const setCleanQueueInterval = setInterval(() => {
            if(ISH){
                cleanQueue();
            }
        }, 1000 * 3);
      
        return () => {
            clearInterval(checkStateInterval);
            clearInterval(setPlaybackInterval);
            clearInterval(authenticateInterval);
            clearInterval(setCleanQueueInterval);
        }
      }, []);

    if(ISH){
        authenticateSpotify();
    }

    if(badState){
        if(!wasGoodState){
            navigate('/');
        }
        if(keepCalling){
            setKeepCalling(false);
        }
        return(
            <Grid container align = "center" spacing={6}>
                <Grid item xs = {12}>
                    <Typography variant="h3" align="center">
                            Party was Ended :(
                    </Typography>
                </Grid>
                <Grid item xs = {12}>
                    <ButtonGroup variant="contained" color="primary">
                        <Button color="secondary" component={Link} to='/'>
                            <HomeIcon/>
                        </Button>
                    </ButtonGroup>
                </Grid>
            </Grid>
            
            
        )
    }
    
    

    return(
        <Grid container align = "center" spacing={1} >
            <Grid item xs = {12}>
                <Typography variant="h3" align="center">
                    PARTY CODE : {code}
                </Typography>
            </Grid>
            <Grid item xs = {12}>
                <Playback code={code}/>
            </Grid>
            <Grid item xs = {12} >
                <SearchBar maxQueues={maxQueues}/>
            </Grid>
            <Grid item xs = {12}>
            </Grid>
            <Grid item xs={12} align="center" spacing={2}>
                <ButtonGroup variant="contained" color="primary">
                    <Button color="secondary" onClick={handleUserLeave}>
                        { isHost ? "End Party" : "Leave Party"}
                    </Button>
                </ButtonGroup>
            </Grid>
        </Grid>
    )

}