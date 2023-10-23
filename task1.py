import pandas as pd

# Load the trade log data
trade_log = pd.read_csv('tradelog.csv')

# Initial portfolio value and risk-free interest rate
initial_portfolio_value = 6500
risk_free_rate = 0.05

# Total Trades
total_trades = len(trade_log)

# Profitable Trades
profitable_trades = len(trade_log[trade_log['Exit Price'] > trade_log['Entry Price']])

# Loss-Making Trades
loss_making_trades = len(trade_log[trade_log['Exit Price'] < trade_log['Entry Price']])

# Win Rate
win_rate = profitable_trades / total_trades

# Average Profit per trade
trade_log['Profit'] = (trade_log['Exit Price'] - trade_log['Entry Price'])
average_profit_per_trade = trade_log[trade_log['Profit'] > 0]['Profit'].mean()

# Average Loss per trade
average_loss_per_trade = trade_log[trade_log['Profit'] < 0]['Profit'].mean()

# Risk Reward Ratio
risk_reward_ratio = average_profit_per_trade / abs(average_loss_per_trade)

# Expectancy
loss_rate = 1 - win_rate
expectancy = (win_rate * average_profit_per_trade) - (loss_rate * abs(average_loss_per_trade))

# Calculate returns and volatility
trade_log['Returns'] = trade_log['Profit'] / initial_portfolio_value
volatility = trade_log['Returns'].std()

# Calculate Sharpe Ratio
sharpe_ratio = (expectancy - risk_free_rate) / volatility

# Calculate Max Drawdown
cumulative_returns = (1 + trade_log['Returns']).cumprod()
peak = cumulative_returns.expanding(min_periods=1).max()
drawdown = (cumulative_returns - peak) / peak
max_drawdown = drawdown.min()

# Max Drawdown Percentage
max_drawdown_percentage = max_drawdown * 100

# Calculate CAGR
ending_value = initial_portfolio_value + trade_log['Profit'].sum()
beginning_value = initial_portfolio_value
num_periods = total_trades
cagr = (ending_value / beginning_value) ** (1 / num_periods) - 1

# Calculate Calmar Ratio
calmar_ratio = cagr / max_drawdown

# Display the calculated parameters
print("Total Trades:", total_trades)
print("Profitable Trades:", profitable_trades)
print("Loss-Making Trades:", loss_making_trades)
print("Win Rate:", win_rate)
print("Average Profit per trade:", average_profit_per_trade)
print("Average Loss per trade:", average_loss_per_trade)
print("Risk Reward Ratio:", risk_reward_ratio)
print("Expectancy:", expectancy)
print("Average ROR per trade:", cagr)
print("Sharpe Ratio:", sharpe_ratio)
print("Max Drawdown:", max_drawdown)
print("Max Drawdown Percentage:", max_drawdown_percentage)
print("CAGR:", cagr)
print("Calmar Ratio:", calmar_ratio)

# Save the results to a CSV file
results = {
    'Parameter': ['Total Trades', 'Profitable Trades', 'Loss-Making Trades', 'Win Rate',
                 'Average Profit per trade', 'Average Loss per trade', 'Risk Reward Ratio',
                 'Expectancy', 'Average ROR per trade', 'Sharpe Ratio', 'Max Drawdown',
                 'Max Drawdown Percentage', 'CAGR', 'Calmar Ratio'],
    'Value': [total_trades, profitable_trades, loss_making_trades, win_rate,
              average_profit_per_trade, average_loss_per_trade, risk_reward_ratio,
              expectancy, cagr, sharpe_ratio, max_drawdown, max_drawdown_percentage,
              cagr, calmar_ratio]
}

results_df = pd.DataFrame(results)
results_df.to_csv('strategy_parameters.csv', index=False)
