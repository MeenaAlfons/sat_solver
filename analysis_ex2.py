import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns

# settings
metrics = ['flip', 'unit']
average_data_over_runs = False

#load the dataset
data = pd.read_csv('results/combined_SingleCummulativeForEachConstraint_0_1011.csv')

#first, let's plot some stuff
# not averaging over runs:
if average_data_over_runs == False:
    data_grouped_by_n_constr = data.groupby(['numOfConstraints'])

#averaging over runs: comment next two lines if not desired
if average_data_over_runs == True:
    data_grouped_by_n_constr = data.groupby(['sudokuID', 'numOfConstraints']).mean().groupby(['numOfConstraints'])
    data=data.groupby(['sudokuID', 'numOfConstraints']).mean().reset_index()

medians = data_grouped_by_n_constr.median()

#plot developement of median
if False:
    for metric in metrics:
        plt.plot(medians[metric], label='median')
        plt.ylabel(metric+'s')
        plt.xlabel('number of constraints')
        plt.legend()
        plt.show()

#plt.hist(data[data['numOfConstraints']==15]['flip'], bins=100)
#plt.show()
# scatter plots
if False:
    for metric in metrics:
        plt.plot('numOfConstraints', metric, data=data, linestyle='', marker='o', markersize=0.5)
        plt.ylabel(metric + 's')
        plt.xlabel('number of constraints')
        plt.show()

# 2D density plots. Basically same as scatter plot but nicer to 'read'. But they don't manage to show anything.
if False:
    for metric in metrics:
        plt.hist2d(data['numOfConstraints'], data[metric], bins=[27, 70], cmap=plt.cm.Reds)
        plt.colorbar()
        plt.show()

# boxplots
if True:
    # add 1 for all values for visualization purposes
    ones = pd.Series([1 for i in range(len(data))])
    biased_data = data
    for metric in metrics:
        biased_data[metric] += ones
        boxplot = biased_data.boxplot(column=[metric],
                                      by=['numOfConstraints'],
                                      figsize=(8, 3),
                                      fontsize=22)
        plt.yscale('log')
        plt.title('')
        if metric != 'flip':
            plt.ylabel(metric+'s [log]', fontsize=21)
        else:
            plt.ylabel('conflicts [log]', fontsize=21)
        plt.grid(False)
        plt.xlabel('number of constraints', fontsize=21)
        plt.ylim(biased_data[metric].min()-1, biased_data[metric].max()+10)
        plt.suptitle('')
        plt.show()

# test if the ranks of the metrics values are correlated with number of constraints with
# kendall's tau
for metric in metrics:
    print('correlation for ' + metric)
    print(kendalltau(data['numOfConstraints'], data[metric]))

#seperate teset for dataset up to constraint 23 and from constraint 23 to 27.
#to see if it first inceases and then drops.
split_at = 14
for metric in metrics:
    print('\nCorrelation for ' + metric + ' for num of constraints 1-23')
    print(kendalltau(data['numOfConstraints'].loc[(data['numOfConstraints'] < split_at)],
                     data[metric].loc[(data['numOfConstraints'] < split_at)]))
    print('\nCorrelation for ' + metric + ' for num of constraints 23-27')
    print(kendalltau(data['numOfConstraints'].loc[(data['numOfConstraints'] > split_at)],
                     data[metric].loc[(data['numOfConstraints'] > split_at)]))