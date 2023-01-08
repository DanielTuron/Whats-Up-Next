import React, { useState, useEffect } from "react";
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import DirectionsIcon from '@mui/icons-material/Directions';
import { Typography, Grid } from '@mui/material';
import SearchResults from "./SearchResults";

export default function SearchBar(props) {
    const [search, setSearch] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [numQueues, setNumQueues] = useState(0);
    function handleSearchChange(e) {
        setSearch(
            e.target.value
        );
        setSearchResults([]);
    }

    function getNumQueues(){
        let numQueues = 0;
        fetch('/api/get-num-queues')
        .then((response) => response.json())
                .then((data) => {
                numQueues = data.num_queues;
                setNumQueues(numQueues)
            });
    }

    async function handleSearchRequest(){
        if(search!=''){
            await fetch("/spotify/search-songs" + "?query=" + search)
                .then((response) => response.json())
                .then((data) => {
                    setSearchResults(data);
                }
            );
        }
    };
    useEffect(() => {
        const checkNumQueuesInterval = setInterval(() => {
            getNumQueues();
          }, 1000 * 3);
      
        return () => {
            clearInterval(checkNumQueuesInterval);
        }
      }, []);

    function handleSelect(){
        setSearchResults([]);
        setSearch('');
        document.getElementById("searchbar").value='';
    }

  return (
    <Grid container align = "center">
        <Grid item xs = {12}>
            <Paper
            component="form"
            sx={{ display: 'flex', alignItems: 'center', width: '100%', height: '100%' }}
            >
                <IconButton aria-label="menu">
                    <MenuIcon />
                </IconButton>
                <InputBase
                    sx={{ ml: 1, flex: 1 }}
                    placeholder="Queue Track"
                    inputProps={{ 'aria-label': 'Queue Track' }}
                    onChange={handleSearchChange}
                    id="searchbar"
                />
                <IconButton type="button" aria-label="search" onClick={handleSearchRequest}>
                    <SearchIcon />
                </IconButton>
                <Divider orientation="vertical" />
                <Typography>
                      Queues used : {numQueues}/{props.maxQueues}
                </Typography>
            </Paper>
        </Grid>
        <Grid item xs = {12}>
            <SearchResults results={searchResults} onSelect={handleSelect} maxQueues={props.maxQueues}/>
        </Grid>
    </Grid>
  );
}