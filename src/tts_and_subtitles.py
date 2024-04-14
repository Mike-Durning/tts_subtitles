from PyQt6.QtWidgets import QTabWidget, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QInputDialog  # noqa: E501
from PyQt6.QtWidgets import QApplication, QComboBox, QPushButton, QCheckBox, QTextEdit, QHBoxLayout  # noqa: E501
#from PyQt6.QtGui  import QIcon
import sys, os
from pathlib import Path
from lib import Config
import subprocess


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # set_up.py 
        self.file_config = Config()
        self.file_config.instantiate_dicts()
        self.file_config.folders_exist()
        self.file_config.save_format_info_to_json()
        self.file_config.save_file_path_to_json()
        self.file_config.save_audio_sequence_to_json()      
                               
        self.setWindowTitle("TTS Converter")
        self.setGeometry(175, 25, 1000, 700)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts
        main_layout = QVBoxLayout() # Changed to a vertical layout for the entire window
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget) # Add the tab widget to the main layout

        # Create the first tab
        first_tab = QWidget()
        tab_widget.addTab(first_tab, "TTS Connections") # Add the first tab to the tab widget  # noqa: E501

        button_layout = QGridLayout() # Grid layout for buttons
        
        # Create a QTextEdit widget for the first output
        self.output_text1 = QTextEdit()
        self.output_text1.setReadOnly(True)

        # Create a QTextEdit widget for the second output
        self.output_text2 = QTextEdit()
        self.output_text2.setReadOnly(True)

        # Add QTextEdit widgets directly to the layout
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_text1, 2)  # 2/3 of horizontal space
        output_layout.addWidget(self.output_text2, 1)  # 1/3 of horizontal space

        # Add layouts and widgets to the first tab
        first_tab_layout = QVBoxLayout()
        first_tab_layout.addLayout(button_layout)
        first_tab_layout.addLayout(output_layout)  # Add the horizontal output layout
        first_tab.setLayout(first_tab_layout)  # Set the layout for the first tab

        # Create a container widget for the layouts
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

        # Apply dark mode stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333;
                color: #FFF;
            }
                  
            QPushButton, QRadioButton, QCheckBox {
                background-color: #444;
                color: #FFF;
                text-align: center;
                border: 1px solid #555;
                padding: 5px;
            }
            
            QComboBox, QComboBox QAbstractItemView::item {
                background-color: #444;
                text-align: center;
                color: #FFF;
            }
            
            QFrame {
                background-color: #444;
                border: 1px solid #555;
            }
            QLineEdit {
                background-color: #555;
                color: #FFF;
                border: 1px solid #666;
                padding: 5px;
            }
            QTextEdit {
                background-color: #555;
                color: #FFF;
                border: 1px solid #666;
                padding: 5px;
            }
            QLabel {
                color: #FFF;
            }
            
            QTabWidget {
                background-color: #444;
            }
       
        """)
   
        dropdown_position = {
            # First button, dropdown menu
            "Select Client"               : (0, 0)
        }
        
        add_remove_client_position = {
            # Middle Left Button Row - ADD REMOVE CLIENT
            "Add"                            : (1, 0),
            "Remove"                       : (1, 1),
        }
        
        button_positions = {
            
            # Top Button Row | Excluding first
            "Create Audio"                : (0, 1),
            "Create Subtitle"            : (0, 2),
           
            
            # Middle Right Button Row
            "Clear Output"                : (1, 2),
            
            # Bottom Toggle Row
            "Select Model .onnx"        : (2, 0),
            "Select Model .json"        : (2, 1),
            "Select Custom Directory" : (2, 2)
        }

        for text, (row, col) in add_remove_client_position.items():
            button = QPushButton(text)
            button.clicked.connect(lambda _, text=text: self.on_button_click(text))
            button_layout.addWidget(button, row, col)
                    
        for text, (row, col) in dropdown_position.items():
            self.drop_menu = QComboBox()
            button_layout.addWidget(self.drop_menu, row, col)
            if text == "Select Client":
                    self.drop_menu.activated.connect(self.on_drop_menu_execute)

        for text, (row, col) in button_positions.items():
            if text.startswith("Select"):
                button = QPushButton(text)
                toggle_button = QCheckBox(text)
                button_layout.addWidget(button, row, col)
                button_layout.addWidget(toggle_button, row, col)
                
                if text == "Select Model .onnx":
                    toggle_button.stateChanged.connect(self.is_default_onnx)
                elif text == "Select Model .json":
                    toggle_button.stateChanged.connect(self.is_default_json)
                elif text == "Select Custom Directory":
                    toggle_button.stateChanged.connect(self.is_default_dir)
            else:
                button = QPushButton(text)
                button_layout.addWidget(button, row, col)
                
                if text == "Create Audio":
                    button.clicked.connect(self.audio_create)
                elif text == "Create Subtitle":
                    button.clicked.connect(self.subtitle_create)
                elif text == "Clear Output":
                    button.clicked.connect(self.clear_output)

        self.audio_sequence_formatted, self.audio_sequence_dict, self.audio_sequence_json_path = self.file_config.print_dict_or_json(Path(self.file_config.path_data["audio_sequence_json"]))
        self.file_config.count_words_and_characters(self.audio_sequence_json_path)

        self.populate_client_list_menu()
    
    def output_states_update(self): 
        self.output_text2.clear()
        output_settings_formatted,A,b = self.file_config.print_dict_or_json(Path(self.file_config.path_data["output_settings_json"]))
        self.output_text2.append(output_settings_formatted)      
            
    def populate_client_list_menu(self): # Inputs client list into Output 2
        
        self.client_list_formatted, client_list_dict, client_list_json_path = self.file_config.print_dict_or_json(Path(self.file_config.path_data["audio_sequence_json"]))
        
        self.output_text2.clear()
        if self.client_list_formatted:
            self.output_text2.append(self.client_list_formatted)
              
        client_dict = client_list_dict
        client_list = client_dict.values() 
        self.drop_menu.addItems(client_list)
    
    def drop_menu_select(self):   
        selected = self.drop_menu.currentText()
        
        if not selected:
            self.output_text1.append("No client selected in the dropdown.")
    
        self.output_text1.append(f"Selected Client: {selected}")
        
        selected_client = self.file_config.select_client_by_value(selected)
        
        if selected_client is not None:
            self.file_config.format_info["client_name"] = selected_client               
    
    def on_drop_menu_execute(self):
        self.drop_menu_select()
        self.output_2_update()             
        
    def audio_create(self):
        audio_sequence_file_name = self.audio_sequence_dict.copy()
        
        
        self.output_text1.append("Create Audio Selected")
        self.output_text2.clear()
        
        if self.audio_sequence_formatted:
            self.output_text2.append(self.audio_sequence_formatted)
                                      
        for key, value in self.audio_sequence_dict.items(): 
            
            audio_create = (
                'echo "{text}" | .\\piper.exe --model {model_onnx_file} --config {model_json_file} --output_file {output_file}.wav'
            )

            
            output_file = str(self.file_config.format_info.get("date")) + "-" + str(key) + "-" + str(self.file_config.format_info.get("project_title"))            
            
            save_file_name=str(output_file + self.file_config.format_info.get("file_type"))
            audio_sequence_file_name[key]=save_file_name
            
            command = audio_create.format(
                    output_file=str(output_file),
                    text=str(value),
                    
                    file_type=self.file_config.format_info.get("file_type"),
                    model_onnx_file=self.file_config.format_info.get("tts_model_onnx"),
                    model_json_file=self.file_config.format_info.get("tts_model_json"),
                    tts_output_dir=self.file_config.format_info.get("tts_output_dir")
                    )

            try:
                os.chdir(self.file_config.path_data["piper_tts_folder"])                
                subprocess.run(command, shell=True, check=True)
                self.file_config.move_specific_files(self.file_config.format_info.get("tts_directory"), self.file_config.format_info.get("tts_output_dir"), save_file_name)
                print("Command executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                
        add_audio_sequence_to_output = {**self.file_config.format_info, **audio_sequence_file_name}
        self.file_config.save_to_json(add_audio_sequence_to_output, self.file_config.path_data["output_settings_json"])

    def subtitle_create(self):
        self.output_text1.append("Create Subtitles Selected")
        os.chdir(self.file_config.format_info["tts_output_dir"])
        self.audio_sequence_formatted, format_audio_sequence_dict, audio_sequence_json_path = self.file_config.print_dict_or_json(Path(self.file_config.path_data["output_settings_json"]))
        
        self.output_text2.clear()
        if self.audio_sequence_formatted:
            self.output_text2.append(self.audio_sequence_formatted)
               
        for key, value in format_audio_sequence_dict.items():          
            if key.isdigit():
                subtitle_create = (
                     'whisper {input_file} --model {model_whisper} --language {language} --output_dir {output_dir} --output_format {output_format} --task {task} --word_timestamps {word_timestamps} --highlight_words {highlight_words} --max_line_width {max_line_width} --max_words_per_line {max_words_per_line}'
                )
                
                project_title = format_audio_sequence_dict.get("project_title")
                
                output_file = str(key) + "-" + project_title
                
                fix_subtitle_numbering_title = format_audio_sequence_dict.get("date") + "-" + output_file + ".vtt"
                
                output = format_audio_sequence_dict.get("tts_output_dir")
                
                fixed_output = output + "/" + fix_subtitle_numbering_title                
                
                print(output_file, fixed_output)
                
                command = subtitle_create.format(
                    input_file=str(value),
                    model_whisper=format_audio_sequence_dict.get("whisper_model"),
                    language=format_audio_sequence_dict.get("language"),
                    output_dir=format_audio_sequence_dict.get("whisper_output_dir"),
                    output_format=format_audio_sequence_dict.get("subtitle_format"),
                    task=format_audio_sequence_dict.get("task"),
                    word_timestamps=format_audio_sequence_dict.get("word_timestamps"),  # Add appropriate values here based on requirements
                    highlight_words=format_audio_sequence_dict.get("highlight_words"),
                    max_line_width=format_audio_sequence_dict.get("max_line_width"),  # Example value, adjust as needed
                    max_words_per_line=format_audio_sequence_dict.get("max_words_per_line")  # Example value, adjust as needed
                )

                try:
                    subprocess.run(command, shell=True, check=True)
                    self.file_config.add_subtitle_order_numbers(fixed_output,fixed_output)
                    self.file_config.save_to_json(self.file_config.format_info,self.file_config.path_data["output_settings_json"])
                    self.output_states_update()
                    print("Command executed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")    

    def clear_output(self):
            self.output_text1.clear()
            self.output_states_update()
            self.populate_client_list_menu()

    def is_default_onnx(self):
            if self.sender().isChecked():
                self.output_text1.append("'Toggle Onnx Model is ON")
                
                self.file_config.format_info["toggle_model"] = True
                
                tts_model_onnx = self.file_config.manual_return_file(directory=self.file_config.path_data["piper_tts_folder"])
                self.file_config.format_info["tts_model_onnx"] = tts_model_onnx
                
                project_title, ok = QInputDialog.getText(self, "Add", "Enter Name:")
                if ok:
                    self.file_config.format_info["project_title"] = project_title
                    self.output_text1.append(f"Added: {project_title} as project title")

            else:
                self.output_text1.append("'Toggle Onnx Model is OFF")
                
                self.file_config.format_info["toggle_model"] = False
                self.file_config.format_info["tts_model_onnx"] = None
            
            self.file_config.save_to_json(self.file_config.format_info,self.file_config.path_data["output_settings_json"])
            self.output_states_update()
            
    def is_default_json(self):
            if self.sender().isChecked():
                self.output_text1.append("'Toggle Json Config is ON")
                
                self.file_config.format_info["toggle_json"] = True
                
                tts_model_json = self.file_config.manual_return_file(directory=self.file_config.path_data["piper_tts_folder"])
                self.file_config.format_info["tts_model_json"] = tts_model_json

            else:
                self.output_text1.append("'Toggle Custom Directory is OFF")
                
                self.file_config.format_info["toggle_json"] = False
                self.file_config.format_info["tts_model_json"] = None
                
            self.file_config.save_to_json(self.file_config.format_info,self.file_config.path_data["output_settings_json"])
            self.output_states_update()
        
    def is_default_dir(self):
        if self.sender().isChecked():
            self.output_text1.append("'Toggle Custom Directory is ON")
            
            self.file_config.format_info["toggle_directory"] = True
            
            tts_directory = self.file_config.manual_return_dir()
            self.file_config.format_info["tts_directory"] = tts_directory
            
            tts_output_dir = self.file_config.manual_return_dir()
            self.file_config.format_info["tts_output_dir"] = tts_output_dir 
            self.file_config.format_info["whisper_output_dir"] = tts_output_dir                       
            
        else:
            self.output_text1.append("'Toggle Custom Directory is OFF")
            
            self.file_config.format_info["toggle_directory"] = False
            self.file_config.format_info["tts_directory"] = None
            self.file_config.format_info["tts_output_dir"] = None
            self.file_config.format_info["whisper_output_dir"] = None
            
        self.file_config.save_to_json(self.file_config.format_info,self.file_config.path_data["output_settings_json"])
        self.output_states_update()

# FOR ADDING AND REMOVE FROM JSON         #elizabeth mary ann
    def on_button_click(self, button_text):        
            if button_text == "Add":
                client_name, ok = QInputDialog.getText(self, "Add", "Enter Name:")
                if ok:
                    self.file_config.add_client(client_name)
                    self.file_config.count_words_and_characters(self.audio_sequence_json_path)
                    self.file_config.save_to_json(self.file_config.format_info,self.file_config.path_data["output_settings_json"])
                    
                    self.output_text1.append(f"Added: {client_name}")
                    self.drop_menu.clear() 
                    self.output_states_update()
            
            elif button_text == "Remove":
                client_index, ok = QInputDialog.getText(self, "Remove", "Enter Index:")
                if ok:
                    self.file_config.delete_client(client_index)
                    self.file_config.count_words_and_characters(self.audio_sequence_json_path)
                    self.file_config.save_to_json(self.file_config.format_info,self.file_config.path_data["output_settings_json"])
                    
                    self.output_text1.append(f"Removed at Index: {client_index}")
                    self.drop_menu.clear() 
                    self.output_states_update()
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())