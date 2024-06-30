import $ from "jquery";
import select2 from "select2";
import "select2/dist/css/select2.css";

$(document).ready(function () {
  // $("#id_category").select2({
  //   closeOnSelect: true,
  // });
  $("#id_genres").select2({
    closeOnSelect: true,
  });
});
