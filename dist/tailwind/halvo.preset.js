/* Halvo preset for Tailwind CSS v3 — generated from tokens.json by tools/build_tailwind.py. Do not edit by hand.
 *
 * tailwind.config.js:
 *   module.exports = { presets: [require('./halvo/tailwind/halvo.preset.js')], prefix: 'tw-', content: [...] }
 * Load tokens.css and components/bundle.css after @tailwind base and @tailwind components, before @tailwind utilities.
 * Put the Be Vietnam Pro @import url(https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap) first in your CSS.
 * Colours are CSS variables, so opacity modifiers (bg-accent/50) do not work in v3; use the *-soft tokens instead.
 */
module.exports = {
  "darkMode": [
    "selector",
    "[data-theme=\"dark\"]"
  ],
  "theme": {
    "extend": {
      "colors": {
        "bg": "var(--bg)",
        "veil": "var(--veil)",
        "glass": "var(--glass)",
        "glass-strong": "var(--glass-strong)",
        "glass-2": "var(--glass-2)",
        "glass-3": "var(--glass-3)",
        "well": "var(--well)",
        "rim": "var(--rim)",
        "rim-2": "var(--rim-2)",
        "ink": "var(--ink)",
        "ink-2": "var(--ink-2)",
        "muted": "var(--muted)",
        "line": "var(--line)",
        "line-2": "var(--line-2)",
        "accent": "var(--accent)",
        "accent-hi": "var(--accent-hi)",
        "accent-ink": "var(--accent-ink)",
        "accent-soft": "var(--accent-soft)",
        "accent-text": "var(--accent-text)",
        "glow": "var(--glow)",
        "cool": "var(--cool)",
        "warm": "var(--warm)",
        "data": "var(--data)",
        "good": "var(--good)",
        "warn": "var(--warn)",
        "bad": "var(--bad)",
        "info": "var(--info)",
        "good-soft": "var(--good-soft)",
        "warn-soft": "var(--warn-soft)",
        "bad-soft": "var(--bad-soft)",
        "info-soft": "var(--info-soft)",
        "mono-ink": "var(--mono-ink)",
        "h1": "var(--h1)",
        "h2": "var(--h2)",
        "h3": "var(--h3)",
        "h4": "var(--h4)",
        "h5": "var(--h5)",
        "h6": "var(--h6)",
        "s1": "var(--s1)",
        "s2": "var(--s2)",
        "s3": "var(--s3)",
        "s4": "var(--s4)",
        "s5": "var(--s5)",
        "s6": "var(--s6)"
      },
      "fontFamily": {
        "sans": [
          "Be Vietnam Pro",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "sans-serif"
        ],
        "halvo": [
          "Be Vietnam Pro",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "sans-serif"
        ]
      },
      "fontSize": {
        "dial-figure": [
          "64px",
          {
            "lineHeight": "1",
            "letterSpacing": "-0.04em",
            "fontWeight": "600"
          }
        ],
        "page-title": [
          "38px",
          {
            "lineHeight": "1.04",
            "letterSpacing": "-0.025em",
            "fontWeight": "600"
          }
        ],
        "display": [
          "34px",
          {
            "lineHeight": "1.1",
            "letterSpacing": "-0.02em",
            "fontWeight": "600"
          }
        ],
        "4xl": [
          "26px",
          {
            "lineHeight": "1.15",
            "letterSpacing": "-0.02em",
            "fontWeight": "600"
          }
        ],
        "3xl": [
          "22px",
          {
            "lineHeight": "1.1",
            "letterSpacing": "-0.01em",
            "fontWeight": "600"
          }
        ],
        "2xl": [
          "20px",
          {
            "lineHeight": "1.2",
            "letterSpacing": "-0.015em",
            "fontWeight": "700"
          }
        ],
        "xl": [
          "17px",
          {
            "lineHeight": "1.25",
            "letterSpacing": "-0.01em",
            "fontWeight": "600"
          }
        ],
        "lg": [
          "15px",
          {
            "lineHeight": "1.25",
            "letterSpacing": "-0.005em",
            "fontWeight": "600"
          }
        ],
        "base": [
          "14px",
          {
            "lineHeight": "1.45",
            "fontWeight": "500"
          }
        ],
        "md": [
          "13.5px",
          {
            "lineHeight": "1.45",
            "fontWeight": "600"
          }
        ],
        "sm": [
          "12.5px",
          {
            "lineHeight": "1.4",
            "fontWeight": "600"
          }
        ],
        "xs": [
          "12px",
          {
            "lineHeight": "1.4",
            "fontWeight": "600"
          }
        ],
        "2xs": [
          "11px",
          {
            "lineHeight": "1.5",
            "letterSpacing": "0.08em",
            "fontWeight": "700"
          }
        ]
      },
      "borderRadius": {
        "sm": "var(--r-sm)",
        "md": "var(--r-md)",
        "lg": "var(--r-lg)",
        "xl": "var(--r-xl)",
        "control": "13px",
        "small": "11px"
      },
      "spacing": {
        "inset": "var(--inset)",
        "gap": "var(--gap)",
        "side": "var(--side)",
        "side-rail": "var(--side-rail)"
      },
      "maxWidth": {
        "content": "1480px"
      },
      "boxShadow": {
        "surface": "var(--shadow)",
        "overlay": "var(--shadow-lg)"
      },
      "transitionTimingFunction": {
        "halvo": "cubic-bezier(.22, 1, .36, 1)",
        "power3-out": "cubic-bezier(.25, 1, .5, 1)",
        "expo-out": "cubic-bezier(.16, 1, .3, 1)",
        "power2-out": "cubic-bezier(.33, 1, .68, 1)",
        "power2-in": "cubic-bezier(.32, 0, .67, 0)",
        "power3-in": "cubic-bezier(.5, 0, .75, 0)",
        "power2-inout": "cubic-bezier(.65, 0, .35, 1)",
        "power3-inout": "cubic-bezier(.76, 0, .24, 1)",
        "back-2": "linear(0,0.23 5%,0.43 10%,0.6 15%,0.74 20%,0.86 25%,0.95 30%,1.02 35%,1.07 40%,1.11 45%,1.12 50%,1.13 55%,1.13 60%,1.12 65%,1.1 70%,1.08 75%,1.06 80%,1.03 85%,1.02 90%,1 95%,1)",
        "back-3": "linear(0,0.28 5%,0.51 10%,0.71 15%,0.87 20%,1 25%,1.1 30%,1.17 35%,1.22 40%,1.24 45%,1.25 50%,1.24 55%,1.22 60%,1.2 65%,1.16 70%,1.12 75%,1.09 80%,1.05 85%,1.03 90%,1.01 95%,1)"
      },
      "transitionDuration": {
        "tick": "0.18s",
        "quick": "0.25s",
        "swift": "0.36s",
        "base": "0.45s",
        "settle": "0.6s",
        "reveal": "0.85s",
        "long": "1.2s"
      }
    }
  }
};
