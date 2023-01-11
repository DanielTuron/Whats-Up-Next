# Whats-Up-Next

The goal of this project was to create my own django/react web application that was both challenging, and fun to use.

The overarching idea of the web app is that anyone can host a 'party room'. This party room gets connected to their spotify account, and then other users can connect to the party room using a party code. 

In a party room, all users can search and queue spotify tracks onto the hosts profile. So that the song will enter the upcoming songs using Spotify's queue. This is intended to be used for either a small group of friends, or large social events with music.

In addition to queueing songs, there is a degree of user interaction within each party room. When a song plays, the username of the user who queued it is displayed along with the song's playback information. Other users can then 'add fire' to a song to indicate they like it. The amount of fire given to each song is displayed for all users along with a sort of leaderboard that keeps track of the user with the most fire given. Called 'Top DJ'.

## Backend

### Python/Django
The backend and api of this project was created using python/django. Inside our database we are storing models for party rooms, users, songs, queue requests etc)

We are also handling Spotify security and authorization in our backend, as well as calls to the Spotify API. All recurring calls to the spotify API are done through the host, and then shared to the other users in order to minimize Spotify API calls, which are limited.

### Breeding Function
The breeding function used throughout this project is one of uniform crossover. One where each gene may be taken from either parent. Although it is not even chance, but instead weighted by fitness dominance. The offspring is then mutated according to the mutation function.

### Frontend
The backend of this project was done using javascript/react. This project also makes frequent use of material UI for cosmetics. https://mui.com/

## Pages
There are currently 4 pages to the Whats-Up-Next web app. In the future I would like to add another page where users can see the upcoming queued songs.

## Run Waiting For GAdot yourself!

This can be done very easily! Find an image you would like to recreate (Nemo was of size 420x370 pixels) and add that into a project folder. See the Nemo project folder for an example. Then, go to the startProject.py file and simply follow the instructions! Your population will periodically get saved in a pickle inside your project folder. To resume a run at a later time, go to loadPop.py and point towards this pickle file.
