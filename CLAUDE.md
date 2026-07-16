# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains standalone, self-contained HTML card components ("cards") with all CSS inlined in a `<style>` block. There is no build system, package manager, test suite, or linter — each `.html` file is a complete, independent deliverable that can be opened directly in a browser.

Current contents:

- `card_seguranca_operacional_unico.html` — a single "Segurança Operacional" (Operational Safety) card: a header with an inline SVG shield icon and title, followed by a bulleted list of checklist items.

## Development

There are no build, lint, or test commands. To preview a card, open the HTML file in a browser (e.g. with a simple static server: `python3 -m http.server`).

## Conventions

Content is in Brazilian Portuguese (`lang="pt-BR"`); keep user-facing text in Portuguese.

The existing card establishes the visual language to follow for new or modified cards:

- **Fonts**: Google Fonts loaded via `<link>` — Montserrat (600/700) for titles, Source Sans 3 (400/500) for body text.
- **Palette**: dark blue `#003A70` for titles, primary blue `#005EB8` for accents (left header bar, bullet dots, icon strokes), light blue `#D9E8F5` for icon backgrounds, `#EDF2F7` page background, `#374151` body text.
- **Structure**: `.card` > `.card-header` (icon in `.icon-wrap` + `.card-title`) + `.card-body` (repeated `.item` rows of `.item-dot` + `.item-text`).
- **Style details**: 340px card width, 14px border radius, layered `rgba(0,58,112,…)` shadows, hover lift effect (`translateY(-5px)` with deepened shadow), inline SVG icons (stroke-based, no fill).

New cards should be created as separate self-contained `.html` files following this same pattern, with no external dependencies beyond Google Fonts.
