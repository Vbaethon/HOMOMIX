// Deterministic SVG rasterization. Fonts and external resources are not loaded.
const {Resvg} = require('@resvg/resvg-js');
const fs = require('node:fs');
const [input, output] = process.argv.slice(2);
const resvg = new Resvg(fs.readFileSync(input), {
  fitTo: {mode: 'width', value: 1440},
  font: {loadSystemFonts: false},
});
fs.writeFileSync(output, resvg.render().asPng());
