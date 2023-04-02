(function () {
  $(document).ready(function () {
    $(".gallery").magnificPopup({
      delegate: 'a',
      gallery: {
        enabled: false,
      },
      iframe: {
        markup:
          '<div class="mfp-iframe-scaler">' +
          '<div class="mfp-close"></div>' +
          '<div><iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe></div>' +
          '<div class="mfp-title">{{title}}</div>' +
          "</div>",
        patterns: {
          soundcloud: {
            index: "soundcloud.com/",
            id: function (url) {
              return encodeURI(url);
            },
            src: "//w.soundcloud.com/player/?url=%id%&amp;auto_play=true&amp;hide_related=true&amp;show_comments=false&amp;show_user=false&amp;show_reposts=false&amp;visual=true;", // URL that will be set as a source for iframe.
          },
        },
        srcAction: "iframe_src",
      },
      inline: {
        markup:
          '<div class="mfp-inline-holder"></div>' ,
      },
      zoom: {
        enabled: false,
      },
      callbacks: {
        open: function () {
          this.content.find(".mfp-title").text(this.st.el.attr("title"));
        },
      },
    });
  });


})();
