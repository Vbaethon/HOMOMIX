# Current icon sources

This is the only active source tree. Previous version directories, full input snapshots and candidate QA screenshots have been removed from the current checkout; Git history preserves them. Current production URLs remain unchanged.

## Rebuild and edit

Use Python 3.12, the exact packages in `requirements.txt`, and the pinned `@resvg/resvg-js` in `package-lock.json`.

```sh
python -m pip install -r Sources/current/requirements.txt
npm ci --prefix Sources/current
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python Sources/current/build_unified.py --output-dir ./build-current-check --jobs 4
```

`plan.json` is the current subject scale/position plan. Backgrounds stay fixed, the circular outline is fixed, and artwork is not stretched. Native editable geometry lives in `compact_originals.py`, `assets/native-baseline/`, `assets/original-geometry/`, `adjustments/` and `animal_redesign.py`. `native.py` provides the shared subject transform; `material.py` provides the shared finish. `render.cjs` is the sole SVG rasterizer. Generated SVGs in `svg/` are build artifacts, not a historical version.

`assets/original-raster/` contains only current extraction inputs, not a complete old release. `assets/composition/` contains only the six full-composition inputs kept by the current plan. Approved calibration inputs/layers belong to the current editable pipeline, not an additional version. Do not replace those inputs with production thumbnails.

## Source provenance

`current-audit.json` covers current identities and confidence. `official/native/provenance.json` and `official/special/provenance.json` retain official URLs, input hashes and transformation limits. Nine previously disclosed brand-identity uncertainties remain; current geometric tests are not a claim that every third-party identity or license was verified.

Third-party marks are not relicensed by this repository. The retained font licenses are in `licenses/`. Some legacy raster backgrounds hidden by artwork are approximately reconstructed from observed pixels. GOG currently uses a 152px official source; long thin wordmarks remain limited at very small sizes rather than being stretched or falsely thickened.

## Compatibility and validation

Default and Large exports retain their historical URL paths. Five aliases are excluded from primary display but still downloadable; the mistaken `Claud` files are removed. The incomplete FDS series retains its two existing files and a separate entry at `Icon/Color/FDS/README.md`; it is the third production category, not a historical source version. `collection-manifest.json` and `render-manifest.json` describe current bytes. Tests check current identities, circular bounds, fixed material, dimensions, aliases, real parameter effects and deterministic rebuilding. Tests are not a proof of equal perceived weight; final visual evidence is in `qa/final/`.

## Effective transform parameters

Use `scale`, `dx`, and `dy` for editable subject branches; compact originals use `compact_scale` instead of legacy `scale`. Supplying a changed legacy scale to a compact item is rejected, not silently ignored. Six fixed full compositions reject non-default transforms; they need source-layer redesign to become independently editable. Reports identify `scale_parameter` and `transform_policy`.

Seven calibrated raster inputs retain their approved default pixels exactly while allowing foreground-only scale/x/y changes. Their immutable `sample-calibration.json` must not be regenerated from an edited plan: doing so would cancel the intended change. Reconstructed concealed background is approximate, not a claim of a recovered original official layer.

Run the same full CI gate locally:

```sh
python scripts/validate_icons.py --tests --generated --cold --jobs 4
```

See [test coverage mapping](../../docs/TEST_COVERAGE.md) and [current repair acceptance](../../docs/AUDIT_FIXES.md).
