# Media kit (trousse média)

Source for the downloadable media kit at `/fr/media/`, `/en/media/`, `/es/media/`.
`/media/` is a short link that redirects to the French page.

| What | Where |
|:--|:--|
| The farm's logo (used as-is, never redrawn) | `public/images/agrilacombe_logo.png` |
| Transparent and black-and-white versions of it | `media-kit/src/logo_files.py` |
| Logo colours (sampled from the logo) | `media-kit/src/brand.py` |
| All texts, contact details, seasons (FR/EN/ES) | `src/data/media-kit.json` |
| Web page | `src/pages/[lang]/media.astro` |
| Generated files (committed, deployed as-is) | `public/media-kit/`, `src/data/media-kit-files.json` |

## Rebuild

After changing the logo file or any text, regenerate everything:

```bash
uv run --no-project --with fonttools --with pillow --with numpy --with scipy python media-kit/build.py
```

Needs Google Chrome, `pdftoppm` (poppler-utils), and the Montserrat and Inter fonts
installed locally.

The build produces the three logo PNGs, the fact sheets (FR/EN), the "Produit local"
store sign, the brand guide, the Facebook cover image, the plain-text descriptions,
and a ZIP of all of it.
