import Alpine from "alpinejs";
import hljs from "highlight.js";
import javascript from "highlight.js/lib/languages/javascript";
import "highlight.js/styles/devibeans.css";
import "htmx.org";
import _hyperscript from "hyperscript.org";
import Sortable from "sortablejs";
import { Carousel, initTWE, Input, Modal, Ripple } from "tw-elements";

const htmx = require("htmx.org");
window.Alpine = Alpine;
window.htmx = htmx;

htmx.config.defaultSwapStyle = "outerHTML";
htmx.config.historyEnabled = true;
htmx.config.historyCacheSize = 10;
htmx.config.refreshOnHistoryMiss = true;
htmx.config.useTemplateFragments = true;

htmx.onLoad(function (content: { querySelectorAll: (arg0: string) => any }) {
  var sortables = content.querySelectorAll(".sortable");
  for (var i = 0; i < sortables.length; i++) {
    var sortable = sortables[i];
    new Sortable(sortable, {
      animation: 150,
      ghostClass: "blue-background-class",
    });
  }
});
Alpine.start();
_hyperscript.browserInit();

hljs.highlightAll();
hljs.registerLanguage("javascript", javascript);

initTWE({ Modal, Ripple, Carousel, Input }, { allowReinits: true });
