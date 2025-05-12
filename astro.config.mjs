// astro.config.mjs
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwind from "@astrojs/tailwind";
import icon from "astro-icon";

export default defineConfig({
  integrations: [
    mdx(), // Add MDX integration, preferably early
    tailwind(),
    icon({
      // Example: include Tabler Icons if you plan to use them
      // You can specify icon packs and individual icons to optimize build size
      include: {
        tabler: ["menu-2", "x", "star", "leaf", "bulb", "users"], // For hamburger menu and commitment icons
      },
    }),
  ],
  // Configure for custom domain
  site: `https://www.agrilacombe.com`, // Your custom domain
  base: `/`, // Site will be at the root of the custom domain
  output: "static", // Ensures static build for GitHub Pages
  trailingSlash: "always", // Or 'always', depending on preference
  // Redirect root to French version by default
  redirects: {
    "/": "/fr/",
  },
});
