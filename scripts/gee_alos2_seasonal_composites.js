// gee_alos2_seasonal_composites.js
// ALOS‑2 PALSAR‑2 ScanSAR L2.2 seasonal composites and delta map.
// Dataset: JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR
// gamma0 (dB) = 10*log10(DN^2) - 83  (per GEE docs)

var aoi = ee.Geometry.Rectangle([-57.0, -3.0, -54.0, -1.0]); // TODO: update
var start = '2015-01-01';
var end   = '2025-01-01';
var pol   = 'HH'; // or 'HV'

var addMonth = function(img) {
  var m = ee.Date(img.get('system:time_start')).get('month');
  return img.set('month', m);
};

var toDb = function(img) {
  var dn = img.select([pol]);
  var db = dn.pow(2).log10().multiply(10).subtract(83).rename(pol + '_db');
  return img.addBands(db, null, true);
};

var col = ee.ImageCollection('JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR')
  .filterBounds(aoi).filterDate(start, end)
  .map(addMonth).map(toDb);

var wetMonths = ee.List([12,1,2,3,4,5]);
var dryMonths = ee.List([6,7,8,9,10,11]);

var wet = col.filter(ee.Filter.inList('month', wetMonths)).median().select([pol + '_db']).rename('wet_db');
var dry = col.filter(ee.Filter.inList('month', dryMonths)).median().select([pol + '_db']).rename('dry_db');
var delta = wet.subtract(dry).rename('delta_db');

Map.centerObject(aoi, 8);
Map.addLayer(wet, {min: -20, max: 5}, 'wet_db');
Map.addLayer(dry, {min: -20, max: 5}, 'dry_db');
Map.addLayer(delta, {min: -5, max: 5}, 'delta_db');

// List contributing IDs (first 20 shown)
print('Wet IDs', col.filter(ee.Filter.inList('month', wetMonths)).aggregate_array('system:index').slice(0,20));
print('Dry IDs', col.filter(ee.Filter.inList('month', dryMonths)).aggregate_array('system:index').slice(0,20));
