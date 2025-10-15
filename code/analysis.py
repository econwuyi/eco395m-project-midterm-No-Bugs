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

# Run the function
if __name__ == "__main__":
    run_regressions()