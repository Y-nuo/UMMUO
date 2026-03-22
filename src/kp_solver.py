"""
D{0-1}KP算法求解模块
实现动态规划求解，记录求解时间
"""
import time


class KPSolver:
    """D{0-1}KP问题求解类"""

    def __init__(self):
        self.max_value = 0  # 最大价值
        self.selected = []  # 选中项集：[(项集索引, 物品索引)]
        self.solve_time = 0  # 求解时间（秒）

    def dp_solve(self, capacity, item_sets):
        """
        动态规划求解D{0-1}KP问题
        :param capacity: 背包容量
        :param item_sets: 项集列表
        :return: (最大价值, 选中项集, 求解时间)
        """
        start_time = time.time()
        n = len(item_sets)

        # 初始化DP表：dp[i][j]表示前i个项集，容量j时的最大价值
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        # 填充DP表
        for i in range(1, n + 1):
            # 当前项集的3个物品
            item1 = item_sets[i - 1][0]
            item2 = item_sets[i - 1][1]
            item3 = item_sets[i - 1][2]

            for j in range(1, capacity + 1):
                # 不选当前项集
                dp[i][j] = dp[i - 1][j]

                # 选第一个物品
                if j >= item1[0] and dp[i - 1][j - item1[0]] + item1[1] > dp[i][j]:
                    dp[i][j] = dp[i - 1][j - item1[0]] + item1[1]

                # 选第二个物品
                if j >= item2[0] and dp[i - 1][j - item2[0]] + item2[1] > dp[i][j]:
                    dp[i][j] = dp[i - 1][j - item2[0]] + item2[1]

                # 选第三个物品
                if j >= item3[0] and dp[i - 1][j - item3[0]] + item3[1] > dp[i][j]:
                    dp[i][j] = dp[i - 1][j - item3[0]] + item3[1]

        # 回溯找选中项
        self.max_value = dp[n][capacity]
        self.selected = []
        j = capacity

        for i in range(n, 0, -1):
            if dp[i][j] != dp[i - 1][j]:
                item_set = item_sets[i - 1]
                # 判断选中的物品
                if j >= item_set[0][0] and dp[i - 1][j - item_set[0][0]] + item_set[0][1] == dp[i][j]:
                    self.selected.append((i - 1, 0))
                    j -= item_set[0][0]
                elif j >= item_set[1][0] and dp[i - 1][j - item_set[1][0]] + item_set[1][1] == dp[i][j]:
                    self.selected.append((i - 1, 1))
                    j -= item_set[1][0]
                elif j >= item_set[2][0] and dp[i - 1][j - item_set[2][0]] + item_set[2][1] == dp[i][j]:
                    self.selected.append((i - 1, 2))
                    j -= item_set[2][0]

        self.solve_time = round(time.time() - start_time, 6)
        return self.max_value, self.selected, self.solve_time

    def get_result(self):
        """获取求解结果"""
        return {
            "max_value": self.max_value,
            "selected": self.selected,
            "solve_time": self.solve_time
        }