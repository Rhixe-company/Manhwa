import $ from "jquery";
import select2 from "select2";
import "select2/dist/css/select2.css";

$(document).ready(function () {
  $("#id_comic").select2({
    closeOnSelect: true,
  });
});
