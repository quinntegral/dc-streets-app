# DC Streets App

## Observable Information
The front-end of this project is an [Observable Framework](https://observablehq.com/framework/) app. To install the required dependencies, run ```npm install```. Then, to start the local preview server, run: ```npm run dev```.

Then visit <http://localhost:3000> to preview your app. For more, see <https://observablehq.com/framework/getting-started>.

A typical Framework project looks like this:

```ini
.
├─ src
│  ├─ components
│  │  └─ timeline.js           # an importable module
│  ├─ data
│  │  ├─ launches.csv.js       # a data loader
│  │  └─ events.json           # a static data file
│  ├─ example-dashboard.md     # a page
│  ├─ example-report.md        # another page
│  └─ index.md                 # the home page
├─ .gitignore
├─ observablehq.config.js      # the app config file
├─ package.json
└─ README.md
```

## Command reference

| Command           | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `npm install`            | Install or reinstall dependencies                        |
| `npm run dev`        | Start local preview server                               |
| `npm run build`      | Build your static site, generating `./dist`              |
| `npm run deploy`     | Deploy your app to Observable                            |
| `npm run clean`      | Clear the local data loader cache                        |
| `npm run observable` | Run commands like `observable help`                      |

## Project Notes
risk score calculation:
* currently using nathan todd's prediction model. if time, will pivot to better model

how long it takes to run intersections.py for each school level:
* high: 339.91 seconds
* middle: 557.20 seconds
* elem: 3498.79 seconds*

routing:
* we took low-cost, naive approach of drawing lines btwn blocks and schools, but it would be better to use google maps API in future

source list
* https://dcps.dc.gov/page/dcps-glance-enrollment

Documentation on schools included
* we include 75 elem schools and there are 74 elementary zones
  * D.C. marks 77 in [this list](https://enrolldcps.dc.gov/node/41). why the mismatch?
    * citywide/no boundary schools that are not included: Dorothy I. Height, Excel Academy
    * Peabody and Watkins are in one zone, Peabody-Watkins
    * Other notes/discrepancies to mention:
      * West Education Campus was renamed to John Lewis
      * Shirley Chisholm is in a zone called Tyler; it used to be called Tyler
      * John Francis Education Campus was renamed(?) to School Without Walls at Francis Stevens
* we include 21 middle schools and there are 21 middle school zones
  * Excel Academy is city-wide and not included
  * Cardozo is not on the list of middle schools published by DC on [this site](https://enrolldcps.dc.gov/node/41), but it is a middle school and has a zone
* 10 high schools and there are 10 high school zones
  * un-included schools are the 6 apply-in or other speciality schools: School Without Walls HS, Phelps ACE HS, Ellington School of the Arts, Banneker HS, McKinley Tech HS, Luke C. Moore

we use 2020 census blocks
* note: the geographic code identifier is the only unique identifier i think, not block number on its own
* 
