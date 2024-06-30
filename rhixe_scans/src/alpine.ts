declare global {
  interface Window {
    Alpine: any;
  }
}

import Alpine from "alpinejs";
import _hyperscript from "hyperscript.org";

window.Alpine = Alpine;

Alpine.start();
_hyperscript.browserInit();
import "./modules";

import hljs from "highlight.js";
import javascript from "highlight.js/lib/languages/javascript";
import "highlight.js/styles/devibeans.css";
hljs.highlightAll();
hljs.registerLanguage("javascript", javascript);
