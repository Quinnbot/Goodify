function play(URI, device_id, token){

    fetch(`https://api.spotify.com/v1/me/player/play?device_id=${device_id}`, {

    method: 'PUT',

    body: JSON.stringify({ uris: [URI] }),

      headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
      },

    });

  }
function update(song_obj){

    song_art_url = song_obj['track_window']['current_track']['album']['images'][0]['url'];
    song_name = song_obj['track_window']['current_track']['name'];
    song_artist = song_obj['track_window']['current_track']['artists'][0]['name']

    document.getElementById("playing_art").src = song_art_url;
    document.getElementById("playing_name").innerHTML = song_name + ' - ' + song_artist;

    
  }