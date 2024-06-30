import { Input, Modal, Ripple, initTWE, Carousel } from "tw-elements";

initTWE({ Modal, Ripple, Carousel, Input }, { allowReinits: true });

// Get the button
const mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button

const scrollFunction = () => {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.classList.remove("hidden");
  } else {
    mybutton.classList.add("hidden");
  }
};
const backToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

window.addEventListener("scroll", scrollFunction);
window.htmx = require("htmx.org");
htmx.config.defaultSwapStyle = "outerHTML";

import Sortable from "sortablejs";

htmx.onLoad(function (content) {
  var sortables = content.querySelectorAll(".sortable");
  for (var i = 0; i < sortables.length; i++) {
    var sortable = sortables[i];
    new Sortable(sortable, {
      animation: 150,
      ghostClass: "blue-background-class",
    });
  }
});
