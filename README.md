# Mech Control Calculator #

![Screenshot Example](https://raw.githubusercontent.com/AfterAStorm/MechControlCalculator/refs/heads/main/media/screenshot1.png)

## How to use ##

Download the repository or ``git clone https://github.com/AfterAStorm/MechControlCalculator.git``

Run ``__main__.pyw`` via your prefered method

* Edit X, Y, and Z calculations via the entries
* See visualizations in the middle and top right corner
* Edit time scale/step with the two sliders respectively

## Equation Operators ##

* `+` -> You'll never add this up
* `-` -> Subtraction
* `*` -> Multiplication
* `/` -> Division
* `^` -> Pow, to the power of

## Equation variables ##

Variables to use in equations

* `dt` -> delta time, the current time, goes from ``0 - 1``, forever, snapping from 1 to 0 each loop

* `pi` -> pi
* `tau` -> pi * 2

## Equation methods ##

* `findKnee(angle)` (angle: radians) -> find the y value to make the knee angle *exactly* ``angle``

* `sin(angle)` (angle: radians) -> sine
* `cos(angle)` (angle: radians) -> cosine
* `tan(angle)` (angle: radians) -> tangent
* `asin(angle)` (x: ratio) -> arcsine
* `acos(angle)` (x: ratio) -> arccosine
* `atan(angle)` (x: ratio) -> arctangent
* `asinh(angle)` (x: ratio) -> hyperbolic arcsine
* `acosh(angle)` (x: ratio) -> hyperbolic arccosine
* `atanh(angle)` (x: ratio) -> hyperbolic arctangent
* `atan2(y, x)` (y & x: number) -> arctanget of y/x, signs are considered (lookup python3 atan2)
* `ceil(x)` (x: number) -> round ceiling aka round up
* `floor(x)` (x: number) -> round floor aka round down
* `sqrt(x)` (x: number) -> square root
* `sign(x)` (x: number) -> the sign of the number
    * \>0 = 1
    * 0 = 0
    * \<0 = -1
* `pow(x, y)` (x & y: number) -> x to the power of y, same as `x ^ y`
* `max(x, y)` (x & y: number) -> the maximum of two numbers
* `min(x, y)` (x & y: number) -> the minimum of two numbers
* `deg(rad)` (rad: radians) -> convert radians to degrees aka ``rad * (180 / pi)``
* `rad(deg)` (deg: degrees) -> convert degrees to radians aka ``deg * (pi / 180)``