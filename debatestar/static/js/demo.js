// Youtube API Iframe to get time events. 
var tag = document.createElement('script');
tag.id = 'iframe-demo';
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// A workaround for Youtube time update
// REF: https://stackoverflow.com/questions/10175367/youtube-api-event-on-a-specified-time/11782167
var videotime = 0;
var timeupdater = null; 

// Load the player when API is ready
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('video', {
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
    console.log("API is ready");
}

// Player is ready
function onPlayerReady(event) {
    console.log("player is ready");
    //timeupdater = setInterval(updateTime, 1000);
}

// On Play/Pause, udpate the time inteval
function onPlayerStateChange(event) {
    console.log("player state changed");

    if (event.data == YT.PlayerState.PLAYING) {
        timeupdater = setInterval(updateTime, 1000);
    }

    if (event.data == YT.PlayerState.PAUSED || 
        event.data == YT.PlayerState.ENDED) {
        clearInterval(timeupdater);
    }
}

// Check the time update for every second video played. 
function updateTime() {
    var oldTime = videotime;
    if(player && player.getCurrentTime) {
      videotime = player.getCurrentTime();
    }
    if(videotime !== oldTime) {
      updateScore(videotime);
    }
}

// update the scores
function updateScore(videotime) {
    console.log("update score " + Math.round(videotime));
}