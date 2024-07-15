const aside = document.getElementById("sidebar") as HTMLElement;

if (aside) {
  const toggleSidebarMobile = (aside: HTMLElement, sidebarBackdrop: HTMLElement, toggleSidebarMobileHamburger: HTMLElement, toggleSidebarMobileClose: HTMLElement) => {
    aside.classList.add("flex");
    aside.classList.toggle("hidden");
    sidebarBackdrop.classList.toggle("hidden");
    toggleSidebarMobileHamburger.classList.toggle("hidden");
    toggleSidebarMobileClose.classList.toggle("hidden");
  };
  const toggleSidebarMobileEl = document.getElementById("toggleSidebarMobile") as HTMLElement;
  const sidebarBackdrop = document.getElementById("sidebarBackdrop") as HTMLElement;
  const toggleSidebarMobileHamburger = document.getElementById("toggleSidebarMobileHamburger") as HTMLElement;
  const toggleSidebarMobileClose = document.getElementById("toggleSidebarMobileClose") as HTMLElement;
  const toggleSidebarMobileSearch = document.getElementById("toggleSidebarMobileSearch") as HTMLElement;
  toggleSidebarMobileSearch.addEventListener("click", () => {
    toggleSidebarMobile(aside, sidebarBackdrop, toggleSidebarMobileHamburger, toggleSidebarMobileClose);
  });

  toggleSidebarMobileEl.addEventListener("click", () => {
    toggleSidebarMobile(aside, sidebarBackdrop, toggleSidebarMobileHamburger, toggleSidebarMobileClose);
  });

  sidebarBackdrop.addEventListener("click", () => {
    toggleSidebarMobile(aside, sidebarBackdrop, toggleSidebarMobileHamburger, toggleSidebarMobileClose);
  });
}
