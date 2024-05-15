import pandas as pd
import numpy as np

def calculate_information_coefficient(predictions, labels):
    """
    计算信息系数 (IC)
    :param predictions: 预测值
    :param labels: 实际值
    :return: 信息系数值 (IC)
    """
    ic = predictions.corr(labels)
    return ic

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    """
    计算夏普比率
    :param returns: 投资组合收益率
    :param risk_free_rate: 无风险利率
    :return: 夏普比率
    """
    excess_returns = returns - risk_free_rate
    sharpe_ratio = excess_returns.mean() / excess_returns.std()
    return sharpe_ratio

def calculate_max_drawdown(cumulative_returns):
    """
    计算最大回撤
    :param cumulative_returns: 累积收益率
    :return: 最大回撤值
    """
    drawdown = cumulative_returns / cumulative_returns.cummax() - 1
    max_drawdown = drawdown.min()
    return max_drawdown

def evaluate_predictions(predictions, labels):
    """
    评估模型预测性能
    :param predictions: 预测值
    :param labels: 实际值
    :return: 评估指标字典
    """
    ic = calculate_information_coefficient(predictions, labels)
    metrics = {
        'IC': ic
    }
    return metrics

def evaluate_portfolio(returns, cumulative_returns, risk_free_rate=0.0):
    """
    评估投资组合性能
    :param returns: 投资组合收益率
    :param cumulative_returns: 累积收益率
    :param risk_free_rate: 无风险利率
    :return: 评估指标字典
    """
    sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate)
    max_drawdown = calculate_max_drawdown(cumulative_returns)
    metrics = {
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': max_drawdown
    }
    return metrics