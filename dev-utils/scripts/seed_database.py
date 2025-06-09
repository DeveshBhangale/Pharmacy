#!/usr/bin/env python3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Protocol, Optional
import os
import json
import sys
import boto3
from datetime import datetime
from pathlib import Path

class DataLoader(Protocol):
    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        ...

class JsonDataLoader:
    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'r') as f:
            return json.load(f)

class DatabaseSeeder(ABC):
    @abstractmethod
    def seed(self, data: List[Dict[str, Any]]) -> None:
        pass

class DynamoDBSeeder(DatabaseSeeder):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def seed(self, data: List[Dict[str, Any]]) -> None:
        with self.table.batch_writer() as batch:
            for item in data:
                batch.put_item(Item=item)

class RDSSeeder(DatabaseSeeder):
    def __init__(self, connection_string: str):
        import sqlalchemy as sa
        from sqlalchemy.orm import sessionmaker
        
        self.engine = sa.create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def seed(self, data: List[Dict[str, Any]]) -> None:
        session = self.Session()
        try:
            # Implementation depends on SQLAlchemy models
            # This is a placeholder for actual implementation
            print(f"Would seed {len(data)} records to RDS")
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

class S3Seeder(DatabaseSeeder):
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def seed(self, data: List[Dict[str, Any]]) -> None:
        for file_info in data:
            try:
                self.s3.upload_file(
                    file_info['local_path'],
                    self.bucket_name,
                    file_info['s3_key']
                )
            except Exception as e:
                print(f"Error uploading {file_info['local_path']}: {e}")

@dataclass
class SeederConfig:
    dynamo_table: str
    rds_connection: str
    s3_bucket: str
    mock_data_path: Path

class SeederFactory:
    @staticmethod
    def create_dynamo_seeder(table_name: str) -> DynamoDBSeeder:
        return DynamoDBSeeder(table_name)

    @staticmethod
    def create_rds_seeder(connection_string: str) -> RDSSeeder:
        return RDSSeeder(connection_string)

    @staticmethod
    def create_s3_seeder(bucket_name: str) -> S3Seeder:
        return S3Seeder(bucket_name)

class DatabaseSeederOrchestrator:
    def __init__(
        self,
        config: SeederConfig,
        data_loader: DataLoader,
        seeder_factory: SeederFactory
    ):
        self.config = config
        self.data_loader = data_loader
        self.seeder_factory = seeder_factory

    def _load_json_data(self, filename: str) -> List[Dict[str, Any]]:
        file_path = self.config.mock_data_path / filename
        return self.data_loader.load_data(str(file_path))

    def seed_dynamodb(self) -> None:
        print("Seeding DynamoDB...")
        medicines = self._load_json_data('medicines.json')
        seeder = self.seeder_factory.create_dynamo_seeder(self.config.dynamo_table)
        seeder.seed(medicines)

    def seed_rds(self) -> None:
        print("Seeding RDS...")
        data_files = {
            'customers': 'customers.json',
            'orders': 'orders.json',
            'prescriptions': 'prescriptions.json'
        }
        
        seeder = self.seeder_factory.create_rds_seeder(self.config.rds_connection)
        for model_name, filename in data_files.items():
            data = self._load_json_data(filename)
            print(f"Seeding {model_name}...")
            seeder.seed(data)

    def seed_s3(self) -> None:
        print("Seeding S3...")
        sample_files_path = self.config.mock_data_path / 'sample_files'
        if not sample_files_path.exists():
            return

        s3_files = []
        for file_path in sample_files_path.rglob('*'):
            if file_path.is_file():
                s3_files.append({
                    'local_path': str(file_path),
                    's3_key': str(file_path.relative_to(sample_files_path))
                })

        if s3_files:
            seeder = self.seeder_factory.create_s3_seeder(self.config.s3_bucket)
            seeder.seed(s3_files)

    def seed_all(self) -> None:
        try:
            self.seed_dynamodb()
            self.seed_rds()
            self.seed_s3()
            print("Database seeding completed successfully!")
        except Exception as e:
            print(f"Error during seeding: {e}")
            sys.exit(1)

def main() -> None:
    config = SeederConfig(
        dynamo_table=os.getenv('DYNAMODB_TABLE', 'pms-dev'),
        rds_connection=os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/pms'),
        s3_bucket=os.getenv('S3_BUCKET', 'pms-storage-dev'),
        mock_data_path=Path(__file__).parent.parent / 'mock-data' / 'mock_data'
    )

    orchestrator = DatabaseSeederOrchestrator(
        config=config,
        data_loader=JsonDataLoader(),
        seeder_factory=SeederFactory()
    )
    
    orchestrator.seed_all()

if __name__ == '__main__':
    main() 