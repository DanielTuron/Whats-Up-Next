import React, { Component, useState, useEffect } from "react";
import {
  Grid,
  Typography,
  Card,
  IconButton,
  LinearProgress,
} from "@material-ui/core";
import { pulse, bounce } from 'react-animations'
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import PauseIcon from "@material-ui/icons/Pause";
import SkipNextIcon from "@material-ui/icons/SkipNext";
import styled, { keyframes } from 'styled-components';
import Badge from '@mui/material/Badge';
import WhatshotIcon from '@mui/icons-material/Whatshot';
import TopDJCard from "./TopDJCard";

const bounceAnimation = keyframes`${bounce}`;
const pulseAnimation = keyframes`${pulse}`

const BouncyDiv = styled.div`
  animation: 1s ${bounceAnimation};
`;
const PulseyDiv = styled.div`
  animation: 2s ${pulseAnimation} infinite
`;

var cardStyle = {
    display: 'block',
    width: '100%',
    transitionDuration: '0.3s',
    height: '10%',
}

export default function Playback(props){
    const [title, setTitle] = useState("");
    const [artist, setArtist] = useState("");
    const [duration, setDuration] = useState(1);
    const [albumCover, setAlbumCover] = useState(null);
    const [time, setTime] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [username, setUsername] = useState("");
    const [fire, setFire] = useState(0);

    function getPlayback(){
        fetch("/api/current-song").then((response) => {
            if(response.ok){
                return response.json();
            }
            else{
                return null;
            }
          })
          .then((data) => {
            if(data==null){
                setTitle("");
                setArtist("");
                setDuration(1);
                setAlbumCover(null);
                setTime(0);
                setIsPlaying(false);
                setUsername("");
              }
              else{
                setTitle(data.title);
                setArtist(data.artist);
                setDuration(data.duration);
                setAlbumCover(data.album_cover);
                setTime(data.time);
                setIsPlaying(data.is_playing);
                setUsername(data.username);
                setFire(data.fire)
              }
          })
    }

    useEffect(() => {
        const getPlaybackInterval = setInterval(() => {
          getPlayback();
        }, 1000);
      
        return () => {
            clearInterval(getPlaybackInterval);
        }
      }, []);

    function getProgress(time,duration){
        return (time/duration)*100;
    }

    function handleFireClick(){
        const RequestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        };
        fetch("/api/give-fire", RequestOptions);
    }

    function renderPlayer(){
        return(
                <Grid container alignItems="center" spacing = {1}>
                    <Grid item xs={10}>
                    <Card style={cardStyle}>
                    <Grid container alignItems="center">
                        <Grid item align="center" xs={3}>
                            <img src={albumCover} height="100%" width="100%"/>
                        </Grid>
                        <Grid item align="center" xs={8}>
                            <Typography component="h5" variant="h5">
                                {title}
                            </Typography>
                            <Typography color="textSecondary" variant="subtitle1">
                                {artist}
                            </Typography>
                            <Typography color="textSecondary" variant="h10">
                                <strong>{username == "" ? "" : "Queued by - " + username}</strong>
                            </Typography>
                        </Grid>
                        <Grid item align="center" xs={1}>
                            <IconButton onClick={handleFireClick}>
                                <Badge badgeContent={fire} color="secondary">
                                        <WhatshotIcon/>
                                </Badge>
                            </IconButton>
                        </Grid>
                    </Grid>
                    <LinearProgress variant="determinate" value={getProgress(time,duration)} />
                </Card>
                    </Grid>
                    <Grid item xs={2} spacing = {1}>
                        <TopDJCard code={props.code}/>
                    </Grid>
                </Grid>
        )
    }
    
    if(isPlaying){
        return(
            <BouncyDiv>
                <PulseyDiv>
                    {renderPlayer()}
                </PulseyDiv>
            </BouncyDiv>
        )
    }
    else{
        return(
            <BouncyDiv>
                {renderPlayer()}
            </BouncyDiv>
        )

    }
}