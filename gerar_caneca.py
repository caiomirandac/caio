import cairosvg

# Escudo do Flamengo simplificado (minimalista, sem personagens)
# Baseado nas cores e forma clássica do CRF
FLAMENGO_CREST = """
  <g transform="translate(-38,-52) scale(0.9)">
    <!-- Shield shape -->
    <path d="M38,4 L76,4 Q82,4 82,10 L82,44 Q82,58 60,72 Q56,75 38,85
             Q20,75 16,72 Q-6,58 -6,44 L-6,10 Q-6,4 0,4 Z"
          fill="#1a1a1a" stroke="#333" stroke-width="1"/>

    <!-- Listras preto e vermelho (horizontal) -->
    <!-- faixa vermelha 1 -->
    <clipPath id="shieldClip">
      <path d="M38,4 L76,4 Q82,4 82,10 L82,44 Q82,58 60,72 Q56,75 38,85
               Q20,75 16,72 Q-6,58 -6,44 L-6,10 Q-6,4 0,4 Z"/>
    </clipPath>

    <g clip-path="url(#shieldClip)">
      <!-- fundo preto -->
      <rect x="-10" y="0" width="100" height="90" fill="#0A0A0A"/>
      <!-- faixa diagonal preta e vermelha clássica do Flamengo -->
      <!-- faixas horizontais: preto, vermelho, preto, vermelho -->
      <rect x="-10" y="0"  width="100" height="22" fill="#0A0A0A"/>
      <rect x="-10" y="22" width="100" height="22" fill="#C8102E"/>
      <rect x="-10" y="44" width="100" height="22" fill="#0A0A0A"/>
      <rect x="-10" y="66" width="100" height="24" fill="#C8102E"/>

      <!-- diagonal clássica (faixa branca diagonal) -->
      <polygon points="-10,0 30,0 -10,55" fill="#FFFFFF" opacity="0.08"/>
    </g>

    <!-- Borda do escudo -->
    <path d="M38,4 L76,4 Q82,4 82,10 L82,44 Q82,58 60,72 Q56,75 38,85
             Q20,75 16,72 Q-6,58 -6,44 L-6,10 Q-6,4 0,4 Z"
          fill="none" stroke="#555" stroke-width="1.2"/>

    <!-- Borda interna dourada fina -->
    <path d="M38,8 L73,8 Q78,8 78,13 L78,43 Q78,55 58,68 Q55,71 38,80
             Q21,71 18,68 Q-2,55 -2,43 L-2,13 Q-2,8 3,8 Z"
          fill="none" stroke="#888" stroke-width="0.5"/>

    <!-- CRF monograma -->
    <text x="38" y="52"
          font-family="Georgia,serif"
          font-size="18"
          font-weight="bold"
          fill="#FFFFFF"
          text-anchor="middle"
          letter-spacing="2">CRF</text>

    <!-- Ano de fundação -->
    <text x="38" y="66"
          font-family="Arial,sans-serif"
          font-size="7"
          fill="rgba(255,255,255,0.55)"
          text-anchor="middle"
          letter-spacing="1">1895</text>
  </g>
"""

