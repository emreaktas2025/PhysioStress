import pickle
from pathlib import Path
import sys

def load_data(subject_id, path=None):
    """
    Load physiological data for a given subject
    
    Args:
        subject_id (str): Subject ID number
        path (str, optional): Path to data directory
    
    Returns:
        tuple: (signal_data, labels)
    """
    if path is None:
        path = Path.cwd().parent / 'data' / 'raw'
        
    # Use the correct path structure: raw/S2/S2.pkl
    file_path = path / f"S{subject_id}" / f"S{subject_id}.pkl"
    
    try:
        # Try different pickle protocols and encoding options
        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file, encoding='bytes')
        except:
            try:
                with open(file_path, 'rb') as file:
                    data = pickle.load(file, encoding='latin1')
            except:
                with open(file_path, 'rb') as file:
                    data = pickle.load(file, encoding='ascii')
        
        # Convert bytes keys to str if necessary
        if isinstance(data, dict):
            # Convert top-level keys
            data = {k.decode('utf-8') if isinstance(k, bytes) else k: v for k, v in data.items()}
            
            # Convert nested dictionary keys if they exist
            if 'signal' in data and isinstance(data['signal'], dict):
                data['signal'] = {k.decode('utf-8') if isinstance(k, bytes) else k: v 
                                for k, v in data['signal'].items()}
        
        return data['signal'], data['label']
    
    except Exception as e:
        print(f"Error reading file at {file_path}")
        print(f"Current working directory: {Path.cwd()}")
        print(f"Python version: {sys.version}")
        raise e