STYLE_SHEET = """
    /* ================ 第一部分：全局样式和主要控件 ================ */
    QWidget {
        background-color: #f8f9fa;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 13px;
        color: #212529;
        line-height: 1.4;
    }

    QMainWindow {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
    }

    QGroupBox {
        font-weight: 600;
        font-size: 14px;
        color: #495057;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 10px;
        background-color: #ffffff;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 12px;
        background-color: #ffffff;
        color: #343a40;
        font-weight: 700;
    }

    QLabel {
        color: #495057;
        font-weight: 500;
        padding: 2px 4px;
        background-color: transparent;
    }

    QPushButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6db4f0, stop: 1 #4a9de8);
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        min-height: 20px;
    }

    QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #4a9de8, stop: 1 #3a8cdb);
        box-shadow: 0 4px 8px rgba(109, 180, 240, 0.3);
    }

    QPushButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #3a8cdb, stop: 1 #2a7bc8);
    }

    QPushButton:disabled {
        background-color: #6c757d;
        color: #adb5bd;
        border: 1px solid #6c757d;
    }

    QLineEdit, QTextEdit {
        border: 2px solid #ced4da;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #ffffff;
        color: #495057;
        font-size: 13px;
        selection-background-color: #6db4f0;
        selection-color: #ffffff;
    }

    QLineEdit:focus, QTextEdit:focus {
        border-color: #6db4f0;
        background-color: #ffffff;
        outline: none;
    }

    QLineEdit:hover, QTextEdit:hover {
        border-color: #adb5bd;
    }

    /* ================ 第二部分：表格、选项卡和进度条 ================ */
    QTableWidget {
        border: 2px solid #e9ecef;
        border-radius: 8px;
        background-color: #ffffff;
        gridline-color: #f8f9fa;
        selection-background-color: #e3f2fd;
        alternate-background-color: #f8f9fa;
        font-size: 13px;
        color: #495057;
    }

    QTableWidget::item {
        padding: 12px 8px;
        border-bottom: 1px solid #e9ecef;
        color: #495057;
    }

    QTableWidget::item:selected {
        background-color: #6db4f0;
        color: #ffffff;
        border: none;
    }

    QTableWidget::item:hover {
        background-color: #f1f3f4;
        color: #212529;
    }

    QHeaderView::section {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6db4f0, stop: 1 #4a9de8);
        color: #ffffff;
        padding: 12px 8px;
        border: none;
        border-right: 1px solid #4a9de8;
        font-weight: 600;
        font-size: 13px;
    }

    QTabWidget::pane {
        border: 2px solid #e9ecef;
        border-radius: 8px;
        background-color: #ffffff;
        margin-top: -1px;
        padding: 16px;
    }

    QTabBar::tab {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
        border: 2px solid #dee2e6;
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        padding: 12px 24px;
        margin-right: 2px;
        color: #6c757d;
        font-weight: 500;
        font-size: 13px;
        min-width: 100px;
    }

    QTabBar::tab:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f8f9fa);
        border-color: #6db4f0;
        color: #6db4f0;
        font-weight: 600;
        border-bottom: 2px solid #ffffff;
        margin-bottom: -2px;
    }

    QProgressBar {
        border: 2px solid #e9ecef;
        border-radius: 8px;
        background-color: #f8f9fa;
        text-align: center;
        font-weight: 600;
        font-size: 13px;
        color: #495057;
        height: 24px;
        margin: 4px 0;
    }

    QProgressBar::chunk {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #28a745, stop: 0.4 #20c997, 
                                    stop: 0.6 #6db4f0, stop: 1 #6f42c1);
        border-radius: 6px;
        margin: 2px;
    }

    /* ================ 第三部分：滚动条、对话框、复选框和特殊效果 ================ */

    /* ================ 滚动条样式 ================ */
    QScrollBar:vertical {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
        width: 14px;
        border: none;
        border-radius: 7px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #adb5bd, stop: 0.5 #6c757d, stop: 1 #adb5bd);
        min-height: 30px;
        border-radius: 6px;
        margin: 1px;
    }

    QScrollBar::handle:vertical:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #6db4f0, stop: 0.5 #4a9de8, stop: 1 #6db4f0);
    }

    QScrollBar::handle:vertical:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #3a8cdb, stop: 0.5 #2a7bc8, stop: 1 #3a8cdb);
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }

    QScrollBar:horizontal {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
        height: 14px;
        border: none;
        border-radius: 7px;
        margin: 0;
    }

    QScrollBar::handle:horizontal {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #adb5bd, stop: 0.5 #6c757d, stop: 1 #adb5bd);
        min-width: 30px;
        border-radius: 6px;
        margin: 1px;
    }

    QScrollBar::handle:horizontal:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6db4f0, stop: 0.5 #4a9de8, stop: 1 #6db4f0);
    }

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
        width: 0px;
    }

    /* ================ 对话框样式 ================ */
    QDialog {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f8f9fa);
        border: 2px solid #6db4f0;
        border-radius: 12px;
    }

    QDialogButtonBox {
        background-color: transparent;
        border: none;
        padding: 12px;
    }

    QDialogButtonBox QPushButton {
        min-width: 100px;
        margin: 0 4px;
    }

    /* ================ 消息框样式 ================ */
    QMessageBox {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f8f9fa);
        border: 2px solid #dee2e6;
        border-radius: 12px;
        font-size: 13px;
    }

    QMessageBox QLabel {
        color: #495057;
        font-weight: 500;
        padding: 16px;
    }

    QMessageBox QPushButton {
        min-width: 80px;
        margin: 4px;
    }

    /* ================ 复选框和单选框样式 ================ */
    QCheckBox {
        spacing: 8px;
        color: #495057;
        font-weight: 500;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #ced4da;
        border-radius: 4px;
        background-color: #ffffff;
    }

    QCheckBox::indicator:hover {
        border-color: #6db4f0;
        background-color: #f8f9fa;
    }

    QCheckBox::indicator:checked {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6db4f0, stop: 1 #4a9de8);
        border-color: #6db4f0;
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xMSAxTDQgOEwxIDUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
    }

    QRadioButton {
        spacing: 8px;
        color: #495057;
        font-weight: 500;
    }

    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #ced4da;
        border-radius: 9px;
        background-color: #ffffff;
    }

    QRadioButton::indicator:hover {
        border-color: #6db4f0;
        background-color: #f8f9fa;
    }

    QRadioButton::indicator:checked {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6db4f0, stop: 1 #4a9de8);
        border-color: #6db4f0;
    }

    QRadioButton::indicator:checked::after {
        content: "";
        width: 8px;
        height: 8px;
        border-radius: 4px;
        background-color: #ffffff;
        margin: 3px;
    }

    /* ================ 下拉框样式 ================ */
    QComboBox {
        border: 2px solid #ced4da;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #ffffff;
        color: #495057;
        font-size: 13px;
        min-width: 100px;
    }

    QComboBox:hover {
        border-color: #adb5bd;
    }

    QComboBox:focus {
        border-color: #6db4f0;
        outline: none;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left: 1px solid #ced4da;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
    }

    QComboBox::down-arrow {
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzZjNzU3ZCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+Cg==);
        width: 12px;
        height: 8px;
    }

    QComboBox QAbstractItemView {
        border: 2px solid #e9ecef;
        border-radius: 8px;
        background-color: #ffffff;
        selection-background-color: #6db4f0;
        selection-color: #ffffff;
        padding: 4px;
    }

    /* ================ 数值输入框样式 ================ */
    QSpinBox, QDoubleSpinBox {
        border: 2px solid #ced4da;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #ffffff;
        color: #495057;
        font-size: 13px;
    }

    QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #6db4f0;
        outline: none;
    }

    QSpinBox::up-button, QDoubleSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #ced4da;
        border-top-right-radius: 6px;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
    }

    QSpinBox::down-button, QDoubleSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 20px;
        border-left: 1px solid #ced4da;
        border-bottom-right-radius: 6px;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #e9ecef, stop: 1 #f8f9fa);
    }

    /* ================ 分割器增强样式 ================ */
    QSplitter::handle {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #e9ecef, stop: 0.5 #dee2e6, stop: 1 #e9ecef);
        border: 1px solid #adb5bd;
        border-radius: 4px;
        margin: 2px;
    }

    QSplitter::handle:horizontal {
        width: 8px;
    }

    QSplitter::handle:vertical {
        height: 8px;
    }

    QSplitter::handle:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #6db4f0, stop: 0.5 #4a9de8, stop: 1 #6db4f0);
    }

    /* ================ 状态栏增强样式 ================ */
    QStatusBar {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
        border-top: 2px solid #dee2e6;
        padding: 8px 16px;
        color: #6c757d;
        font-size: 12px;
        font-weight: 500;
    }

    /* ================ 菜单系统增强 ================ */
    QMenuBar {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f8f9fa);
        border-bottom: 2px solid #dee2e6;
        padding: 4px 8px;
        color: #495057;
        font-weight: 500;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 8px 16px;
        border-radius: 6px;
        color: #495057;
    }

    QMenuBar::item:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #e9ecef, stop: 1 #dee2e6);
        color: #212529;
    }

    QMenuBar::item:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6db4f0, stop: 1 #4a9de8);
        color: #ffffff;
    }

    QMenu {
        background-color: #ffffff;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        padding: 8px 0;
        color: #495057;
        font-size: 13px;
    }

    QMenu::item {
        padding: 10px 20px;
        border: none;
        background-color: transparent;
    }

    QMenu::item:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6db4f0, stop: 1 #4a9de8);
        color: #ffffff;
        border-radius: 4px;
        margin: 2px 4px;
    }

    QMenu::separator {
        height: 1px;
        background-color: #e9ecef;
        margin: 4px 16px;
    }

    /* ================ 工具提示增强 ================ */
    QToolTip {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #343a40, stop: 1 #495057);
        color: #ffffff;
        border: 2px solid #6c757d;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 12px;
        font-weight: 500;
        opacity: 240;
    }

    /* ================ 特殊效果和动画样式 ================ */

    /* 阴影效果 */
    QGroupBox, QDialog, QMessageBox {
        border: 2px solid #e9ecef;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f8f9fa);
    }

    /* 统计数值标签特殊样式 - 增强版 */
    QLabel[objectName*="count"] {
        color: #6db4f0;
        font-weight: 700;
        font-size: 24px;
        padding: 15px 20px;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f8f9fa);
        border: 3px solid #6db4f0;
        border-radius: 12px;
        min-width: 80px;
        min-height: 40px;
        text-align: center;
    }

    /* 统计区域增强样式 */
    QGroupBox[objectName="stats_group"] {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f0f8ff);
        border: 3px solid #6db4f0;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        font-size: 16px;
        font-weight: 700;
    }

    QGroupBox[objectName="stats_group"]::title {
        color: #6db4f0;
        font-size: 18px;
        font-weight: 800;
        padding: 0 15px;
    }

    /* 统计标签文字样式 */
    QLabel[objectName*="stat_label"] {
        color: #343a40;
        font-weight: 600;
        font-size: 16px;
        padding: 10px 15px;
    }

    /* 成功状态按钮 */
    QPushButton[class="success"] {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #28a745, stop: 1 #1e7e34);
    }

    QPushButton[class="success"]:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #1e7e34, stop: 1 #155724);
    }

    /* 警告状态按钮 */
    QPushButton[class="warning"] {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffc107, stop: 1 #e0a800);
        color: #212529;
    }

    QPushButton[class="warning"]:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #e0a800, stop: 1 #d39e00);
    }

    /* 危险状态按钮 */
    QPushButton[class="danger"] {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #dc3545, stop: 1 #c82333);
    }

    QPushButton[class="danger"]:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #c82333, stop: 1 #a71d2a);
    }

    /* 只读文本框特殊样式 */
    QTextEdit[readOnly="true"] {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff, stop: 1 #f8f9fa);
        border: 2px solid #e9ecef;
        color: #495057;
    }

    /* 焦点指示器 */
    QWidget:focus {
        outline: none;
    }
    """  # noqa