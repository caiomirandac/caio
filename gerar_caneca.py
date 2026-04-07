import cairosvg
from PIL import Image, ImageDraw, ImageFont
import io, os

# SVG completo da caneca — frente + lateral + especificações
SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="560" viewBox="0 0 900 560"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">

  <defs>
    <!-- fundo escuro -->
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e1e1e"/>
      <stop offset="100%" stop-color="#141414"/>
    </linearGradient>

    <!-- corpo caneca frontal -->
    <linearGradient id="bodyF" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#d8d8d8"/>
      <stop offset="12%"  stop-color="#ffffff"/>
      <stop offset="88%"  stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#c4c4c4"/>
    </linearGradient>

    <!-- corpo caneca lateral -->
    <linearGradient id="bodyS" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#cccccc"/>
      <stop offset="25%"  stop-color="#f5f5f5"/>
      <stop offset="75%"  stop-color="#f5f5f5"/>
      <stop offset="100%" stop-color="#bbbbbb"/>
    </linearGradient>

    <!-- rim -->
    <linearGradient id="rimG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#aaaaaa"/>
      <stop offset="50%"  stop-color="#f0f0f0"/>
      <stop offset="100%" stop-color="#999999"/>
    </linearGradient>

    <!-- base -->
    <linearGradient id="baseG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#d0d0d0"/>
      <stop offset="100%" stop-color="#aaaaaa"/>
    </linearGradient>

    <!-- sombra suave nas canecas -->
    <filter id="dropShadow" x="-20%" y="-10%" width="150%" height="130%">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000000" flood-opacity="0.55"/>
    </filter>
  </defs>

  <!-- ══════════════════ FUNDO ══════════════════ -->
  <rect width="900" height="560" fill="url(#bg)"/>

  <!-- linha decorativa topo vermelha -->
  <rect x="0" y="0" width="900" height="3" fill="#C8102E" opacity="0.7"/>

  <!-- título -->
  <text x="450" y="38" font-family="Georgia,serif" font-size="11" fill="#555"
        letter-spacing="5" text-anchor="middle" text-transform="uppercase">
    CLEVERSON · FLAMENGO EDITION · DESIGN PREVIEW
  </text>

  <!-- ══════════════════════════════════════════
       CANECA 1 — VISTA FRONTAL
  ══════════════════════════════════════════ -->
  <g transform="translate(90, 60)" filter="url(#dropShadow)">

    <!-- corpo -->
    <path d="M20,22 Q20,16 30,16 L220,16 Q230,16 230,22 L238,296 Q238,305 228,305 L22,305 Q12,305 12,296 Z"
          fill="url(#bodyF)" stroke="#c0c0c0" stroke-width="0.6"/>

    <!-- elipse topo -->
    <ellipse cx="125" cy="18" rx="106" ry="13" fill="url(#rimG)" stroke="#b0b0b0" stroke-width="0.5"/>
    <ellipse cx="125" cy="18" rx="94"  ry="9"  fill="#dddddd"/>
    <ellipse cx="125" cy="20" rx="92"  ry="7"  fill="#cccccc"/>

    <!-- base -->
    <ellipse cx="125" cy="303" rx="114" ry="9" fill="url(#baseG)" stroke="#b0b0b0" stroke-width="0.5"/>

    <!-- ── DESIGN IMPRESSO ── -->

    <!-- linha vermelha superior -->
    <line x1="38" y1="112" x2="210" y2="112" stroke="#C8102E" stroke-width="1.4"/>

    <!-- nome CLEVERSON -->
    <text x="124" y="158"
          font-family="Impact,Arial Black,sans-serif"
          font-size="38"
          font-weight="900"
          fill="#0A0A0A"
          letter-spacing="6"
          text-anchor="middle">CLEVERSON</text>

    <!-- linha vermelha inferior -->
    <line x1="38" y1="172" x2="210" y2="172" stroke="#C8102E" stroke-width="1.4"/>

    <!-- slogan -->
    <text x="44" y="196"
          font-family="Georgia,serif"
          font-style="italic"
          font-size="12"
          fill="#3A3A3A"
          letter-spacing="0.8">uma vez flamengo,</text>
    <text x="44" y="213"
          font-family="Georgia,serif"
          font-style="italic"
          font-size="12"
          fill="#3A3A3A"
          letter-spacing="0.8">sempre flamengo.</text>

    <!-- ── cabo ── -->
    <path d="M232,88 Q285,88 285,152 Q285,216 232,216"
          fill="none" stroke="#cccccc" stroke-width="20" stroke-linecap="round"/>
    <path d="M232,88 Q272,88 272,152 Q272,216 232,216"
          fill="none" stroke="#eeeeee" stroke-width="9" stroke-linecap="round"/>

    <!-- reflexos -->
    <path d="M34,28 Q31,165 36,290" stroke="rgba(255,255,255,0.65)" stroke-width="4"
          fill="none" stroke-linecap="round"/>
    <path d="M90,22 Q87,165 92,295" stroke="rgba(255,255,255,0.2)" stroke-width="7"
          fill="none" stroke-linecap="round"/>
  </g>

  <!-- label vista frontal -->
  <text x="215" y="398" font-family="Arial,sans-serif" font-size="9" fill="#444"
        letter-spacing="3" text-anchor="middle">VISTA FRONTAL</text>

  <!-- ══════════════════════════════════════════
       CANECA 2 — VISTA LATERAL
  ══════════════════════════════════════════ -->
  <g transform="translate(480, 80)" filter="url(#dropShadow)">

    <!-- corpo mais estreito (vista lateral) -->
    <path d="M15,18 Q15,12 24,12 L175,12 Q184,12 184,18 L190,280 Q190,288 181,288 L19,288 Q10,288 10,280 Z"
          fill="url(#bodyS)" stroke="#c0c0c0" stroke-width="0.6"/>

    <!-- topo -->
    <ellipse cx="100" cy="14" rx="86" ry="10" fill="url(#rimG)" stroke="#b0b0b0" stroke-width="0.5"/>
    <ellipse cx="100" cy="14" rx="76"  ry="7"  fill="#dddddd"/>
    <ellipse cx="100" cy="16" rx="74"  ry="5"  fill="#cccccc"/>

    <!-- base -->
    <ellipse cx="100" cy="287" rx="90" ry="8" fill="url(#baseG)" stroke="#b0b0b0" stroke-width="0.5"/>

    <!-- ── "sogrão" ── -->
    <line x1="68" y1="264" x2="132" y2="264" stroke="#dedede" stroke-width="0.6"/>
    <text x="100" y="278"
          font-family="Arial,Helvetica,sans-serif"
          font-weight="300"
          font-size="8.5"
          fill="#999999"
          letter-spacing="3"
          text-anchor="middle">sogrão</text>

    <!-- cabo lateral -->
    <path d="M184,78 Q228,78 228,138 Q228,198 184,198"
          fill="none" stroke="#cccccc" stroke-width="17" stroke-linecap="round"/>
    <path d="M184,78 Q218,78 218,138 Q218,198 184,198"
          fill="none" stroke="#eeeeee" stroke-width="8" stroke-linecap="round"/>

    <!-- reflexo -->
    <path d="M27,24 Q25,150 29,275" stroke="rgba(255,255,255,0.6)" stroke-width="3"
          fill="none" stroke-linecap="round"/>
  </g>

  <!-- label vista lateral -->
  <text x="608" y="398" font-family="Arial,sans-serif" font-size="9" fill="#444"
        letter-spacing="3" text-anchor="middle">VISTA LATERAL · "sogrão"</text>

  <!-- ══════════════════════════════════════════
       PAINEL DE SPECS (rodapé)
  ══════════════════════════════════════════ -->

  <!-- linha divisória -->
  <line x1="60" y1="420" x2="840" y2="420" stroke="#2a2a2a" stroke-width="1"/>

  <!-- TIPOGRAFIA -->
  <text x="100" y="445" font-family="Arial,sans-serif" font-size="8" fill="#C8102E" letter-spacing="3">TIPOGRAFIA</text>
  <text x="100" y="462" font-family="Arial,sans-serif" font-size="10" fill="#555">Nome · Impact / Barlow Condensed ExtraBold</text>
  <text x="100" y="477" font-family="Arial,sans-serif" font-size="10" fill="#555">Slogan · Cormorant Garamond Light Italic</text>
  <text x="100" y="492" font-family="Arial,sans-serif" font-size="10" fill="#555">Sogrão · Inter Light · 8pt</text>

  <!-- PALETA -->
  <text x="370" y="445" font-family="Arial,sans-serif" font-size="8" fill="#C8102E" letter-spacing="3">PALETA</text>
  <circle cx="375" cy="462" r="8" fill="#0A0A0A"/>
  <circle cx="398" cy="462" r="8" fill="#C8102E"/>
  <circle cx="421" cy="462" r="8" fill="#3A3A3A"/>
  <circle cx="444" cy="462" r="8" fill="#999999"/>
  <circle cx="467" cy="462" r="8" fill="#FFFFFF" stroke="#333" stroke-width="0.8"/>
  <text x="375" y="483" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#0A0A0A</text>
  <text x="398" y="483" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#C8102E</text>
  <text x="421" y="483" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#3A3A3A</text>
  <text x="444" y="483" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#999999</text>
  <text x="467" y="483" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#FFFFFF</text>

  <!-- HIERARQUIA -->
  <text x="570" y="445" font-family="Arial,sans-serif" font-size="8" fill="#C8102E" letter-spacing="3">HIERARQUIA VISUAL</text>
  <text x="570" y="462" font-family="Arial,sans-serif" font-size="10" fill="#555">1 · CLEVERSON — impacto imediato</text>
  <text x="570" y="477" font-family="Arial,sans-serif" font-size="10" fill="#555">2 · Linhas vermelhas — identidade esportiva</text>
  <text x="570" y="492" font-family="Arial,sans-serif" font-size="10" fill="#555">3 · Slogan → 4 · sogrão (easter egg)</text>

  <!-- linha decorativa base vermelha -->
  <rect x="0" y="557" width="900" height="3" fill="#C8102E" opacity="0.5"/>

</svg>"""

# Renderizar SVG → PNG
png_bytes = cairosvg.svg2png(bytestring=SVG.encode(), output_width=1800, output_height=1120)

out_path = "/home/user/caio/caneca-preview.png"
with open(out_path, "wb") as f:
    f.write(png_bytes)

print(f"Imagem gerada: {out_path} ({len(png_bytes)//1024} KB)")
