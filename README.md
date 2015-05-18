# Ionospheric test scenario

This repository contains files and information for the ionospheric model test scenario which was first proposed at AT-RASC 2015 and for which there is a dedicated session at ESWW12.

If you are interested in taking part in this test please contact Sean Elvidge: s.elvidge@bham.ac.uk

## The Scenario
Date: Dec 8th 2008 - Jan 7th 2009

Ionosonde stations to assimilate (if applicable): RL052, JR055, PQ052 .

GPS receivers to assimilate (if applicable): bor1, brus, gope, helg, hert, obec, opmt, pots, ptbb, wroc, wsr2t, zimm.

We will then ask the model owners to provide the electron density profile above DB049 (lat: 50.1, lon: 4.6) and differential slant TEC values for a set of given times and satellite positions (more details to be provided later).

## Code
`download_test_data.py` will download the GPS RINEX files and ionosonde SAO files for the stations in this test scenario, for the given times. By default it will download them to your current working directory into two subfolders, 'gps' and 'sao'. Or you can pass a location parameter to the code to specify a different location.

`download_truth_data.py` will download the truth/observation data used in the test scenario.

