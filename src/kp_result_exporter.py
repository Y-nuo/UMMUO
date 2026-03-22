"""
D{0-1}KP结果导出模块
支持导出TXT/Excel格式
"""
import pandas as pd

class KPResultExporter:
    """结果导出类"""
    
    def export_txt(self, result, file_path):
        """
        导出为TXT文件
        :param result: 结果字典（capacity, max_value, selected, solve_time, item_sets）
        :param file_path: 导出路径
        :return: 成功返回True
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("===== D{0-1}KP问题求解结果 =====\n")
                f.write(f"背包容量：{result['capacity']}\n")
                f.write(f"求解时间：{result['solve_time']:.6f}秒\n")
                f.write(f"最大价值：{result['max_value']}\n\n")
                f.write("选中项集详情：\n")
                
                total_weight = 0
                for set_idx, item_idx in result['selected']:
                    w, v = result['item_sets'][set_idx][item_idx]
                    total_weight += w
                    f.write(f"  项集{set_idx+1} - 物品{item_idx+1}：重量={w}，价值={v}\n")
                
                f.write(f"\n选中物品总重量：{total_weight}\n")
            return True
        except Exception as e:
            print(f"TXT导出失败：{str(e)}")
            return False
    
    def export_excel(self, result, file_path):
        """
        导出为Excel文件
        :param result: 结果字典
        :param file_path: 导出路径
        :return: 成功返回True
        """
        try:
            # 选中项详情
            selected_data = []
            total_weight = 0
            for set_idx, item_idx in result['selected']:
                w, v = result['item_sets'][set_idx][item_idx]
                total_weight += w
                selected_data.append({
                    '项集编号': set_idx + 1,
                    '物品编号': item_idx + 1,
                    '重量': w,
                    '价值': v
                })
            
            # 汇总数据
            summary_data = [{
                '项集编号': '汇总',
                '物品编号': '-',
                '重量': total_weight,
                '价值': result['max_value']
            }]
            
            # 写入Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # 选中项详情
                df_selected = pd.DataFrame(selected_data + summary_data)
                df_selected.to_excel(writer, sheet_name='选中项详情', index=False)
                
                # 求解信息
                df_info = pd.DataFrame({
                    '指标': ['背包容量', '求解时间(秒)', '最大价值', '总重量'],
                    '数值': [
                        result['capacity'],
                        round(result['solve_time'], 6),
                        result['max_value'],
                        total_weight
                    ]
                })
                df_info.to_excel(writer, sheet_name='求解信息', index=False)
            
            return True
        except Exception as e:
            print(f"Excel导出失败：{str(e)}")
            return False