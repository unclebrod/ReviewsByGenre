# Initialize the workspace
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from itertools import combinations

# Always make it pretty.
plt.style.use('ggplot')
sns.set_style(style="whitegrid")

def coll_to_df(collections, names):
    '''
    Given a list of MongoDB collections and their associated names (for
    record keeping), this function returns that name and the collection as a
    dataframe

    Parameters:
    collections (list): list of MongoDB collections
    names (list of strings): list of names associated with collections, input
    in order

    Returns:
    df_list (list of tuples): list of name-dataframe tuples
    '''
    df_list = []
    for coll, name in zip(collections, names):
        df = pd.DataFrame(list(coll.find())).set_index('_id')
        if 'test' in df.columns:
            df.drop(columns='test', inplace=True)
        if True in df.duplicated(['album', 'artist']).values:
            df.drop_duplicates(['album', 'artist'], inplace=True)
        if coll == altcountry:
            df.drop(df.index[0], inplace=True)
        df_list.append((name, df))
    return df_list

def df_to_scores(df_list):
    '''
    Given a list of name-dataframe tuples (created in coll_to_df), this 
    function returns a list of name-arrays (specifically for 'score') tuples

    Parameters:
    df_list (list of tuples): list of name-dataframe tuples

    Returns:
    score_list (list of tuples): list of name-series tuples
    '''
    score_list = []
    for df in df_list:
        score_array = df[1]['score']
        score_list.append((df[0], score_array))
    return score_list

def plot_scores(score_list):
    '''
    Given a list of name-array tuples (created in df_to_scores), this 
    function plots their histograms and saves it.

    Parameters:
    score_list (list of tuples): list of name-series tuples
    '''
    fig, axs = plt.subplots(5, 5, figsize=(16, 16), sharex=True,
                            sharey=True)
    for (name, arr), ax in zip(score_list, axs.flatten()):
        ax.hist(arr, bins=15, density=True, color='cornflowerblue')
        ax.set_title(name.capitalize(), size=14)
    fig.tight_layout
    fig.suptitle('Normalized Review Score Counts by Genre', y=0.93,
                 size='xx-large', weight='bold',
                 stretch='expanded')
    fig.text(0.5, 0.1, 'Review Score', ha='center', va='center',
             size='xx-large', stretch='semi-expanded')
    fig.text(0.06, 0.5, 'Counts (Normalized)', ha='center', va='center',
             rotation='vertical', size='xx-large',
             stretch='semi-expanded')
    plt.savefig('images/genrehists.png')

def count_scores(score_list):
    '''
    Given a list of name-array tuples (created in df_to_scores), this 
    function provides the count of scores in each genre 

    Parameters:
    score_list (list of tuples): list of name-series tuples

    Returns:
    score_dict (dict): dictionary of genres and respective review counts
    '''
    score_dict = {}
    for name, array in score_list:
        score_dict[name] = len(array)
        print('The {} genre has {} recorded scores'.format(name, len(array)))
    return score_dict

def plot_by_genre(genre, score_list):
    '''
    Given a valid genre and a score_list, this function will plot the 
    histogram of that genre and save it.

    Parameters:
    genre (string): name of genre to plot
    score_list (list of tuples): list of name-series tuples
    '''
    df_tup = [tup for tup in score_list if tup[0] == genre]
    name = df_tup[0][0]
    df = df_tup[0][1].values
    plt.figure(figsize=(7, 5))
    ax = sns.distplot(df, kde=False, bins=15, color='plum')
    ax.set_title(f'Review Count for {name.capitalize()}', size=18)
    ax.set_xlabel('Review Score', size=14)
    ax.set_ylabel('Counts', size=14)
    plt.savefig('images/{}hist.png'.format(genre))

