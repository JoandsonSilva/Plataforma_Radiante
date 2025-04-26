import os
import shutil
import sys

def restore_database(backup_file):
    # Caminho do banco de dados
    db_path = 'instance/dev.db'
    
    # Verificar se o arquivo de backup existe
    if not os.path.exists(backup_file):
        print(f'Erro: Arquivo de backup {backup_file} não encontrado')
        return False
    
    try:
        # Fazer backup do banco atual antes de restaurar
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            current_backup = f'backups/dev_current_{timestamp}.db'
            shutil.copy2(db_path, current_backup)
            print(f'Backup do banco atual criado: {current_backup}')
        
        # Restaurar o backup
        shutil.copy2(backup_file, db_path)
        print(f'Banco de dados restaurado com sucesso a partir de {backup_file}')
        return True
        
    except Exception as e:
        print(f'Erro ao restaurar banco de dados: {str(e)}')
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso: python restore_db.py <arquivo_de_backup>')
        sys.exit(1)
    
    restore_database(sys.argv[1]) 