from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QHBoxLayout
from PyQt5 import QtCore

class ModificationList(QWidget):
    updated = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.checkboxes = []
        self.labels = []

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(16)
        self.layout.addStretch()

    def add_modification(self, modification, count):
        checkbox = QCheckBox(f"{modification} ({count})", self)
        # label = QLabel(f'({count})')
        # label.width = 100
        self.layout.insertWidget(len(self.layout) - 1, checkbox)
        # self.layout.insertWidget(len(self.layout) - 1, label)
        self.checkboxes.append(checkbox)
        # self.labels.append(label)
        checkbox.stateChanged.connect(lambda: self.updated.emit(self.get_checked_modifications()))

    def set_modifications(self, modifications, counts):
        self.clear()
        for modification, count in zip(modifications, counts):
            self.add_modification(modification, count)

    def get_checked_modifications(self):
        return [checkbox.text().split()[0] for checkbox in self.checkboxes if checkbox.isChecked()]

    def clear(self):
        for checkbox in self.checkboxes:
            self.layout.removeWidget(checkbox)
            checkbox.deleteLater()
        self.checkboxes = []

    def __del__(self):
        self.clear()