const datetime = new Date().getFullYear();
const dateElement = document.getElementById("footer-date") as HTMLBodyElement;

dateElement.textContent = `${datetime}`;
