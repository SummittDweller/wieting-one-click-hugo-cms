function checkTweetDate( ) {
  var card = document.getElementsByClassName('timeline-card')[0];
  var iframe = document.getElementById("twitter-widget-0");
  //console.log(iframe);
  var metadata = iframe.contentWindow.document.getElementsByClassName('timeline-Tweet-metadata')[0];
  //console.log(metadata);
  var target = metadata.getElementsByTagName('time')[0];
  //console.log(target);
  var pubTime = Date.parse(target.getAttribute('datetime'));
  //console.log(pubTime);

  var now = Date.parse(Date());
  //console.log(now);

  var diff = now - pubTime;

  // check if tweet is more than 12 hours old
  if (diff > 12*60*60*1000) {
    //alert("Tweet is stale");
    card.style.display = "none";
  }
}
