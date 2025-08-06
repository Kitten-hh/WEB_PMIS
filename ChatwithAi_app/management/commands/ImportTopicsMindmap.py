from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

class Command(BaseCommand):
    help = 'Import a CSV file into SQL Server.'

    def add_arguments(self, parser):
        parser.add_argument('dbname', type=str, help='SQL Server Name in setting')
        parser.add_argument('csv_path', type=str, help='Path to the CSV file.')
        parser.add_argument('table_name', type=str, help='Target SQL Server table name.')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        table_name = options['table_name']
        dbname = options['dbname']

        # 获取默认数据库配置
        default_db_config = settings.DATABASES[dbname]
        
        # 构建数据库URL
        database_url = f"mssql+pyodbc://{default_db_config['USER']}:{default_db_config['PASSWORD']}@{default_db_config['HOST']}/{default_db_config['NAME']}?driver=ODBC+Driver+17+for+SQL+Server"
        print(database_url)
        # 创建数据库引擎
        engine = create_engine(database_url)        

        # 读取CSV文件
        df = pd.read_csv(csv_path)

        # 将DataFrame导入到数据库表中
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {csv_path} into {table_name}.'))
