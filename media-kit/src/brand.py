"""Brand colours, sampled from the farm's logo."""

PALETTE = [
    {"key": "forest", "hex": "#1E3A1B", "name": {"fr": "Vert forêt", "en": "Forest green", "es": "Verde bosque"},
     "role": {"fr": "Couleur principale : texte du logo, dôme", "en": "Main colour: logo lettering, dome",
              "es": "Color principal: texto del logotipo, cúpula"}},
    {"key": "green", "hex": "#8A9A45", "name": {"fr": "Vert asperge", "en": "Asparagus green", "es": "Verde espárrago"},
     "role": {"fr": "Illustration, feuillage", "en": "Illustration, leaves", "es": "Ilustración, hojas"}},
    {"key": "light", "hex": "#C3C973", "name": {"fr": "Vert tendre", "en": "Fresh green", "es": "Verde tierno"},
     "role": {"fr": "Reflets, champs", "en": "Highlights, fields", "es": "Reflejos, campos"}},
    {"key": "gold", "hex": "#C9962F", "name": {"fr": "Or oignon", "en": "Onion gold", "es": "Oro cebolla"},
     "role": {"fr": "Accent : oignon, appels à l’action", "en": "Accent: onion, calls to action",
              "es": "Acento: cebolla, llamadas a la acción"}},
    {"key": "cream", "hex": "#F4F5EB", "name": {"fr": "Crème", "en": "Cream", "es": "Crema"},
     "role": {"fr": "Fond du logo", "en": "Logo background", "es": "Fondo del logotipo"}},
]


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
