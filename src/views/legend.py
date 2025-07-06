from PyQt6.QtWidgets import QMenu, QWidget, QHBoxLayout, QLabel, QFrame, QVBoxLayout
from PyQt6.QtGui import QAction, QColor, QFont

class LegendItem(QWidget):
    def __init__(self, description, color=QColor("white")):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)
        
        desc_label = QLabel(description)
        font = QFont("Arial", 10)
        desc_label.setFont(font)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        if color and color != QColor("white"):
            color_box = QFrame()
            color_box.setFixedSize(20, 20)
            color_box.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            layout.addWidget(color_box)

    @staticmethod
    def setup_legend(layout):
        """Setup the legend with all availability types and their colors"""
        legend_data = [
            ("Business Trip (BT)", None),
            ("Parental Leave (PL)", None),
            ("Compassionate Leave (CL)", None),
            ("Home Office (HO)", None),
            ("Vacation (V)", None),
            ("Training (T)", None),
            ("Bank Holiday (DE)", QColor(102, 102, 0)),
            ("Bank Holiday (UK)", QColor(0, 102, 0)),
            ("Bank Holiday (DE and UK)", QColor(0, 102, 153)),
            ("Bridge Day (DE)", QColor(204, 71, 0)),
            ("School Holidays (DE)", QColor(0, 51, 153)),
            ("School Holidays (UK)", QColor(153, 51, 102)),
            ("School Holidays (DE and UK)", QColor(75, 0, 130)),
            ("Team Event", QColor(153, 102, 51)),
            ("Planned Go Live", QColor(153, 0, 0))
        ]
        
        # Add title
        title_label = QLabel("Availability Legend")
        title_font = QFont("Arial", 12, QFont.Weight.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Add legend items
        for desc, color in legend_data:
            item = LegendItem(desc, color)
            layout.addWidget(item)
        
        layout.addStretch()
