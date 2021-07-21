
    

async function request(url, meth){

  var rj = await fetch(url, {method:meth}).then(response => response.json());
  return rj
  
}
// var tokens = request('/API/token', 'GET');
// console.log(tokens);

window.onSpotifyWebPlaybackSDKReady = () => {
  
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
      // upnext += '<div><img id=play_pause src="'+track['album']['images'][2]['url']+'"width="250" height="250"><br>'+ track['name'] + ' - '+ track['artists'][0]['name']+'</div>'
      upnext += '<p>'+ track['name'] + ' - '+ track['artists'][0]['name']+'</p>'
    }

    document.getElementById("up_next").innerHTML = upnext;

    console.log(state['context'])

    fetch("/API/player_state", {
      method: "POST", 
      body: JSON.stringify(state)
    });
  })



  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);

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
};