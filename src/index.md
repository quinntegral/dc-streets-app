---
toc: false
---
<script src="https://unpkg.com/maplibre-gl@3.0.0/dist/maplibre-gl.js"></script>

<div>
  <h1>D.C. safe school commutes app </h1>
  <h2>for visualizing traffic safety risks across school boundaries</h2>
</div>

<div style="width: 100%; position: relative;">
<div class=card style="max-width: 270px; position: absolute; top:0; margin-left: 14px; right:14px; z-index:1;">

# card title
## card subtitle
${colorLegend}

<div style="font-size: small; text-align: right; font-style: italic;"><a href="https://www.datadrivenstreets.org/">source link</a></div>

## priorities

```js
const risk = view(Inputs.range([0, 10], {value: 1, label: "Risk score", step: 1}));
const slider = view(Inputs.range([0, 10], {value: 1, label: "Distance", step: 1}));
```

</div>
<div id="container" style="background: rgb(18,35,48); height: 800px; width: 100%;"></div>
</div>


```js
import deck from "npm:deck.gl";
import maplibregl from "npm:maplibre-gl";
// could also use AmbientLight, LightingEffect, PointLight
const {DeckGL, MapView, MapController, GeoJsonLayer, ScatterplotLayer} = deck;

const colorRange = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78]
];

const colorLegend = Plot.plot({
  margin: 0,
  marginTop: 20,
  width: 270,
  height: 35,
  x: {padding: 0, round: false, axis: null},
  marks: [
    Plot.cellX(colorRange, {
      fill: ([r, g, b]) => `rgb(${r},${g},${b})`
    }),
    Plot.text(["Fewer"], {frameAnchor: "top-left", dy: -12}),
    Plot.text(["More"], {frameAnchor: "top-right", dy: -12})
  ]
});

//const data = FileAttachment("/data/visualization_of_aws_model").csv({array: true, typed: true});

const INITIAL_VIEW_STATE = {
  longitude: -77.0369, //center around Washington, D.C.
  latitude: 38.9072,
  zoom: 12,
  pitch: 0,
  bearing: 0
};

const deckgl = new DeckGL({
  initialViewState: INITIAL_VIEW_STATE,
  container: 'container',
  views: new MapView({repeat: true, controller: MapController}),
  mapStyle: "https://tiles.basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  //mapStyle: "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json",
  layers: [
    new ScatterplotLayer({
      data: [
        {position: [-77.0369, 38.9072], color: [255, 0, 0], radius: 100}
      ],
      getPosition: d => d.position,
      getFillColor: d => d.color,
      getRadius: d => d.radius
    })
  ]
});
```

<style>

.custom {
  display: flex;
  flex-direction: column;
  align-items: left;
  font-family: var(--sans-serif);
  margin: 0rem 0 2rem;
  text-wrap: balance;
  text-align: left;
}

.custom h1 {
  max-width: none;
  font-size: 10vw;
  font-weight: 800;
  line-height: 1;
  background: currentColor;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.custom h2 {
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .custom h1 {
    font-size: 60px;
  }
}

</style>