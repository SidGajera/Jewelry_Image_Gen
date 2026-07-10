# assets/references — pose & source reference index

Reference images (source SKUs, lifestyle poses) live in Google Drive; this folder documents where they are. Higgsfield `media_id`s expire across sessions — the durable cache is the Drive file IDs in `docs/06_CACHE.md`.

- Source SKU parent: `1mKqVAi2iv_35zs12jn91UYaeX2vKGdyy` (per-SKU `LR-XXXX` subfolders)
- Studio/Office pose references: `1A9UJJcnlVA1Tvohd6Wa8O57eenCb7sQ2`
- Home Lifestyle references (wider + close-up): `1GFwd4SHSPuCoaQj2WHYJWb7nTsvFUPzi`
- Output folder: `1NGoqWNTGX4SxPNyQkL_6ZU1jnuqpB5_2`

Import into Higgsfield with: `media_import_url("https://drive.google.com/uc?id=<FILE_ID>&export=download")`.
Pose-variety rule: use DIFFERENT lifestyle/closeup files per SKU than the previous SKU; studio branded refs may repeat.
