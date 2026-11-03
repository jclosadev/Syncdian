"""
Generador de iconos vectoriales monocromáticos y limpios estilo Flaticon / Lucide / Obsidian.
Sin emojis de móvil: líneas limpias y profesionales con cambio de color automático al activarse.
"""

from typing import Dict
from PySide6.QtCore import QByteArray, Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

SVG_PATHS: Dict[str, str] = {
    # Acerca De (Info / Círculo con usuario o 'i' sutil)
    "about": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="16" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12.01" y2="8"/>'
    ),
    # Dashboard / Estado (Panel de cuadrícula limpia)
    "dashboard": (
        '<rect width="7" height="9" x="3" y="3" rx="1"/>'
        '<rect width="7" height="5" x="14" y="3" rx="1"/>'
        '<rect width="7" height="9" x="14" y="12" rx="1"/>'
        '<rect width="7" height="5" x="3" y="16" rx="1"/>'
    ),
    # Bóvedas / Vaults (Carpeta de archivos limpia)
    "vaults": (
        '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>'
    ),
    # Programación / Reloj (Temporizador circular)
    "schedule": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="12 6 12 12 16 14"/>'
    ),
    # Google Drive (Nube)
    "gdrive": (
        '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>'
    ),
    # Historial / Registros (Lista de comprobación o documento)
    "history": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>'
        '<polyline points="10 9 9 9 8 9"/>'
    ),
    # Ajustes Generales (Deslizadores / Sliders)
    "settings": (
        '<line x1="4" x2="20" y1="21" y2="21"/>'
        '<line x1="4" x2="20" y1="3" y2="3"/>'
        '<line x1="4" x2="20" y1="12" y2="12"/>'
        '<circle cx="8" cy="12" r="2"/>'
        '<circle cx="16" cy="3" r="2"/>'
        '<circle cx="12" cy="21" r="2"/>'
    ),
    # Sincronización (Refresh / Sync)
    "sync": (
        '<path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
        '<path d="M3 3v5h5"/>'
        '<path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>'
        '<path d="M16 21h5v-5"/>'
    ),
    # Buscar (Lupa)
    "search": (
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    ),
    # Añadir (Plus)
    "plus": (
        '<line x1="12" y1="5" x2="12" y2="19"/>'
        '<line x1="5" y1="12" x2="19" y2="12"/>'
    ),
    # Eliminar (Papelera)
    "trash": (
        '<polyline points="3 6 5 6 21 6"/>'
        '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
    ),
    # Editar (Lápiz)
    "edit": (
        '<path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>'
    ),
    # Carpeta abierta
    "folder_open": (
        '<path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2"/>'
    )
}


def _render_svg_to_pixmap(paths: str, color: str, size: int = 18) -> QPixmap:
    svg_xml = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
         fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        {paths}
    </svg>
    """.strip()

    renderer = QSvgRenderer(QByteArray(svg_xml.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter)
    painter.end()

    return pixmap


def get_clean_icon(
    name: str,
    size: int = 18,
    color_normal: str = "#bfaea0",
    color_checked: str = "#16110d"
) -> QIcon:
    paths = SVG_PATHS.get(name, SVG_PATHS["about"])
    
    icon = QIcon()
    pix_normal = _render_svg_to_pixmap(paths, color_normal, size)
    pix_checked = _render_svg_to_pixmap(paths, color_checked, size)

    icon.addPixmap(pix_normal, QIcon.Normal, QIcon.Off)
    icon.addPixmap(pix_checked, QIcon.Normal, QIcon.On)
    icon.addPixmap(pix_normal, QIcon.Active, QIcon.Off)
    icon.addPixmap(pix_checked, QIcon.Active, QIcon.On)

    return icon
