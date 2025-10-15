import pandas as pd
import statsmodels.formula.api as smf

def run_regressions(data_path='artifacts/cleaned_merged_dataset.csv', output_path='artifacts/regression.csv'):
    """
    Conduct two OLS regressions of median_earnings on independent variables with state-level clustering and save results to a CSV file.

    This function conducts two separate regression using data from a specified CSV file:
    1. Regresses 'median_earnings' on 'avgrk' (renamed from 'avgtk'), 'tuition', and their interaction,
       with clustering at the state level.
    2. Regresses 'median_earnings' on 'sat_score', 'tuition', and their interaction,
       with clustering at the state level.

    The results are combined into a single DataFrame, including coefficients, standard errors,
    t-statistics, p-values, confidence intervals, R-squared, and adjusted R-squared, and saved
    to a specified output CSV file.

    Parameters:
        data_path (str, optional): Path to the input CSV file containing the dataset.
                                  Defaults to 'artifacts/cleaned_merged_dataset.csv'.
        output_path (str, optional): Path to save the regression results CSV file.
                                    Defaults to 'artifacts/regression.csv'.

    Returns:
        None: The function saves the regression results to the specified CSV file and
              prints the summary for debugging purposes.
    """
    df = pd.read_csv(data_path)

    # Drop the observations with empty variables
    df = df.dropna(subset=['median_earnings', 'avgtk', 'sat_score', 'tuition', 'state'])
    df = df.rename(columns={'avgtk': 'avgrk'})

    # Regression 1: income on avgrk, tuition and their interactions, cluster on state
    formula1 = 'median_earnings ~ avgrk + tuition + avgrk:tuition'
    model1 = smf.ols(formula1, data=df)
    results1 = model1.fit(cov_type='cluster', cov_kwds={'groups': df['state']})

    # Regression 2: income on sat score, tuition and their interactions, cluster on state
    formula2 = 'median_earnings ~ sat_score + tuition + sat_score:tuition'
    model2 = smf.ols(formula2, data=df)
    results2 = model2.fit(cov_type='cluster', cov_kwds={'groups': df['state']})

    summary1 = results1.summary()
    summary2 = results2.summary()
    summary_table1 = pd.read_html(summary1.tables[1].as_html(), header=0, index_col=0)[0]
    summary_table2 = pd.read_html(summary2.tables[1].as_html(), header=0, index_col=0)[0]
    summary_table1['Model'] = 'OLS with State Clustering (avgrk)'
    summary_table1['R-squared'] = results1.rsquared
    summary_table1['Adj. R-squared'] = results1.rsquared_adj
    summary_table2['Model'] = 'OLS with State Clustering (sat_score)'
    summary_table2['R-squared'] = results2.rsquared
    summary_table2['Adj. R-squared'] = results2.rsquared_adj
    summary_table1['Model_Type'] = 'avgrk'
    summary_table2['Model_Type'] = 'sat_score'
    combined_table = pd.concat([summary_table1, summary_table2], axis=0)

    # Save the result to CSV
    combined_table.to_csv(output_path)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def get_text_positions(x_data, y_data, txt_width, txt_height):
    a = list(zip(y_data, x_data))
    text_positions = y_data.copy()
    for index, (y, x) in enumerate(a):
        local_text_coordinates = [i for i in a if i[0] > (y - txt_height) and abs(i[1] - x) < txt_width * 2 and i != (y, x)]
        if local_text_coordinates:
            sorted_ltp = sorted(local_text_coordinates)
            if abs(sorted_ltp[0][0] - y) < txt_height:
                differ = np.diff(sorted_ltp, axis=0)
                a[index] = (sorted_ltp[-1][0] + txt_height, x)
                text_positions[index] = sorted_ltp[-1][0] + txt_height * 1.01
                for k, (j, m) in enumerate(differ):
                    if j > txt_height * 2:
                        a[index] = (sorted_ltp[k][0] + txt_height, x)
                        text_positions[index] = sorted_ltp[k][0] + txt_height
                        break
    return text_positions

