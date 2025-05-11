# Agri Lacombe Website (`agrilacombe-website`)

## Purpose

This repository contains the source code and content for the official Agri Lacombe informational website. The website is built with [Astro](https://astro.build), [Tailwind CSS](https://tailwindcss.com), and [GSAP](https://greensock.com/gsap/) for a modern, responsive, and engaging user experience. It is designed for static deployment, for instance via GitHub Pages, serving as a public-facing platform to share our story, products, and commitment to sustainable agriculture.

(Refer to `plan.md`, Section III.B for the initial project plan details regarding this website.)

## Key Features & Content

The website provides a comprehensive overview of Agri Lacombe, with key features including:

*   **Modern Astro Architecture:** Leveraging Astro for optimal performance and developer experience.
*   **Multilingual Support (i18n):** Content available in English (default), French, and Spanish. Managed through Astro's content collections and JSON locale files.
*   **Responsive Design:** Fully responsive, mobile-first design achieved with Tailwind CSS.
*   **Engaging Animations:** Smooth animations and scroll-triggered effects powered by GSAP.
*   **Content Sections:**
    *   **Fixed Navbar:** For easy navigation.
    *   **Hero Section:** Welcoming visitors with an engaging tagline.
    *   **Our Commitments:** Highlighting core principles (Quality, Sustainability, Innovation).
    *   **Our Story:** Sharing the family heritage, mission, and vision.
    *   **Our Products:** Detailed descriptions of asparagus and Spanish onions.
    *   **Product Insights:** Informative articles on our crops.
    *   **Sustainability:** Outlining our commitment to environmentally sound farming.
    *   **Where to Buy:** Information on where to find Agri Lacombe produce.
    *   **FAQ:** Answers to common questions.
    *   **Contact Us:** For wholesale inquiries (simulated form).
    *   **Footer:** Basic information and copyright.
*   **SEO Friendly:** With meta tags and structured content.

## Technical Details

*   **Framework:** [Astro](https://astro.build)
*   **Styling:** [Tailwind CSS v3](https://tailwindcss.com) (integrated via `@astrojs/tailwind`)
*   **Animations:** [GSAP (GreenSock Animation Platform)](https://greensock.com/gsap/)
*   **Content Management:** [MDX](https://mdxjs.com/) for page content (`.mdx` files in `src/content/`)
*   **Internationalization (i18n):**
    *   Content collections per language in `src/content/`.
    *   UI strings managed via JSON files in `src/locales/`.
*   **Icons:** [Astro Icon](https://github.com/natemoo-re/astro-icon) for SVG icons.
*   **Deployment:** Static site generation (`output: 'static'` in Astro config).

## Directory Structure

```
agrilacombe-website/
├── public/                     # Static assets (images, CNAME, admin config)
│   ├── admin/
│   │   └── config.yml          # Decap CMS configuration (optional)
│   ├── images/                 # Site images, favicons, placeholders
│   └── CNAME                   # Custom domain for GitHub Pages
├── src/
│   ├── components/             # Reusable Astro/UI components (.astro)
│   ├── content/                # Content collections (MDX files per language)
│   │   ├── en/                 # English content
│   │   ├── es/                 # Spanish content
│   │   └── fr/                 # French content
│   │   └── config.ts           # Content collection schema definitions
│   ├── layouts/                # Base page layouts (.astro)
│   ├── locales/                # i18n JSON files (en.json, es.json, fr.json)
│   ├── pages/                  # Astro pages (dynamic routes for content)
│   ├── styles/                 # Global styles (global.css)
│   └── env.d.ts                # TypeScript definitions for Astro
├── .gitignore
├── astro.config.mjs            # Astro configuration file
├── package.json                # Project dependencies and scripts
├── tailwind.config.cjs         # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
├── LICENSE
└── README.md                   # This file
```
*(Note: The `index.html` file at the root of the repository is from a previous version and is not used by the Astro application.)*

## Getting Started / Development

Follow these steps to get the project running locally:

1.  **Prerequisites:**
    *   [Node.js](https://nodejs.org/) (LTS version recommended, e.g., v18 or v20)
    *   npm (comes with Node.js) or [pnpm](https://pnpm.io/) or [yarn](https://yarnpkg.com/)

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/<your-username>/agrilacombe-website.git
    cd agrilacombe-website
    ```

3.  **Install Dependencies:**
    ```bash
    npm install
    # or
    # pnpm install
    # or
    # yarn install
    ```

4.  **Run the Development Server:**
    ```bash
    npm run dev
    ```
    This will start the Astro development server, typically at `http://localhost:4321/`. The site will automatically reload when you make changes. By default, it redirects to the English version (`/en/`). You can access other languages directly (e.g., `http://localhost:4321/fr/`, `http://localhost:4321/es/`).

5.  **Build the Project:**
    To create a production build of the website:
    ```bash
    npm run build
    ```
    The static files will be generated in the `dist/` directory.

6.  **Preview the Build:**
    To preview the production build locally before deploying:
    ```bash
    npm run preview
    ```

## Deployment

This website is configured for static output and can be deployed to any static hosting provider. Here are instructions for GitHub Pages.

### 1. Configure Astro for GitHub Pages

Ensure your `astro.config.mjs` is set up correctly for your deployment target.
*   `output: 'static'` (already configured)
*   `site`: Set to your final domain (e.g., `https://www.agrilacombe.com`). This is crucial for sitemaps and canonical URLs. (Currently set to `https://www.agrilacombe.com`)
*   `base`: Set to `/` if deploying to the root of a custom domain. If deploying to a subdirectory like `<username>.github.io/<repo-name>/`, set `base: '/<repo-name>/'`. (Currently set to `/`)

The `CNAME` file (for custom domains) is placed in the `public/` directory and will be copied to the root of the `dist/` directory during the build process.

### 2. Deploying to GitHub Pages via GitHub Actions

This project is set up for automated deployment to GitHub Pages using GitHub Actions. A workflow file located at `.github/workflows/deploy-gh-pages.yml` handles the build and deployment process.

**How it Works:**
1.  **Trigger:** The workflow automatically runs whenever changes are pushed to the `main` branch.
2.  **Build:**
    *   It checks out your code.
    *   Sets up Node.js (version 20.x, as specified in the workflow).
    *   Installs project dependencies using `npm ci` (which uses `package-lock.json` for consistent builds).
    *   Builds the Astro site using `npm run build`. The Astro configuration (`astro.config.mjs`) is already set up for static output (`output: 'static'`), the correct `site` URL (`https://www.agrilacombe.com`), and `base: '/'`.
3.  **Deploy:**
    *   The contents of the generated `dist/` directory are then deployed to a special branch named `gh-pages`.
    *   The `CNAME` file (containing `www.agrilacombe.com`) located in your `public/` directory will be automatically included in the `dist/` folder by Astro's build process and deployed to the `gh-pages` branch, ensuring GitHub Pages uses your custom domain.

**Repository Settings for GitHub Pages:**

After the workflow runs for the first time and successfully creates the `gh-pages` branch:
1.  Go to your GitHub repository settings: **Settings → Pages**.
2.  Under "Build and deployment":
    *   For **Source**, select **Deploy from a branch**.
    *   For **Branch**, select `gh-pages` and the `/(root)` folder.
3.  Click **Save**.

GitHub will then serve your site from the `gh-pages` branch.

**Monitoring Deployments:**
You can monitor the status of your deployments in the "Actions" tab of your GitHub repository.

### 3. Adding a Custom Domain (e.g., `www.agrilacombe.com` from Namecheap)

The `CNAME` file in `public/` should contain `www.agrilacombe.com`. Astro will copy this to the `dist/` directory.

**A. In Your GitHub Repository (`agrilacombe-website`):**
   Ensure the `CNAME` file exists in your `public/` directory with your custom domain (e.g., `www.agrilacombe.com`). Astro will automatically copy this to the root of your `dist/` directory during the build, and the GitHub Actions workflow will deploy it to the `gh-pages` branch.

**B. In Your Namecheap Dashboard (or other DNS provider):**
   The DNS configuration remains largely the same as for any GitHub Pages site:

1.  **Select Your Domain:** Log in to Namecheap, go to your Domain List, and select `agrilacombe.com`.
2.  **Advanced DNS Tab:** Navigate to the "Advanced DNS" tab.
3.  **Remove Conflicting Records:** Delete any default Namecheap parking page records or conflicting `A` or `CNAME` records for `@` and `www`.
4.  **Add A Records (for Apex Domain - e.g., `agrilacombe.com` if you want it to point to `www.agrilacombe.com` or directly to GitHub Pages):**
    *   If you want `agrilacombe.com` to redirect to `www.agrilacombe.com`, Namecheap usually has a redirect feature.
    *   To point the apex domain directly to GitHub Pages (if your `CNAME` file contains `agrilacombe.com` instead of `www.agrilacombe.com`):
        *   Add `A` records for `Host = @` pointing to GitHub Pages' IP addresses:
            *   `185.199.108.153`
            *   `185.199.109.153`
            *   `185.199.110.153`
            *   `185.199.111.153`
5.  **Add CNAME Record (for `www` Subdomain - e.g., `www.agrilacombe.com`):**
    *   Type: `CNAME Record`
    *   Host: `www`
    *   Value: `<your-github-username-or-orgname>.github.io` (e.g., if your GitHub username is `agri-lacombe-farm`, this would be `agri-lacombe-farm.github.io`. **Do not include the repository name here when using a custom domain.**).
    *   TTL: Automatic (or 30 min).
6.  **Save All Changes.**

**C. Back in GitHub Pages Settings:**

1.  Go to your repository's **Settings → Pages**.
2.  **Custom Domain:**
    *   Under "Custom domain", type your custom domain (e.g., `www.agrilacombe.com`). This **must** match the content of your `CNAME` file.
    *   Click **Save**.
    *   GitHub will attempt to verify your domain settings. This may take some time.
3.  **Enforce HTTPS:**
    *   Once GitHub confirms your custom domain is set up correctly (you'll see a green checkmark or similar confirmation) and a TLS certificate has been issued (this is usually automatic), check the box for **Enforce HTTPS**. This is highly recommended.

**D. Wait for DNS Propagation:**
    DNS changes can take anywhere from a few minutes to 48 hours to propagate globally. After propagation, your custom domain `www.agrilacombe.com` should serve the content from the `gh-pages` branch of your Astro-built site.

## Making Updates

*   **Content:**
    *   Page content and frontmatter (metadata): Edit the `.mdx` files within `src/content/{lang}/` (e.g., `src/content/en/story.mdx`).
    *   UI text strings (e.g., button labels, static text in components): Edit the corresponding keys in the JSON files in `src/locales/` (e.g., `src/locales/en.json`).
*   **Structure & Layouts:**
    *   Overall page structure: Modify `.astro` files in `src/layouts/`.
    *   Routing and page generation logic (if any beyond content collections): Check `src/pages/`.
*   **Components:**
    *   Reusable UI elements: Modify or create `.astro` components in `src/components/`.
*   **Styling:**
    *   Apply or change Tailwind CSS utility classes directly in `.astro` or `.mdx` files.
    *   Global styles: Edit `src/styles/global.css`.
    *   Tailwind configuration (e.g., custom colors, fonts): Edit `tailwind.config.cjs`.
*   **Images:**
    *   Static images: Place in `public/images/` and reference them with a leading slash (e.g., `/images/my-photo.jpg`).
    *   For optimized images using `@astrojs/image`, consider placing source images in `src/assets/` and importing them into your Astro components or MDX files. (The current setup primarily uses `public/images/` for placeholders referenced in MDX frontmatter).
*   **Astro Configuration:** Modify `astro.config.mjs` for site-wide settings, integrations, etc.

After making changes:
1.  Commit and push your changes to the `main` branch.
2.  If using GitHub Actions, the deployment will typically trigger automatically.
3.  If deploying manually, run `npm run build` and redeploy the `dist/` directory.

## Licensing

The content and code in this repository are subject to the `LICENSE` file found herein. This license allows public viewing and forking for non-commercial, educational, or personal experimentation, but protects Agri Lacombe's branding, specific textual and visual content, and commercial interests. (Refer to `plan.md` Section III.B & III.G).