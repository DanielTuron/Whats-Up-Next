import React, { useEffect, useState } from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import { ListItemButton } from '@mui/material';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import { Collapse } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";

export default function SearchResults(props) {
  const [errMsg, setErrMsg] = useState("");

  useEffect(() => {
    setErrMsg('');
  
    return () => {;
    }
  }, []);

  function handleQueueRequest(song){
    setErrMsg('');
    fetch('/api/get-num-queues')
      .then((response) => response.json())
        .then((data) => {
          if(data.num_queues < props.maxQueues){
            fetch('/api/is-queued?song-id=' + song.id)
            .then((response) => response.json())
              .then((data) => {
                if(data.queue_found){
                  setErrMsg('already in queue')
                }
                else{
                  setErrMsg('Success!')
                  queueSong(song);
                }
              })
          }
          else{
            setErrMsg('You have used all available queues, wait for one of your songs to complete')
          }
        });
  }

  function queueSong(song){
    let song_id = song.id
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        song_id: song_id,
      }),
    };
    fetch('/spotify/queue', requestOptions);
    props.onSelect()
  }

  const Row = ({ index, style }) => (
    <ListItemButton alignItems="flex-start" 
      style={style} 
      key={index} 
      component="div" 
      disablePadding
      onClick={(event) => handleQueueRequest(props.results[index])}
    >
      <ListItemAvatar>
        <Avatar alt={props.results[index].title} src={props.results[index].album_cover} />
      </ListItemAvatar>
      <ListItemText
        primary={props.results[index].title}
        secondary={
          <Typography
            sx={{ display: 'inline' }}
            component="span"
            variant="body2"
            color="text.primary"
          >
            {props.results[index].artist}
          </Typography>
        }
      />
    </ListItemButton>
  );
  if(errMsg != ""){
    return(
      <Alert 
            severity={errMsg == "Success!"? "success" : "error" }
            onClose={() => {setErrMsg("");}
        }>
            {errMsg}
        </Alert>
    );
  }
  else if(props.results.length==0){
    return(
      <></>
    )
  }
  else{
    return (
    <Box
      sx={{ width: '100%', height: props.results.length==1? 60 : 120, bgcolor: 'background.paper' }}
    >
    <FixedSizeList 
      height={120}
      width={'100%'}
      itemSize={60}
      itemCount={props.results.length}
      sx={{ width: '65%', bgcolor: 'background.paper' }}
    >
      {Row}
    </FixedSizeList>
    </Box>
  );
  }
}