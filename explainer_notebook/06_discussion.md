# 6. Discussion

#### What went well
The source of visualizations is obviously data. As this assignment basically started in the search of a data set,  
we spend a fair amount of time seeking out a data set of high quality and not just seemed interesting on the surface.
Eventually, we found the Chicago data sets that seemed promising. This was indeed the case, as we found the data sets 
to be rich and well-groomed with few missing data points and many interesting attributes, more than had time to cover in 
this project. This in turn resulted in a very smooth data cleaning and pre-processing phase that quickly launched us into
doing actual visualization work. Hence, taking the time to research a promising data was likely a good use of our time on this project.
For the visualizations, we have had a focus on temporal plots and animations which has shown interesting patterns of traffic
in different regions of the city through-out the day, month and the grander scheme of a whole year. Furthermore, the focus on
primary causes for traffic accidents enabling us to see which causes are most common on different times of the day.
  
#### What is still missing? What could be improved? Why?

At the outset of this project on of our main goals was to make a quantified assessment of how dangerous
the streets of Chicago is in terms of its regions and time of day, e.g. to state the probability of a
crash given location and time. 

By intuition, however, an increase in number of vehicles on the streets leads to an increase in occurrences of crashes.
This was early on verified by plotting the distribution of crashes throughout the hours of the day.  
This plot revealed spikes around the conventional times for commuting to and from work.
Simply concluding that these are the most dangerous times to participate in the traffic of Chicago would thus be an erroneous conclusion, 
at least on that basis. To be able to state if one region is generally more dangerous than another,
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

For future work, it could be interesting to access the amount of traffic more precisely, to be able to precisely visualize and assess which
 parts of the city has the highest change of a crash relatively to the amount of traffic. This would ultimately require a different means of
gathering the data, e.g. via satellite photos. 
