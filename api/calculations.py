import numpy as np

# Calculate the total return (%)
def calculate_total_return(trades):
    initial_balance = trades[0]['balance'] if trades else 0
    final_balance = trades[-1]['balance'] if trades else 0
    if initial_balance > 0:
        return ((final_balance - initial_balance) / initial_balance) * 100
    return 0

# Calculate the max drawdown (%)
def calculate_max_drawdown(trades):
    if not trades:
        return 0
    balances = [trade['balance'] for trade in trades]
    max_drawdown = 0
    peak = balances[0]
    for balance in balances:
        if balance > peak:
            peak = balance
        drawdown = (peak - balance) / peak
        max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown * 100

# Calculate the Sharpe Ratio
def calculate_sharpe_ratio(trades, risk_free_rate=0.01):
    if not trades:
        return 0
    returns = [trade['profit'] / trade['balance'] for trade in trades if trade['balance'] > 0]
    if len(returns) < 2:
        return 0
    avg_return = np.mean(returns)
    std_dev_return = np.std(returns)
    sharpe_ratio = (avg_return - risk_free_rate) / std_dev_return if std_dev_return != 0 else 0
    return sharpe_ratio

# Update performance metrics
def update_performance_metrics(user):
    from core.models import Trade, PerformanceMetrics  # Import your models
    trades = Trade.objects.filter(user=user).order_by('date')
    trades_data = [
        {'balance': trade.balance, 'profit': trade.profit}
        for trade in trades
    ]
    total_return = calculate_total_return(trades_data)
    max_drawdown = calculate_max_drawdown(trades_data)
    sharpe_ratio = calculate_sharpe_ratio(trades_data)

    # Update or create the metrics entry
    metrics, _ = PerformanceMetrics.objects.get_or_create(user=user)
    metrics.total_return = total_return
    metrics.max_drawdown = max_drawdown
    metrics.sharpe_ratio = sharpe_ratio
    metrics.save()
    