
/* jshint undef: true, unused: vars, esnext: true */
/* globals window, document, Image, CustomEvent */

function youtubeReady() {
    "use strict";

    function onYouTubeIframeAPIReady() {
        for (const placeholder of document.querySelectorAll('.youtube-placeholder')) {
            processYoutubePlaceholder(placeholder);
        }
    }

    function processYoutubePlaceholder(placeholder) {
        /**
         * YouTube thumbnails
         * ------------------
         * Medium Quality: https://img.youtube.com/vi/{video-id}/mqdefault.jpg (320Ã—180 pixels)
         * High Quality: https://img.youtube.com/vi/{video-id}/hqdefault.jpg (480Ã—360 pixels)
         * Standard Definition (SD): https://img.youtube.com/vi/{video-id}/sddefault.jpg (640Ã—480 pixels)
         * Maximum Resolution: https://img.youtube.com/vi/{video-id}/maxresdefault.jpg (1920Ã—1080 pixels)
         */

        let img = new Image();
        let quality = 'sddefault';

        placeholder.addEventListener('click', onClick);
        placeholder.addEventListener('mouseenter', onMouseMove);
        placeholder.addEventListener('mouseleave', onMouseMove);

        img.addEventListener('load', onLoad);
        img.src = `https://img.youtube.com/vi/${placeholder.dataset.id}/${quality}.jpg`;

        function onClick(evt) {
            let event;

            event = new CustomEvent('onLoadYouTubePlayer', {
                bubbles: true,
                detail: { 'elm': placeholder }
            });
            evt.target.dispatchEvent(event);
        }

        function onMouseMove(evt) {
            evt.target.querySelector('.play-button').classList.toggle('hover');
        }

        function onLoad(evt) {
            let img = evt.target;

            if (img.width < 320) {
                quality = 'hqdefault';
                img.src = `https://img.youtube.com/vi/${placeholder.dataset.id}/${quality}.jpg`;
            } else {
                placeholder.appendChild(img);
            }
        }
    }

    window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
};

youtubeReady();
