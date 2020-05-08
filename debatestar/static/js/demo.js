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

// Array to store the Persuasiveness scores. 
var scoresArr = [];

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
    fillScoresArr(scoresArr);
}

// On Play/Pause, udpate the time inteval
// 1000ms = 1s
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

// TODO: this hardcoded version won't be used
function fillScoresArr(scoresArr) {
    const max = 0.76;
    const min = 0.39;
    // intro part
    for (var i = 0; i < 240; i++)
        scoresArr.push(0.5);
    // begin the debate
    for (var i = 241; i < 4472; i++)
        scoresArr.push(Math.random() * (max - min) + min);
    // end part
    for (var i = 4473; i < 5000; i++)
        scoresArr.push(scoresArr[4470]);
    console.log("Score Array Generated");
}

// update the scores
function updateScore(videotime) {
    //console.log("update score " + Math.round(videotime));
    var forrate = scoresArr[Math.round(videotime)] * 100;
    forrate = forrate.toFixed(2);
    var againstrate = 100 - forrate;
    againstrate = againstrate.toFixed(2);
    document.getElementById("forrate").textContent = forrate.toString() + "%";
    document.getElementById("againstrate").textContent = againstrate.toString() + "%";
}