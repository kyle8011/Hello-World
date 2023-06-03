# Overview

Data analysis is important for many software engineers and programmers. They need to know how do deal with data and organize it to draw conclusions. For this reason I have learned how to do basic data analysis with this software.

The data sets that I have chosen include rating comparisons between different games that can be related between genres, consoles, and release date.
I found the data sets on kaggle.com:
* [kaggle](https://www.kaggle.com/datasets/mohamedhanyyy/video-games)

My purpose for writing this software is to answer some questions about the relationship between genres, platforms, and ratings. Specifically, what genre of game has the highest ratings and which console has the highest rating.

[Software Demo Video](https://youtu.be/5ZPyavZ2svI)

# Data Analysis Results

Which three genres have the highest ratings?
Visual Novel (8.01/10), Turn Based Strategy (7.77/10), RPG (7.67/10)

Which three consoles have the highest ratings?
With no filter
IOS - Apple (8.03/10), WEB (8/10), MAC (7.86/10)
With a filter (games unique to a single console)
IOS - Apple (8.17/10), WEB (8/10), NS - Nintendo Switch (7.1/10)

# Development Environment

I used R language via the extension in VS Code. This coding language is helpful with dataframes, tables, and has several graphing options. There is plenty of info online.

I didn't include any extra libraries, but used some functions that can read from a csv file, print graphs, clean strings, and manipulate data.

# Useful Websites

* [r graph gallery](https://r-graph-gallery.com/)
* [geeksforgeeks](https://www.geeksforgeeks.org/r-charts-and-graphs/#)
* [w3schools](https://www.w3schools.com/r/r_graph_bars.asp)
* [bookdown](https://bookdown.org/dli/rguide/bar-graph.html#basic-r-bar-graph)

# Future Work

* Make some comparisons having to do with the companies and number of playthroughs.
* Make some more exciting charts like circular ones.
* Match games between the two datasets and compare their ratings.