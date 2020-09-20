import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns

metrics = ['loop', 'backtrack']#, 'flip', 'unit']

#load the dataset
data = pd.read_csv('SingleCummulativeForEachConstraint_0_1011.csv')
print(data.describe())

#first, let's plot some stuff
data_grouped_by_n_constr = data.groupby(['numOfConstraints'])
medians = data_grouped_by_n_constr.median()

#plot developement of means
if False:
    for metric in metrics:
        plt.plot(medians[metric], label='mean')
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

# test if the ranks of the metrics values are correlated with number of constraints with
# kendall's tau
for metric in metrics:
    print('correlation for ' + metric)
    print(kendalltau(data['numOfConstraints'], data[metric]))