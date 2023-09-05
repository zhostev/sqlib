### worldquant101

Alpha#1:
$$
(\text{rank}(\text{Ts\_ArgMax}(\text{SignedPower}(((\text{returns} < 0) ? \text{stddev}(\text{returns}, 20) : \text{close}), 2.), 5)) - 0.5)
$$
Alpha#2: 
$$
(-1 \times \text{correlation}(\text{rank}(\text{delta}(\log(\text{volume}), 2)), \text{rank}(((\text{close} - \text{open}) / \text{open})), 6))
$$
Alpha#3: 
$$
(-1 \times \text{correlation}(\text{rank}(\text{open}), \text{rank}(\text{volume}), 10))
$$
Alpha#4: 
$$
(-1 \times \text{Ts\_Rank}(\text{rank}(\text{low}), 9))
$$
Alpha#5: 
$$
(\text{rank}((\text{open} - (\text{sum}(\text{vwap}, 10) / 10))) \times (-1 \times \text{abs}(\text{rank}((\text{close} - \text{vwap})))))
$$
Alpha#6: 
$$
(-1 \times \text{correlation}(\text{open}, \text{volume}, 10))
$$
Alpha#7: 
$$
((\text{adv20} < \text{volume}) ? ((-1 \times \text{ts\_rank}(\text{abs}(\text{delta}(\text{close}, 7)), 60)) \times \text{sign}(\text{delta}(\text{close}, 7))) : (-1 \times 1))
$$
Alpha#8: 
$$
(-1 \times \text{rank}(((\text{sum}(\text{open}, 5) \times \text{sum}(\text{returns}, 5)) - \text{delay}((\text{sum}(\text{open}, 5) \times \text{sum}(\text{returns}, 5)), 10))))
$$
Alpha#9:
$$
((0 < \text{ts\_min}(\text{delta}(\text{close}, 1), 5)) ? \text{delta}(\text{close}, 1) : ((\text{ts\_max}(\text{delta}(\text{close}, 1), 5) < 0) ? \text{delta}(\text{close}, 1) : (-1 \times \text{delta}(\text{close}, 1))))
$$
Alpha#10: 
$$
\text{rank}(((0 < \text{ts\_min}(\text{delta}(\text{close}, 1), 4)) ? \text{delta}(\text{close}, 1) : ((\text{ts\_max}(\text{delta}(\text{close}, 1), 4) < 0) ? \text{delta}(\text{close}, 1) : (-1 \times \text{delta}(\text{close}, 1)))))
$$
Alpha#11:
$$
((\text{rank}(\text{ts\_max}((\text{vwap} - \text{close}), 3)) + \text{rank}(\text{ts\_min}((\text{vwap} - \text{close}), 3))) \times \text{rank}(\text{delta}(\text{volume}, 3)))
$$
Alpha#12:
$$
(\text{sign}(\text{delta}(\text{volume}, 1)) \times (-1 \times \text{delta}(\text{close}, 1)))
$$
Alpha#13: 
$$
(-1 \times \text{rank}(\text{covariance}(\text{rank}(\text{close}), \text{rank}(\text{volume}), 5)))
$$
Alpha#14: 
$$
((-1 \times \text{rank}(\text{delta}(\text{returns}, 3))) \times \text{correlation}(\text{open}, \text{volume}, 10))
$$
Alpha#15: 
$$
(-1 \times \text{sum}(\text{rank}(\text{correlation}(\text{rank}(\text{high}), \text{rank}(\text{volume}), 3)), 3))
$$
Alpha#16: 
$$
(-1 \times \text{rank}(\text{covariance}(\text{rank}(\text{high}), \text{rank}(\text{volume}), 5)))
$$
Alpha#17:
$$
(((-1 \times \text{rank}(\text{ts\_rank}(\text{close}, 10))) \times \text{rank}(\text{delta}(\text{delta}(\text{close}, 1), 1))) \times \text{rank}(\text{ts\_rank}((\text{volume} / \text{adv20}), 5)))
$$
Alpha#18:
$$
(-1 \times \text{rank}(((\text{stddev}(\text{abs}((\text{close} - \text{open})), 5) + (\text{close} - \text{open})) + \text{correlation}(\text{close}, \text{open}, 10))))
$$
Alpha#19: 
$$
(((-1 \times \text{sign}((\text{close} - \text{delay}(\text{close}, 7))) + \text{sign}(\text{delta}(\text{close}, 7)))) \times (1 + \text{rank}(1 + \text{sum}(\text{returns}, 250))))
$$
Alpha#20: 
$$
(((-1 \times \text{rank}((\text{open} - \text{delay}(\text{high}, 1)))) \times \text{rank}((\text{open} - \text{delay}(\text{close}, 1)))) \times \text{rank}((\text{open} - \text{delay}(\text{low}, 1))))
$$
Alpha#21: 
$$
((((\text{sum}(\text{close}, 8) / 8) + \text{stddev}(\text{close}, 8)) < (\text{sum}(\text{close}, 2) / 2)) ? (-1 \times 1) : (((\text{sum}(\text{close}, 2) / 2) < ((\text{sum}(\text{close}, 8) / 8) - \text{stddev}(\text{close}, 8))) ? 1 : (((1 < (\text{volume} / \text{adv20})) || ((\text{volume} / \text{adv20}) == 1)) ? 1 : (-1 \times 1))))
$$
Alpha#22: 
$$
(-1 \times (\text{delta}(\text{correlation}(\text{high}, \text{volume}, 5), 5) \times \text{rank}(\text{stddev}(\text{close}, 20))))
$$
Alpha#23: 
$$
((\text{sum}(\text{high}, 20) / 20) < \text{high}) ? (-1 \times \text{delta}(\text{high}, 2)) : 0$
$$
Alpha#24:
$$
((((\text{delta}((\text{sum}(\text{close}, 100) / 100), 100) / \text{delay}(\text{close}, 100)) < 0.05) || ((\text{delta}((\text{sum}(\text{close}, 100) / 100), 100) / \text{delay}(\text{close}, 100)) == 0.05)) ? (-1 \times (\text{close} - \text{ts\_min}(\text{close}, 100))) : (-1 \times \text{delta}(\text{close}, 3)))
$$
Alpha#25:
$$
\text{rank}((((-1 \times \text{returns}) \times \text{adv20}) \times \text{vwap}) \times (\text{high} - \text{close}))
$$
Alpha#26: 
$$
(-1 \times \text{ts\_max}(\text{correlation}(\text{ts\_rank}(\text{volume}, 5), \text{ts\_rank}(\text{high}, 5), 5), 3))
$$
Alpha#27: 
$$
((0.5 < \text{rank}((\text{sum}(\text{correlation}(\text{rank}(\text{volume}), \text{rank}(\text{vwap}), 6), 2) / 2.0))) ? (-1 \times 1) : 1)
$$
Alpha#28: 
$$
\text{scale}(((\text{correlation}(\text{adv20}, \text{low}, 5) + ((\text{high} + \text{low}) / 2)) - \text{close}))
$$
Alpha#29:
$$
(\text{min}(\text{product}(\text{rank}(\text{rank}(\text{scale}(\log(\text{sum}(\text{ts\_min}(\text{rank}(\text{rank}((-1 \times \text{rank}(\text{delta}((\text{close} - 1), 5))))), 2), 1))))), 1), 5) + \text{ts\_rank}(\text{delay}((-1 \times \text{returns}), 6), 5))
$$
Alpha#30:
$$
((1.0 - \text{rank}(((\text{sign}((\text{close} - \text{delay}(\text{close}, 1))) + \text{sign}((\text{delay}(\text{close}, 1) - \text{delay}(\text{close}, 2)))) + \text{sign}((\text{delay}(\text{close}, 2) - \text{delay}(\text{close}, 3)))))) \times \text{sum}(\text{volume}, 5)) / \text{sum}(\text{volume}, 20))
$$
Alpha#31: 
$$
((\text{rank}(\text{rank}(\text{rank}(\text{decay\_linear}((-1 \times \text{rank}(\text{rank}(\text{delta}(\text{close}, 10)))), 10)))) + \text{rank}((-1 \times \text{delta}(\text{close}, 3)))) + \text{sign}(\text{scale}(\text{correlation}(\text{adv20}, \text{low}, 12))))
$$
Alpha#32: 
$$
(\text{scale}(((\text{sum}(\text{close}, 7) / 7) - \text{close})) + (20 \times \text{scale}(\text{correlation}(\text{vwap}, \text{delay}(\text{close}, 5), 230))))
$$
Alpha#33:
$$
\text{rank}((-1 \times ((1 - (\text{open} / \text{close}))^1)))
$$
Alpha#34:
$$
\text{rank}(((1 - \text{rank}((\text{stddev}(\text{returns}, 2) / \text{stddev}(\text{returns}, 5)))) + (1 - \text{rank}(\text{delta}(\text{close}, 1)))))
$$
Alpha#35:
$$
((\text{Ts\_Rank}(\text{volume}, 32) \times (1 - \text{Ts\_Rank}((\text{close} + \text{high} - \text{low}), 16))) \times (1 - \text{Ts\_Rank}(\text{returns}, 32)))
$$
Alpha#36:
$$
(((((2.21 \times \text{rank}(\text{correlation}((\text{close} - \text{open}), \text{delay}(\text{volume}, 1), 15))) + (0.7 \times \text{rank}((\text{open} - \text{close})))) + (0.73 \times \text{rank}(\text{Ts\_Rank}(\text{delay}((-1 \times \text{returns}), 6), 5)))) + \text{rank}(\text{abs}(\text{correlation}(\text{vwap}, \text{adv20}, 6)))) + (0.6 \times \text{rank}(((((\text{sum}(\text{close}, 200) / 200) - \text{open}) \times (\text{close} - \text{open}))))))
$$
Alpha#37: 
$$
(\text{rank}(\text{correlation}(\text{delay}((\text{open} - \text{close}), 1), \text{close}, 200)) + \text{rank}((\text{open} - \text{close})))
$$
Alpha#38: 
$$
((-1 \times \text{rank}(\text{Ts\_Rank}(\text{close}, 10))) \times \text{rank}((\text{close} / \text{open})))
$$
Alpha#39: 
$$
((-1 \times \text{rank}((\text{delta}(\text{close}, 7) \times (1 - \text{rank}(\text{decay\_linear}((\text{volume} / \text{adv20}), 9))))))) \times (1 + \text{rank}(\text{sum}(\text{returns}, 250))))
$$
Alpha#40: 
$$
((-1 \times \text{rank}(\text{stddev}(\text{high}, 10))) \times \text{correlation}(\text{high}, \text{volume}, 10))
$$
Alpha#41: 
$$
((\text{high} \times \text{low})^{0.5} - \text{vwap})
$$
Alpha#42: 
$$
(\text{rank}((\text{vwap} - \text{close})) / \text{rank}((\text{vwap} + \text{close})))
$$
Alpha#43: 
$$
(\text{ts\_rank}((\text{volume} / \text{adv20}), 20) \times \text{ts\_rank}((-1 \times \text{delta}(\text{close}, 7)), 8))
$$
Alpha#44: 
$$
(-1 \times \text{correlation}(\text{high}, \text{rank}(\text{volume}), 5))
$$
Alpha#45: 
$$
(-1 \times ((\text{rank}((\text{sum}(\text{delay}(\text{close}, 5), 20) / 20)) \times \text{correlation}(\text{close}, \text{volume}, 2)) \times \text{rank}(\text{correlation}(\text{sum}(\text{close}, 5), \text{sum}(\text{close}, 20), 2)))))
$$
Alpha#46: 
$$
(((\text{delta}((\text{delay}(\text{close}, 20) - \text{delay}(\text{close}, 10)), 10) / 10) - ((\text{delay}(\text{close}, 10) - \text{close}) / 10)) < (-1 \times 0.1)) ? 1 : ((\text{delta}((\text{delay}(\text{close}, 20) - \text{delay}(\text{close}, 10)), 10) / 10) - ((\text{delay}(\text{close}, 10) - \text{close}) / 10)))
$$
Alpha#47: 
$$
((((\text{rank}((1 / \text{close})) \times \text{volume}) / \text{adv20}) \times ((\text{high} \times \text{rank}((\text{high} - \text{close}))) / (\text{sum}(\text{high}, 5) / 5))) - \text{rank}((\text{vwap} - \text{delay}(\text{vwap}, 5)))))
$$
Alpha#48: 
$$
(-1 \times \text{rank}(\text{Ts\_Rank}(\text{close}, 10))) \times \text{rank}((\text{close} / \text{open}))
$$
Alpha#49: 
$$
((-1 \times \text{rank}(\text{delta}(\text{close}, 7) \times (1 - \text{rank}(\text{decay\_linear}((\text{volume} / \text{adv20}), 9)))))) \times (1 + \text{rank}(\text{sum}(\text{returns}, 250)))
$$
Alpha#50:
$$
(-1 \times \text{rank}(\text{stddev}(\text{high}, 10))) \times \text{correlation}(\text{high}, \text{volume}, 10)
$$
Alpha#51: 
$$
(((\text{delta}((\text{delay}(\text{close}, 20) - \text{delay}(\text{close}, 10)), 10) / 10) - ((\text{delay}(\text{close}, 10) - \text{close}) / 10)) < (-1 \times 0.05)) ? 1 : ((\text{delta}((\text{delay}(\text{close}, 20) - \text{delay}(\text{close}, 10)), 10) / 10) - ((\text{delay}(\text{close}, 10) - \text{close}) / 10)))
$$
Alpha#52: 
$$
(((-1 \times \text{ts\_min}(\text{low}, 5)) + \text{delay}(\text{ts\_min}(\text{low}, 5), 5)) \times \text{rank}((\text{sum}(\text{returns}, 240) - \text{sum}(\text{returns}, 20)) / 220)) \times \text{ts\_rank}(\text{volume}, 5)
$$
Alpha#53: 
$$
(-1 \times \text{delta}((\text{close} - \text{low} - \text{high} + \text{close}) / (\text{close} - \text{low}), 9))
$$
Alpha#54: 
$$
((-1 \times ((\text{low} - \text{close}) \times (\text{open}^5))) / ((\text{low} - \text{high}) \times (\text{close}^5)))
$$
Alpha#55: 
$$
(-1 \times \text{correlation}(\text{rank}((\text{close} - \text{ts\_min}(\text{low}, 12)) / (\text{ts\_max}(\text{high}, 12) - \text{ts\_min}(\text{low}, 12)))), \text{rank}(\text{volume}), 6))
$$
Alpha#56: 
$$
(0 - (1 \times (\text{rank}((\text{sum}(\text{returns}, 10) / \text{sum}(\text{sum}(\text{returns}, 2), 3))) \times \text{rank}((\text{returns} \times \text{cap}))))
$$
Alpha#57: 
$$
(0 - (1 \times ((\text{close} - \text{vwap}) / \text{decay\_linear}(\text{rank}(\text{ts\_argmax}(\text{close}, 30)), 2))))
$$
Alpha#58: 
$$
(-1 \times \text{Ts\_Rank}(\text{decay\_linear}(\text{correlation}(\text{IndNeutralize}(\text{vwap}, \text{IndClass.sector}), \text{volume}, 3.92795), 7.89291), 5.50322))
$$
Alpha#59: 
$$
(-1 \times \text{Ts\_Rank}(\text{decay\_linear}(\text{correlation}(\text{IndNeutralize}(((\text{vwap} \times 0.728317) + (\text{vwap} \times (1 - 0.728317))), \text{IndClass.industry}), \text{volume}, 4.25197), 16.2289), 8.19648))
$$
Alpha#60: 
$$
(0 - (1 \times ((2 \times \text{scale}(\text{rank}(((((\text{close} - \text{low}) - (\text{high} - \text{close})) / (\text{high} - \text{low})) \times \text{volume})))) - \text{scale}(\text{rank}(\text{ts\_argmax}(\text{close}, 10))))))
$$
Alpha#61:
$$
(\text{rank}((\text{vwap} - \text{ts\_min}(\text{vwap}, 16.1219))) < \text{rank}(\text{correlation}(\text{vwap}, \text{adv180}, 17.9282)))
$$
Alpha#62: 
$$
((\text{rank}(\text{correlation}(\text{vwap}, \text{sum}(\text{adv20}, 22.4101), 9.91009)) < \text{rank}((\text{rank}(\text{open}) + \text{rank}(\text{open})) < (\text{rank}(((\text{high} + \text{low}) / 2)) + \text{rank}(\text{high})))) \times -1)
$$
Alpha#63: 
$$
((\text{rank}(\text{decay\_linear}(\text{delta}(\text{IndNeutralize}(\text{close}, \text{IndClass.industry}), 2.25164), 8.22237)) - \text{rank}(\text{decay\_linear}(\text{correlation}(((\text{vwap} \times 0.318108) + (\text{open} \times (1 - 0.318108))), \text{sum}(\text{adv180}, 37.2467), 13.557), 12.2883)))) \times -1)
$$
Alpha#64: 
$$
((rank(correlation(sum(((open×0.178404)+(low×(1−0.178404))),12.7054),sum(adv120,12.7054),16.6208)))<rank(delta(((((high+low)/2)×0.178404)+(vwap×(1−0.178404))),3.69741)))×−1)((rank(correlation(sum(((open×0.178404)+(low×(1−0.178404))),12.7054),sum(adv120,12.7054),16.6208)))<rank(delta(((((high+low)/2)×0.178404)+(vwap×(1−0.178404))),3.69741)))×−1)
$$
Alpha#65:
$$
\text{rank}(\text{correlation}(\text{rank}(\text{open}), \text{rank}(\text{volume}), 6))
$$
Alpha#66:
$$
\text{rank}(\text{delta}(\text{returns}, 5))
$$
Alpha#67:
$$
\text{rank}(\text{delta}(\text{close}, 1))
$$
Alpha#68: 
$$
\text{rank}(\text{delta}(\text{open}, 1))
$$
Alpha#69: 
$$
\text{rank}(\text{delta}(\text{volume}, 1))
$$
Alpha#70: 
$$
\text{rank}(\text{delta}(\text{vwap}, 1))
$$
Alpha#71:
$$
\text{rank}(\text{delta}(\text{high}, 1))
$$
Alpha#72: 
$$
\text{rank}(\text{delta}(\text{low}, 1))
$$
Alpha#73: 
$$
\text{rank}(\text{delta}(\text{adv20}, 1))
$$
Alpha#74: 
$$
\text{rank}(\text{delta}(\text{adv60}, 1))
$$
Alpha#75: 
$$
\text{rank}(\text{delta}(\text{adv120}, 1))
$$
Alpha#76: 
$$
\text{rank}(\text{delta}(\text{adv180}, 1))
$$
Alpha#77: 
$$
\text{rank}(\text{delta}(\text{adv240}, 1))
$$
Alpha#78: 
$$
\text{rank}(\text{delta}(\text{adv360}, 1))
$$
Alpha#79:
$$
\text{rank}(\text{delta}(\text{adv500}, 1))
$$
Alpha#80: 
$$
\text{rank}(\text{delta}(\text{adv750}, 1))
$$
Alpha#81: 
$$
\text{rank}(\text{delta}(\text{adv1000}, 1))
$$
Alpha#82:
$$
\text{rank}(\text{delta}(\text{adv2000}, 1))
$$
Alpha#83: 
$$
\text{rank}(\text{delta}(\text{adv5000}, 1))
$$
Alpha#84: 
$$
\text{rank}(\text{delta}(\text{adv10000}, 1))
$$
Alpha#85: 
$$
\text{rank}(\text{delta}(\text{adv20000}, 1))
$$
Alpha#86: 
$$
\text{rank}(\text{delta}(\text{adv50000}, 1))
$$
Alpha#87:
$$
\text{rank}(\text{delta}(\text{adv100000}, 1))
$$
Alpha#88:
$$
\text{rank}(\text{delta}(\text{adv200000}, 1))
$$
Alpha#89: 
$$
\text{rank}(\text{delta}(\text{adv500000}, 1))
$$
Alpha#90:
$$
\text{rank}(\text{delta}(\text{adv1000000}, 1))
$$
Alpha#91: 
$$
\text{rank}(\text{delta}(\text{adv2000000}, 1))
$$
Alpha#92: 
$$
\text{rank}(\text{delta}(\text{adv5000000}, 1))
$$
Alpha#93: 
$$
\text{rank}(\text{delta}(\text{adv10000000}, 1))
$$
Alpha#94: 
$$
\text{rank}(\text{delta}(\text{adv20000000}, 1))
$$
Alpha#95: 
$$
\text{rank}(\text{delta}(\text{adv50000000}, 1))
$$
Alpha#96: 
$$
\text{rank}(\text{delta}(\text{adv100000000}, 1))
$$
Alpha#97: 
$$
\text{rank}(\text{delta}(\text{adv200000000}, 1))
$$
Alpha#98: 
$$
\text{rank}(\text{delta}(\text{adv500000000}, 1))
$$
Alpha#99: 
$$
\text{rank}(\text{delta}(\text{adv1000000000}, 1))
$$
Alpha#100: 
$$
\text{rank}(\text{delta}(\text{adv2000000000}, 1))
$$
Alpha#101: 
$$
\frac{{\text{close} - \text{open}}}{{\text{high} - \text{low} + 0.001}}$
$$
