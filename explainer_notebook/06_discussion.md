# 6. Discussion

#### What went well

#### What is still missing? What could be improved? Why?


At the outset of this project the overarching goal was to make a quantified assessment of how dangerous
the streets of Chicago is in terms of its regions and time of day—to state the probability of a
crash given location and time.

By intuition, however, an increase in number of vehicles on the streets leads to an increase in occurrences of crashes.
To be able to state if one region is generally more dangerous than another,
one would have to account for the _amount of traffic_ in the regions.

The ultimate measure for the amount of traffic would be the exact number of vehicles
passing any given location at any given time. Such data is _not_ available for the City of Chicago, if anywhere.

Instead, det Congestion data set provides estimates of the traffic congestion in terms of average speed of public
transportation buses; a lower average speed indicates a higher level of congestion.
It is—reasonably—assumed that a higher level of congestion means a higher amount of vehicles on the streets.
However, the average speed of buses is not only affected by other vehicles taking up space on the streets.
It is also affected by the number of commuters utilizing them; more commuters means the buses spend more time at each
bus stop, pushing the average speed downwards.

Though not the perfect solution, for this project traffic congestion where used as a measure for the amount of traffic.
