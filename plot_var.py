import csv
import numpy as np
import matplotlib.pyplot as plt

import csv
import numpy as np
import matplotlib.pyplot as plt

with open('ground_truth_odom.log', 'r') as file:
    data = [line.strip().split() for line in file]
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Measurement', 'HedgePos X', 'HedgePos Y', 'OdomGlob X', 'OdomGlob Y'])
    for line in data:
        writer.writerow(line)

table = []
for measurement in range(1, 26):
    hedgepos_x = []
    hedgepos_y = []
    odomglob_x = []
    odomglob_y = [] 
    true_value = []
    good_measurement = False
    for row in data:
        # if len(row) == 3 and row[0] != measurement:
        #     good_measurement = False
        if len(row) == 3 and row[0] != str(measurement):
            good_measurement = False
        if len(row) == 3 and row[0] == str(measurement):
            true_value.append(float(row[1].split('(')[1].split(',')[0]))
            true_value.append(float(row[2].split(')')[0]))
            good_measurement = True
        if (good_measurement):
            if len(row) == 1:
                break
            elif row[2] == 'HedgePos,' and good_measurement:
                print('ROW', row)
                if float(measurement) == 5 or float(measurement) == 8:
                    hedgepos_x.append(float(row[3].split(':')[1].split(',')[0])) #[float(row.split()[1]) for row in data if row.split()[0] == str(measurement)]
                    hedgepos_y.append(float(row[4].split(':')[1].split(',')[0]))
                else:          
                    hedgepos_x.append(float(row[3].split(':')[1].split(',')[0])+0.091) #[float(row.split()[1]) for row in data if row.split()[0] == str(measurement)]
                    hedgepos_y.append(float(row[4].split(':')[1].split(',')[0]))
            elif row[2] == 'OdomGlob,' and good_measurement:
                print('ROW', row)
                if float(measurement)  == 5 or float(measurement) == 8:
                    odomglob_x.append(float(row[3].split(':')[1].split(',')[0])-0.091)
                    odomglob_y.append(float(row[4].split(':')[1].split(',')[0]))
                else:
                    odomglob_x.append(float(row[3].split(':')[1].split(',')[0]))
                    odomglob_y.append(float(row[4].split(':')[1].split(',')[0]))
    hedgepos_median_x = np.median(hedgepos_x)
    hedgepos_median_y = np.median(hedgepos_y)
    hedgepos_std_x = np.std(hedgepos_x)
    hedgepos_std_y = np.std(hedgepos_y)
    # hedgepos_variance = np.var(hedgepos_x + hedgepos_y)
    odomglob_median_x = np.median(odomglob_x)
    odomglob_median_y = np.median(odomglob_y)
    odomglob_std_x = np.std(odomglob_x)
    odomglob_std_y = np.std(odomglob_y)
    # odomglob_variance = np.var(odomglob_x + odomglob_y)
    # print('data:',[measurement, hedgepos_median_x, hedgepos_median_y, hedgepos_variance, odomglob_median_x, odomglob_median_y, odomglob_variance])
    table.append([measurement, true_value, hedgepos_median_x, hedgepos_median_y, hedgepos_std_x, hedgepos_std_y, odomglob_median_x, odomglob_median_y, odomglob_std_x, odomglob_std_y])

print('Measurement |   True Values   | HedgePos Median|    Variance    | OdomGlob Median |   Variance')
for row in table:
    measurement, true_value, hedgepos_median_x, hedgepos_median_y, hedgepos_std_x, hedgepos_std_y, odomglob_median_x, odomglob_median_y, odomglob_std_x, odomglob_std_y = row
    print(f'{measurement:11} | ({true_value[0]:.3f}, {true_value[1]:.3f}) |({hedgepos_median_x:.3f}, {hedgepos_median_y:.3f}) | ({hedgepos_std_x:.3f}, {hedgepos_std_y:.3f}) | ({odomglob_median_x:.3f}, {odomglob_median_y:.3f}) | ({odomglob_std_x:.3f}, {odomglob_std_y:.3f})')

true_values = [(row[0], row[1][0], row[1][1]) for row in table]
hedgepos_medians = [(row[0], row[2], row[3]) for row in table]
hedgepos_variances = [(row[0], row[4], row[5]) for row in table]
odomglob_medians = [(row[0], row[6], row[7]) for row in table]
odomglob_variances = [(row[0], row[8], row[9]) for row in table]


import matplotlib.pyplot as plt

true_values = [(row[0], row[1][0], row[1][1]) for row in table]
hedgepos_medians = [(row[0], row[2], row[3]) for row in table]
hedgepos_variances = [(row[0], row[4], row[5]) for row in table]
odomglob_medians = [(row[0], row[6], row[7]) for row in table]
odomglob_variances = [(row[0], row[8], row[9]) for row in table]

plt.figure(figsize=(8, 6))

# Plotting True Values
true_x = [value[1] for value in true_values]
true_y = [value[2] for value in true_values]
plt.scatter(true_x, true_y, color='red', label='True Values')

# Plotting HedgePos Median
hedgepos_x = [value[1] for value in hedgepos_medians]
hedgepos_y = [value[2] for value in hedgepos_medians]
plt.scatter(hedgepos_x, hedgepos_y, color='blue', label='HedgePos Median')

