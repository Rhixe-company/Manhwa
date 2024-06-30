declare global {
  interface Window {
    Alpine: any;
  }
}

declare module "*.svg" {
  const content: any;
  export default content;
}

declare module "*.png" {
  const content: any;
  export default content;
}

declare module "svgmap";
