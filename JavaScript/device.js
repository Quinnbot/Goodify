window.onSpotifyWebPlaybackSDKReady = () => {

    //get login token
    fetch('https://accounts.spotify.com/authorize?'
      +'client_id=5fe01282e44241328a84e7c5cc169165'
      +'&response_type=code'
      +'&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback'
      +'&scope=user-read-private%20user-read-email'
      +'&state=34fFs29kd09')


    const token = '';

    const player = new Spotify.Player({

      name: 'Goodify',
      getOAuthToken: cb => { cb(token); }

    });

    // Error handling
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });

    // Playback status updates
    player.addListener('player_state_changed', state => {
        
        //sends the new song obj to Main.js to update the webpage
        update(state);
    
    });

    // Ready
    player.addListener('ready', ({ device_id }) => {

      console.log('Ready with Device ID', device_id);

      play('spotify:track:2HvtedoEeymVWrBPyAMNwZ', device_id, token);

    });

    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {

      console.log('Device ID has gone offline', device_id);

    });

    // Connect to the player!
    player.connect();

  };