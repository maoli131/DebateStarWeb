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
var time_score = {"0": "0.13075700088583697", "62": "0.5105205230845925", "126": "0.10011484503160173", "183": "0.3086853483777452", "204": "0.2886627851520196", "302": "0.9676914426226466", "388": "0.45660353230635364", "449": "0.6134228050517195", "483": "0.45434017544380056", "541": "0.264385775880314", "609": "0.6744431413022345", "662": "0.5122547713074662", "722": "0.08717340202484736", "789": "0.9845644007989384", "847": "0.8797478682211551", "900": "0.6914511164569603", "963": "0.6671272252799955", "1034": "0.8631313369752514", "1084": "0.8382652533059134", "1157": "0.5624644171416868", "1209": "0.25650021318133664", "1264": "0.9969276464849899", "1335": "0.6031638092714032", "1413": "0.48131057148745426", "1453": "0.14997474538738698", "1514": "0.3262435435395855", "1564": "0.1754296768489414", "1638": "0.3254836428466523", "1684": "0.45595362938559336", "1750": "0.1038809449329211", "1817": "0.757941915193208", "1868": "0.4677679941416505", "1925": "0.17427290293548015", "1989": "0.801425943308036", "2049": "0.7270364284585062", "2107": "0.6009465138463409", "2177": "0.11446658757763395", "2225": "0.9238755559530901", "2291": "0.23903901631421587", "2349": "0.1304383188403606", "2403": "0.23578307362230222", "2469": "0.1358797021489051", "2522": "0.08299040792590962", "2581": "0.749011916789788", "2648": "0.6275083539925793", "2706": "0.6430457061398276", "2769": "0.8214372641026222", "2836": "0.326717786640511", "2895": "0.4176266208652538", "2952": "0.5540433034950534", "3016": "0.7036155376817417", "3070": "0.8727830972735812", "3129": "0.4419373553780168", "3195": "0.011213099920529435", "3255": "0.2692324055346602", "3365": "0.5814847483009336", "3425": "0.12934989391254081", "3493": "0.48361210401377697", "3551": "0.08648998216477732", "3609": "0.5479910950978304", "3668": "0.12958963058970963", "3725": "0.30272121026717835", "3786": "0.8766386055110165", "3849": "0.21022809262764908", "3900": "0.3782184138243908", "3982": "0.3053852444318731", "4041": "0.5558086944922975", "4104": "0.6314542406172092", "4146": "0.9649284853258743", "4219": "0.7562899256811448", "4266": "0.7129322670792431", "4338": "0.03669700391513486", "4390": "0.6697758747793482", "4461": "0.04427711081830432", "4509": "0.671915960026053", "4576": "0.6293503373082688", "4636": "0.9304046885590418", "4697": "0.14017233697141807", "4758": "0.9001068658538237", "4866": "0.5569735764616728"};

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

// update the scores
function updateScore(videotime) {
    
    //console.log('videotime: ' + Math.round(videotime));

    // if reached a new time-stamp
    if (time_score.hasOwnProperty(Math.round(videotime))) {
    
        var forrate = parseFloat(time_score[Math.round(videotime)]);
        forrate = forrate.toFixed(4) * 100;
        var againstrate = 100 - forrate;
        againstrate = againstrate.toFixed(2);
        document.getElementById("forrate").textContent = forrate.toString() + "%";
        document.getElementById("againstrate").textContent = againstrate.toString() + "%";

        console.log("update score " + forrate);
    }
}