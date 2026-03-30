# Centy marketing site — design system alignment

## Source of truth

| Token | Value | App reference |
|-------|--------|----------------|
| Primary / CTA | `#00a865` | `design-system/tokens/colors.ts` → `accent`, `btn` |
| Primary hover | `#007a49` | `btnHover` |
| Primary light surface | `#e6f7f0` | `accentLight` |
| Page background | `#f7f8fa` | `bg` |
| Card / off-white | `#ffffff` / `#f2f4f7` | `white`, `bgCard` |
| Text primary | `#111827` | `ink` |
| Text secondary | `#374151` | `inkSoft` |
| Text muted | `#6b7280` | `inkMuted` |
| Border | `#e4e7ed` | `border` |
| Display font | Fraunces | `typography.fontDisplay` |
| Body font | DM Sans | `typography.fontFamily` |
| Mono / data | DM Mono | `typography.fontMono` |

## Implementation phases

1. **Static v1 (current)** — Single `index.html` + `styles.css` on LiteSpeed docroot; tokens in CSS `:root`; all CTAs → `https://app.centyhq.com` (signup at `/signup`).
2. **Parity checks** — When the app shell changes, refresh the product mock (sidebar labels) so marketing matches production nav where intentional.
3. **Optional next** — Extract repeated UI (buttons, cards) into partials via Eleventy/Astro; add `sitemap.xml`, `robots.txt`, and Open Graph tags; wire footer “Blog” to a real CMS or `/blog`.
4. **Analytics** — Add privacy-preserving analytics on `www.getcenty.com` only after cookie/consent policy exists.
5. **i18n** — If East Africa expansion needs Swahili, externalise strings and load a second CSS font subset if needed.

## Deploy

See `deploy/rsync-marketing.sh` and `deploy/lsws/` for server paths and vhosts.
