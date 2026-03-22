"""
D{0-1}KP数据集解析模块
编码规范遵循：
1. 缩进：4个空格
2. 变量命名：小写+下划线
3. 每行字符数≤80
4. 函数最大行数≤50
5. 注释：类/函数需有文档字符串，关键逻辑有单行注释
"""
class KPDataParser:
    """D{0-1}KP数据集解析类，负责读取和校验数据集"""
    
    def __init__(self):
        self.item_sets = []  # 存储项集：[(w1,v1), (w2,v2), (w3,v3)]
        self.capacity = 0    # 背包容量
    
    def parse_txt(self, file_path):
        """
        解析txt格式数据集，第一行为背包容量，后续每行一个项集
        每行格式：w1 v1 w2 v2 w3 v3
        :param file_path: 数据集文件路径
        :return: 解析成功返回True，失败返回False
        """
        try:
            self.item_sets = []
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            # 第一行是背包容量
            if not lines:
                raise ValueError("数据集文件为空")
            self.capacity = int(lines[0])
            
            # 解析项集
            for line_num, line in enumerate(lines[1:], 2):
                parts = list(map(int, line.split()))
                if len(parts) != 6:
                    raise ValueError(f"第{line_num}行格式错误，需6个数字")
                
                w1, v1, w2, v2, w3, v3 = parts
                # 验证D{0-1}KP规则
                if w3 >= w1 + w2:
                    raise ValueError(f"第{line_num}行：第三项重量≥前两项之和")
                if v3 != v1 + v2:
                    raise ValueError(f"第{line_num}行：第三项价值≠前两项之和")
                
                self.item_sets.append([(w1, v1), (w2, v2), (w3, v3)])
            
            return True
        except Exception as e:
            print(f"解析失败：{str(e)}")
            return False
    
    def sort_by_ratio(self):
        """按项集第三项的价值重量比非递增排序"""
        if not self.item_sets:
            return False
        
        self.item_sets.sort(key=lambda x: (x[2][1]/x[2][0]), reverse=True)
        return True
    
    def get_item_sets(self):
        """获取解析后的项集"""
        return self.item_sets
    
    def get_capacity(self):
        """获取背包容量"""
        return self.capacity