def text_plotter(ax, x_data, y_data, text_positions, texts, txt_width, txt_height):
    for x, y, t, text_label in zip(x_data, y_data, text_positions, texts):
        ax.annotate(text_label, (x, t), fontsize=11, ha='center', va='bottom', color='black',
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        if y != t:
            ax.plot([x, x], [y, t], color='black', alpha=0.3, linewidth=0.5, zorder=0)

def plot_scatter(df, state_style, x_col, x_label, title, x_median):
    plt.figure(figsize=(14, 10))
    for state, (marker, color) in state_style.items():
        state_data = df[df['state'] == state]
        plt.scatter(state_data[x_col], state_data['median_earnings'],
                    marker=marker, color=color, label=state, alpha=0.7, s=100)
    
    ax = plt.gca()
    ax.spines['left'].set_position(('data', x_median))
    ax.spines['bottom'].set_position(('data', df['median_earnings'].median()))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    
   
    df_sorted = df.sort_values(x_col).reset_index(drop=True)
    texts = df_sorted['school_name'].tolist()
    x_data = df_sorted[x_col].tolist()
    y_data = df_sorted['median_earnings'].tolist()
    
    
    y_range = abs(plt.ylim()[1] - plt.ylim()[0])
    x_range = abs(plt.xlim()[1] - plt.xlim()[0])
    txt_height = 0.04 * y_range
    txt_width = 0.02 * x_range
    
    text_positions = get_text_positions(x_data, y_data, txt_width, txt_height)
    
    
    text_plotter(ax, x_data, y_data, text_positions, texts, txt_width, txt_height)
    
    plt.xlabel(x_label, loc='right', fontsize=12, fontweight='bold')
    plt.ylabel('Median Earnings ($)', loc='top', fontsize=12, fontweight='bold')
    plt.legend(title='State', loc='center left', bbox_to_anchor=(1, 0.5),
               fontsize=10, frameon=True, facecolor='white', edgecolor='gray')
    plt.title(title, fontsize=14, pad=20)
    plt.tight_layout()
    plt.margins(x=0.1, y=0.1)
    plt.savefig(f'plot/{x_col}_vs_median_earnings.png', bbox_inches='tight', dpi=300)
    plt.close()

def generate_plots(csv_path='artifacts/cleaned_merged_dataset.csv'):
    
    os.makedirs('plot', exist_ok=True)
    
    df = pd.read_csv(csv_path)
    
    school_abbr = {
        "Princeton University": "Princeton",
        "Massachusetts Institute of Technology": "MIT",
        "Harvard University": "Harvard",
        "Stanford University": "Stanford",
        "Yale University": "Yale",
        "California Institute of Technology": "Caltech",
        "Duke University": "Duke",
        "Johns Hopkins University": "JHU",
        "Northwestern University": "Northwestern",
        "University of Pennsylvania": "UPenn",
        "University of Chicago": "Chicago",
        "Cornell University": "Cornell",
        "Brown University": "Brown",
        "Columbia University": "Columbia",
        "University of California, Los Angeles": "UCLA",
        "Dartmouth College": "Dartmouth",
        "University of California, Berkeley": "UCB",
        "Rice University": "Rice",
        "Vanderbilt University": "Vanderbilt",
        "University of Notre Dame": "Notre Dame",
        "University of Michigan--Ann Arbor": "UMich",
        "Washington University in St. Louis": "WashU",
        "Carnegie Mellon University": "CMU",
        "Georgetown University": "Georgetown",
        "Emory University": "Emory",
        "University of Virginia": "Virginia",
        "University of North Carolina--Chapel Hill": "UNC",
        "University of Southern California": "USC",
        "University of California, San Diego": "UCSD",
        "University of Florida": "Florida",
        "The University of Texas--Austin": "UT",
        "New York University": "NYU",
        "University of California, Davis": "UCD",
        "University of California, Irvine": "UCI",
        "Georgia Institute of Technology": "Georgia Tech",
        "University of Illinois Urbana-Champaign": "UIUC",
        "Boston College": "BC",
        "Tufts University": "Tufts",
        "University of California, Santa Barbara": "UCSB",
        "University of Wisconsin--Madison": "UWM",
        "Rutgers University--New Brunswick": "Rutgers",
        "Boston University": "BU",
        "The Ohio State University": "OSU",
        "University of Maryland, College Park": "Maryland",
        "University of Rochester": "Rochester",
        "University of Washington": "UW",
        "Purdue University--Main Campus": "Purdue",
        "University of Georgia": "Georgia",
        "Lehigh University": "Lehigh",
        "Northeastern University": "Northeastern"
    }
    
    df['school_name'] = df['school_name'].map(school_abbr).fillna(df['school_name'])
    
    states = df['state'].unique()
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'x', '+', '>', '<', 'd', 'P', 'H', 'X']
    colors = sns.color_palette("husl", len(states))
    state_style = {state: (markers[i % len(markers)], colors[i % len(colors)]) for i, state in enumerate(states)}
    
    def standardize_to_range(series):
        min_val = series.min()
        max_val = series.max()
        range_val = max_val - min_val
        if range_val == 0:
            return np.zeros_like(series)
        standardized = 2 * (series - min_val) / range_val - 1
        return standardized
    
    df['tuition_std'] = standardize_to_range(df['tuition'])
    df['sat_score_std'] = standardize_to_range(df['sat_score'])
    
    plot_scatter(df, state_style, 'sort_rank', 'School Rank (2026)', 'School Rank vs Median Earnings by State', df['sort_rank'].median())
    plot_scatter(df, state_style, 'tuition_std', 'Standardized Tuition', 'Standardized Tuition vs Median Earnings by State', 0)
    plot_scatter(df, state_style, 'sat_score_std', 'Standardized SAT Score', 'Standardized SAT Score vs Median Earnings by State', 0)
    plot_scatter(df, state_style, 'avgtk', 'Avg TK', 'Avg TK vs Median Earnings by State', df['avgtk'].median())

if __name__ == "__main__":
    # Adjust the path to match your Downloads folder
    csv_path = '~/Downloads/cleaned_merged_dataset.csv'
    generate_plots(csv_path)
