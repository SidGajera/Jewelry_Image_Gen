# 06 — CACHE (durable reusable assets)

> **IMPORTANT:** Higgsfield `media_id`s are **session-ephemeral** — they expire across sessions. The **durable cache is the Google Drive file IDs** below. Re-run `media_import_url` on the Drive `uc?id=<ID>&export=download` link whenever a `generate_image` call rejects a media_id with "Media input not found".

## GOOGLE DRIVE — FOLDERS (durable)
| Purpose | Folder ID |
|---|---|
| Parent "Lucent" | `17fxsv1hJXoDm0vRgDOAm_YfNgG1xnLKv` |
| Source parent (SKU subfolders) | `1mKqVAi2iv_35zs12jn91UYaeX2vKGdyy` |
| Studio / Office references | `1A9UJJcnlVA1Tvohd6Wa8O57eenCb7sQ2` |
| Home Lifestyle references | `1GFwd4SHSPuCoaQj2WHYJWb7nTsvFUPzi` |
| Output | `1NGoqWNTGX4SxPNyQkL_6ZU1jnuqpB5_2` |
| Tracking sheet | `1Sburxb4cOdD52EnXWuNAX7Z3UF5-d_1RRWhP7-YHCM8` |
| Auto log sheet | `1p2Qs5cs3D9NqjPnGp7EZvw9cPsIOBHK6it2aFXpXJ7k` |
| Logo asset folder | `1ih1bP-ACl0iXNlMH074Jejq_HL6AqZrF` |

## LOGO ASSET (locked, P0)
| File | Drive file ID | Repo path |
|---|---|---|
| Lucent Carat Lab Logo.png (official) | `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH` | `/assets/logo/logo_official.png` |
| Transparent-ink derivative | (derived locally) | `/assets/logo/logo_official_transparent.png` |

Also: `Offie_photoshoot (1).png` (`1orscL2F2NYpyPb7jA70CqSboqBYqrCvH`) is a studio reference that CONTAINS the correct printed logo (useful as a placement/scale reference).

## STUDIO / OFFICE POSE REFERENCES (branded cloth, reused every catalog)
| Angle | Drive file ID |
|---|---|
| Offie_photoshoot (1) — front + logo ref | `1orscL2F2NYpyPb7jA70CqSboqBYqrCvH` |
| Offie_photoshoot (2) | `1m4paT3cvdBvwsgPl_dD6cy1tgN3Y_d6h` |
| Offie_photoshoot (3) | `1B8alfmVEoWR-1ps3RWstunuX8hB9f_sr` |
| Offie_photoshoot (4) | `1nuc9dseZnVoJsN0uOXMji9oKinh1kAkE` |
| Offie_photoshoot (5) | `1r7Yb5s9YXAnQhLyTN40nFro1NxXDHidF` |

## LIFESTYLE — WIDER SCENE REFERENCES (`Reference_US_Ring`)
| # | Drive file ID |
|---|---|
| (2) | `10lX8o2IhRwiq3zbgPCyVMqYKGWZNM0_w` |
| (6) | `12zRXerpNEhdqo4DMLgQkiJnt7YDg7NV9` |
| (8) Copy | `1u5JNWqQ9GKgYwAB3PVW02zKVmnC4GW_K` |
| (9) | `1pikNgx5RIMjmniABU-frf1n7NDsMF47Y` |

## LIFESTYLE — CLOSE-UP REFERENCES (`Closup_houselifestyle`)
| # | Drive file ID | # | Drive file ID |
|---|---|---|---|
| (2) | `1d_Rxs5djy5W9xO6rxBo6HNOEwxsOvMkE` | (10) | `1tbJACkJUk0W5J7i-AaiKVIS-2iAPe7wl` |
| (3) | `1C7gMaVixfWwiY9yfTXZaByNGqv7NDSV7` | (11) | `1Lqpgc4lz59u9_kEz0KJtiLdgu3AJA5r6` |
| (5) | `1_NwJiAxRklEEMcMc2iOUe5AW-a72eOsg` | (12) | `17ozftZRAPtotvLPEHkdPJJkQdTWViXaE` |
| (6) | `1qNGDjhWT86SW1LfAXhbgOHh4OVC0fmA9` | (13) | `1TFG37rNRzGr5gec_XoJAY__paWHsjzyC` |
| (7) | `16Jh0jjtMEtUoM63lFtdGttgpHmRxxovA` | (14) | `1nA-fzOhogQQluPKlwOWvVuhHKgkAH4N5` |
| (8) | `1UUWVDbJ0WLvNYxrtR9TJf3QRTxp9ZttH` | (15) | `1cEixik3XL9BAcv1sffE2U0U-UfJeL0b8` |
| (9) | `1NF2XNYAmGUOC6ANb7M3KzcCxijAkRzco` | (16) | `11ulp1TgRdL6kBvpa9DRFkGuVSDfD317b` |

**Pose-variety rule:** use DIFFERENT lifestyle/closeup files for each SKU than the previous SKU (studio branded refs may repeat since they are the fixed branded set).

## SOURCE SKUs PROCESSED (folders under source parent)
| SKU | Source folder ID | Design |
|---|---|---|
| LR-0136 | `159MjisakODelkPZKFFDiAJoii7EKQR8_` | Oval diamond + 2 GREEN emerald-cut emeralds + plain yellow band (3ct) |
| LR-0137 | `1ADZwnTDCLX4q3PWUG6j0s58RFWB5nN1f` | Oval diamond + 2 tapered baguette diamonds + plain yellow band (3ct) |
(Earlier SKUs LR-0156/0160/0162/0164/0165/0166/0167/0168/0190/0191/0192 processed in prior sessions — see `LUCENT_MASTER.md` §14.)

## MODEL / GENERATION SETTINGS (constant)
- Model: `nano_banana_2` · `resolution:"2k"` · `aspect_ratio:"1:1"` · `count:1`
- medias order: `[ pose/studio reference , SOURCE ring ]`
- Import URL form: `https://drive.google.com/uc?id=<FILE_ID>&export=download`

## OFFICIAL LOGO — GENERATION REFERENCE (session-ephemeral)
Import `assets/logo/logo_official.png` (Drive `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH`) via `media_import_url` each session to get a media_id, then pass it as the 3rd studio reference so the printed logo matches the official artwork exactly. media_ids expire across sessions — re-import when needed.
