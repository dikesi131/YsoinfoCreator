import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QTabWidget, QGroupBox, QLabel, QLineEdit, QPushButton,
    QTextEdit, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
    QProgressBar, QSplitter, QDialog, QDialogButtonBox, QHeaderView,
    QAbstractItemView, QInputDialog, QMenuBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QFont, QAction, QFontDatabase

# 导入主要功能模块
from main import SocialEngDictionaryTool
from core.collect_input import CollectInput

# 导入全局设置
from gui_settings import STYLE_SHEET


class GenerationWorker(QThread):
    """字典生成工作线程"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, dict)

    def __init__(self, tool: SocialEngDictionaryTool):
        super().__init__()
        self.tool = tool

    def run(self):
        '''执行字典生成任务'''
        try:
            self.status.emit("开始生成字典...")
            self.progress.emit(20)

            # 生成字典
            success = self.tool.generate_dictionaries()
            self.progress.emit(60)
            usernames_count = len(self.tool.results['usernames'])
            passwords_count = len(self.tool.results['passwords'])

            if success:
                results = {
                    'usernames': usernames_count,
                    'passwords': passwords_count,
                    'total': usernames_count + passwords_count
                }
                self.status.emit("字典生成完成!")
                self.progress.emit(100)
                self.finished.emit(True, results)
            else:
                self.status.emit("字典生成失败")
                self.finished.emit(False, {})

        except Exception as e:
            self.status.emit(f"生成过程中出错: {str(e)}")
            self.finished.emit(False, {})


class PersonalInfoWidget(QWidget):
    """个人信息输入部件"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 基本信息组
        basic_group = QGroupBox("基本信息")
        basic_layout = QGridLayout()

        self.name_zh = QLineEdit()
        self.name_en = QLineEdit()
        self.nickname_zh = QLineEdit()
        self.nickname_en = QLineEdit()
        self.birthday = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.username = QLineEdit()

        # 添加占位符文本
        self.name_zh.setPlaceholderText("例: 张三")
        self.name_en.setPlaceholderText("例: John Smith")
        self.nickname_zh.setPlaceholderText("例: 小张")
        self.nickname_en.setPlaceholderText("例: Johnny")
        self.birthday.setPlaceholderText("例: 1990-01-01")
        self.email.setPlaceholderText("例: user@example.com")
        self.phone.setPlaceholderText("例: 13800138000")
        self.username.setPlaceholderText("例: john123")

        basic_layout.addWidget(QLabel("中文姓名:"), 0, 0)
        basic_layout.addWidget(self.name_zh, 0, 1)
        basic_layout.addWidget(QLabel("英文姓名:"), 0, 2)
        basic_layout.addWidget(self.name_en, 0, 3)

        basic_layout.addWidget(QLabel("中文昵称:"), 1, 0)
        basic_layout.addWidget(self.nickname_zh, 1, 1)
        basic_layout.addWidget(QLabel("英文昵称:"), 1, 2)
        basic_layout.addWidget(self.nickname_en, 1, 3)

        basic_layout.addWidget(QLabel("生日:"), 2, 0)
        basic_layout.addWidget(self.birthday, 2, 1)
        basic_layout.addWidget(QLabel("邮箱:"), 2, 2)
        basic_layout.addWidget(self.email, 2, 3)

        basic_layout.addWidget(QLabel("手机号:"), 3, 0)
        basic_layout.addWidget(self.phone, 3, 1)
        basic_layout.addWidget(QLabel("用户名:"), 3, 2)
        basic_layout.addWidget(self.username, 3, 3)

        basic_group.setLayout(basic_layout)

        # 公司信息组
        company_group = QGroupBox("公司信息")
        company_layout = QGridLayout()

        self.company_en = QLineEdit()
        self.company_zh = QLineEdit()
        self.department_en = QLineEdit()
        self.department_zh = QLineEdit()

        self.company_en.setPlaceholderText("例: ABC Company")
        self.company_zh.setPlaceholderText("例: ABC公司")
        self.department_en.setPlaceholderText("例: IT Department")
        self.department_zh.setPlaceholderText("例: 信息技术部")

        company_layout.addWidget(QLabel("英文公司名:"), 0, 0)
        company_layout.addWidget(self.company_en, 0, 1)
        company_layout.addWidget(QLabel("中文公司名:"), 0, 2)
        company_layout.addWidget(self.company_zh, 0, 3)

        company_layout.addWidget(QLabel("英文部门:"), 1, 0)
        company_layout.addWidget(self.department_en, 1, 1)
        company_layout.addWidget(QLabel("中文部门:"), 1, 2)
        company_layout.addWidget(self.department_zh, 1, 3)

        company_group.setLayout(company_layout)

        # 自定义设置组
        custom_group = QGroupBox("自定义设置")
        custom_layout = QGridLayout()

        self.special_chars = QLineEdit()
        self.custom_affix = QLineEdit()
        self.custom_years = QLineEdit()

        self.special_chars.setPlaceholderText("例: !@#$%^&*()")
        self.custom_affix.setPlaceholderText("例: 666,888,love")
        self.custom_years.setPlaceholderText("例: 1995,2020,88")

        custom_layout.addWidget(QLabel("特殊字符:"), 0, 0)
        custom_layout.addWidget(self.special_chars, 0, 1)
        custom_layout.addWidget(QLabel("自定义后缀:"), 1, 0)
        custom_layout.addWidget(self.custom_affix, 1, 1)
        custom_layout.addWidget(QLabel("自定义年份:"), 2, 0)
        custom_layout.addWidget(self.custom_years, 2, 1)

        custom_group.setLayout(custom_layout)

        # 按钮组
        button_layout = QHBoxLayout()

        self.load_btn = QPushButton("从文件加载")
        self.save_btn = QPushButton("保存到文件")
        self.clear_btn = QPushButton("清空")
        self.validate_btn = QPushButton("验证信息")

        self.load_btn.clicked.connect(self.load_from_file)
        self.save_btn.clicked.connect(self.save_to_file)
        self.clear_btn.clicked.connect(self.clear_all)
        self.validate_btn.clicked.connect(self.validate_info)

        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.validate_btn)
        button_layout.addStretch()

        # 添加到主布局
        layout.addWidget(basic_group)
        layout.addWidget(company_group)
        layout.addWidget(custom_group)
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def get_info_dict(self) -> Dict[str, Any]:
        """获取信息字典"""
        info_dict = {}

        # 基本信息
        if self.name_zh.text().strip():
            info_dict['name_zh'] = self.name_zh.text().strip()
        if self.name_en.text().strip():
            info_dict['name_en'] = self.name_en.text().strip()
        if self.nickname_zh.text().strip():
            info_dict['nickname_zh'] = self.nickname_zh.text().strip()
        if self.nickname_en.text().strip():
            info_dict['nickname_en'] = self.nickname_en.text().strip()
        if self.birthday.text().strip():
            info_dict['birthday'] = self.birthday.text().strip()
        if self.email.text().strip():
            info_dict['email'] = self.email.text().strip()
        if self.phone.text().strip():
            info_dict['phone'] = self.phone.text().strip()
        if self.username.text().strip():
            info_dict['username'] = self.username.text().strip()

        # 公司信息
        if self.company_en.text().strip():
            info_dict['company_en'] = self.company_en.text().strip()
        if self.company_zh.text().strip():
            info_dict['company_zh'] = self.company_zh.text().strip()
        if self.department_en.text().strip():
            info_dict['department_en'] = self.department_en.text().strip()
        if self.department_zh.text().strip():
            info_dict['department_zh'] = self.department_zh.text().strip()

        # 自定义设置
        if self.special_chars.text().strip():
            info_dict['special_chars'] = self.special_chars.text().strip()
        if self.custom_affix.text().strip():
            affix_list = [item.strip() for item in self.custom_affix.text().split(',') if item.strip()]  # noqa
            if affix_list:
                info_dict['common_suffix'] = affix_list
        if self.custom_years.text().strip():
            years_list = [item.strip() for item in self.custom_years.text().split(',') if item.strip()]  # noqa
            if years_list:
                info_dict['regular_years'] = years_list

        return info_dict

    def set_info_dict(self, info_dict: Dict[str, Any]):
        """设置信息字典"""
        self.name_zh.setText(info_dict.get('name_zh', ''))
        self.name_en.setText(info_dict.get('name_en', ''))
        self.nickname_zh.setText(info_dict.get('nickname_zh', ''))
        self.nickname_en.setText(info_dict.get('nickname_en', ''))
        self.birthday.setText(info_dict.get('birthday', ''))
        self.email.setText(info_dict.get('email', ''))
        self.phone.setText(info_dict.get('phone', ''))
        self.username.setText(info_dict.get('username', ''))
        self.company_en.setText(info_dict.get('company_en', ''))
        self.company_zh.setText(info_dict.get('company_zh', ''))
        self.department_en.setText(info_dict.get('department_en', ''))
        self.department_zh.setText(info_dict.get('department_zh', ''))
        self.special_chars.setText(info_dict.get('special_chars', ''))

        # 自定义后缀
        if 'common_suffix' in info_dict:
            self.custom_affix.setText(','.join(info_dict['common_suffix']))

        # 自定义年份
        if 'regular_years' in info_dict:
            self.custom_years.setText(','.join(info_dict['regular_years']))

    def load_from_file(self):
        """从文件加载"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择个人信息文件", "", "JSON文件 (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.set_info_dict(data)
                QMessageBox.information(self, "成功", f"已从 {file_path} 加载个人信息")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载文件失败: {str(e)}")

    def save_to_file(self):
        """保存到文件"""
        info_dict = self.get_info_dict()
        if not info_dict:
            QMessageBox.warning(self, "警告", "没有信息可保存")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存个人信息", "personal_info.json", "JSON文件 (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(info_dict, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "成功", f"个人信息已保存到 {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")

    def clear_all(self):
        """清空所有输入"""
        for widget in self.findChildren(QLineEdit):
            widget.clear()

    def validate_info(self):
        """验证信息"""
        info_dict = self.get_info_dict()
        if not info_dict:
            QMessageBox.warning(self, "警告", "请先输入个人信息")
            return

        try:
            temp_info = CollectInput(**info_dict)
            validation = temp_info.validate_input()

            invalid_fields = [field for field,
                              valid in validation.items() if not valid]

            if invalid_fields:
                QMessageBox.warning(
                    self, "验证警告",
                    f"以下字段格式不正确:\n{', '.join(invalid_fields)}"
                )
            else:
                QMessageBox.information(self, "验证成功", "所有信息格式正确!")

        except Exception as e:
            QMessageBox.critical(self, "验证错误", f"验证过程中出错: {str(e)}")


class ResultDisplayWidget(QWidget):
    """结果显示部件"""

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # 保存主窗口引用
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 统计信息 - 增强版
        stats_group = QGroupBox("📊 生成统计")
        stats_group.setObjectName("stats_group")  # 用于CSS选择器
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)  # 增加间距

        # 创建统计卡片样式的标签
        username_card = QWidget()
        username_card_layout = QVBoxLayout()
        username_card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        username_title = QLabel("用户名数量")
        username_title.setObjectName("stat_label")
        username_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_count_label = QLabel("0")
        self.username_count_label.setObjectName("username_count")
        self.username_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        username_card_layout.addWidget(username_title)
        username_card_layout.addWidget(self.username_count_label)
        username_card.setLayout(username_card_layout)

        # 密码数量卡片
        password_card = QWidget()
        password_card_layout = QVBoxLayout()
        password_card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        password_title = QLabel("密码数量")
        password_title.setObjectName("stat_label")
        password_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.password_count_label = QLabel("0")
        self.password_count_label.setObjectName("password_count")
        self.password_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        password_card_layout.addWidget(password_title)
        password_card_layout.addWidget(self.password_count_label)
        password_card.setLayout(password_card_layout)

        # 总计卡片
        total_card = QWidget()
        total_card_layout = QVBoxLayout()
        total_card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        total_title = QLabel("总计")
        total_title.setObjectName("stat_label")
        total_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.total_count_label = QLabel("0")
        self.total_count_label.setObjectName("total_count")
        self.total_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        total_card_layout.addWidget(total_title)
        total_card_layout.addWidget(self.total_count_label)
        total_card.setLayout(total_card_layout)

        # 添加卡片到网格布局
        stats_layout.addWidget(username_card, 0, 0)
        stats_layout.addWidget(password_card, 0, 1)
        stats_layout.addWidget(total_card, 0, 2)

        # 添加弹性空间
        stats_layout.setColumnStretch(3, 1)

        stats_group.setLayout(stats_layout)

        # 结果显示区域
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 用户名列表
        username_group = QGroupBox("👤 用户名列表")
        username_layout = QVBoxLayout()

        self.username_list = QTextEdit()
        self.username_list.setReadOnly(True)
        self.username_list.setFont(self._get_monospace_font())

        username_layout.addWidget(self.username_list)
        username_group.setLayout(username_layout)

        # 密码列表
        password_group = QGroupBox("🔐 密码列表")
        password_layout = QVBoxLayout()

        self.password_list = QTextEdit()
        self.password_list.setReadOnly(True)
        self.password_list.setFont(self._get_monospace_font())

        password_layout.addWidget(self.password_list)
        password_group.setLayout(password_layout)

        splitter.addWidget(username_group)
        splitter.addWidget(password_group)
        splitter.setSizes([400, 400])

        # 按钮组
        button_layout = QHBoxLayout()

        self.export_btn = QPushButton("📁 导出到文件")
        self.save_db_btn = QPushButton("💾 保存到数据库")
        self.clear_btn = QPushButton("🗑️ 清空结果")
        self.copy_usernames_btn = QPushButton("📋 复制用户名")
        self.copy_passwords_btn = QPushButton("📋 复制密码")

        self.export_btn.clicked.connect(self.export_results)
        self.save_db_btn.clicked.connect(self.save_to_database)
        self.clear_btn.clicked.connect(self.clear_results)
        self.copy_usernames_btn.clicked.connect(self.copy_usernames)
        self.copy_passwords_btn.clicked.connect(self.copy_passwords)

        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.save_db_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.copy_usernames_btn)
        button_layout.addWidget(self.copy_passwords_btn)
        button_layout.addStretch()

        # 添加到主布局
        layout.addWidget(stats_group, 0)  # 不拉伸
        layout.addWidget(splitter, 1)     # 拉伸
        layout.addLayout(button_layout, 0)  # 不拉伸

        self.setLayout(layout)

        # 存储结果数据
        self.usernames = set()
        self.passwords = set()

    def _get_monospace_font(self) -> QFont:
        """获取跨平台的等宽字体"""
        # 修复: 在 PyQt6 中使用静态方法获取字体族
        try:
            # 使用静态方法获取可用字体族
            available_families = QFontDatabase.families()
        except Exception:
            # 如果静态方法不可用，尝试其他方法
            available_families = []

        # 按优先级尝试不同的等宽字体
        preferred_fonts = [
            "SF Mono",           # macOS 默认
            "Monaco",            # macOS 经典
            "Menlo",             # macOS
            "Consolas",          # Windows
            "Courier New",       # 通用
            "Courier",           # 通用备选
            "Liberation Mono",   # Linux
            "DejaVu Sans Mono",  # Linux
        ]

        # 寻找第一个可用的等宽字体
        for font_name in preferred_fonts:
            if font_name in available_families:
                font = QFont(font_name, 10)
                return font

        # 如果没有找到，使用系统默认等宽字体
        font = QFont()
        font.setStyleHint(QFont.StyleHint.TypeWriter)
        font.setFamily("monospace")
        font.setPointSize(10)
        return font

    def update_results(self, usernames: set, passwords: set):
        """更新结果显示"""
        self.usernames = usernames
        self.passwords = passwords

        # 更新统计
        self.username_count_label.setText(str(len(usernames)))
        self.password_count_label.setText(str(len(passwords)))
        self.total_count_label.setText(str(len(usernames) + len(passwords)))

        # 更新列表显示
        self.username_list.clear()
        sorted_usernames = sorted(usernames)
        self.username_list.setText('\n'.join(sorted_usernames))

        self.password_list.clear()
        sorted_passwords = sorted(passwords)
        self.password_list.setText('\n'.join(sorted_passwords))

    def clear_results(self):
        """清空结果"""
        self.usernames.clear()
        self.passwords.clear()
        self.username_list.clear()
        self.password_list.clear()
        self.username_count_label.setText("0")
        self.password_count_label.setText("0")
        self.total_count_label.setText("0")

    def export_results(self):
        """导出结果到文件"""
        if not self.usernames and not self.passwords:
            QMessageBox.warning(self, "警告", "没有结果可导出")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if output_dir:
            try:
                output_path = Path(output_dir)

                # 导出用户名
                if self.usernames:
                    username_file = output_path / "usernames.txt"
                    with open(username_file, 'w', encoding='utf-8') as f:
                        for username in sorted(self.usernames):
                            f.write(username + '\n')

                # 导出密码
                if self.passwords:
                    password_file = output_path / "passwords.txt"
                    with open(password_file, 'w', encoding='utf-8') as f:
                        for password in sorted(self.passwords):
                            f.write(password + '\n')

                QMessageBox.information(
                    self, "导出成功",
                    f"结果已导出到:\n{output_dir}\n\n"
                    f"用户名: {len(self.usernames)} 个\n"
                    f"密码: {len(self.passwords)} 个"
                )

            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"导出过程中出错: {str(e)}")

    def save_to_database(self):
        """保存到数据库"""
        # 修复: 通过保存的主窗口引用调用方法
        if self.main_window:
            self.main_window.save_current_results()
        else:
            QMessageBox.warning(self, "错误", "无法访问主窗口")

    def copy_usernames(self):
        """复制用户名到剪贴板"""
        if self.usernames:
            clipboard = QApplication.clipboard()
            if clipboard is not None:
                clipboard.setText('\n'.join(sorted(self.usernames)))
                QMessageBox.information(self, "复制成功", f"已复制 {len(self.usernames)} 个用户名到剪贴板")  # noqa
            else:
                QMessageBox.warning(self, "错误", "无法访问剪贴板，请确保应用程序已正确初始化")
        else:
            QMessageBox.warning(self, "警告", "没有用户名可复制")

    def copy_passwords(self):
        """复制密码到剪贴板"""
        if self.passwords:
            clipboard = QApplication.clipboard()
            if clipboard is not None:
                clipboard.setText('\n'.join(sorted(self.passwords)))
                QMessageBox.information(self, "复制成功", f"已复制 {len(self.passwords)} 个密码到剪贴板")  # noqa
            else:
                QMessageBox.warning(self, "错误", "无法访问剪贴板，请确保应用程序已正确初始化")
        else:
            QMessageBox.warning(self, "警告", "没有密码可复制")


class DatabaseWidget(QWidget):
    """数据库管理部件"""

    def __init__(self, tool: SocialEngDictionaryTool, main_window=None):
        super().__init__()
        self.tool = tool
        self.main_window = main_window  # 保存主窗口引用
        self.init_ui()
        self.refresh_tasks()

    def init_ui(self):
        layout = QVBoxLayout()

        # 顶部按钮组
        top_button_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("刷新列表")
        self.search_btn = QPushButton("搜索任务")
        self.stats_btn = QPushButton("数据库统计")
        self.export_all_btn = QPushButton("导出所有唯一条目")

        self.refresh_btn.clicked.connect(self.refresh_tasks)
        self.search_btn.clicked.connect(self.search_tasks)
        self.stats_btn.clicked.connect(self.show_database_stats)
        self.export_all_btn.clicked.connect(self.export_all_unique)

        top_button_layout.addWidget(self.refresh_btn)
        top_button_layout.addWidget(self.search_btn)
        top_button_layout.addWidget(self.stats_btn)
        top_button_layout.addWidget(self.export_all_btn)
        top_button_layout.addStretch()

        # 任务列表表格
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(6)
        self.task_table.setHorizontalHeaderLabels([
            "ID", "任务名称", "用户名数", "密码数", "总数", "创建时间"
        ])

        # 隐藏垂直表头（行号）
        vertical_header = self.task_table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setVisible(False)

        # 设置表格属性
        header = self.task_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # noqa
        self.task_table.setAlternatingRowColors(True)

        # 底部按钮组
        bottom_button_layout = QHBoxLayout()

        self.load_btn = QPushButton("加载任务")
        self.export_btn = QPushButton("导出任务")
        self.delete_btn = QPushButton("删除任务")
        self.view_details_btn = QPushButton("查看详情")

        self.load_btn.clicked.connect(self.load_selected_task)
        self.export_btn.clicked.connect(self.export_selected_task)
        self.delete_btn.clicked.connect(self.delete_selected_task)
        self.view_details_btn.clicked.connect(self.view_task_details)

        bottom_button_layout.addWidget(self.load_btn)
        bottom_button_layout.addWidget(self.export_btn)
        bottom_button_layout.addWidget(self.delete_btn)
        bottom_button_layout.addWidget(self.view_details_btn)
        bottom_button_layout.addStretch()

        # 添加到主布局
        layout.addLayout(top_button_layout)
        layout.addWidget(self.task_table)
        layout.addLayout(bottom_button_layout)

        self.setLayout(layout)

    def refresh_tasks(self):
        """刷新任务列表"""
        try:
            tasks = self.tool.read_handler.get_all_tasks(limit=100)

            self.task_table.setRowCount(len(tasks))

            for row, task in enumerate(tasks):
                self.task_table.setItem(row, 0,
                                        QTableWidgetItem(str(task['id'])))
                self.task_table.setItem(row, 1,
                                        QTableWidgetItem(task['name']))
                self.task_table.setItem(row, 2, QTableWidgetItem(str(task['username_count'])))  # noqa
                self.task_table.setItem(row, 3, QTableWidgetItem(str(task['password_count'])))  # noqa
                self.task_table.setItem(row, 4, QTableWidgetItem(str(task['total_count'])))  # noqa

                # 格式化创建时间
                created_at = task['created_at'][:19] if task['created_at'] else "未知"  # noqa
                self.task_table.setItem(row, 5, QTableWidgetItem(created_at))

        except Exception as e:
            QMessageBox.critical(self, "错误", f"刷新任务列表失败: {str(e)}")

    def search_tasks(self):
        """搜索任务"""
        text, ok = QInputDialog.getText(self, "搜索任务", "请输入搜索关键词:")
        if ok and text.strip():
            try:
                tasks = self.tool.read_handler.search_tasks_by_name(text.strip())  # noqa

                self.task_table.setRowCount(len(tasks))

                for row, task in enumerate(tasks):
                    self.task_table.setItem(row, 0,
                                            QTableWidgetItem(str(task['id'])))
                    self.task_table.setItem(row, 1,
                                            QTableWidgetItem(task['name']))
                    self.task_table.setItem(row, 2, QTableWidgetItem(str(task['username_count'])))  # noqa
                    self.task_table.setItem(row, 3, QTableWidgetItem(str(task['password_count'])))  # noqa
                    self.task_table.setItem(row, 4, QTableWidgetItem(str(task['total_count'])))  # noqa

                    created_at = task['created_at'][:19] if task['created_at'] else "未知"  # noqa
                    self.task_table.setItem(row, 5,
                                            QTableWidgetItem(created_at))

                if not tasks:
                    QMessageBox.information(self, "搜索结果",
                                            f"未找到匹配 '{text}' 的任务")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"搜索失败: {str(e)}")

    def show_database_stats(self):
        """显示数据库统计"""
        try:
            stats = self.tool.save_handler.get_database_stats()

            if stats:
                msg = f"""数据库统计信息:

