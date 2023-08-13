# 网页显示可交互图表

import numpy as np
import plotly.graph_objs as go

month_list = [i + 1 for i in range(12)]
score_list = np.random.randint(0, 100, 12)
print("考试月份：", month_list)
print("考试分数：", score_list)
fig = go.Figure()
fig.add_trace(go.Scatter(x=month_list, y=score_list))
fig.update_layout(title="成绩单", xaxis=dict(title='month'), yaxis=dict(title='score'))
fig.show()
