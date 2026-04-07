import cairosvg

SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="600" viewBox="0 0 1000 600"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- fundo -->
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1c1c1c"/>
      <stop offset="100%" stop-color="#111111"/>
    </linearGradient>

    <!-- corpo frontal -->
    <linearGradient id="bodyF" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#d2d2d2"/>
      <stop offset="10%"  stop-color="#fafafa"/>
      <stop offset="88%"  stop-color="#fafafa"/>
      <stop offset="100%" stop-color="#c0c0c0"/>
    </linearGradient>

    <!-- corpo lateral -->
    <linearGradient id="bodyS" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#c8c8c8"/>
      <stop offset="20%"  stop-color="#f5f5f5"/>
      <stop offset="80%"  stop-color="#f5f5f5"/>
      <stop offset="100%" stop-color="#b8b8b8"/>
    </linearGradient>

    <!-- rim / borda -->
    <linearGradient id="rimG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#aaaaaa"/>
      <stop offset="50%"  stop-color="#eeeeee"/>
      <stop offset="100%" stop-color="#999999"/>
    </linearGradient>

    <!-- base -->
    <linearGradient id="baseG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#cccccc"/>
      <stop offset="100%" stop-color="#aaaaaa"/>
    </linearGradient>

    <!-- cabo -->
    <linearGradient id="canoG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#bbbbbb"/>
      <stop offset="60%"  stop-color="#e8e8e8"/>
      <stop offset="100%" stop-color="#b0b0b0"/>
    </linearGradient>

    <filter id="sombra" x="-30%" y="-15%" width="180%" height="150%">
      <feDropShadow dx="0" dy="20" stdDeviation="28" flood-color="#000" flood-opacity="0.6"/>
    </filter>

    <filter id="sombraLeve" x="-30%" y="-15%" width="180%" height="150%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000" flood-opacity="0.45"/>
    </filter>
  </defs>

  <!-- ── FUNDO ── -->
  <rect width="1000" height="600" fill="url(#bg)"/>
  <!-- faixa vermelha topo -->
  <rect x="0" y="0" width="1000" height="2.5" fill="#C8102E" opacity="0.8"/>
  <!-- faixa vermelha base -->
  <rect x="0" y="597.5" width="1000" height="2.5" fill="#C8102E" opacity="0.4"/>

  <!-- título do preview -->
  <text x="500" y="36" font-family="Arial,sans-serif" font-size="10"
        fill="#444" letter-spacing="5" text-anchor="middle">
    CLEVERSON · FLAMENGO EDITION · DESIGN PREVIEW
  </text>

  <!-- ════════════════════════════════════════
       CANECA FRONTAL  (cx ≈ 280)
  ════════════════════════════════════════ -->
  <g transform="translate(100, 58)" filter="url(#sombra)">

    <!-- corpo trapezoidal slim (levemente cônico) -->
    <path d="M 28,20
             Q 28,13  38,13
             L 302,13
             Q 312,13  312,20
             L 320,342
             Q 320,352  310,352
             L 30,352
             Q 20,352  20,342 Z"
          fill="url(#bodyF)" stroke="#bbbbbb" stroke-width="0.7"/>

    <!-- elipse boca topo -->
    <ellipse cx="170" cy="15"  rx="143" ry="15" fill="url(#rimG)" stroke="#b0b0b0" stroke-width="0.6"/>
    <ellipse cx="170" cy="15"  rx="128" ry="10" fill="#e0e0e0"/>
    <ellipse cx="170" cy="17"  rx="125" ry="8"  fill="#d2d2d2"/>

    <!-- elipse base -->
    <ellipse cx="170" cy="350" rx="150" ry="11" fill="url(#baseG)" stroke="#b0b0b0" stroke-width="0.6"/>

    <!-- ── ARTE IMPRESSA ── -->

    <!-- linha vermelha superior -->
    <line x1="62"  y1="130" x2="286" y2="130" stroke="#C8102E" stroke-width="1.6"/>

    <!-- CLEVERSON -->
    <text x="62" y="190"
          font-family="'Arial Black', Impact, sans-serif"
          font-size="32"
          font-weight="900"
          fill="#0A0A0A"
          letter-spacing="8"
          text-anchor="start">CLEVERSON</text>

    <!-- linha vermelha inferior -->
    <line x1="50"  y1="205" x2="286" y2="205" stroke="#C8102E" stroke-width="1.6"/>

    <!-- slogan -->
    <text x="62" y="232"
          font-family="Georgia,'Times New Roman',serif"
          font-style="italic"
          font-size="13.5"
          fill="#3A3A3A"
          letter-spacing="0.8">uma vez flamengo,</text>
    <text x="58" y="251"
          font-family="Georgia,'Times New Roman',serif"
          font-style="italic"
          font-size="13.5"
          fill="#3A3A3A"
          letter-spacing="0.8">sempre flamengo.</text>

    <!-- ── CABO ── -->
    <path d="M 315,100 Q 390,100 390,175 Q 390,250 315,250"
          fill="none" stroke="url(#canoG)" stroke-width="26" stroke-linecap="round"/>
    <path d="M 315,100 Q 378,100 378,175 Q 378,250 315,250"
          fill="none" stroke="#efefef" stroke-width="12" stroke-linecap="round"/>

    <!-- reflexos corpo -->
    <path d="M 44,28  Q 41,185  46,335" stroke="rgba(255,255,255,0.7)" stroke-width="5"
          fill="none" stroke-linecap="round"/>
    <path d="M 110,18 Q 107,185 112,345" stroke="rgba(255,255,255,0.18)" stroke-width="9"
          fill="none" stroke-linecap="round"/>
  </g>

  <!-- label frontal -->
  <text x="310" y="444" font-family="Arial,sans-serif" font-size="9"
        fill="#444" letter-spacing="4" text-anchor="middle">VISTA FRONTAL</text>

  <!-- ════════════════════════════════════════
       CANECA LATERAL  (cx ≈ 730)
  ════════════════════════════════════════ -->
  <g transform="translate(560, 78)" filter="url(#sombraLeve)">

    <!-- corpo lateral — mais estreito -->
    <path d="M 18,18
             Q 18,12  26,12
             L 230,12
             Q 238,12  238,18
             L 244,318
             Q 244,326  236,326
             L 22,326
             Q 14,326  14,318 Z"
          fill="url(#bodyS)" stroke="#bbbbbb" stroke-width="0.6"/>

    <!-- boca -->
    <ellipse cx="129" cy="14"  rx="112" ry="12" fill="url(#rimG)" stroke="#b0b0b0" stroke-width="0.5"/>
    <ellipse cx="129" cy="14"  rx="99"  ry="8"  fill="#e0e0e0"/>
    <ellipse cx="129" cy="16"  rx="97"  ry="6"  fill="#d2d2d2"/>

    <!-- base -->
    <ellipse cx="129" cy="324" rx="116" ry="9" fill="url(#baseG)" stroke="#b0b0b0" stroke-width="0.5"/>

    <!-- ── "sogrão" ── -->
    <line x1="94"  y1="300" x2="164" y2="300" stroke="#dedede" stroke-width="0.7"/>
    <text x="129" y="316"
          font-family="Arial,Helvetica,sans-serif"
          font-weight="300"
          font-size="9"
          fill="#999999"
          letter-spacing="3.5"
          text-anchor="middle">sogrão</text>

    <!-- cabo lateral -->
    <path d="M 242,88  Q 296,88  296,158 Q 296,228 242,228"
          fill="none" stroke="url(#canoG)" stroke-width="20" stroke-linecap="round"/>
    <path d="M 242,88  Q 285,88  285,158 Q 285,228 242,228"
          fill="none" stroke="#efefef" stroke-width="9" stroke-linecap="round"/>

    <!-- reflexo -->
    <path d="M 30,24  Q 28,168  33,310" stroke="rgba(255,255,255,0.65)" stroke-width="4"
          fill="none" stroke-linecap="round"/>
  </g>

  <!-- label lateral -->
  <text x="730" y="444" font-family="Arial,sans-serif" font-size="9"
        fill="#444" letter-spacing="4" text-anchor="middle">VISTA LATERAL · detalhe "sogrão"</text>

  <!-- ════════════════════════════════════════
       PAINEL SPECS — RODAPÉ
  ════════════════════════════════════════ -->
  <line x1="60" y1="465" x2="940" y2="465" stroke="#272727" stroke-width="1"/>

  <!-- TIPOGRAFIA -->
  <text x="90" y="487" font-family="Arial,sans-serif" font-size="8"
        fill="#C8102E" letter-spacing="3">TIPOGRAFIA</text>
  <text x="90" y="503" font-family="Arial,sans-serif" font-size="10" fill="#555">Nome · Arial Black / Barlow Condensed ExtraBold</text>
  <text x="90" y="518" font-family="Arial,sans-serif" font-size="10" fill="#555">Slogan · Georgia Light Italic · cinza #3A3A3A</text>
  <text x="90" y="533" font-family="Arial,sans-serif" font-size="10" fill="#555">Sogrão · Inter Light · 8–9pt · cinza #999</text>

  <!-- PALETA -->
  <text x="420" y="487" font-family="Arial,sans-serif" font-size="8"
        fill="#C8102E" letter-spacing="3">PALETA</text>

  <!-- swatches -->
  <circle cx="426" cy="508" r="10" fill="#0A0A0A"/>
  <text x="426" y="527" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#0A0A0A</text>

  <circle cx="460" cy="508" r="10" fill="#C8102E"/>
  <text x="460" y="527" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#C8102E</text>

  <circle cx="494" cy="508" r="10" fill="#3A3A3A"/>
  <text x="494" y="527" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#3A3A3A</text>

  <circle cx="528" cy="508" r="10" fill="#999999"/>
  <text x="528" y="527" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#999999</text>

  <circle cx="562" cy="508" r="10" fill="#FFFFFF" stroke="#333" stroke-width="0.8"/>
  <text x="562" y="527" font-family="Arial,sans-serif" font-size="8" fill="#444" text-anchor="middle">#FFFFFF</text>

  <!-- HIERARQUIA -->
  <text x="680" y="487" font-family="Arial,sans-serif" font-size="8"
        fill="#C8102E" letter-spacing="3">HIERARQUIA VISUAL</text>
  <text x="680" y="503" font-family="Arial,sans-serif" font-size="10" fill="#555">1 · CLEVERSON — impacto imediato</text>
  <text x="680" y="518" font-family="Arial,sans-serif" font-size="10" fill="#555">2 · Linhas vermelhas — identidade esportiva</text>
  <text x="680" y="533" font-family="Arial,sans-serif" font-size="10" fill="#555">3 · Slogan italic · 4 · "sogrão" easter egg</text>
</svg>"""

png = cairosvg.svg2png(bytestring=SVG.encode(), output_width=2000, output_height=1200)

out = "/home/user/caio/caneca-preview.png"
with open(out, "wb") as f:
    f.write(png)

print(f"OK — {out}  ({len(png)//1024} KB)")
