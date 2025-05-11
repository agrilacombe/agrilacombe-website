// src/utils/i18n.ts
import enStrings from '../locales/en.json';
import esStrings from '../locales/es.json';
import frStrings from '../locales/fr.json';

export type Language = 'en' | 'es' | 'fr';

const translations: Record<Language, Record<string, string>> = {
  en: enStrings,
  es: esStrings,
  fr: frStrings,
};

/**
 * Translates a key to the specified language.
 * Falls back to English if the key is not found in the target language,
 * then falls back to the key itself if not found in English.
 * @param key The translation key (e.g., "nav.home")
 * @param lang The target language ('en', 'es', 'fr')
 * @returns The translated string
 */
export function t(key: string, lang: Language): string {
  return translations[lang]?.[key] || translations['en']?.[key] || key;
}

/**
 * Generates the base path for a given language.
 * English ('en') is considered the default and resides at the root of the `site.base`.
 * Other languages are prefixed (e.g., /es/, /fr/).
 * @param lang The target language
 * @param siteBase The base path of the site from Astro.config (e.g., /repo-name or /)
 * @returns The language-specific base path (e.g., /repo-name/ or /repo-name/es/)
 */
export function getLangBase(lang: Language, siteBase: string): string {
  // Normalize siteBase: if it's more than just "/", remove trailing slash. If it's "/", treat as empty for prefixing.
  const normalizedSiteBase = siteBase === '/' ? '' : (siteBase.endsWith('/') ? siteBase.slice(0, -1) : siteBase);
  // Due to redirects: { "/": "/en/" }, English content is also under a lang prefix.
  return `${normalizedSiteBase}/${lang}/`; // Results in /en/, /es/, /fr/ or /repo-name/en/, etc.
}

/**
 * Creates a localized path for navigation.
 * @param relativePath The path relative to the language root (e.g., "story" or "products/asparagus")
 * @param targetLang The language for the new path
 * @param siteBase The base path of the site from Astro.config
 * @returns The fully qualified localized path
 */
export function createLocalizedPath(relativePath: string, targetLang: Language, siteBase: string): string {
  const langBase = getLangBase(targetLang, siteBase); // e.g., /en/ or /repo/en/
  // Ensure relativePath doesn't start with a slash if langBase already ends with one
  const cleanRelativePath = relativePath.startsWith('/') ? relativePath.substring(1) : relativePath;
  
  let finalPath = `${langBase}${cleanRelativePath}`;
  
  // Ensure trailing slash if relativePath was not empty and finalPath doesn't have one,
  // or if relativePath was empty (meaning root of language, which getLangBase handles)
  // Astro's trailingSlash: "always" will handle this at the end, but good to be consistent.
  if (cleanRelativePath !== '' && !finalPath.endsWith('/')) {
    finalPath += '/';
  }
  // If relativePath is empty, langBase from getLangBase already ends with a slash.
  
  return finalPath;
}


/**
 * Constructs a localized path for switching languages, attempting to preserve the current page context.
 * @param currentPath The current absolute path (Astro.url.pathname)
 * @param targetLang The language to switch to
 * @param currentLang The current language
 * @param siteBase The base path of the site from Astro.config (Astro.config.base)
 * @returns The new localized path
 */
export function getLocalizedPathForSwitcher(currentPath: string, targetLang: Language, currentLang: Language, siteBase: string): string {
  const currentActualLangBase = getLangBase(currentLang, siteBase); // e.g., /en/ or /repo/en/
  const targetActualLangBase = getLangBase(targetLang, siteBase);   // e.g., /es/ or /repo/es/

  let pageSlug = '';

  if (currentPath.startsWith(currentActualLangBase)) {
    pageSlug = currentPath.substring(currentActualLangBase.length); // e.g., "products/" or "" (includes trailing slash if present)
  } else {
    // This case might occur if currentPath is the site root before Astro's redirect to /en/
    // or if siteBase itself is complex and not handled by getLangBase as expected for `currentPath`.
    // Given the redirect "/": "/en/", currentPath for English homepage should be /en/ (or siteBase + /en/).
    // If it's truly the root path '/' and currentLang is 'en', the slug is effectively empty.
    const normalizedSiteRoot = siteBase.endsWith('/') ? siteBase : `${siteBase}/`;
    if (currentLang === 'en' && currentPath === normalizedSiteRoot) {
      pageSlug = ''; // English root page slug is empty
    } else {
      console.warn(`[i18n] Path switcher issue: currentPath "${currentPath}" did not start with expected base "${currentActualLangBase}" for lang "${currentLang}". Defaulting to target language root.`);
      return targetActualLangBase; // Fallback to the root of the target language
    }
  }

  // `pageSlug` should now be like "products/" or "" or "some/page/"
  // It will retain a trailing slash if currentPath had one after the language base.
  // `targetActualLangBase` already ends with a slash.
  const newPath = `${targetActualLangBase}${pageSlug}`;

  // Astro's trailingSlash: "always" means all generated URLs should end with a slash.
  // `getLangBase` ensures its output ends with a slash.
  // If `pageSlug` is empty, `newPath` correctly ends with a slash (e.g., /es/).
  // If `pageSlug` is not empty (e.g. "products/"), `newPath` is /es/products/, which is correct.
  // No need for further slash manipulation if `pageSlug` correctly captures the trailing slash from `currentPath`.

  return newPath;
}