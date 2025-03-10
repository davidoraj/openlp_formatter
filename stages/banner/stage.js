/******************************************************************************
 * OpenLP - Open Source Lyrics Projection                                      *
 * --------------------------------------------------------------------------- *
 * Copyright (c) 2008-2021 OpenLP Developers                                   *
 * --------------------------------------------------------------------------- *
 * This program is free software; you can redistribute it and/or modify it     *
 * under the terms of the GNU General Public License as published by the Free  *
 * Software Foundation; version 2 of the License.                              *
 *                                                                             *
 * This program is distributed in the hope that it will be useful, but WITHOUT *
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    *
 * more details.                                                               *
 *                                                                             *
 * You should have received a copy of the GNU General Public License along     *
 * with this program; if not, write to the Free Software Foundation, Inc., 59  *
 * Temple Place, Suite 330, Boston, MA 02111-1307 USA                          *
 ******************************************************************************/

window.OpenLP = { // Connect to the OpenLP Remote WebSocket to get pushed updates
  myWebSocket: function (data, status) {
    const host = window.location.hostname;
    const websocket_port = 4317;
    var myTwelve;

    ws = new WebSocket(`ws://${host}:${websocket_port}`);
    ws.onmessage = (event) => {
      const reader = new FileReader();
      reader.onload = () => {
        data = JSON.parse(reader.result.toString()).results;
        // set some global var
        OpenLP.myTwelve = data.twelve;
        if (OpenLP.currentItem != data.item ||
            OpenLP.currentService != data.service) {
          OpenLP.currentItem = data.item;
          OpenLP.currentService = data.service;
          OpenLP.loadSlides();
        } else if (OpenLP.currentSlide != data.slide) {
          OpenLP.currentSlide = parseInt(data.slide, 10);
          OpenLP.updateSlide();
        }
        OpenLP.loadService();
      };
      reader.readAsText(event.data);
    };
  },

  loadService: function (event) {
    $.getJSON(
        "/api/v2/service/items",
        function (data, status) {
          OpenLP.nextSong = "";
          $("#notes").html("");
          data.forEach(function (item, index, array) {
            //if (data.length > index + 1) {
            //console.log("next title");
            //console.log(data[index + 1].title);
            //};
            if (item.selected) {
              //console.log("notes");
              //console.log(item.notes)
              //$("#notes").html(item.notes).replace(/\n/g, "<br />");
              $("#notes").html(item.notes);
              if (data.length > index + 1) {
                OpenLP.nextSong = data[index + 1].title;
              } else {
                OpenLP.nextSong = "End of Service";
              }
            }
          });
          OpenLP.updateSlide();
        }
    );
  },

  loadSlides: function (event) {
    $.getJSON(
        "/api/v2/controller/live-items",
        function (data, status) {
          OpenLP.currentSlides = data.slides;
          OpenLP.currentSlide = 0;
          OpenLP.currentTags = Array();
          var div = $("#verseorder");
          div.html("");
          var tag = "";
          var tags = 0;
          var lastChange = 0;
          $.each(data.slides, function (idx, slide) {
            var prevtag = tag;
            tag = slide["tag"];
            if (tag != prevtag) {
              // If the tag has changed, add new one to the list
              lastChange = idx;
              tags = tags + 1;
              div.append("&nbsp;<span>");
              $("#verseorder span").last().attr("id", "tag" + tags).text(tag);
            } else {
              if ((slide["text"] == data.slides[lastChange]["text"]) &&
                  (data.slides.length >= idx + (idx - lastChange))) {
                // If the tag hasn't changed, check to see if the same verse
                // has been repeated consecutively. Note the verse may have been
                // split over several slides, so search through. If so, repeat the tag.
                var match = true;
                for (var idx2 = 0; idx2 < idx - lastChange; idx2++) {
                  if (data.slides[lastChange + idx2]["text"] != data.slides[idx
                  + idx2]["text"]) {
                    match = false;
                    break;
                  }
                }
                if (match) {
                  lastChange = idx;
                  tags = tags + 1;
                  div.append("&nbsp;<span>");
                  $("#verseorder span").last().attr("id", "tag" + tags).text(
                      tag);
                }
              }
            }
            OpenLP.currentTags[idx] = tags;
            if (slide["selected"]) {
              OpenLP.currentSlide = idx;
            }
          })
          OpenLP.loadService();
        }
    );
  },

  updateSlide: function () {
    // Show the current slide on top. Any trailing slides for the same verse
    // are shown too underneath in grey.
    // Then leave a blank line between following verses
    $("#verseorder span").removeClass("currenttag");
    $("#tag" + OpenLP.currentTags[OpenLP.currentSlide]).addClass("currenttag");
    var slide = OpenLP.currentSlides[OpenLP.currentSlide];
    text = slide["text"]
    slide_delim = "\n\n"

    // Check if the slide contains a delimiter ("|")
    if (text.includes(slide_delim)) {
      var parts = text.split(slide_delim);

      var leftText = parts[0].trim() || "No Left Text";
      var rightText = parts[1].trim() || "No Right Text";

      // Show two-column layout
      $("#singleColumn").hide();
      $("#twoColumn").show();
      $("#leftSlide").html(leftText.replace(/\n/g, "<br>"));
      $("#rightSlide").html(rightText.replace(/\n/g, "<br>"));
    } else {
      // Show single centered column
      $("#twoColumn").hide();
      $("#singleColumn").show();
      $("#singleColumn").html(text.replace(/\n/g, "<br>"));
    }

  },

}
$.ajaxSetup({cache: false});
setInterval("OpenLP.updateClock();", 500);
OpenLP.myWebSocket();
