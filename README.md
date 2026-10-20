# Lens Reach

Lens equivalent and reach arithmetic. A 50 mm lens on a sensor 23.5 mm wide frames like 76.6 mm on a 36 mm wide full frame sensor, a crop factor of 1.53 by width.

## What it computes

- **The equivalent truth** - the focal length a lens frames like on a 36 mm wide full frame sensor, and the crop factor by width (sensor 1 to 60 mm wide, lens 1 to 1200 mm).
- **The coverage truth** - the width and height of the scene a lens covers at a distance (0.1 to 1000 m).
- **The distance truth** - how far away to stand to fit a subject 0.1 to 1000 m wide across the sensor.

## Boundary

Arithmetic only. The sensor size, focal length, distance and subject width are the owner's own entries, and the geometry is the simple distant-subject ratio. It has not seen any lens and does not know its focusing behaviour, distortion, crop modes or stabilisation, and it gives no verdict that a lens or camera is right for a shot or a purchase. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on tenths, half-up rounding).
- `oracle.py` - the Python mirror (Fractions of the entered numbers) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/lensreach/
Repo: https://github.com/iLanis-agent/lensreach
