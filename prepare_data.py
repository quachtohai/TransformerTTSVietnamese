import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import os
from utils import get_spectrograms
import hyperparams as hp
import librosa

class PrepareDataset(Dataset):
    """LJSpeech dataset."""

    def __init__(self, output_dir, root_dir):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the wavs.

        """
        self.landmarks_frame = self.read_txt(root_dir)
        self.root_dir = root_dir
        self.output_dir = output_dir

    def load_wav(self, filename):
        return librosa.load(filename, sr=hp.sample_rate)

    def read_txt(self, in_dir):
        all_files = os.listdir(in_dir)
        txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
        txt_file_wavs = []
        for txt_file in txt_files:            
            txt_file_wavs.append(txt_file.replace(".txt",""))            
        return txt_file_wavs
    
    def __len__(self):
        return len(self.landmarks_frame)
    def read_first_line(self, file):
        with open(file, 'rt', encoding='utf-8') as fd:
            first_line = fd.readline()
            return first_line
    def __getitem__(self, idx):
        wav_name = os.path.join(self.root_dir, self.landmarks_frame[idx]) + '.wav'
        mel, mag = get_spectrograms(wav_name)
        wav_name_saving = os.path.join(self.output_dir,self.landmarks_frame[idx])+ '.wav'
        
        np.save(wav_name_saving[:-4] + '.pt', mel)
        np.save(wav_name_saving[:-4] + '.mag', mag)

        sample = {'mel':mel, 'mag': mag}

        return sample
    
if __name__ == '__main__':
    dataset = PrepareDataset(os.path.join(hp.output_dir,''), os.path.join(hp.data_path,''))
    dataloader = DataLoader(dataset, batch_size=1, drop_last=False, num_workers=8)
    from tqdm import tqdm
    pbar = tqdm(dataloader)
    for d in pbar:
        pass
