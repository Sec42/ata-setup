# ATA gnuradio hackaton notes

Just some notes and scripts from the [Allen Telescope Array](https://seti.org/sites/default/files/2020-06/ATA%20Interface%20Document%20V1.0.pdf) hacking weekend 2020-10-03.

## Infrastructure things:

- made a docker gr3.8 image (gnuradio38).

  Check source [Dockerfile](docker/Dockerfile), but see ISSUES below

- got pybombs running and made a working local gnuradio3.8 + [gr-iridium](https://github.com/muccc/gr-iridium) + [inspectrum](https://github.com/miek/inspectrum/) setup in `~/GR38`

  pybombs setup documentation is in https://github.com/Sec42/sec-gr/blob/master/README

  use with `source ~sec/GR38/setup_env.sh`

- some small python scripts for various [ATA-Utils](https://github.com/SETIatHCRO/ATA-Utils) functions
  - `~/ata_status.py` # fullscreen ascii status of the array
  - `~/ata_getfreq.py [antenna]` # print LO and focus for that antenna.
  - `~/ata_setfreq.py [antenna] [freq]` # set LO & focus for that antenna
  - `~/ata_atten.py [antenna] [attenuation]` # set attenuation for that antenna (both x&y pol) (20-31.5)
  - `~/ata_azel.py [az] [el] [antenna]` # position antenna. (e.g. use to manually stow with az=0 el=18)
  - `~/tracking/ata_tle.py [tlefile] [antenna]` # start tracking based on TLE
        TLE files are only two-line without name in them. there is `~/tracking/mktle.pl` to fetch the [iridium-NEXT celestrack TLEs](https://www.celestrak.com/NORAD/elements/iridium-NEXT.txt) and split it into appropriate files.

## Issues:

- had problems with apt-get inside docker container. Seemed to randomly fail
  when too many packages were downloaded at once. Some "hacky" workarounds in
  the Dokerfile to fix

- Walsh function makes decoding signals (BPSK/QPSK) nearly impossible.
  Need to figure out how to disable that for next time.

- Direct overpasses of iridium are still a bit to bright even with USRP gain=0
  and antenna attenuation=31.5.
  Need to check if there is a way to get even more attenuation...

- Look for previous work to record pointing and frequency changes into sigmf

- Find a way to get pointing info into sigmf for recording: maybe try to get
  ephemeris file from control and time-synchronize with recording

- Find a way to get sky frequency changes into sigmf for recording: each change
  requires new ssh connection which is slow, time based synchronisation is will
  be hard.

## Typical LEO satellite recording:
#####  activate the gnuradio 3.9-install in each shell by running

`source ~dkozel/activate-gr`

to get/activate gnuradio-3.9 (including [gr-ata](https://github.com/SETIatHCRO/gr-ata/))

##### setup ATA things (IF switch, gain, frequency, etc.) 
`./ifswitch.py`
- this sets IF switch, gain, frequency, etc.
- these values are currently hardcoded in the flowgraph.

keep this running until you are done. Run the rest in another terminal

##### Configure attenuation
`./ata_atten.py 1h 31.5`

- default set by gr-ata is 20.

Iridium is relatively strong, so we want max attenuation for now

##### start the tracking
`(cd tracking;./ata_tle.py IRIDIUM-110 1h)`

This command will return once the dish it reaches the starting position.

If the satellite has not yet risen above ~18° elevation, it will wait in the starting position. Check `~/ata_status.py` to see when the tracking starts.

##### start the recording
`./usrp_2chrx_save.py --gaindB=0`

this will start recording (ursp1, 12.5Msps, X-Polarisation) to test.cfile 

These values are currently hardcoded in the flowgraph.

Valid gain value is 0-60. 

##### monitor the recording
Check `~/ata_status.py` to see the dish tracking. 
When the satellite has moved out of view it will show "Stay Put".

##### end the recording
- hit `^c` when done to stop the recording

##### repeat if needed
You can repeat from "start the tracking" as many times as you want.

##### clean up / stow antenna
When you're done with everything

- hit enter in the `./ifswitch.py` terminal

This will stow the antenna and free everything.

## zeromq fft watching

The `./usrp_2chrx_save.py` also serves a one-per-second FFT via zeromq on port `50001`.

Check the `grc/ATA_ZMQ-display.grc` flowgraph to watch live from home.
