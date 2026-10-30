"""Construit les deux versions dérivées de la présentation.

- Presentation_..._autonome.html : un seul fichier, images intégrées, vidéo intégrée (pour présenter en local).
- vibe-coding-cdtp.html (dossier donné en argument) : version pour le lien privé claude.ai,
  sans squelette HTML ; la vidéo y devient un lien, car l'Artifact ne peut pas intégrer d'autres sites.

Usage : python3 construire_versions.py <dossier_de_la_version_artifact>
"""
import base64
import re
import sys
from pathlib import Path

ICI = Path(__file__).parent
SOURCE = ICI / "index.html"
AUTONOME = ICI / "Presentation_Vibe_Coding_CdTp_20261030_autonome.html"


def integrer_images(texte):
    def remplacer(m):
        chemin = ICI / m.group(1)
        mime = "image/jpeg" if chemin.suffix == ".jpg" else "image/png"
        return 'src="data:%s;base64,%s"' % (mime, base64.b64encode(chemin.read_bytes()).decode())
    return re.sub(r'src="(assets/[^"]+)"', remplacer, texte)


texte = integrer_images(SOURCE.read_text())
AUTONOME.write_text(texte)

if len(sys.argv) > 1:
    art = texte
    for balise in ['<!doctype html>\n', '<html lang="fr">\n', '<head>\n', '<meta charset="utf-8">\n',
                   '<meta name="viewport" content="width=device-width, initial-scale=1">\n',
                   '</head>\n', '<body>\n', '</body>\n', '</html>\n']:
        art = art.replace(balise, '', 1)
    art = re.sub(r'\s*<iframe data-embed[^>]*></iframe>', '', art)
    art = art.replace('data-fallback hidden', 'data-fallback')
    (Path(sys.argv[1]) / "vibe-coding-cdtp.html").write_text(art)

print("Versions construites.")
