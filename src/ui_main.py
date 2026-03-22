"""
主界面模块
基于PyQt5实现图形化界面
"""
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QTextEdit,
                             QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from kp_data_parser import KPDataParser
from kp_solver import KPSolver
from kp_visualizer import KPVisualizer
from kp_result_exporter import KPResultExporter

class MainWindow(QMainWindow):
    """主界面窗口"""
    
    def __init__(self):
        super().__init__()
        self.parser = KPDataParser()
        self.solver = KPSolver()
        self.visualizer = KPVisualizer()
        self.exporter = KPResultExporter()
        self.current_result = None
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        # 窗口设置
        self.setWindowTitle('D{0-1}KP问题求解系统')
        self.setGeometry(100, 100, 900, 600)
        
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 布局
        main_layout = QVBoxLayout(central_widget)
        
        # 功能按钮区
        btn_layout = QHBoxLayout()
        
        # 读取数据按钮
        self.btn_load = QPushButton('读取数据集')
        self.btn_load.clicked.connect(self.load_data)
        btn_layout.addWidget(self.btn_load)
        
        # 绘制散点图按钮
        self.btn_plot = QPushButton('绘制散点图')
        self.btn_plot.clicked.connect(self.plot_scatter)
        self.btn_plot.setEnabled(False)
        btn_layout.addWidget(self.btn_plot)
        
        # 排序按钮
        self.btn_sort = QPushButton('按价值重量比排序')
        self.btn_sort.clicked.connect(self.sort_data)
        self.btn_sort.setEnabled(False)
        btn_layout.addWidget(self.btn_sort)
        
        # 求解按钮
        self.btn_solve = QPushButton('求解最优解')
        self.btn_solve.clicked.connect(self.solve_problem)
        self.btn_solve.setEnabled(False)
        btn_layout.addWidget(self.btn_solve)
        
        # 导出按钮
        self.cb_export = QComboBox()
        self.cb_export.addItems(['导出TXT', '导出Excel'])
        btn_layout.addWidget(self.cb_export)
        
        self.btn_export = QPushButton('导出结果')
        self.btn_export.clicked.connect(self.export_result)
        self.btn_export.setEnabled(False)
        btn_layout.addWidget(self.btn_export)
        
        main_layout.addLayout(btn_layout)
        
        # 结果显示区
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText('求解结果将显示在这里...')
        main_layout.addWidget(self.result_display)
        
        self.show()
    
    def load_data(self):
        """读取数据集文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择数据集文件', '', 'Text Files (*.txt)'
        )
        
        if not file_path:
            return
        
        if self.parser.parse_txt(file_path):
            self.result_display.append(f"✅ 成功读取数据集：{file_path}")
            self.result_display.append(f"📦 背包容量：{self.parser.get_capacity()}")
            self.result_display.append(f"📊 项集数量：{len(self.parser.get_item_sets())}\n")
            
            self.btn_plot.setEnabled(True)
            self.btn_sort.setEnabled(True)
            self.btn_solve.setEnabled(True)
        else:
            QMessageBox.warning(self, '错误', '数据集解析失败！')
    
    def plot_scatter(self):
        """绘制散点图"""
        if self.visualizer.plot_scatter(self.parser.get_item_sets()):
            self.result_display.append("✅ 散点图绘制完成！\n")
        else:
            QMessageBox.warning(self, '错误', '散点图绘制失败！')
    
    def sort_data(self):
        """按价值重量比排序"""
        if self.parser.sort_by_ratio():
            self.result_display.append("✅ 数据已按第三项价值重量比非递增排序！\n")
        else:
            QMessageBox.warning(self, '错误', '排序失败！')
    
    def solve_problem(self):
        """求解最优解"""
        capacity = self.parser.get_capacity()
        item_sets = self.parser.get_item_sets()
        
        max_value, selected, solve_time = self.solver.dp_solve(capacity, item_sets)
        
        # 保存结果
        self.current_result = {
            'capacity': capacity,
            'max_value': max_value,
            'selected': selected,
            'solve_time': solve_time,
            'item_sets': item_sets
        }
        
        # 显示结果
        self.result_display.append("===== 最优解求解结果 =====")
        self.result_display.append(f"求解时间：{solve_time:.6f}秒")
        self.result_display.append(f"最大价值：{max_value}")
        self.result_display.append("选中项集：")
        
        for set_idx, item_idx in selected:
            w, v = item_sets[set_idx][item_idx]
            self.result_display.append(f"  项集{set_idx+1} - 物品{item_idx+1}（重量：{w}，价值：{v}）")
        
        self.result_display.append("\n")
        self.btn_export.setEnabled(True)
    
    def export_result(self):
        """导出结果"""
        if not self.current_result:
            QMessageBox.warning(self, '警告', '暂无求解结果可导出！')
            return
        
        # 选择导出格式和路径
        if self.cb_export.currentText() == '导出TXT':
            file_path, _ = QFileDialog.getSaveFileName(
                self, '保存结果', 'dkp_result.txt', 'Text Files (*.txt)'
            )
            if file_path:
                if self.exporter.export_txt(self.current_result, file_path):
                    self.result_display.append(f"✅ 结果已导出至：{file_path}\n")
                else:
                    QMessageBox.warning(self, '错误', 'TXT导出失败！')
        
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self, '保存结果', 'dkp_result.xlsx', 'Excel Files (*.xlsx)'
            )
            if file_path:
                if self.exporter.export_excel(self.current_result, file_path):
                    self.result_display.append(f"✅ 结果已导出至：{file_path}\n")
                else:
                    QMessageBox.warning(self, '错误', 'Excel导出失败！')

def main():
    """启动界面"""
    app = sys.argv
    QApplication = sys.modules["PyQt5.QtWidgets"].QApplication
    app = QApplication(app)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()