# BACKGROUND RULES — POINTER

> This file is a **pointer, not a policy store.** Per the repository's one-owner-per-topic rule, the background/cloth standard has exactly one authoritative owner and must never be duplicated:
>
> **Owner: [`docs/11_BACKGROUND_STANDARD.md`](docs/11_BACKGROUND_STANDARD.md)**
>
> Append changes there. Do not restate policy text in this file — a second copy will drift out of sync with the owner and create ambiguity about which one binds.

## Office photoshoot background — velvet only (user-locked 2026-07-24)

The rule in force, in one line: **office photoshoot images use premium pure-white plush VELVET as the background and nothing else.**

Full text, including the two mandatory enforcement gates and the revocation of cotton as an alternate, lives in `docs/11_BACKGROUND_STANDARD.md` → *CLOTH MATERIAL — VELVET ONLY*.

### Where it is enforced

| Point | File |
|---|---|
| Policy (authoritative) | `docs/11_BACKGROUND_STANDARD.md` |
| Prompt build — CLOTH (P3) runtime rule | `prompts/07_PROMPTS.md` |
| Prompt build — STUDIO WRAPPER / STUDIO WRAPPER v2 | `prompts/07_PROMPTS.md` |
| Rejection log | `config/QUALITY_MEMORY.json` → `fixes[]`, id `office-photoshoot-background-must-be-velvet` |

## Priority

**JEWELRY IS THE HERO.** The jewelry is always the clear focus and highlight of every image. The logo is secondary and must NEVER hide, distract from, or compete with it. Where any other rule would make the logo more prominent, the jewelry wins.

## Source locking — ROOT FIX

The source CAD is **always** passed as a locked visual reference (image-to-image), never described from memory. It goes **first** in `medias`; the scene plate goes last and donates only background, lighting, camera and white balance. **Only the camera angle may change.** Never ADD a halo, pavé or accent that is not in the source; never REMOVE one that is. Owner: `prompts/07_PROMPTS.md` → *SOURCE LOCKING*.

## Delivery checklist (all four, every image)

Compare **side-by-side with the source** before delivering. Reject on any mismatch.

1. **Jewelry is the clear highlight.**
2. **Every diamond matches the source exactly** — shape, count, size, placement. No halo, extra or missing stones. Facets, cut and angles sharp; no blur, melting, rounding or merging. Owner: `prompts/07_PROMPTS.md` → *STONE SHAPE LOCK*.
3. **Background = velvet.**
4. **Any visible logo reads as naturally printed and stays subtle / partly hidden** — otherwise remove it and ship plain velvet.

### The gates

1. **Prompt-build gate** — before submitting, confirm the prompt names velvet and names no other fabric. Correct it *before* submission, not after.
2. **Pre-delivery gate** — validate the rendered background reads as velvet. Non-velvet = automatic reject + Failure Memory record.
3. **Logo gate** — if a logo is present it must read as naturally printed into the velvet pile (follows folds, perspective, lighting; no sticker / overlay / floating / white-box look). **Fallback:** if it cannot print naturally, deliver PLAIN velvet with NO logo. Never ship a pasted-looking logo.

Automated checks for gates 2–3: `scripts/validate_render.py` (`velvet`, `logo_natural` gates).