# Plotting HedgePos Variance
hedgepos_var_x = [value[1] for value in hedgepos_variances]
hedgepos_var_y = [value[2] for value in hedgepos_variances]
plt.errorbar(hedgepos_x, hedgepos_y, xerr=hedgepos_var_x, yerr=hedgepos_var_y, fmt='o', color='blue', alpha=0.2)

# Plotting OdomGlob Median
odomglob_x = [value[1] for value in odomglob_medians]
odomglob_y = [value[2] for value in odomglob_medians]
plt.scatter(odomglob_x, odomglob_y, color='green', label='OdomGlob Median')

# Plotting OdomGlob Variance
odomglob_var_x = [value[1] for value in odomglob_variances]
odomglob_var_y = [value[2] for value in odomglob_variances]
plt.errorbar(odomglob_x, odomglob_y, xerr=odomglob_var_x, yerr=odomglob_var_y, fmt='o', color='green', alpha=0.2)

plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()
plt.show()

import matplotlib.pyplot as plt

true_values = [(row[0], row[1][0], row[1][1]) for row in table]
hedgepos_medians = [(row[0], row[2], row[3]) for row in table]
hedgepos_variances = [(row[0], row[4], row[5]) for row in table]
odomglob_medians = [(row[0], row[6], row[7]) for row in table]
odomglob_variances = [(row[0], row[8], row[9]) for row in table]

plt.figure(figsize=(8, 6))

# Plotting True Values
true_x = [value[1] for value in true_values]
true_y = [value[2] for value in true_values]
plt.scatter(true_x, true_y, color='red', label='True Values')

# Plotting HedgePos Median
hedgepos_x = [value[1] for value in hedgepos_medians]
hedgepos_y = [value[2] for value in hedgepos_medians]
plt.scatter(hedgepos_x, hedgepos_y, color='blue', label='HedgePos Median')

# Plotting HedgePos Variance
hedgepos_var_x = [value[1] for value in hedgepos_variances]
hedgepos_var_y = [value[2] for value in hedgepos_variances]
plt.errorbar(hedgepos_x, hedgepos_y, xerr=hedgepos_var_x, yerr=hedgepos_var_y, fmt='o', color='blue', alpha=0.2)

# Plotting OdomGlob Median
odomglob_x = [value[1] for value in odomglob_medians]
odomglob_y = [value[2] for value in odomglob_medians]
plt.scatter(odomglob_x, odomglob_y, color='green', label='OdomGlob Median')

# Plotting OdomGlob Variance
odomglob_var_x = [value[1] for value in odomglob_variances]
odomglob_var_y = [value[2] for value in odomglob_variances]
plt.errorbar(odomglob_x, odomglob_y, xerr=odomglob_var_x, yerr=odomglob_var_y, fmt='o', color='green', alpha=0.2)

plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()

plt.axis('equal')  # Set x and y axes to have the same scale

plt.show()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

true_values = [(row[0], row[1][0], row[1][1]) for row in table]
odomglob_medians = [(row[0], row[6], row[7]) for row in table]

plt.figure(figsize=(8, 6))

# Calculate the error in x and y position
errors_x = [true_value[1] - odomglob_value[1] for true_value, odomglob_value in zip(true_values, odomglob_medians)]
errors_y = [true_value[2] - odomglob_value[2] for true_value, odomglob_value in zip(true_values, odomglob_medians)]

# Plotting the error as rectangles at the locations of the true values
for true_value, error_x, error_y in zip(true_values, errors_x, errors_y):
    rect = Rectangle((true_value[1] - error_x/2, true_value[2] - error_y/2), error_x, error_y, color='orange', alpha=0.5)
    plt.gca().add_patch(rect)

# Plotting True Values
true_x = [value[1] for value in true_values]
true_y = [value[2] for value in true_values]
plt.scatter(true_x, true_y, color='red', label='True Values')

plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()

plt.show()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

true_values = [(row[0], row[1][0], row[1][1]) for row in table]
odomglob_medians = [(row[0], row[6], row[7]) for row in table]

plt.figure(figsize=(8, 6))

# Calculate the error in x and y position
errors_x = [true_value[1] - odomglob_value[1] for true_value, odomglob_value in zip(true_values, odomglob_medians)]
errors_y = [true_value[2] - odomglob_value[2] for true_value, odomglob_value in zip(true_values, odomglob_medians)]

# Plotting the error as rectangles at the locations of the true values
# for true_value, error_x, error_y in zip(true_values, errors_x, errors_y):
#     rect = Rectangle((true_value[1] - error_x/2, true_value[2] - error_y/2), error_x, error_y, color='orange', alpha=0.5)
    # plt.gca().add_patch(rect)
    # plt.text(true_value[1], true_value[2], f'({true_value[1]}, {true_value[2]})', ha='center', va='bottom')

# Plotting Error in X and Y
# plt.scatter(errors_x, errors_y, color='blue', label='Error')
for error_x, error_y, true_value in zip(errors_x, errors_y, true_values):
    plt.text(error_x, error_y, f'({true_value[1]}, {true_value[2]})')
    plt.plot(error_x, error_y, marker='+', color='black')

plt.xlabel('Error in X Position')
plt.ylabel('Error in Y Position')
plt.legend()

# Set the limits of the x and y axes to zoom in on the points
plt.xlim(min(errors_x), max(errors_x))
plt.ylim(min(errors_y), max(errors_y))

plt.show()
