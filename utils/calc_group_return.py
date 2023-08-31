import pandas as pd


def get_group_return(pred_label: pd.DataFrame = None, reverse: bool = False, N: int = 5, **kwargs) -> pd.DataFrame:
	"""
	:param pred_label:
	:param reverse:
	:param N:
	:return:
	"""
	if reverse:
		pred_label["score"] *= -1
	
	pred_label = pred_label.sort_values("score", ascending=False)
	
	# Group1 ~ Group5 only consider the dropna values
	pred_label_drop = pred_label.dropna(subset=["score"])
	
	# Group
	t_df = pd.DataFrame(
		{
			"Group%d"
			% (i + 1): pred_label_drop.groupby(level="datetime")["label"].apply(
				lambda x: x[len(x) // N * i: len(x) // N * (i + 1)].mean()  # pylint: disable=W0640
			)
			for i in range(N)
		}
	)
	t_df.index = pd.to_datetime(t_df.index)
	
	# Long-Short
	t_df["long-short"] = t_df["Group1"] - t_df["Group%d" % N]
	
	# Long-Average
	t_df["long-average"] = t_df["Group1"] - pred_label.groupby(level="datetime")["label"].mean()
	
	t_df = t_df.dropna(how="all")  # for days which does not contain label
	
	# Cumulative Return By Group
	group_return_df = t_df.cumsum()
	group_return_df['date'] = group_return_df.index
	
	return group_return_df
