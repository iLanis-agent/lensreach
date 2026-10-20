// Lens Reach engine: equivalent focal length against a 36 mm wide full frame sensor, the width and height a lens covers at a distance, and the distance that fits a subject. Exact integers on tenths, results rounded half up.
function _t(t, err, lo, hi) { // decimal text with at most one place -> tenths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _SW = "the sensor width must be from 1 to 60 mm with at most one decimal place";
var _SH = "the sensor height must be from 1 to 60 mm with at most one decimal place";
var _F = "the focal length must be from 1 to 1200 mm with at most one decimal place";
var _D = "the distance must be from 0.1 to 1000 m with at most one decimal place";
var _W = "the subject width must be from 0.1 to 1000 m with at most one decimal place";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _m(h) { return h === 0 ? "under 0.01 m" : _dec(h, 2) + " m"; } // hundredths of a metre

function equivTruth(sensorW, focal) {
  var sw = _t(sensorW, _SW, 10, 600), f = _t(focal, _F, 10, 12000);
  return "A " + _dec(f, 1) + " mm lens on a sensor " + _dec(sw, 1) + " mm wide frames like " + _dec(_hu(360 * f, sw), 1) + " mm on a 36 mm wide full frame sensor, a crop factor of " + _dec(_hu(36000, sw), 2) + " by width.";
}
function coverTruth(sensorW, sensorH, focal, dist) {
  var sw = _t(sensorW, _SW, 10, 600), sh = _t(sensorH, _SH, 10, 600), f = _t(focal, _F, 10, 12000), d = _t(dist, _D, 1, 10000);
  return "At " + _dec(d, 1) + " m, a " + _dec(f, 1) + " mm lens on a " + _dec(sw, 1) + " by " + _dec(sh, 1) + " mm sensor covers " + _m(_hu(10 * d * sw, f)) + " wide by " + _m(_hu(10 * d * sh, f)) + " high.";
}
function distanceTruth(sensorW, focal, subjW) {
  var sw = _t(sensorW, _SW, 10, 600), f = _t(focal, _F, 10, 12000), w = _t(subjW, _W, 1, 10000);
  return "To fit a " + _dec(w, 1) + " m wide subject across a " + _dec(sw, 1) + " mm wide sensor with a " + _dec(f, 1) + " mm lens, stand " + _m(_hu(10 * w * f, sw)) + " away.";
}
