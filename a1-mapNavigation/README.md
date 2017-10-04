# To execute
## ./route.py [start-city] [end-city] [routing-algorithm] [cost-function]
<br/>where routing-algorithm could be either bfs, dfs, uniform, or astar.
<br/>and cost-function could be either segments, distance, or time.

<br/>city-gps.txt contains one line per city, with three fields per line, delimited by spaces. The first field is the city, followed by the latitude, followed by the longitude.

<br/>road-segments.txt has one line per road segment connecting two cities. The space delimited fields are:

- first city
- second city
- length (in miles)
- speed limit (in miles per hour)
- name of highway