SVG = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1100" height="580" viewBox="0 0 1100 580"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- fundo ambiente claro, como a foto -->
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f2ede8"/>
      <stop offset="100%" stop-color="#e0d8d0"/>
    </linearGradient>

    <!-- corpo caneca — cerâmica branca real -->
    <linearGradient id="mugBody" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#d6d6d6"/>
      <stop offset="6%"   stop-color="#f8f8f8"/>
      <stop offset="92%"  stop-color="#f5f5f5"/>
      <stop offset="100%" stop-color="#c8c8c8"/>
    </linearGradient>

    <!-- topo / boca -->
    <linearGradient id="mugTop" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#bbbbbb"/>
      <stop offset="40%"  stop-color="#e8e8e8"/>
      <stop offset="60%"  stop-color="#e0e0e0"/>
      <stop offset="100%" stop-color="#aaaaaa"/>
    </linearGradient>

    <!-- cabo -->
    <linearGradient id="handle" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#cccccc"/>
      <stop offset="50%"  stop-color="#f0f0f0"/>
      <stop offset="100%" stop-color="#bbbbbb"/>
    </linearGradient>

    <!-- sombra drop -->
    <filter id="shadow" x="-25%" y="-10%" width="160%" height="140%">
      <feDropShadow dx="4" dy="16" stdDeviation="20"
                    flood-color="#8a7a6a" flood-opacity="0.35"/>
    </filter>

    <!-- sombra suave caneca lateral -->
    <filter id="shadowB" x="-25%" y="-10%" width="160%" height="140%">
      <feDropShadow dx="4" dy="14" stdDeviation="16"
                    flood-color="#8a7a6a" flood-opacity="0.28"/>
    </filter>

    <!-- brilho interno da boca -->
    <radialGradient id="innerMouth" cx="50%" cy="40%" r="55%">
      <stop offset="0%"   stop-color="#c0c0c0"/>
      <stop offset="100%" stop-color="#a0a0a0"/>
    </radialGradient>
  </defs>

  <!-- ── FUNDO ── -->
  <rect width="1100" height="580" fill="url(#bg)"/>

  <!-- sombra no chão das canecas -->
  <ellipse cx="298" cy="535" rx="165" ry="16" fill="rgba(100,80,60,0.18)"/>
  <ellipse cx="798" cy="535" rx="145" ry="14" fill="rgba(100,80,60,0.15)"/>

  <!-- label discreto topo -->
  <text x="550" y="30" font-family="Arial,sans-serif" font-size="10"
        fill="#aaa" letter-spacing="5" text-anchor="middle">
    CLEVERSON · FLAMENGO EDITION
  </text>


  <!-- ═══════════════════════════════════════════════
       CANECA FRONTAL  — estilo foto referência
  ═══════════════════════════════════════════════ -->
  <g transform="translate(80, 48)" filter="url(#shadow)">

    <!-- CORPO — forma mais quadrada / latte mug -->
    <path d="M 40,28
             Q 40,20  50,20
             L 370,20
             Q 380,20  380,28
             L 388,468
             Q 388,478  378,478
             L 42,478
             Q 32,478  32,468 Z"
          fill="url(#mugBody)" stroke="#c8c8c8" stroke-width="0.8"/>

    <!-- elipse boca -->
    <ellipse cx="210" cy="22" rx="172" ry="17" fill="url(#mugTop)" stroke="#b8b8b8" stroke-width="0.6"/>
    <ellipse cx="210" cy="22" rx="156" ry="12" fill="url(#innerMouth)"/>
    <ellipse cx="210" cy="24" rx="153" ry="9"  fill="#b8b8b8"/>

    <!-- elipse base -->
    <ellipse cx="210" cy="472" rx="180" ry="12" fill="#c8c8c8" stroke="#b8b8b8" stroke-width="0.6"/>

    <!-- ══ ARTE IMPRESSA — estilo da foto ══ -->

    <!-- "Cleverson" mixed case, bold, grande -->
    <text x="72" y="218"
          font-family="'Arial Black','Helvetica Neue',Arial,sans-serif"
          font-size="58"
          font-weight="900"
          fill="#111111">Cleverson</text>

    <!-- underline vermelho fino (como na foto) -->
    <rect x="72" y="228" width="76" height="4" fill="#C8102E" rx="1"/>

    <!-- slogan — fonte leve -->
    <text x="72" y="270"
          font-family="Arial,Helvetica,sans-serif"
          font-size="16"
          font-weight="300"
          fill="#444444"
          letter-spacing="0.3">Uma vez Flamengo, sempre Flamengo.</text>

    <!-- "Sogrão" — pequeno, canto inferior esquerdo -->
    <text x="72" y="436"
          font-family="Arial,Helvetica,sans-serif"
          font-size="13"
          font-weight="300"
          fill="#999999"
          letter-spacing="0.5">Sogrão</text>

    <!-- ── CABO ── -->
    <path d="M 383,120 Q 470,120 470,210 Q 470,300 383,300"
          fill="none" stroke="url(#handle)" stroke-width="34"
          stroke-linecap="round"/>
    <path d="M 383,120 Q 454,120 454,210 Q 454,300 383,300"
          fill="none" stroke="#f2f2f2" stroke-width="14"
          stroke-linecap="round"/>

    <!-- reflexos corpo -->
    <path d="M 56,36  Q 53,250  58,460"
          stroke="rgba(255,255,255,0.72)" stroke-width="6"
          fill="none" stroke-linecap="round"/>
    <path d="M 130,26 Q 127,250 132,470"
          stroke="rgba(255,255,255,0.2)" stroke-width="10"
          fill="none" stroke-linecap="round"/>
  </g>

  <!-- label -->
  <text x="298" y="558" font-family="Arial,sans-serif" font-size="9"
        fill="#bbb" letter-spacing="4" text-anchor="middle">FRENTE</text>


  <!-- ═══════════════════════════════════════════════
       CANECA TRASEIRA — escudo do Flamengo
  ═══════════════════════════════════════════════ -->
  <g transform="translate(570, 60)" filter="url(#shadowB)">

    <!-- corpo -->
    <path d="M 34,24
             Q 34,16  44,16
             L 330,16
             Q 340,16  340,24
             L 347,452
             Q 347,462  337,462
             L 37,462
             Q 27,462  27,452 Z"
          fill="url(#mugBody)" stroke="#c8c8c8" stroke-width="0.8"/>

    <!-- boca -->
    <ellipse cx="187" cy="18" rx="155" ry="15" fill="url(#mugTop)" stroke="#b8b8b8" stroke-width="0.6"/>
    <ellipse cx="187" cy="18" rx="140" ry="11" fill="url(#innerMouth)"/>
    <ellipse cx="187" cy="20" rx="137" ry="8"  fill="#b8b8b8"/>

    <!-- base -->
    <ellipse cx="187" cy="456" rx="162" ry="11" fill="#c8c8c8" stroke="#b8b8b8" stroke-width="0.6"/>

    <!-- ══ ESCUDO FLAMENGO ══ -->
    <g transform="translate(187,230) scale(1.3)">
      {FLAMENGO_CREST}
    </g>

    <!-- "Clube de Regatas do Flamengo" micro texto abaixo do escudo -->
    <text x="187" y="362"
          font-family="Arial,Helvetica,sans-serif"
          font-size="8.5"
          font-weight="300"
          fill="#bbb"
          text-anchor="middle"
          letter-spacing="1.5">CLUBE DE REGATAS DO FLAMENGO</text>

    <!-- cabo traseiro -->
    <path d="M 343,108 Q 420,108 420,196 Q 420,284 343,284"
          fill="none" stroke="url(#handle)" stroke-width="30"
          stroke-linecap="round"/>
    <path d="M 343,108 Q 408,108 408,196 Q 408,284 343,284"
          fill="none" stroke="#f2f2f2" stroke-width="12"
          stroke-linecap="round"/>

    <!-- reflexos -->
    <path d="M 50,30  Q 47,235  52,445"
          stroke="rgba(255,255,255,0.70)" stroke-width="5"
          fill="none" stroke-linecap="round"/>
    <path d="M 115,22 Q 112,235 117,454"
          stroke="rgba(255,255,255,0.18)" stroke-width="9"
          fill="none" stroke-linecap="round"/>
  </g>

  <!-- label -->
  <text x="798" y="558" font-family="Arial,sans-serif" font-size="9"
        fill="#bbb" letter-spacing="4" text-anchor="middle">VERSO</text>

</svg>"""

png = cairosvg.svg2png(bytestring=SVG.encode(), output_width=2200, output_height=1160)

out = "/home/user/caio/caneca-preview.png"
with open(out, "wb") as f:
    f.write(png)

print(f"OK — {out}  ({len(png)//1024} KB)")
