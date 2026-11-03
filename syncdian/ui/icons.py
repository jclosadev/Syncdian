"""
Generador de iconos vectoriales monocromáticos y limpios estilo Flaticon / Lucide / Obsidian.
Sin emojis: líneas finas, profesionales y con cambio de color automático al activarse.

Los iconos se dibujan a partir de trazados SVG para poder recolorearlos en tiempo real
y mantener una apariencia nítida en cualquier escala de pantalla.
"""

import hashlib
import tempfile
from pathlib import Path
from typing import Dict

from PySide6.QtCore import QByteArray, QRectF, Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

# Paleta usada por la interfaz (coincide con theme.py)
ICON_COLOR = "#c9bba9"
ICON_COLOR_ACTIVE = "#241a09"

SVG_PATHS: Dict[str, str] = {
    # Acerca de (información)
    "about": (
        '<circle cx="12" cy="12" r="9.25"/>'
        '<line x1="12" y1="11" x2="12" y2="16.5"/>'
        '<line x1="12" y1="7.75" x2="12.01" y2="7.75"/>'
    ),
    # Panel / Estado (cuadrícula)
    "dashboard": (
        '<rect width="7" height="7" x="3" y="3" rx="1.5"/>'
        '<rect width="7" height="7" x="14" y="3" rx="1.5"/>'
        '<rect width="7" height="7" x="3" y="14" rx="1.5"/>'
        '<rect width="7" height="7" x="14" y="14" rx="1.5"/>'
    ),
    # Bóvedas (carpeta)
    "vaults": (
        '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>'
    ),
    # Programación (reloj)
    "schedule": (
        '<circle cx="12" cy="12" r="9.25"/>'
        '<polyline points="12 7 12 12 15.5 14"/>'
    ),
    # Google Drive (nube)
    "gdrive": (
        '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>'
    ),
    # Historial (documento con líneas)
    "history": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>'
    ),
    # Ajustes (deslizadores)
    "settings": (
        '<line x1="4" x2="20" y1="5" y2="5"/>'
        '<line x1="4" x2="20" y1="12" y2="12"/>'
        '<line x1="4" x2="20" y1="19" y2="19"/>'
        '<circle cx="9" cy="5" r="2.1"/>'
        '<circle cx="15" cy="12" r="2.1"/>'
        '<circle cx="8" cy="19" r="2.1"/>'
    ),
    # Sincronizar (flechas circulares)
    "sync": (
        '<path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
        '<path d="M3 3v5h5"/>'
        '<path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>'
        '<path d="M16 21h5v-5"/>'
    ),
    # Buscar (lupa)
    "search": (
        '<circle cx="11" cy="11" r="7.25"/>'
        '<line x1="20.5" y1="20.5" x2="16.2" y2="16.2"/>'
    ),
    # Añadir (más)
    "plus": (
        '<line x1="12" y1="5" x2="12" y2="19"/>'
        '<line x1="5" y1="12" x2="19" y2="12"/>'
    ),
    # Eliminar (papelera)
    "trash": (
        '<polyline points="3 6 5 6 21 6"/>'
        '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>'
        '<path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
        '<line x1="10" y1="11" x2="10" y2="17"/>'
        '<line x1="14" y1="11" x2="14" y2="17"/>'
    ),
    # Editar (lápiz)
    "edit": (
        '<path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>'
    ),
    # Carpeta abierta
    "folder_open": (
        '<path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2"/>'
    ),
    # Guardar (disquete)
    "save": (
        '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>'
        '<polyline points="17 21 17 13 7 13 7 21"/>'
        '<polyline points="7 3 7 8 15 8"/>'
    ),
    # Descargar
    "download": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" y1="15" x2="12" y2="3"/>'
    ),
    # Subir
    "upload": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="17 8 12 3 7 8"/>'
        '<line x1="12" y1="3" x2="12" y2="15"/>'
    ),
    # Enlace
    "link": (
        '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>'
        '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>'
    ),
    # Desconectar
    "unplug": (
        '<path d="M19 5 5 19"/>'
        '<path d="M6.5 6.5 3 10l3 3 3.5-3.5"/>'
        '<path d="M17.5 17.5 21 14l-3-3-3.5 3.5"/>'
    ),
    # Comprobado
    "check": (
        '<polyline points="20 6 9 17 4 12"/>'
    ),
    # Chevron hacia abajo
    "chevron_down": (
        '<polyline points="6 9 12 15 18 9"/>'
    ),
    # Chevron hacia arriba
    "chevron_up": (
        '<polyline points="6 15 12 9 18 15"/>'
    ),
    # Chevron doble (selector)
    "chevrons_updown": (
        '<polyline points="7 15 12 20 17 15"/>'
        '<polyline points="7 9 12 4 17 9"/>'
    ),
    # Globo / idioma
    "globe": (
        '<circle cx="12" cy="12" r="9.25"/>'
        '<line x1="3" y1="12" x2="21" y2="12"/>'
        '<path d="M12 2.75a14.5 14.5 0 0 1 0 18.5 14.5 14.5 0 0 1 0-18.5Z"/>'
    ),
    # Escudo / seguridad
    "shield": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        '<polyline points="9 12 11 14 15 10"/>'
    ),
    # Almacenamiento
    "storage": (
        '<ellipse cx="12" cy="5" rx="8" ry="3"/>'
        '<path d="M4 5v14c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/>'
        '<path d="M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3"/>'
    ),
    # Campana / notificaciones
    "bell": (
        '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>'
        '<path d="M13.73 21a2 2 0 0 1-3.46 0"/>'
    ),
    # Ventana minimizada
    "minimize": (
        '<line x1="5" y1="12" x2="19" y2="12"/>'
    ),
    # Enlace externo
    "external_link": (
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
        '<polyline points="15 3 21 3 21 9"/>'
        '<line x1="10" y1="14" x2="21" y2="3"/>'
    ),
    # Cerrar
    "x": (
        '<line x1="18" y1="6" x2="6" y2="18"/>'
        '<line x1="6" y1="6" x2="18" y2="18"/>'
    ),
}

