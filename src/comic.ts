import $ from "jquery";
$(document).on("click", "#like-button", function (e) {
  e.preventDefault();
  const likecount = document.getElementById("like_count") as HTMLElement;
  $.ajax({
    type: "POST",
    url: '{% url "bookmarks:like" %}',
    data: {
      comicid: $("#like-button").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      action: "post",
    },
    success: function (json) {
      likecount.innerHTML = json["result"];
    },
    error: function (xhr, errmsg, err) {},
  });
});
