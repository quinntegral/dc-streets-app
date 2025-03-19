<script src="https://unpkg.com/maplibre-gl@3.0.0/dist/maplibre-gl.js"></script>

<div>
  <h1>D.C. safe school commutes dashboard </h1>
  <h2>visualizing traffic safety risks across school boundaries</h2>
</div>

<div style="width: 100%; position: relative;">
<div class=card style="max-width: 270px; position: absolute; top:0; margin-left: 14px; right: 14px; z-index:1;">

# street risk score
## as determined by method described here (link to page with writeup)

${colorLegend}

```js
const  streetToggle = view(Inputs.toggle({label: "Toggle street view", value: true}));
```

<div style="font-size: small; text-align: right; font-style: italic;"><a href="https://www.datadrivenstreets.org/">source link</a></div>

# priority adjustment
## use the sliders to adjust weight of factors in objective function

```js
const risk = view(Inputs.range([0, 10], {value: 1, label: "Risk Score", step: 1}));
const slider = view(Inputs.range([0, 10], {value: 1, label: "Distance", step: 1}));
```

# school level
## select school level to view

```js
const schoolLevel = view(Inputs.select(["None", "Elementary", "Middle", "High"], {value: "Elementary", label: "School Level"}));
```

</div>
<div id="container" style="background: rgb(18,35,48); height: 800px; width: 100%;"></div>
</div>

```js
// HTML ENDS, JS CODE STARTS HERE ******************************************************************************************************************

import {scaleThreshold} from "npm:d3-scale";
import deck from "npm:deck.gl";
import maplibregl from "npm:maplibre-gl";
const {DeckGL, MapView, MapController, GeoJsonLayer, ScatterplotLayer, AmbientLight, LightingEffect, PointLight} = deck;

const elemZonesJson = await FileAttachment("/data/map-assets/school-zones/elem-school-zones.geojson").json();
const msZonesJson = await FileAttachment("/data/map-assets/school-zones/middle-school-zones.geojson").json();
const hsZonesJson = await FileAttachment("/data/map-assets/school-zones/high-school-zones.geojson").json();
// also add school gps coordinates here
const streetJson = await FileAttachment("/data/map-assets/streets.geojson").json(); // note this
const censusBlocksJson = await FileAttachment("/data/map-assets/census-blocks.geojson").json();
const crashValues = streetJson.features.map(f => f.properties?.predicted_crashes_2022 || 0);

// color scale & legend

const COLOR_SCALE = d3.scaleSequential(d3.interpolateMagma)
  .domain([Math.max(...crashValues), Math.min(...crashValues)]);

const linearScale = d3.scaleLinear().domain([0, 5]).range(d3.extent(crashValues));

const colorRange = d3.range(6).map(i => {
  const value = linearScale(i);
  return { x: value, color: COLOR_SCALE(value) };
});

const colorLegend = Plot.plot({
  margin: 0,
  marginTop: 20,
  width: 270,
  height: 50,
  x: {padding: 0, round: false, axis: null, type: "band"},
  marks: [
    Plot.cellX(colorRange, {x: "x", fill: "color"}),
    Plot.text(["Fewer"], {frameAnchor: "top-left", dy: -12}),
    Plot.text(["More"], {frameAnchor: "top-right", dy: -12})
  ]
});

// interactivity

// map
// note: need incoming data to be in geojson format

function getLayerTooltip({ object, layer }) {
  if (!object) return null;
  switch (layer.id) {
    case 'streetLayer':
      return `${object.properties?.crash_count_2022 || 0} crashes here in 2022 (risk score will go here)`;
    case 'hsLayer':
      return `High School Zone: ${object.properties?.NAME || "Unknown"}`;
    case 'msLayer':
      return `Middle School Zone: ${object.properties?.NAME || "Unknown"}`;
    case 'elemLayer':
      return `Elementary School Zone: ${object.properties?.NAME || "Unknown"}`;
    default:
      return null; // other layers
  }
}

const INITIAL_VIEW_STATE = {
  longitude: -76.99, // center D.C.
  latitude: 38.89,
  zoom: 12,
  minZoom: 11.5,
  maxZoom: 19,
  pitch: 45,
  bearing: -15
};

// lighting
// const effects = [
//   new LightingEffect({
//     ambientLight: new AmbientLight({color: [255, 255, 255], intensity: 1.0}),
//     pointLight: new PointLight({color: [255, 255, 255], intensity: 0.8, position: [-0.144528, 49.739968, 80000]}),
//     pointLight2: new PointLight({color: [255, 255, 255], intensity: 0.8, position: [-3.807751, 54.104682, 8000]})
//   })
// ];

const deckInstance = new DeckGL({
  initialViewState: INITIAL_VIEW_STATE,
  getTooltip: getLayerTooltip,
  container: 'container',
  views: new MapView({repeat: true, controller: MapController}),
  //effects,
  interleaveLabels: true, // doesn't work sadly
  mapStyle: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  // dark mode labels "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
  // light mode labels "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  // no labels vers "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json"
  mapOptions: {attributionControl: false, compact: true}
});

// clean up if this code re-runs
invalidation.then(() => {
  deckInstance.finalize();
  container.innerHTML = "";
});

const borderRGB = [133, 211, 235, 255] // slightly darker blue: 149, 205, 222, 255]
deckInstance.setProps({
  layers: [
    new GeoJsonLayer({
    id: 'elemLayer',
    data: elemZonesJson,
    visible: schoolLevel === "Elementary",
    getFillColor: [255, 255, 255, 100], // blue [189, 213, 231, 100]
    getLineColor: borderRGB,
    getLineWidth: 50,
    lineWidthUnits: "meters",
    //autoHighlight: true,
    pickable: true
    }),
    new GeoJsonLayer({
    id: 'msLayer',
    data: msZonesJson,
    visible: schoolLevel === "Middle",
    getFillColor: [255, 255, 255, 100],
    getLineColor: borderRGB,
    getLineWidth: 50,
    lineWidthUnits: "meters",
    //autoHighlight: true,
    pickable: true
    }),
    new GeoJsonLayer({
    id: 'hsLayer',
    data: hsZonesJson,
    visible: schoolLevel === "High",
    getFillColor: [255, 255, 255, 100], // blue [189, 213, 231, 100]
    getLineColor: borderRGB,
    getLineWidth: 50,
    lineWidthUnits: "meters",
    //autoHighlight: true,
    pickable: true
    }),
    new GeoJsonLayer({
    id: 'streetLayer',
    data: streetJson,
    visible: streetToggle === true, // add a toggle???? maybe??
    getLineWidth: 3,
    lineWidthUnits: "pixels",
    lineJointRounded: true,
    lineCapRounded: true,
    getLineColor: f => {
      const crashes = f.properties?.crash_count_2022 || 0;
      const color = d3.color(COLOR_SCALE(crashes)); // Convert CSS color string to d3 color object
      return [color.r, color.g, color.b, 250]; // Extract RGB values properly
    },
    pickable: true,
    autoHighlight: true
    })
  ]
});

// JS CODE ENDS HERE ******************************************************************************************************************

```

Base map by © [CARTO](https://carto.com/platform), © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors

## header example

yippeee

yippeeeeeeeeee

## end page