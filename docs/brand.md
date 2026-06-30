# Setup OS Brand

Date: 2026-06-30

## Locked Direction

The locked mark is the half system gear opening into a terminal prompt and circuit graph.

Use [assets/brand/setup-os-mark.svg](../assets/brand/setup-os-mark.svg) as the canonical source. PNG exports, README art, GitHub avatars, and social cards should be derived from this SVG instead of copied from generated image explorations.

## Assets

| Asset | Use |
| --- | --- |
| [setup-os-mark.svg](../assets/brand/setup-os-mark.svg) | Primary app icon, GitHub avatar, favicon source |
| [setup-os-mark-mono.svg](../assets/brand/setup-os-mark-mono.svg) | Monochrome and small-size fallback |
| [setup-os-logo.svg](../assets/brand/setup-os-logo.svg) | README and wide lockup |
| [setup-os-social-card.svg](../assets/brand/setup-os-social-card.svg) | GitHub social preview source |
| [setup-os-mark-512.png](../assets/brand/setup-os-mark-512.png) | GitHub organization avatar upload |
| [setup-os-mark-256.png](../assets/brand/setup-os-mark-256.png) | Small PNG icon fallback |
| [setup-os-mark-mono-512.png](../assets/brand/setup-os-mark-mono-512.png) | Monochrome PNG fallback |
| [setup-os-social-card.png](../assets/brand/setup-os-social-card.png) | GitHub repository social preview upload |

## Palette

| Token | Hex | Use |
| --- | --- | --- |
| `setup-ink` | `#071923` | Background |
| `setup-navy` | `#0B3750` | Structural outline |
| `setup-aqua` | `#6EE7D8` | System/circuit primary |
| `setup-amber` | `#F6B85A` | Terminal prompt and graph nodes |
| `setup-text` | `#F7FBFC` | Wordmark text |
| `setup-muted` | `#9BB5BF` | Supporting text |

## Recreate Exactly

The brand source is deterministic SVG. To recreate the same mark, use the exact SVG file plus these fixed decisions:

- Canvas: `512 x 512`
- Outer rounded square radius: `112`
- Background: `#071923`
- Concept: left half system gear, center terminal prompt, right circuit graph
- Primary colors: navy outline, aqua body/circuit, amber prompt/nodes
- No letter `S`
- No `AI`, `OS`, or product text inside the mark
- No gradients, shadows, 3D effects, watermarks, stock artwork, or copied marketplace icons

Suggested prompt for future exploration:

```text
Original vector-friendly brand mark for "Setup OS": a left half system gear opening into a small terminal prompt and right-side circuit graph with rounded node endpoints. Flat modern developer-tool icon, strong GitHub avatar readability at 32px, deep navy background, aqua system/circuit, warm amber terminal prompt and nodes. No letter S, no AI text, no OS text, no watermark, no stock-art style, no mascot, no gradients, no shadows.
```

Future generated explorations should be treated as direction only. The final production asset should remain an original vector drawing in this repository.

PNG files are exports from the SVG source. Re-export them with any standards-compliant SVG renderer at the exact target sizes:

```bash
# Examples
rsvg-convert assets/brand/setup-os-mark.svg -w 512 -h 512 -o assets/brand/setup-os-mark-512.png
rsvg-convert assets/brand/setup-os-mark.svg -w 256 -h 256 -o assets/brand/setup-os-mark-256.png
rsvg-convert assets/brand/setup-os-social-card.svg -w 1280 -h 640 -o assets/brand/setup-os-social-card.png
```

## Legal Notes

This asset is intended to be original project artwork inspired by a broad category of developer-tool, setup, gear, terminal, and circuit motifs. Do not use the pasted stock or marketplace reference files directly.

Practical guardrails:

- Keep the final SVG source in this repo as the canonical asset.
- Avoid tracing any third-party icon, stock image, or generated candidate.
- Do a trademark search before commercial launch or major public branding.
- Keep the mark simple enough to be ownable, but do not claim the broad idea of "gear plus circuit" as exclusive.

This is project hygiene, not legal advice. For fundraising, commercial launch, or trademark filing, get an IP attorney to review the final mark and name.
