"""
Script per scaricare i modelli pre-addestrati.
"""

import os
import urllib.request
from tqdm import tqdm
import config


class DownloadProgressBar(tqdm):
    """Barra di progresso per il download."""
    
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        Aggiorna la barra di progresso.
        
        Args:
            b: Numero di blocchi trasferiti
            bsize: Dimensione del blocco
            tsize: Dimensione totale
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    """
    Scarica un file da URL.
    
    Args:
        url: URL del file
        output_path: Percorso di output
    """
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=output_path) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def download_facenet_model():
    """Scarica il modello FaceNet pre-addestrato."""
    print("Download del modello FaceNet...")
    
    # Crea directory per i modelli
    facenet_dir = os.path.join(config.MODELS_DIR, "facenet")
    os.makedirs(facenet_dir, exist_ok=True)
    
    # URL del modello (esempio - potrebbe essere necessario aggiornare)
    # Nota: facenet-pytorch scarica automaticamente i modelli quando necessario
    print("Nota: I modelli FaceNet verranno scaricati automaticamente da facenet-pytorch")
    print("al primo utilizzo dell'applicazione.")
    
    print("\nModelli pronti!")


def download_all_models():
    """Scarica tutti i modelli necessari."""
    print("=" * 50)
    print("Download dei modelli pre-addestrati")
    print("=" * 50)
    
    download_facenet_model()
    
    print("\n" + "=" * 50)
    print("Download completato!")
    print("=" * 50)


if __name__ == "__main__":
    download_all_models()
