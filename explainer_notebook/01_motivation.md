# 1. Motivation
Two data sets are used for this project:
* Traffic Crashes - Crashes
* Chicago Traffic Tracker - Historical Congestion Estimates by Region - 2018-Current

In the following, these are referred to as the *Crashes* and *Congestion* data sets, respectively.
Both sets are freely available via [Chicago Data Portal](https://data.cityofchicago.org).

The Crashes data set contains information about each traffic crash on the streets of the City of Chicago.

The Congestion data set contains information about the congestion of the streets.
Congestion is estimated by probing GPS traces from the public transportation buses, yielding regional average speeds of
buses with 10 minutes intervals.

The combination of theses two data sets allows for relating each crash to one of the 29 defined regions of the City of
Chicago, as well as the estimated level of congestion at the time of the crash.

Through careful analysis of the data, the goal is to elicit interesting findings and convey them in an intuitive manner
to educate, non-scientific readers.