"""
D{0-1}KP数据可视化模块
绘制重量-价值散点图
"""
import matplotlib.pyplot as plt

class KPVisualizer:
    """数据可视化类"""
    
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_scatter(self, item_sets, save_path=None):
        """
        绘制物品重量-价值散点图
        :param item_sets: 项集列表
        :param save_path: 保存路径（None则显示）
        :return: 绘制成功返回True
        """
        try:
            if not item_sets:
                return False
            
            # 提取所有物品数据
            weights = []
            values = []
            labels = []
            
            for i, item_set in enumerate(item_sets):
                for j, (w, v) in enumerate(item_set):
                    weights.append(w)
                    values.append(v)
                    labels.append(f'项{i+1}-物{j+1}')
            
            # 绘制散点图
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(weights, values, c='steelblue', alpha=0.8, s=60)
            
            # 添加标注（前15个，避免重叠）
            for i in range(min(15, len(labels))):
                ax.annotate(labels[i], (weights[i], values[i]), 
                           fontsize=8, ha='right')
            
            ax.set_xlabel('重量', fontsize=12)
            ax.set_ylabel('价值', fontsize=12)
            ax.set_title('D{0-1}KP数据集重量-价值散点图', fontsize=14)
            ax.grid(True, alpha=0.3)
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.show()
            return True
        except Exception as e:
            print(f"绘图失败：{str(e)}")
            return False