_ICON_CACHE_DIR = Path(tempfile.gettempdir()) / "syncdian_icons"


def _build_svg(name: str, color: str, size: int = 18, stroke_width: float = 1.8) -> str:
    paths = SVG_PATHS.get(name, SVG_PATHS["about"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'
    )


def svg_file(name: str, color: str, size: int = 16, stroke_width: float = 1.8) -> str:
    """Devuelve una ruta de archivo SVG reutilizable por las hojas de estilo Qt."""
    digest = hashlib.md5(f"{name}|{color}|{size}|{stroke_width}".encode("utf-8")).hexdigest()[:10]
    try:
        _ICON_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        path = _ICON_CACHE_DIR / f"{name}_{digest}.svg"
        if not path.exists():
            path.write_text(_build_svg(name, color, size, stroke_width), encoding="utf-8")
        return path.as_posix()
    except Exception:
        # Si no se puede escribir en temp, se devuelve una ruta inexistente:
        # Qt simplemente no mostrará la imagen, sin romper la aplicación.
        return ""


def _render_svg_to_pixmap(paths: str, color: str, size: int = 18) -> QPixmap:
    svg_xml = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        f"{paths}</svg>"
    )

    renderer = QSvgRenderer(QByteArray(svg_xml.encode("utf-8")))
    scale = 2
    pixmap = QPixmap(size * scale, size * scale)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter, QRectF(0, 0, size * scale, size * scale))
    painter.end()

    pixmap.setDevicePixelRatio(scale)
    return pixmap


def get_clean_icon(
    name: str,
    size: int = 18,
    color_normal: str = ICON_COLOR,
    color_checked: str = ICON_COLOR_ACTIVE,
) -> QIcon:
    """Icono con estado normal y activo (para botones seleccionables)."""
    paths = SVG_PATHS.get(name, SVG_PATHS["about"])

    icon = QIcon()
    pix_normal = _render_svg_to_pixmap(paths, color_normal, size)
    pix_checked = _render_svg_to_pixmap(paths, color_checked, size)

    icon.addPixmap(pix_normal, QIcon.Normal, QIcon.Off)
    icon.addPixmap(pix_checked, QIcon.Normal, QIcon.On)
    icon.addPixmap(pix_normal, QIcon.Active, QIcon.Off)
    icon.addPixmap(pix_checked, QIcon.Active, QIcon.On)
    icon.addPixmap(pix_normal, QIcon.Disabled, QIcon.Off)
    icon.addPixmap(pix_normal, QIcon.Disabled, QIcon.On)

    return icon


def get_icon(name: str, size: int = 16, color: str = ICON_COLOR) -> QIcon:
    """Icono simple de un solo color para botones de acción."""
    paths = SVG_PATHS.get(name, SVG_PATHS["about"])
    icon = QIcon()
    pixmap = _render_svg_to_pixmap(paths, color, size)
    icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
    icon.addPixmap(pixmap, QIcon.Active, QIcon.Off)
    icon.addPixmap(pixmap, QIcon.Disabled, QIcon.Off)
    return icon


def icon_size(size: int = 16) -> QSize:
    return QSize(size, size)
