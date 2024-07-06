import $ from "jquery";
import "select2";
import "select2/dist/css/select2.min.css";
import "select2/dist/js/select2.full.min.js";

$(document).ready(function () {
  $("#id_category").select2({
    closeOnSelect: true,
    placeholder: "Select a category",
    multiple: true,
    // amdLanguageBase: "select2/i18n/",
    // theme: "classic",
  });
  $("#id_genres").select2({
    closeOnSelect: true,
    placeholder: "Select a genre",
    multiple: true,
    // amdLanguageBase: "select2/i18n/",
    // theme: "classic",
  });
});
