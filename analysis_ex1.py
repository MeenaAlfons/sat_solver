import pandas
from pandas import DataFrame
from matplotlib import pyplot as plt
from scipy.stats import shapiro, friedmanchisquare, wilcoxon
from scikit_posthocs import posthoc_nemenyi_friedman

# load the data
data = pandas.read_csv('results/SolverComparison_0_1011.csv')

# group data by solver
grouped_data = data.groupby(by=['name'])
print(grouped_data)

columns = ['DLIS(True)', 'DLIS(False)', 'JW-OS', 'DLCS', 'Dummy', 'RandomFalse', 'Random']

# split data for easier comparison
loop_data = DataFrame(columns=columns,
                      index=range(1, int(len(data)/5)+1))
flip_data = DataFrame(columns=columns,
                      index=range(1, int(len(data)/5)+1))
backtrack_data = DataFrame(columns=columns,
                      index=range(1, int(len(data)/5)+1))
unit_data = DataFrame(columns=columns,
                      index=range(1, int(len(data)/5)+1))
split_data = {'loop':loop_data, 'flip':flip_data, 'backtrack':backtrack_data, 'unit':unit_data}

# fill in the values
for key, _ in grouped_data:
    curr_group=grouped_data.get_group(key).set_index(['sudokuID'])

    loop_data[key] = curr_group['loop']
    flip_data[key] = curr_group['flip']
    backtrack_data[key] = curr_group['backtrack']
    unit_data[key] = curr_group['unit']

# plot boxplots
if True:
    for curr_data in split_data:
        df = split_data[curr_data]
        col = df.columns.values
        boxplot = df.boxplot(column=columns,
                             grid=False)
        plt.ylabel(f'{curr_data}s')
        plt.ylim(0, 650)
        plt.show()

#Analysis of normality for the data: (none is normally distributed)
for curr_data in split_data:
    print('\n' + curr_data + ' data:')
    for solver in split_data[curr_data].columns.values:
        print('Normality test for ' + solver)
        print(shapiro(loop_data[solver]))

# Is there at least one solver which is significantly better?
# -> The performances are significantly different with p approx. 0
for curr_data in split_data:
    print('\n' + curr_data + ' friedman test:')
    print(friedmanchisquare(split_data[curr_data]['DLIS(True)'],
                            split_data[curr_data]['DLIS(False)'],
                            split_data[curr_data]['JW-OS'],
                            split_data[curr_data]['DLCS'],
                            split_data[curr_data]['Dummy'],
                            split_data[curr_data]['RandomFalse'],
                            split_data[curr_data]['Random']))

    # pvalue matrix for pairwise test
    # Indicates that for all metrics Dummy and DLIS(True) are not
    # significantly different. Neither are the other solvers between
    # them.
    print('\nPairwise comparison:')
    print(posthoc_nemenyi_friedman(split_data[curr_data].values))

# Test whether there is a significant difference between Dummy and DLIS(True). #todo: this part is flawed
'''for curr_data in split_data:
    if False:
        split_data[curr_data].boxplot(column=['Dummy', 'DLIS(True)'])
        plt.title(curr_data)
        plt.ylim(0, 40)
        plt.show()
    print('\nWilcox test for Dummy against DLIS(True) for ' + curr_data + ' counts: ')
    print('means: randomfalse: ' + str(split_data[curr_data]['RandomFalse'].mean()) + '\t dlis(true): ' +str(split_data[curr_data]['DLIS(True)'].mean()))
    one=np.array(split_data[curr_data]['RandomFalse']).flatten()
    two=np.array(split_data[curr_data]['DLIS(True)']).squeeze()
    print(wilcoxon(np.array(split_data[curr_data]['RandomFalse']),
                   np.array(split_data[curr_data]['DLIS(True)'])))'''
