# Vendored dependencies

This repository is self-contained. Former Git submodules are tracked as regular files at the audited commits below. Their original directory layout is preserved so runtime imports and entry points remain compatible.

| Path | Source | Pinned commit |
| --- | --- | --- |
| `src/che_data_to_spatial_coord` | [che_data_to_spatial_coord](https://github.com/TopologicalKnotIndexer/che_data_to_spatial_coord) | `9cf66fe76ff9af8cde26511b7f9b8cd62f2afb27` |
| `src/spatial_coord_to_pd_code` | [spatial_coord_to_pd_code](https://github.com/TopologicalKnotIndexer/spatial_coord_to_pd_code) | `1215f22321b16e7484bff0573d7a80b8f45b2938` |

## Updating a vendored dependency

Replace the listed tree from a reviewed source commit, update this table, and run this repository's complete validation suite. Do not reintroduce Git submodules; every organization project must remain independently cloneable.
