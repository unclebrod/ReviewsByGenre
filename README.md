# Reviews By Genre: Analyzing How Album Review Scores Change Across Genres
The goal of this project is to explore how albums across various genres are reviewed by critics, based on normalized album reviews from Metacritic. While data across all genres are analyzed, I take a deeper look in particular at how rap album reviews differ from other genres.

# Background & Inspiration
Like most people, I'm a big fan of music. When I see recommendations on music, whether it be my from friends, publications, or social media, I add that new suggestion to a running list I keep on my Notes app. One of the albums to which I recently listened is "Don't Quit Your Day Job!", an album by Consequence (a former GOOD Music signee) that dropped in 2007. After a few spins, I wondered how this album was received by critics when it initially came out over a decade ago. I went to [Metacritic](https://www.metacritic.com) to see if I could find any content on the album. The website assigns scores to albums (similar to Rotten Tomatoes), based on its own normalizing criteria. While the album ultimately didn't have any reviews on the site, it did lead me into a rabbit hole of reading other available reviews, and in this process I began to think: are there discrepancies in how genres are ultimately reviewed and scored? Do some tend to be treated more leniently or harshly than others? My motivation was to see if I could draw real insights from the available music review scores.

# Hypothesis
While I explored all of the data I received across all genres (see below for my EDA), I keyed in on the available reviews for rap albums. I compared rap to all other genres. I had no specific theories on the genres from which rap would be different, but I felt that there had to be differences with at least a handful.

* H<sub>0</sub>: The mean album review score from rap and each other genre, respectively, is the same 
* H<sub>A</sub>: The mean album review score from rap and each other genre, respectively, is different

These analyses were completed using a two-tailed Welch's t-test between rap and each genre respectively to account for the differences in sample size. All genres analyzed had a sample size of at least 37. I used an alpha of 0.05 with a Bonferroni correction to account for familywise errors across the 24 tests completed.

# Data
I scraped all data from [Metacritic](https://www.metacritic.com/browse/albums/genre/date/alt-country), which conveniently has a "Browse by Genre" page. All available data from all available genres were collected, except for "comedy" and "psychedelic" due to limited data. My webscraper uses Beautiful Soup, and while collecting this data it stores it dynamically into a MongoDB database. I collected the scores (called Metascores by the site), album titles, artists, and dates. Each genre was placed into its own collection.

Upon completion, I used an SFTP to grab all of this data, and using PyMongo & Pandas I converted the collections into dataframes for easy manipulation.

In total, I collected 16,604 rows of data across genres. My analysis focuses entirely on the Metascore values.

# Exploratory Data Analysis

# Results

# Technologies
* Python (including Seaborn, Matplotlib, PyMongo, Beautiful Soup, SciPy, Pandas, and Numpy)
* MongoDB
* Amazon EC2

# Looking Forward
I'm particularly interested in knowing if there are different inferences we can draw between user and critic scores. Metacritic assigns scores by taking critic reviews and assigning a number that is specific to their system (you can read more about it [here](https://www.metacritic.com/faq#item11) - users provide scores between 0 and 10. Given this discrepancy, I wonder if there are material differences between the two (are they the same in the aggregate, or do users tend to be harsher/lenient?)

As I grow my skills, I'd like to return and look more specifically at user reviews and their associated comments. I believe I can gather real insights using natural language processing to see how comments vary across the range of reviews.

Lastly, I'd also be interested in exploring if reviews have changed over the years. Data for dates is not quite as robust across the site, but given the vast number of websites dedicated to music, I'm sure it could be done by obtaining and combining multiple datasets if not solely through Metacritic.

# Acknowledgements
A big thanks to Dan Rupp, Juliana Duncan, Peter Galea, and Austin Penner, each of whom poured a lot of their time and energy in helping me complete this project. A special thanks, too, to [Metacritic](https://www.metacritic.com) which is where I received all data used for this project.
