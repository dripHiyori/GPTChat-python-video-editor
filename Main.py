import os
import subprocess
from PyQt5 import QtWidgets, QtGui

class VideoEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a QLineEdit for the input file
        self.input_edit = QtWidgets.QLineEdit()
        self.input_edit.setPlaceholderText('Input file')

        # Create a QLineEdit for the output file
        self.output_edit = QtWidgets.QLineEdit()
        self.output_edit.setPlaceholderText('Output file')

        # Create a QSpinBox for the start time
        self.start_spinbox = QtWidgets.QSpinBox()
        self.start_spinbox.setMinimum(0)
        self.start_spinbox.setMaximum(3600)

        # Create a QSpinBox for the end time
        self.end_spinbox = QtWidgets.QSpinBox()
        self.end_spinbox.setMinimum(0)
        self.end_spinbox.setMaximum(3600)

        # Create a QComboBox for the quality
        self.quality_combobox = QtWidgets.QComboBox()
        self.quality_combobox.addItems(['Low', 'Medium', 'High', 'Custom'])
        self.quality_combobox.currentTextChanged.connect(self.update_quality)

        # Create a QLineEdit for the custom quality value
        self.quality_edit = QtWidgets.QLineEdit()
        self.quality_edit.setPlaceholderText('Quality value')
        self.quality_edit.setVisible(False)

        # Create a QPushButton for the trim action
        self.trim_button = QtWidgets.QPushButton('Trim')
        self.trim_button.clicked.connect(self.trim_video)

        # Create a layout and add the widgets
        layout = QtWidgets.QFormLayout()
        layout.addRow('Input:', self.input_edit)
        layout.addRow('Output:', self.output_edit)
        layout.addRow('Start time (seconds):', self.start_spinbox)
        layout.addRow('End time (seconds):', self.end_spinbox)
        layout.addRow('Quality:', self.quality_combobox)
        layout.addRow(self.quality_edit)
        layout.addRow(self.trim_button)
        self.setLayout(layout)

    def update_quality(self, quality):
        # Show or hide the custom quality line edit based on the selected quality level
        if quality == 'Custom':
            self.quality_edit.setVisible(True)
        else:
            self.quality_edit.setVisible(False)

    def trim_video(self):
        # Get the input and output file paths
        input_file = self.input_edit.text()
        output_file = self.output_edit.text()

                # Get the start and end times
        start_time = self.start_spinbox.value()
        end_time = self.end_spinbox.value()

        # Get the quality level and value
        quality = self.quality_combobox.currentText()
        if quality == 'Custom':
            quality_value = self.quality_edit.text()
        else:
            quality_value = quality

        # Use FFmpeg to trim the video
        command = ['ffmpeg', '-i', input_file, '-ss', str(start_time), '-to', str(end_time)]
        
        # Add the quality options
        if quality == 'Low':
            command += ['-b:v', '250k']
        elif quality == 'Medium':
            command += ['-b:v', '500k']
        elif quality == 'High':
            command += ['-b:v', '750k']
        elif quality == 'Custom':
            command += ['-b:v', quality_value]

        command += ['-c:a', 'copy', output_file]
        subprocess.run(command)

app = QtWidgets.QApplication([])

# Set the style sheet to apply a dark theme
app.setStyleSheet('''
    QWidget {
        background-color: #333333;
        color: white;
    }
    QLineEdit {
        background-color: #444444;
        border: 1px solid #555555;
        color: white;
    }
    QSpinBox {
        background-color: #444444;
        border: 1px solid #555555;
        color: white;
    }
    QComboBox {
        background-color: #444444;
        border: 1px solid #555555;
        color: white;
    }
        QPushButton {
        background-color: #444444;
        border: 1px solid #555555;
        color: white;
    }
''')

window = VideoEditor()
window.show()
app.exec_()