def plot_all_genres(score_list):
    '''
    Given a list of name-array tuples (created in df_to_scores), this 
    function plots the histogram of all reviews combined

    Parameters:
    score_list (list of tuples): list of name-series tuples

    Returns:
    all_scores (list): a list of all score values across genres
    '''
    all_scores = []
    for name, arr in score_list:
        all_scores.extend(arr.values)
    plt.figure(figsize=(7, 5))
    ax = sns.distplot(all_scores, kde=False, bins=30, color='darkmagenta')
    ax.set_title('Review Count for All Scores', size=18)
    ax.set_xlabel('Review Score', size=14)
    ax.set_ylabel('Counts', size=14)
    # I'm returning the all_scores matrix so I can do analysis on it later!
    plt.savefig('images/combinedhist.png')
    return all_scores

def plot_genre_counts(score_dict):
    '''
    Given a dictionary of genres and review counts, this function plots the
    review count of each genre

    Parameters:
    score_dict (dict): dictionary of genres and respective review counts
    '''
    sorted_scores_tups = sorted(score_dict.items(), key=lambda x: x[1])
    sorted_genres = []
    for tup in sorted_scores_tups:
        sorted_genres.append(tup[0].capitalize())
    sorted_scores = []
    for tup in sorted_scores_tups:
        sorted_scores.append(tup[1])
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(sorted_genres, sorted_scores, palette="Blues_d")
    ax.set_title('Review Count for All Genres', size=18)
    ax.set_xlabel('Genre', size=14)
    ax.set_ylabel('Count of Recorded Album Reviews', size=14)
    for tick in ax.get_xticklabels():
        tick.set_rotation(70)
    plt.savefig('images/genrecounts.png')

def plot_genre_means(score_list):
    '''
    Given a list of name-series tuples, this function plots the mean score
    of each genre

    Parameters:
    score_list (list of tuples): list of name-series tuples
    '''
    all_scores = []
    for name, arr in score_list:
        all_scores.extend(arr.values)
    genre_mean_dict = {}
    genre_mean_dict['All Genres'] = np.mean(all_scores)
    for genre, scores in score_list:
        genre_mean_dict[genre] = scores.mean()
    sorted_gm_dict = sorted(genre_mean_dict.items(), key=lambda x: x[1])
    sorted_genres = []
    for tup in sorted_gm_dict:
        sorted_genres.append(tup[0].capitalize())
    sorted_means = []
    for tup in sorted_gm_dict:
        sorted_means.append(tup[1])
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(sorted_genres, sorted_means, palette='Blues_d')
    ax.set_title('Mean Album Review Scores across Genres', size=18)
    ax.set_xlabel('Genre', size=14)
    ax.set_ylabel('Mean of Album Reviews', size=14)
    for tick in ax.get_xticklabels():
        tick.set_rotation(70)
    plt.savefig('images/genremeans.png')

def ttest_for_reviews(score_list, alpha=0.05):
    '''
    Given a list of name-array tuples (created in df_to_scores), this 
    function runs a Welch's t-test between all pairs with an Bonferroni
    correction.

    Parameters:
    score_list (list of tuples): list of name-series tuples
    alpha (float): desired alpha for each individual t-test

    Returns:
    results (list of tuples): list of tuples for any t-tests that provide an
    p-value less than alpha (Bonferroni corrected)
    '''
    results = []
    bonf = alpha / len(list(combinations(score_list, 2)))
    for x, y in combinations(score_list, 2):
        name1, name2, scores1, scores2 = x[0], y[0], x[1], y[1]
        tstat, pvalue = stats.ttest_ind(scores1, scores2, equal_var=False)
        if pvalue < bonf:
            results.append((name1, name2))
    return results

def ttest_for_rap(score_list, alpha=0.05):
    '''
    Given a list of name-array tuples (created in df_to_scores), this 
    function runs a Welch's t-test between rap and all other genres with
    a Bonferroni correction.

    Parameters:
    score_list (list of tuples): list of name-series tuples
    alpha (float): desired alpha for each individual t-test

    Returns:
    diff_list (list): list of genres for which we reject the null
    same_list (list): list of genres for which we fail to reject the null
    '''
    diff_list = []
    same_list = []
    bonf = 24
    for tup in score_list:
        if tup[0] == 'rap':
            rap_scores = tup[1]
    for tup in score_list:
        if tup[0] == 'rap':
            continue
        else:
            tstat, pvalue = stats.ttest_ind(rap_scores, tup[1],
                                            equal_var=False)
            if pvalue < alpha/2/bonf:
                diff_list.append(tup[0])
            else:
                same_list.append(tup[0])
    return diff_list, same_list

