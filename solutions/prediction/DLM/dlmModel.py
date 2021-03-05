from pydlm import dlm, trend, dynamic, seasonality, autoReg, longSeason
import math

def DLM(data,
        predict_n,
        is_trend=False,
        trend_degree=0,
        trend_discount=1,
        is_seasonality=False,
        seasonality_period=96,
        seasonality_discount=1,
        is_long_season=False,
        long_season_n_period=7,
        long_season_period_duration=96,
        long_season_discount=0.99,
        is_auto_reg=False,
        auto_reg_degree=4,
        auto_reg_discount=0.99,
        is_dynamic=False,
        dynamic_train_features=None,
        dynamic_pred_features=None,
        dynamic_discount=0.99,
        cut_below_zero=True
        ):
    myDLM = dlm(data)

    if is_trend:
        myDLM = myDLM + trend(degree=trend_degree,
                              discount=trend_discount,
                              name="trend")

    if is_seasonality:
        myDLM = myDLM + seasonality(period=seasonality_period,
                                    discount=seasonality_discount,
                                    name="seasonality")

    if is_long_season:
        myDLM = myDLM + longSeason(data=data,
                                   period=long_season_n_period,
                                   stay=long_season_period_duration,
                                   discount=long_season_discount,
                                   name="long_season")

    if is_auto_reg:
        myDLM = myDLM + autoReg(degree=auto_reg_degree,
                                discount=auto_reg_discount,
                                name='auto_reg')

    if is_dynamic:
        myDLM = myDLM + dynamic(features=dynamic_train_features,
                                discount=dynamic_discount,
                                name="dynamic")

    myDLM.fit()

    if is_dynamic:
        values, var = myDLM.predictN(predict_n, featureDict=dynamic_pred_features)
    else:
        values, var = myDLM.predictN(predict_n)

    if cut_below_zero:
        for i, val in enumerate(values):
            if val < 0:
                values[i] = 0

    ret = {
        'data': data,
        'pred_values': values,
        'pred_variance': var,
        'fit': myDLM.getMean(filterType='backwardSmoother'),
    }
    ret['fit_error'] = [a-b for a, b in zip(ret['fit'], data)]
    ret['fit_abs_error'] = [math.fabs(a) for a in ret['fit_error']]
    ret['fit_sum_error'] = []
    s = 0
    for a in ret['fit_abs_error']:
        s += a
        ret['fit_sum_error'].append(s)

    if is_trend:
        ret['trend'] = myDLM.getMean(name='trend')
    if is_seasonality:
        ret['seasonality'] = myDLM.getMean(name='seasonality')
    if is_long_season:
        ret['long_season'] = myDLM.getMean(name='long_season')
    if is_auto_reg:
        ret['auto_reg'] = myDLM.getMean(name='auto_reg')
    if is_dynamic:
        ret["dynamic"] = myDLM.getMean(name="dynamic")
    return ret
