import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QTableView, QMessageBox, QTextEdit, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5 import QtCore

from modificationlist import ModificationList
from dataframemodel import DataFrameModel
from utility import read_files, get_modifications, filter_by_modifications

class PTMViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # initialize instance variables
        self.input_file_path = None
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.modifications = []
        
        # initialize UI
        self.setWindowTitle("PTM Viewer")

        self.input_file_path_label = QLabel(self)
        self.input_file_path_label.setFixedHeight(26)
        self.input_file_path_label.setText("File Path: ")

        self.input_file_path_text = QTextEdit(self)
        self.input_file_path_text.setFixedHeight(26)
        self.input_file_path_text.setDisabled(True)
        self.input_file_path_text.setWordWrapMode(0)
        self.input_file_path_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.input_file_path_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.open_file_button = QPushButton("Open File", self)
        self.open_file_button.clicked.connect(self.open_file)

        self.table = QTableView(self)

        self.modifications_label = QLabel(self)
        self.modifications_label.setText("Detected Modifications: ")

        self.modifications_list = ModificationList(self)
        self.modifications_list.updated.connect(self.filter_df)

        self.export_button = QPushButton("Export", self)
        self.export_button.clicked.connect(self.export)
        self.export_button.setDisabled(True)

        # create layout
        self.top_row = QHBoxLayout()
        self.top_row.addWidget(self.input_file_path_label)
        self.top_row.addWidget(self.input_file_path_text)
        self.top_row.addWidget(self.open_file_button)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.addWidget(self.modifications_label)
        self.bottom_row.addWidget(self.modifications_list)
        self.bottom_row.addWidget(self.export_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_row)
        self.main_layout.addWidget(self.table)
        self.main_layout.addLayout(self.bottom_row)

        # set layout
        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "CSV Files (*.csv);;TSV Files (*.tsv);;Excel Files (*.xlsx)")
        if not file_path:
            return
        
        try:
            self.df = read_files(self.input_file_path)
            self.modifications, counts = get_modifications(self.df)
            self.input_file_path = file_path

            self.table.setModel(DataFrameModel(self.df))
            self.modifications_list.set_modifications(self.modifications, counts)
            self.input_file_path_text.setText(",".join(self.input_file_path))
            self.export_button.setDisabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def export(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if not file_path:
            return
        
        self.filtered_df.to_csv(file_path, index=False)

    def filter_df(self, modifications):
        self.filtered_df = filter_by_modifications(self.df, modifications) if modifications else self.df
        self.table.setModel(DataFrameModel(self.filtered_df))

def main():
    app = QApplication(sys.argv)
    window = PTMViewerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