def compare_genres(score_list, genre1, genre2='rap', alpha=0.05):
    '''
    Given a list of name array tuples, two genres, and an alpha value, this
    function will plot the raw histogram of those genres, the normalized
    histogram of those two genres, and the distribution of their samples.
    It will also save this image.

    Parameters:
    score_list (list of tuples): list of name-series tuples
    genre1 (string): a genre of interest
    genre2 (string): a genre of interest
    alpha (float): the alpha value to be used for this test

    Returns:
    pvalue (float): the calculated p-value using a Welch's t-test
    '''
    df_tup1 = [tup for tup in score_list if tup[0] == genre1]
    name1 = df_tup1[0][0]
    df1 = df_tup1[0][1].values

    df_tup2 = [tup for tup in score_list if tup[0] == genre2]
    name2 = df_tup2[0][0]
    df2 = df_tup2[0][1].values

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 16))

    # Plot the raw histograms of two genres
    sns.distplot(df1, kde=False, bins=20, color='plum', ax=ax1,
                 label=f'{name1.capitalize()}')
    sns.distplot(df2, kde=False, bins=20, color='mediumseagreen', ax=ax1,
                 label=f'{name2.capitalize()}')
    ax1.set_title(f'Review Counts for {name1.capitalize()} and '
                  f'{name2.capitalize()}',
                  size=16)
    ax1.set_xlabel('Review Score', size=12)
    ax1.set_ylabel('Counts', size=12)
    ax1.legend()

    # Plot the normalized histograms of two genres
    sns.distplot(df1, kde=False, bins=20, color='plum', ax=ax2,
                 norm_hist=True, label=f'{name1.capitalize()}')
    sns.distplot(df2, kde=False, bins=20, color='mediumseagreen', ax=ax2,
                 norm_hist=True, label=f'{name2.capitalize()}')
    ax2.set_title(f'Normalized Review Counts for {name1.capitalize()} '\
                  f'and {name2.capitalize()} ',
                  size=16)
    ax2.set_xlabel('Review Score', size=12)
    ax2.set_ylabel('Counts (Normalized)', size=12)
    ax2.legend()

    # Plot the distributions of the samples and compare
    x = np.linspace(0, 100, 1000)
    norm1 = stats.norm(loc=np.mean(df1), scale=np.std(df1))
    norm2 = stats.norm(loc=np.mean(df2), scale=np.std(df2))

    sns.lineplot(x, norm1.pdf(x), color='plum', ax=ax3,
                 label=f'{name1.capitalize()}')
    sns.lineplot(x, norm2.pdf(x), color='mediumseagreen', ax=ax3,
                 label=f'{name2.capitalize()}')
    ax3.set_title(f'Sample Distributions for {name1.capitalize()} and '\
                  f'{name2.capitalize()}',
                  size=16)
    ax3.set_xlabel('Review Score', size=12)
    ax3.set_ylabel('Density', size=12)
    ax3.set_xlim(40, 100)
    ax3.axvline(x=np.mean(df1), ls='--', label=f'Mean ({name1})',
                c='mediumorchid')
    ax3.axvline(x=np.mean(df2), ls='--', label=f'Mean ({name2})',
                c='darkseagreen')
    ax3.axhline(c='black')
    ax3.set_ylim(bottom=0.000001)
    ax3.legend()
    plt.savefig(f'images/{genre1}{genre2}comp.png')

    # Determine if there is significance in the means of our genres
    tstat, pvalue = stats.ttest_ind(df1, df2, equal_var=False)
    conf = 100 - (alpha * 100)
    print(pvalue)
    if pvalue < alpha/2:
        print(f'With {conf}% confidence, we reject the null hypothesis '\
              'that these means are the same')
        return pvalue
    else:
        print(f'With {conf}% confidence, we fail to reject the null '\
              'hypothesis that these means are the same')
        return pvalue