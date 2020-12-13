window.onSpotifyWebPlaybackSDKReady = () => {

    const token = 'BQDwPBqQS-Ajy6-AM8k6rHuijDCw1aq3ChMzqvwPCelkcidovwf0EB2OnHPtcVtxi6ogx6s7LZoqcdl1t4mN3wHGH4Qfs0RP7wB2uOhWZNk0O_mxX2KJUadx9qZz1BedXErIeU_XaJYWLpNMlqbGSppgT7fd5Yun5l0H';

    const player = new Spotify.Player({

      name: 'Web Playback SDK',
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