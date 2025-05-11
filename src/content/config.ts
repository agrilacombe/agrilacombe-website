// src/content/config.ts
import { defineCollection, z } from 'astro:content';

// Define a common schema for page frontmatter
const pageSchema = z.object({
  title: z.string(),
  description: z.string(),
  navTitle: z.string().optional(), // Optional shorter title for navigation menus
  // SEO related fields (optional)
  metaTitle: z.string().optional(), // For <title> tag if different from main title
  metaDescription: z.string().optional(), // For meta description tag if different
  // Specific fields for the homepage (index.mdx)
  hero: z.object({
    tagline: z.string(),
    subtitle: z.string(),
    buttonText: z.string(),
    buttonLink: z.string(), // e.g., "products" (relative to language base)
    backgroundImage: z.string().optional(), // Path to hero background image
  }).optional(),
  // Specific fields for the commitments section (could be in index.mdx or its own file)
  commitments: z.array(z.object({
    icon: z.string().optional(), // Placeholder for icon name or SVG path
    titleKey: z.string(), // Key for translated title, e.g., "commitments.quality.title"
    textKey: z.string(),   // Key for translated text, e.g., "commitments.quality.text"
  })).optional(),
   // Specific fields for product highlights (could be in index.mdx or products.mdx)
  product_highlights: z.array(z.object({
    image: z.string(), // Placeholder image path
    titleKey: z.string(),
    textKey: z.string(),
    availabilityKey: z.string().optional(),
  })).optional(),
  // Specific fields for product insights (could be in index.mdx or individual insight files)
  product_insights: z.array(z.object({
    image: z.string(),
    titleKey: z.string(),
    contentKey: z.string(), // Could be a key to a larger block of text, or content is in body
    sections: z.array(z.object({
        titleKey: z.string(),
        listKey: z.string().optional(), // for bullet points, key prefix
        paragraphKey: z.string().optional() // for text block
    })).optional(),
  })).optional(),
  // Specific fields for FAQ page
  faq_items: z.array(z.object({
    questionKey: z.string(),
    answerKey: z.string(),
  })).optional(),
});

// Define collections for each language
const enCollection = defineCollection({
  type: 'content',
  schema: pageSchema,
});

const esCollection = defineCollection({
  type: 'content',
  schema: pageSchema,
});

const frCollection = defineCollection({
  type: 'content',
  schema: pageSchema,
});

export const collections = {
  'en': enCollection,
  'es': esCollection,
  'fr': frCollection,
};
