# Vendored dependencies

This repository is self-contained. Former Git submodules are tracked as regular files at the audited commits below. Their original directory layout is preserved so runtime imports and entry points remain compatible.

| Path | Source | Pinned commit |
| --- | --- | --- |
| `src/khovanov-solver` | [khovanov-solver](https://github.com/TopologicalKnotIndexer/khovanov-solver) | `09aee50e389ed02046016dd555ac7fed8f965515` |
| `src/khovanov-solver/src/pd_code_de_r1_k8` | [pd_code_de_r1_k8](https://github.com/TopologicalKnotIndexer/pd_code_de_r1_k8) | `395d0b272a06e90c28db90a38803412e8eb9edb5` |
| `src/khovanov-solver/src/pd_code_input_sanity` | [pd_code_input_sanity](https://github.com/TopologicalKnotIndexer/pd_code_input_sanity) | `9f0233a3b48043a9e164d98ad6cee644cc792a28` |
| `src/khovanov-homology-list` | [khovanov-homology-list](https://github.com/TopologicalKnotIndexer/khovanov-homology-list) | `d3ae43d297b8de7689afd6a925e991fa762420bb` |
| `src/slow_dict_reader` | [slow_dict_reader](https://github.com/TopologicalKnotIndexer/slow_dict_reader) | `85e9af7681b8a9b569d3ffae2c68e8d861f89c54` |
| `src/slow_dict_reader/src/knotname-reg` | [knotname-reg](https://github.com/TopologicalKnotIndexer/knotname-reg) | `fce68fc3d45a8f3d4e6da81efc07b069ed8179ad` |

## Updating a vendored dependency

Replace the listed tree from a reviewed source commit, update this table, and run this repository's complete validation suite. Do not reintroduce Git submodules; every organization project must remain independently cloneable.
