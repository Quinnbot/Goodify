
window.onSpotifyWebPlaybackSDKReady = () => {
  // document.getElementById("Menu").innerHTML = 

  const player = new Spotify.Player({
    name: 'Goodify',
    getOAuthToken: cb => { 
 
      fetch('/API/token')
      .then(response => response.json())
      .then(data => cb(data['token']));
      
    }
  });

  // Error handling
  player.addListener('initialization_error', ({ message }) => {
    console.error(message); 
  });

  player.addListener('authentication_error', ({ message }) => {
    console.error(message); 
  });

  player.addListener('account_error', ({ message }) => { console.error(message); });
  player.addListener('playback_error', ({ message }) => { console.error(message); });

  player.addListener('player_state_changed', state => {

    document.getElementById("playing_art").src = state['track_window']['current_track']['album']['images'][2]['url'];
    document.getElementById("playing_name").innerHTML = state['track_window']['current_track']['name'] + ' - ' + state['track_window']['current_track']['artists'][0]['name'];
    
    if (state['paused']) { document.getElementById('play_pause').src='pictures\\play.png'}
    else { document.getElementById('play_pause').src='pictures\\pause.png' }



    var upnext = 'Up Next:';

    for (let track of state['track_window']['next_tracks']){
      upnext += '<p>'+ track['name'] + ' - '+ track['artists'][0]['name']+'</p>'
    }

    console.log(state)
    if (state['paused'] && state['position'] == 0 && !state['loading']){
      fetch("/API/auto-dj", {
        method: "POST",
        body: JSON.stringify(state)
      });
    }

    fetch("/API/player_state", {
      method: "POST", 
      body: JSON.stringify(state)
    });
  })



  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);

    player.setVolume(0.5)

    fetch("/API/device_ready", {
      method: "POST", 
      body: JSON.stringify(device_id)
    });
  });

  // Not Ready
  player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id);
  });

  // Connect to the player!
  player.connect();

  fetch('/API/playlists')
  .then(response => response.json())
  .then(data => console.log(data));

  //play / pause button
  
  var PlayPause = document.getElementById("play_pause");
  PlayPause.onclick = function() {
    player.togglePlay();
  }

  var slider = document.getElementById("vol_control");
  slider.oninput = function() {
    player.setVolume(this.value);
  }

};