总任务数: {stats.get('total_tasks', 0)}
总用户名: {stats.get('total_usernames', 0)}
总密码数: {stats.get('total_passwords', 0)}
唯一用户名: {stats.get('unique_usernames', 0)}
唯一密码: {stats.get('unique_passwords', 0)}
总条目数: {stats.get('total_entries', 0)}"""

                QMessageBox.information(self, "数据库统计", msg)
            else:
                QMessageBox.warning(self, "警告", "无法获取数据库统计信息")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取统计信息失败: {str(e)}")

    def get_selected_task_id(self) -> Optional[int]:
        """获取选中的任务ID"""
        current_row = self.task_table.currentRow()
        if current_row >= 0:
            id_item = self.task_table.item(current_row, 0)
            if id_item:
                return int(id_item.text())
        return None

    def load_selected_task(self):
        """加载选中的任务"""
        task_id = self.get_selected_task_id()
        if task_id is None:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return

        # 通知主窗口加载任务
        if self.main_window:
            self.main_window.load_task_from_database(task_id)
        else:
            QMessageBox.warning(self, "错误", "无法访问主窗口")

    def export_selected_task(self):
        """导出选中的任务"""
        task_id = self.get_selected_task_id()
        if task_id is None:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "选择导出目录")
        if output_dir:
            try:
                success = self.tool.save_handler.export_to_files(task_id,
                                                                 output_dir)
                if success:
                    QMessageBox.information(self, "导出成功",
                                            f"任务 {task_id} 已导出到 {output_dir}")
                else:
                    QMessageBox.warning(self, "导出失败", "导出过程中出现错误")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    def delete_selected_task(self):
        """删除选中的任务"""
        task_id = self.get_selected_task_id()
        if task_id is None:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return

        # 确认删除
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除任务 {task_id} 吗?\n此操作不可恢复!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.tool.save_handler.delete_task(task_id)
                if success:
                    QMessageBox.information(self, "删除成功", f"任务 {task_id} 已删除")
                    self.refresh_tasks()
                else:
                    QMessageBox.warning(self, "删除失败", "删除过程中出现错误")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {str(e)}")

    def view_task_details(self):
        """查看任务详情"""
        task_id = self.get_selected_task_id()
        if task_id is None:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return

        try:
            task = self.tool.read_handler.get_task_by_id(task_id)
            if task:
                # 创建详情对话框
                dialog = TaskDetailsDialog(task, self)
                dialog.exec()
            else:
                QMessageBox.warning(self, "警告", f"任务 {task_id} 不存在")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取任务详情失败: {str(e)}")

    def export_all_unique(self):
        """导出所有唯一条目"""
        output_dir = QFileDialog.getExistingDirectory(self, "选择导出目录")
        if output_dir:
            try:
                success = self.tool.read_handler.export_all_unique_entries(output_dir)  # noqa
                if success:
                    QMessageBox.information(self, "导出成功",
                                            f"所有唯一条目已导出到 {output_dir}")
                else:
                    QMessageBox.warning(self, "导出失败", "导出过程中出现错误")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")


class TaskDetailsDialog(QDialog):
    """任务详情对话框"""

    def __init__(self, task: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.task = task
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"任务详情 - {self.task['name']}")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        # 任务基本信息
        info_group = QGroupBox("基本信息")
        info_layout = QGridLayout()

        info_layout.addWidget(QLabel("任务ID:"), 0, 0)
        info_layout.addWidget(QLabel(str(self.task['id'])), 0, 1)

        info_layout.addWidget(QLabel("任务名称:"), 1, 0)
        info_layout.addWidget(QLabel(self.task['name']), 1, 1)

        info_layout.addWidget(QLabel("描述:"), 2, 0)
        info_layout.addWidget(QLabel(self.task.get('description', '无')), 2, 1)

        info_layout.addWidget(QLabel("创建时间:"), 3, 0)
        info_layout.addWidget(QLabel(self.task['created_at']), 3, 1)

        info_layout.addWidget(QLabel("用户名数量:"), 4, 0)
        info_layout.addWidget(QLabel(str(self.task['username_count'])), 4, 1)

        info_layout.addWidget(QLabel("密码数量:"), 5, 0)
        info_layout.addWidget(QLabel(str(self.task['password_count'])), 5, 1)

        info_group.setLayout(info_layout)

        # 个人信息
        personal_info = self.task.get('personal_info', {})
        if personal_info:
            personal_group = QGroupBox("个人信息")
            personal_text = QTextEdit()
            personal_text.setReadOnly(True)
            personal_text.setMaximumHeight(150)

            info_text = ""
            for key, value in personal_info.items():
                if value:
                    info_text += f"{key}: {value}\n"

            personal_text.setText(info_text)

            personal_layout = QVBoxLayout()
            personal_layout.addWidget(personal_text)
            personal_group.setLayout(personal_layout)

            layout.addWidget(personal_group)

        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)

        layout.addWidget(info_group)
        layout.addWidget(button_box)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.tool = SocialEngDictionaryTool()
        self.generation_worker = None
        self.tab_widget = None  # 保存选项卡引用
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("社会工程学字典生成工具 - 安全研究专用 By dikesi131@github")
        self.setMinimumSize(1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建选项卡
        self.tab_widget = QTabWidget()

        # 个人信息选项卡
        self.personal_info_widget = PersonalInfoWidget()
        self.tab_widget.addTab(self.personal_info_widget, "个人信息")

        # 生成结果选项卡 - 传入主窗口引用
        self.result_widget = ResultDisplayWidget(main_window=self)
        self.tab_widget.addTab(self.result_widget, "生成结果")

        # 数据库管理选项卡 - 传入主窗口引用
        self.database_widget = DatabaseWidget(self.tool, main_window=self)
        self.tab_widget.addTab(self.database_widget, "数据库管理")

        # 主控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout()

        # 生成按钮组
        generate_group = QGroupBox("字典生成")
        generate_layout = QHBoxLayout()

        self.generate_btn = QPushButton("生成字典")
        self.generate_btn.setMinimumHeight(40)
        self.generate_btn.clicked.connect(self.generate_dictionaries)

        self.stop_btn = QPushButton("停止生成")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_generation)

        generate_layout.addWidget(self.generate_btn)
        generate_layout.addWidget(self.stop_btn)
        generate_layout.addStretch()

        generate_group.setLayout(generate_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # 状态标签
        self.status_label = QLabel("就绪")

        control_layout.addWidget(generate_group)
        control_layout.addWidget(self.progress_bar)
        control_layout.addWidget(self.status_label)
        control_layout.addStretch()

        control_panel.setLayout(control_layout)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget, 1)
        main_layout.addWidget(control_panel, 0)

        central_widget.setLayout(main_layout)

        # 创建菜单栏
        self.create_menu_bar()

        # 安全警告
        self.show_security_warning()

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        if menubar is None:
            menubar = QMenuBar(self)
            self.setMenuBar(menubar)
        else:
            # On some platforms, menuBar() may return None
            # until setMenuBar is called
            if not isinstance(menubar, QMenuBar):
                menubar = QMenuBar(self)
                self.setMenuBar(menubar)

        # 文件菜单
        file_menu = menubar.addMenu('文件')

        load_action = QAction('加载个人信息', self)
        load_action.triggered.connect(self.personal_info_widget.load_from_file)
        file_menu.addAction(load_action)  # type: ignore

        save_action = QAction('保存个人信息', self)
        save_action.triggered.connect(self.personal_info_widget.save_to_file)
        file_menu.addAction(save_action)  # type: ignore

        file_menu.addSeparator()  # type: ignore

        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)  # type: ignore

        # 工具菜单
        tools_menu = menubar.addMenu('工具')

        validate_action = QAction('验证个人信息', self)
        validate_action.triggered.connect(self.personal_info_widget.validate_info)  # noqa
        tools_menu.addAction(validate_action)  # type: ignore

        clear_action = QAction('清空所有信息', self)
        clear_action.triggered.connect(self.clear_all)
        tools_menu.addAction(clear_action)  # type: ignore

        # 帮助菜单
        help_menu = menubar.addMenu('帮助')

        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)  # type: ignore

        warning_action = QAction('安全提醒', self)
        warning_action.triggered.connect(self.show_security_warning)
        help_menu.addAction(warning_action)  # type: ignore

    def show_security_warning(self):
        """显示安全警告"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("安全警告")
        msg.setText("重要安全提醒")
        msg.setInformativeText("""
本工具仅用于授权的安全测试和研究目的！

使用前请确保:
• 已获得适当的授权
• 遵守相关法律法规和道德准则
• 在隔离的测试环境中使用
• 不用于恶意攻击或非法入侵

使用者需自行承担使用本工具的所有责任和风险。
开发者不对任何滥用行为承担责任。
        """)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def show_about(self):
        """显示关于信息"""
        QMessageBox.about(
            self, "关于",
            """社会工程学字典生成工具

版本: 1.0.0
用途: 安全研究和授权测试

功能特点:
• 基于个人信息生成字典
• 支持中英文姓名处理
• 拼音和首字母组合生成
• 数据库持久化存储
• 结果导出和管理

⚠️ 仅用于授权的安全研究！
            """
        )

    def clear_all(self):
        """清空所有信息"""
        reply = QMessageBox.question(
            self, "确认清空",
            "确定要清空所有信息和结果吗?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.personal_info_widget.clear_all()
            self.result_widget.clear_results()
            self.tool.personal_info = None
            self.tool.results = {'usernames': set(), 'passwords': set()}
            self.status_label.setText("已清空所有信息")

    def generate_dictionaries(self):
        """生成字典"""
        # 获取个人信息
        info_dict = self.personal_info_widget.get_info_dict()
        if not info_dict:
            QMessageBox.warning(self, "警告", "请先输入个人信息")
            return

        # 设置个人信息
        try:
            if not self.tool.set_personal_info(**info_dict):
                QMessageBox.critical(self, "错误", "设置个人信息失败")
                return
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置个人信息失败: {str(e)}")
            return

        # 开始生成
        self.generate_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # 创建工作线程
        self.generation_worker = GenerationWorker(self.tool)
        self.generation_worker.progress.connect(self.progress_bar.setValue)
        self.generation_worker.status.connect(self.status_label.setText)
        self.generation_worker.finished.connect(self.on_generation_finished)
        self.generation_worker.start()

    def stop_generation(self):
        """停止生成"""
        if self.generation_worker and self.generation_worker.isRunning():
            self.generation_worker.terminate()
            self.generation_worker.wait()
            self.on_generation_finished(False, {})

    def on_generation_finished(self, success: bool, results: Dict[str, int]):
        """生成完成处理"""
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)

        if success:
            # 更新结果显示
            self.result_widget.update_results(
                self.tool.results['usernames'],
                self.tool.results['passwords']
            )

            self.status_label.setText(
                f"生成完成! 用户名: {results['usernames']} 个, "
                f"密码: {results['passwords']} 个, 总计: {results['total']} 个"
            )

            # 自动切换到结果选项卡
            if self.tab_widget is not None:
                self.tab_widget.setCurrentIndex(1)

        else:
            self.status_label.setText("生成失败或被中断")

    def save_current_results(self):
        """保存当前结果到数据库"""
        if not self.tool.personal_info:
            QMessageBox.warning(self, "警告", "没有个人信息可保存")
            return

        if not self.tool.results['usernames'] and not self.tool.results['passwords']:  # noqa
            QMessageBox.warning(self, "警告", "没有生成结果可保存")
            return

        # 获取任务名称和描述
        dialog = SaveTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_name, description = dialog.get_task_info()

            try:
                task_id = self.tool.save_to_database(task_name, description)
                if task_id > 0:
                    QMessageBox.information(
                        self, "保存成功",
                        f"结果已保存到数据库\n任务ID: {task_id}"
                    )
                    # 刷新数据库列表
                    self.database_widget.refresh_tasks()
                else:
                    QMessageBox.warning(self, "保存失败", "保存到数据库时出现错误")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")

    def load_task_from_database(self, task_id: int):
        """从数据库加载任务"""
        try:
            if self.tool.load_from_database(task_id):
                # 更新个人信息显示
                if self.tool.personal_info:
                    info_dict = self.tool.personal_info.to_dict()
                    self.personal_info_widget.set_info_dict(info_dict)

                # 更新结果显示
                self.result_widget.update_results(
                    self.tool.results['usernames'],
                    self.tool.results['passwords']
                )

                self.status_label.setText(f"已加载任务 {task_id}")

                # 切换到结果选项卡
                if self.tab_widget is not None:
                    self.tab_widget.setCurrentIndex(1)

                QMessageBox.information(
                    self, "加载成功",
                    f"任务 {task_id} 已加载\n"
                    f"用户名: {len(self.tool.results['usernames'])} 个\n"
                    f"密码: {len(self.tool.results['passwords'])} 个"
                )
            else:
                QMessageBox.warning(self, "加载失败", f"无法加载任务 {task_id}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载任务失败: {str(e)}")

    def load_settings(self):
        """加载设置"""
        settings = QSettings('SocialEngDict', 'MainWindow')
        self.restoreGeometry(settings.value('geometry', b''))
        self.restoreState(settings.value('windowState', b''))

    def save_settings(self):
        """保存设置"""
        settings = QSettings('SocialEngDict', 'MainWindow')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())

    def closeEvent(self, event):
        """关闭事件"""
        self.save_settings()

        # 停止正在运行的线程
        if self.generation_worker and self.generation_worker.isRunning():
            self.generation_worker.terminate()
            self.generation_worker.wait()

        event.accept()


class SaveTaskDialog(QDialog):
    """保存任务对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("保存到数据库")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # 任务名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("任务名称:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请输入任务名称")
        # 设置默认名称
        default_name = f"任务_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.name_edit.setText(default_name)
        name_layout.addWidget(self.name_edit)

        # 任务描述
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("任务描述 (可选):"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        self.desc_edit.setPlaceholderText("请输入任务描述...")
        desc_layout.addWidget(self.desc_edit)

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel  # noqa
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(name_layout)
        layout.addLayout(desc_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_task_info(self) -> tuple:
        """获取任务信息"""
        return (self.name_edit.text().strip(),
                self.desc_edit.toPlainText().strip())


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置应用程序信息
    app.setApplicationName("社会工程学字典生成工具")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SecurityResearch")

    # 设置样式
    app.setStyle('Fusion')

    # 设置完整的美化样式表
    app.setStyleSheet(STYLE_SHEET)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
