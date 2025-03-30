# Fundamental-factors-of-the-ferrous-metals-sector

data文件夹：程序处理过程中依赖的数据和产生的中间数据。
result文件夹：回测产生的结果文件。
alpha.py：用于提交的 alpha 函数。
backtest.py：公司回测框架接口，主程序可以利用这一文件对因子进行回测。
black_parse.ipynb：主处理程序。内含对各个基本面数据的验证、处理和筛选，并包含处理成最终因子的逻辑。
config.py：对程序运行必要的一些参数设置。
factor_composition.ipynb：一些对因子进行合成的尝试。已弃用。
factor_selection.ipynb ：对基本面数据的初筛过程。较为粗糙。
hc_parse.ipynb ：对热轧板卷的择时因子合成。筛选了一些有效的因子。
rb_parse.ipynb ：对螺纹钢的因子合成。筛选了一些有效的因子。
utils.py ：一些支持性的函数。
