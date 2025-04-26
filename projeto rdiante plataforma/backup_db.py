import os
import shutil
from datetime import datetime

def backup_database():
    # Caminho do banco de dados
    db_path = 'instance/dev.db'
    
    # Diretório de backup
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Nome do arquivo de backup com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'{backup_dir}/dev_{timestamp}.db'
    
    # Copiar o arquivo do banco de dados
    shutil.copy2(db_path, backup_file)
    print(f'Backup criado com sucesso: {backup_file}')

if __name__ == '__main__':
    backup_database() 