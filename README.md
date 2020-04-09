# Reviews By Genre: Analyzing How Album Review Scores Change Across Genres

The goal of this project is to explore how genre

# Background & Inspiration
Like most people, I'm a big fan of music. In my free time, I'm usually consuming music in one way or another, and I'm always looking for new artists & albums to explore. When I see recommendations on music, whether it be my from friends, publications, social media, or just from hearing something new, I add that new suggestion to a running list I keep on my Notes app. One of the albums that I got around to listening to is "Don't Quit Your Day Job!", an album by Consequence (a former GOOD Music signee), that dropped back in 2007. After a few spins, I started to wonder how this album was received by critics when it initially came out over a decade ago. I went to Metacritic, a website that aggregates music, video game, television, and movie reviews from reputable critics, to see if I could find any content on the album. The website assigns scores to albums (similar to Rotten Tomatoes), based on its own normalizing criteria. While it ultimately didn't have any reviews on the site, it did lead me into a rabbit hole of reading other available reviews, and in this process I began to think: are there discrepancies in how genres are ultimately reviewed and scored? Do some tend to be treated more leniently or harshly than others?

# Technologies
* Python (including Seaborn, Matplotlib, PyMongo, Beautiful Soup, SciPy, Pandas, and Numpy)
* MongoDB
* Amazon EC2

# Looking Forward
I believe there are many directions to go from here, both with the data I've collected and with other data from Metacritic that I did not. I'm particularly interested in knowing if there are different inferences we can draw between user and critic scores. Metacritic assigns scores by taking critic reviews and assigning a number that is specific to their system - users provide scores between 0 and 10. Given this discrepancy, I wonder if there are material differences between the two (are they the same in the aggregate, or do users tend to be harsher?)

As I grow my skills, I'd also like to return and look more specifically at user reviews and their associated comments. I believe I could gather real insights from by using natural language processing to see how comments vary across the range of reviews.

Lastly, I'd also be interested in exploring if reviews have changed over the years. Data for dates is not quite as robust across the site, but given the vast number of websites dedicated to music, I'm sure it could be done by obtaining and combining multiple datasets if not solely through Metacritic.

# Acknowledgements
A big thanks to Dan Rupp, Juliana Duncan, Peter Galea, and Austin Penner, each of whom poured a lot of their time and energy in helping me complete this assignment. A special thanks, too, to Metacritic which is where I received all data used for this project.
