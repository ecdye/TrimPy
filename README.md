# TrimPy
A basic tool for interfacing with Trimlight Select systems.

Install:
```
$ python3 -m pip install TrimPy
```

Usage:
```
$ python3 -m TrimPy
Usage: TrimPy [options]

Options:
  -h, --help            show this help message and exit
  -i IP, --ip=IP        IP address to connect to
  -m MODE, --mode=MODE  set trimlight to mode: timer, or manual
  -p PATTERN, --pattern=PATTERN
                        set trimlight to pattern: NEW_YEARS, VALENTINES,
                        ST_PATRICKS, MOTHERS_DAY, INDEPENDENCE_DAY, DEFAULT,
                        HALLOWEEN, THANKSGIVING, CHRISTMAS (also accepts
                        custom values in the form of integers representing the
                        pattern number) [default: DEFAULT]
  -n NAME, --set-name=NAME
                        set trimlight device name (< 25 characters)
  -d N, --dot-count=N   set trimlight device dot count (< 4096 dots)
  -q QUERY, --query-pattern=QUERY
                        query trimlight for information about pattern number
  -v, --verbose         make lots of noise [default: False]
  -V, --version         print version and exit

  Update Pattern:
    update a trimlight pattern number to match your liking

    --update-pattern=N  pattern number N to update
    --name=PATNAME      set pattern name (< 25 characters)
    --animation=ANIMATION
                        set animation style: STATIC, CHASE_FORWARD,
                        CHASE_BACKWARD, MIDDLE_TO_OUT, OUT_TO_MIDDLE, STROBE,
                        FADE, COMET_FORWARD, COMET_BACKWARD, WAVE_FORWARD,
                        WAVE_BACKWARD, SOLID_FADE
    --speed=SPEED       set animation speed [0-255]
    --brightness=BRIGHTNESS
                        set brightness [0-255]
    --color-one=R G B   set 'R G B' integer values for color index one
    --color-two=R G B   set 'R G B' integer values for color index two
    --color-three=R G B
                        set 'R G B' integer values for color index three
    --color-four=R G B  set 'R G B' integer values for for color index four
    --color-five=R G B  set 'R G B' integer values for color index five
    --color-six=R G B   set 'R G B' integer values for color index six
    --color-seven=R G B
                        set 'R G B' integer values for color index seven
    --count-one=N       set color index one to repeat N times [0-30]
    --count-two=N       set color index two to repeat N times [0-30]
    --count-three=N     set color index three to repeat N times [0-30]
    --count-four=N      set color index four to repeat N times [0-30]
    --count-five=N      set color index five to repeat N times [0-30]
    --count-six=N       set color index six to repeat N times [0-30]
    --count-seven=N     set color index seven to repeat N times [0-30]
```
