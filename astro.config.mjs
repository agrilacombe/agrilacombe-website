// astro.config.mjs
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  integrations: [
    mdx(), // Add MDX integration, preferably early
    sitemap({
      // Configuration for sitemap
      i18n: {
        defaultLocale: 'fr',
        locales: {
          en: 'en',
          es: 'es',
          fr: 'fr',
        },
      },
      // Exclude admin pages if any
      // Exclude admin pages and the /media/ short-link redirect
      filter: (page) => !page.includes('/admin/') && new URL(page).pathname !== '/media/',
      // Change frequency and priority can be adjusted as needed
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
    }),
  ],
  // Configure for custom domain
  site: `https://www.agrilacombe.com`, // Your custom domain
  base: `/`, // Site will be at the root of the custom domain
  output: "static", // Ensures static build for GitHub Pages
  trailingSlash: "always", // Or 'always', depending on preference
  // Root URL handled by custom index.astro with instant redirect to French version
});
