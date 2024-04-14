from tkinter.filedialog import askdirectory, askopenfilename
from datetime import datetime
from pathlib import Path
import json
import os,wave,shutil

class Config:
    def __init__(self):
        
        self.src_folder = Path(__file__).resolve().parent
        self.project_folder = self.src_folder.parent
        
        self.config_folder      = self.project_folder / "config"
        self.output_folder      = self.project_folder / "output"
        self.piper_tts_folder   = self.project_folder / "piper"
      
    def instantiate_dicts(self):
                         
        self.path_data = {
            "project_folder"            : str(self.project_folder),
            "config_folder"             : str(self.config_folder),
            "piper_tts_folder"          : str(self.piper_tts_folder),
            "config_file_path_json"     : str(self.config_folder       / "file_path.json"),
            "settings_json"             : str(self.config_folder       / "settings.json"),
            "audio_sequence_json"       : str(self.config_folder       / "audio_sequence.json"),
            "output_settings_json"      : str(self.output_folder       / "output_settings.json"),
            "output_folder"             : str(self.output_folder),
            "src_folder"                : str(self.src_folder),
            "config_set_default_folder" : str(),
        }
                
        self.format_info = { #json_output
            "date"             : datetime.now().strftime('%m-%d-%Y'),
            "owner"            : "Michael Durning",
            "project_title"    : str(),
            "tts_model_onnx"   : str(),
            "tts_model_json"   : str(),
            "tts_directory"    : str(),
            "tts_output_dir"   : str(),
            "file_type"        : ".wav",
            "file_duration"    : None,
            "tts_entiries_num" : 0,
            "tts_word_num"     : 0,
            "tts_char_num"     : 0,
            
            "toggle_json"      : False,
            "toggle_model"     : False,            
            "toggle_directory" : False,

            "whisper_model"     : "medium",          
            "whisper_output_dir": None,
            "whisper_output"    : None,
            "max_line_width"    :"20",  # Example value, adjust as needed
            "max_words_per_line": "3",
            "subtitle_nums"     : True,
            "subtitle_format"   : "vtt",
            "task"              : "transcribe",
            "language"          : "en", 
            "whisper_word_num"  : int(),
            "whisper_char_num"  : int(),
            "highlight_words"   : False,
            "word_timestamps"   : True, 
        }
        
        self.replacement_dict = {"’" : "'",
                                 "”" : "'",
                                 "“" : "'",
                                 '"' : "'",
                                 "\n": " ",
                                 "AITA": "Am I the Asshole",
                                 "TIFU": "today i fucked up"}

    def folders_exist(self):
        self.config_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)
        self.piper_tts_folder.mkdir(exist_ok=True)

    def save_file_path_to_json(self):
        path_data = Path(self.path_data["config_file_path_json"])
        try:
            with open(path_data, "w") as file:
                json.dump(self.path_data, file, indent=4)
            return f"Config data saved to {path_data}"
        except Exception as e:
            return f"Error while saving to JSON: {e}"
        
    def save_settings_to_json(self):
        settings_dict = {}
        settings_json = self.config_folder / "settings.json"
        if not settings_json.exists():
            try:
                with open(settings_json, "w") as file:
                    json.dump(settings_dict, file, indent=4)
                return f"Config data saved to {settings_json}"
            except Exception as e:
                return f"Error while saving to JSON: {e}"
        else:
            return f"{settings_json} already exists. Skipping the saving process."
        
    def save_to_json(self, data_to_save, path_filename):
        if Path(path_filename).exists():
            file = path_filename
            try:
                with open(file, "w") as file:
                    json.dump(data_to_save, file, indent=4)
                return f"Config data saved to {path_filename}"
            except Exception as e:
                return f"Error while saving to JSON: {e}"
        else:
            return f"{path_filename} does not exists. Skipping the saving process."
        
    def save_format_info_to_json(self):
        path_data = Path(self.path_data["output_settings_json"])
        try:
            with open(path_data, "w") as file:
                json.dump(self.format_info, file, indent=4)
            return f"Config data saved to {path_data}"
        except Exception as e:
            return f"Error while saving to JSON: {e}"
            
    def save_audio_sequence_to_json(self):
        audio_sequence_dict = {}
        audio_sequence_json = self.config_folder / "audio_sequence.json"
        if not audio_sequence_json.exists():
            try:
                with open(audio_sequence_json, "w") as file:
                    json.dump(audio_sequence_dict, file, indent=4)
                return f"Config data saved to {audio_sequence_json}"
            except Exception as e:
                return f"Error while saving to JSON: {e}"
        else:
            return f"{audio_sequence_json} already exists. Skipping the saving process."
        
    def manual_return_dir(self, directory=None):
        return_dir = askdirectory(initialdir=directory, title="Select Folder")
        return return_dir

    def manual_return_file(self, directory=None):
        file_path = askopenfilename(initialdir=directory, title="Select File")
        file_name = os.path.basename(file_path)
        return file_name

    def print_dict_or_json(self, dict_or_json_path):
        if isinstance(dict_or_json_path, dict):
            formatted_data = ""
            for key, value in dict_or_json_path.items():
                formatted_data += f"{key}: {value}\n"
            return formatted_data, dict_or_json_path
        elif isinstance(dict_or_json_path, Path):
            if dict_or_json_path.exists():
                with dict_or_json_path.open('r') as json_file:
                    json_dict = json.load(json_file)
                    formatted_data = ""
                    for key, value in json_dict.items():
                        formatted_data += f"{key}: {value}\n"
                    return formatted_data, json_dict, dict_or_json_path
        else:
            return "Dictionary or JSON file does not exist."
            
    def select_client_by_value(self, selected_value):
        audio_sequence_path = Path(self.path_data["audio_sequence_json"])

        if audio_sequence_path.exists():
            with audio_sequence_path.open('r') as json_file:
                clients_data = json.load(json_file)

            for key, client_value in clients_data.items():
                if client_value == selected_value:
                    return client_value
        else:
            print("audio_sequence JSON file does not exist.")
            return None

    def delete_client(self, key_to_delete):
        
        json_file_path = Path(self.path_data["audio_sequence_json"])

        try:
            with json_file_path.open('r') as json_file:
                audio_sequence = json.load(json_file)
        except FileNotFoundError:
            print("Clients JSON file does not exist.")
            return

        if key_to_delete in audio_sequence:
            del audio_sequence[key_to_delete]

            updated_audio_sequence_data = {}
            sorted_keys = sorted(map(int, audio_sequence.keys()))
            for index, old_key in enumerate(sorted_keys):
                new_key = str(index + 1)
                updated_audio_sequence_data[new_key] = audio_sequence[str(old_key)]
                self.format_info["tts_entiries_num"]=int(new_key)
                
            with json_file_path.open('w') as json_file:
                json.dump(updated_audio_sequence_data, json_file, indent=4)
        else:
            print(f"Key {key_to_delete} does not exist in the clients JSON.")
            
    def add_client(self, name_to_add):
        
        json_file_path = Path(self.path_data["audio_sequence_json"])

        try:
            with json_file_path.open('r') as json_file:
                audio_sequence = json.load(json_file)
        except FileNotFoundError:
            print("Clients JSON file does not exist.")
            return

        if name_to_add in audio_sequence.values():
            print(f"Client with name '{name_to_add}' already exists.")
            return

        new_key = str(len(audio_sequence.keys()) + 1)
        
        self.format_info["tts_entiries_num"]=int(new_key)

        name_to_add_processed = name_to_add
        for old_encoding, new_encoding in self.replacement_dict.items():
            name_to_add_processed = name_to_add_processed.replace(old_encoding, new_encoding)

        audio_sequence[new_key] = name_to_add_processed

        with json_file_path.open('w') as json_file:
            json.dump(audio_sequence, json_file, indent=4)

    def add_subtitle_order_numbers(self, input_file_path, output_file_path):
        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # Track subtitle order number
        order_number = 1

        with open(output_file_path, 'w') as f:
            for line in lines:
                # Check if line contains timestamp
                if '-->' in line:
                    colon_count = line.count(":")
                    
                    if colon_count == 2:
                        modified_line = "00:" + line
                        modified_colon_count = modified_line.count(":")
                        
                    if modified_colon_count == 3:
                        completed_line = modified_line[:17] + "00:" + modified_line[17:]
                        completed_colon_count = completed_line.count(":")
                        
                    if completed_colon_count == 4:
                        f.write(f"{order_number}\n{completed_line}")
                        order_number += 1

                    
                else:
                    f.write(line)
                    
                    
        

    def count_words_and_characters(self, json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        new_key = len(data.keys())
        
        self.format_info["tts_entiries_num"]=new_key
        
        for key in data:
            # Split the string into words
            words = data[key].split()
            # Count the number of words
            self.format_info["tts_word_num"] += len(words)
            # Count the number of characters
            self.format_info["tts_char_num"] += sum(len(word) for word in words)
            
 
    def move_specific_files(self, source_dir, destination_dir, filename):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)
        shutil.move(source_file, destination_file)
            

'''
    def get_wav_duration(file_path):
        with wave.open(file_path, 'rb') as wav_file:
            num_frames = wav_file.getnframes()
            framerate = wav_file.getframerate()
            duration = num_frames / float(framerate)
            return duration

    
    def process_wav_files(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".wav"):
                    file_path = os.path.join(root, file)
                    duration = get_wav_duration(file_path)  
'''            
            '''
