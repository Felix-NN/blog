/* jshint undef: true, unused: vars, esnext: true */
/* globals window, document, CustomEvent */

function video() {
    "use strict";

    var querySelector = document.querySelector.bind(document);
    var querySelectorAll = document.querySelectorAll.bind(document);
    var jumpSourceTag;
    var jumpDestTag;
    var sourceTimings = [];
    var destTimings = [];
    var sourceTimingsTag;
    var destTimingsTag;
    var sourceTimingIndex = 0;
    var destTimingIndex = 0;
    var sourcePlayer = null;
    var destPlayer = null;
    var isSourcePlayerCreated = false;
    var isDestPlayerCreated = false;
    var isSourcePlayerReady = false;
    var isDestPlayerReady = false;

    sourceTimingsTag = querySelector('#sample-source-timing');
    destTimingsTag = querySelector('#sample-dest-timing');

    if (sourceTimingsTag) {
        sourceTimings = sourceTimingsTag.dataset.timings.split(',').map(
            function (x) {
                return parseInt(x, 10);
            }
        );
    }

    if (destTimingsTag) {
        destTimings = destTimingsTag.dataset.timings.split(',').map(
            function (x) {
                return parseInt(x, 10);
            }
        );
    }

    jumpSourceTag = querySelector('#jump-source');
    jumpDestTag = querySelector('#jump-dest');

    if (jumpSourceTag) {
        jumpSourceTag.addEventListener('click', onClickSourceButton);
    }

    if (jumpDestTag) {
        jumpDestTag.addEventListener('click', onClickDestButton);
    }

    for (const timingTag of querySelectorAll('.source-timing')) {
        timingTag.addEventListener('click', onClickSourceTiming);
    }

    for (const timingTag of querySelectorAll('.dest-timing')) {
        timingTag.addEventListener('click', onClickDestTiming);
    }

    //document.addEventListener('onLoadYouTubePlayer', onLoadYouTubePlayer, { once: true });
    $('.sample-embed').one('onLoadYouTubePlayer', onLoadYouTubePlayer);

    // Functions

    function onLoadYouTubePlayer(evt) {
        var elm;
        var parentElement;

        elm = evt.detail.elm;
        parentElement = evt.detail.elm.parentElement;


        if (parentElement.classList.contains('embed-source')) {
            if (sourceTimings.length > 0) {
                sourcePlayer = createPlayer(elm, onReadySource);
            }
        } else {
            if (destTimings.length > 0) {
                destPlayer = createPlayer(elm, onReadyDest);
            }
        }

        function createPlayer(elm, onReadyHandler) {
            return new window.YT.Player(elm, {
                'width': elm.dataset.width,
                'height': elm.dataset.height,
                'videoId': elm.dataset.id,
                'playerVars': JSON.parse(elm.dataset.playerVars),
                'events': { 'onReady': onReadyHandler }
            });
        }

        function onReadySource() {
            isSourcePlayerCreated = true;
            isSourcePlayerReady = true;
            sourcePlayer.playVideo();
            sourcePlayer.getIframe().dispatchEvent(
                new CustomEvent('onSourcePlayerCreated', { bubbles: true })
            );
        }

        function onReadyDest() {
            isDestPlayerCreated = true;
            isDestPlayerReady = true;
            destPlayer.playVideo();
            destPlayer.getIframe().dispatchEvent(
                new CustomEvent('onDestPlayerCreated', { bubbles: true })
            );
        }
    }

    function checkSourcePlayerCreated() {
        if (!isSourcePlayerCreated) {
            querySelector('.embed-source .youtube-placeholder').click();
        } else {
            sourcePlayer.getIframe().dispatchEvent(
                new CustomEvent('onSourcePlayerCreated', { bubbles: true })
            );
        }
    }

    function checkDestPlayerCreated() {
        if (!isDestPlayerCreated) {
            querySelector('.embed-dest .youtube-placeholder').click();
        } else {
            destPlayer.getIframe().dispatchEvent(
                new CustomEvent('onDestPlayerCreated', { bubbles: true })
            );
        }
    }

    function onClickSourceButton() {
        document.addEventListener('onSourcePlayerCreated', _onClickSourceButton,
            { 'once': true });
        checkSourcePlayerCreated();

        function _onClickSourceButton() {
            var sourceTimingSeconds, timingTag;

            sourceTimingSeconds = (
                sourceTimings[sourceTimingIndex % sourceTimings.length]
            );
            sourceTimingIndex += 1;
            timingTag = querySelector('#source-timing-' + sourceTimingSeconds);
            playSourcePlayer(sourceTimingSeconds, timingTag);

        }
    }

    function onClickDestButton() {
        document.addEventListener('onDestPlayerCreated', _onClickDestButton,
            { 'once': true });
        checkDestPlayerCreated();

        function _onClickDestButton() {
            var destTimingSeconds, timingTag;

            destTimingSeconds = destTimings[destTimingIndex % destTimings.length];
            destTimingIndex += 1;

            timingTag = querySelector('#dest-timing-' + destTimingSeconds);
            playDestPlayer(destTimingSeconds, timingTag);

        }
    }

    function onClickSourceTiming(evt) {
        document.addEventListener('onSourcePlayerCreated', _onClickSourceTiming,
            { 'once': true });
        checkSourcePlayerCreated();

        function _onClickSourceTiming() {
            var sourceTimingSeconds, timingTag;

            timingTag = evt.target;
            sourceTimingIndex = parseInt(timingTag.dataset.timingIndex, 10);
            sourceTimingSeconds = (
                sourceTimings[sourceTimingIndex % sourceTimings.length]
            );
            sourceTimingIndex += 1;

            playSourcePlayer(sourceTimingSeconds, timingTag);

        }
    }

    function onClickDestTiming(evt) {
        document.addEventListener('onDestPlayerCreated', _onClickDestTiming,
            { 'once': true });
        checkDestPlayerCreated();

        function _onClickDestTiming() {
            var destTimingSeconds, timingTag;

            timingTag = evt.target;
            destTimingIndex = parseInt(timingTag.dataset.timingIndex, 10);
            destTimingSeconds = destTimings[destTimingIndex % destTimings.length];
            destTimingIndex += 1;

            playDestPlayer(destTimingSeconds, timingTag);


        }
    }

    function playSourcePlayer(timingSeconds, timingTag) {
        if (isDestPlayerReady &&
            destPlayer.getPlayerState() === window.YT.PlayerState.PLAYING
        ) {
            destPlayer.pauseVideo();
        }

        sourcePlayer.seekTo(timingSeconds);
        sourcePlayer.playVideo();
        showHighlightEffect(timingTag);
    }

    function playDestPlayer(timingSeconds, timingTag) {
        if (isSourcePlayerReady &&
            sourcePlayer.getPlayerState() === window.YT.PlayerState.PLAYING
        ) {
            sourcePlayer.pauseVideo();
        }

        destPlayer.seekTo(timingSeconds);
        destPlayer.playVideo();
        showHighlightEffect(timingTag);
    }

    function showHighlightEffect(timingTag) {
        timingTag.classList.add('selected');
        window.setTimeout(function () {
            timingTag.classList.remove('selected');
        }, 1000);
    }
    $(function () {
        $(document).on('click', 'button, div.blurred, #sample-source-timing, #source-play, #source-play-btn', function () {
            $('div').removeClass('blurred');
        });
    });

    $(document).on('click', '.btnAns', function () {
        var artist = document.getElementById('artist').innerText;
        var track = document.getElementById('track').innerText;
        var rightAnswer = artist + ' - ' + track;
        var chosen = $(this).text();
        var chosenButt = this;
        var rightButt = "button:contains(" + rightAnswer + ")";
        if (chosen === rightAnswer) {
            $(chosenButt).addClass("btn-success");
            $(chosenButt).removeClass("btn-outline-default");
        } else {
            $(chosenButt).addClass("btn-danger");
            $(chosenButt).removeClass("btn-outline-default");
            $(rightButt).addClass("btn-success");
            $(rightButt).removeClass("btn-outline-default");
        }
        onClickSourceButton();
    });

};

video();
