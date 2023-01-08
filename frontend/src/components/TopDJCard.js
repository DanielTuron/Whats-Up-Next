import React, { Component, useState, useEffect } from "react";
import { useTheme } from '@mui/material/styles';
import {
  Grid,
} from "@material-ui/core";
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Badge from '@mui/material/Badge';
import WhatshotIcon from '@mui/icons-material/Whatshot';
import HeadphonesIcon from '@mui/icons-material/Headphones';

var cardStyle = {
  width: '100%',
  height: '100%',
}

export default function TopDJCard(props) {
  const [username, setUsername] = useState("");
  const [fire, setFire] = useState(0);
  fetch("/api/get-top-dj?code=" + props.code)
    .then((response) => response.json())
    .then((data) => {
      setUsername(data.username);
      setFire(data.fire)
    })

  return(
      <div className='.center'>
          <Card style={cardStyle}>
              <Grid container sx={{ display: 'flex', flexDirection: 'column' }} alignItems="center" spacing={1}>
                <Grid item xs={12}>
                  <Typography component="h8" variant="h8">
                    <HeadphonesIcon/>
                    Top DJ
                    <HeadphonesIcon/>
                  </Typography>
                </Grid>
                <Grid item xs={12} spacing={6}>
                  <Typography color="textSecondary" variant="h10">
                    <strong>{username}</strong>
                  </Typography>
                </Grid>
                <Grid item xs={12} spacing={6}>
                  <Badge badgeContent={fire} color="secondary">
                    <WhatshotIcon/>
                  </Badge>
                </Grid>
              </Grid>
          </Card>
      </div>
  );
}