#!/usr/bin/env python3
"""
Script to import initial data from CSV files into the database
"""

import os
import sys
import csv
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app, db
from src.models.plo import PLO
from src.models.clo import CLO, CLOPLOMapping, CLOKeyword, ScoringScale

def import_plos(csv_file_path):
    """Import PLOs from CSV file"""
    print(f"Importing PLOs from {csv_file_path}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            # Check if PLO already exists
            existing = PLO.query.filter_by(code=row['code']).first()
            if existing:
                print(f"PLO {row['code']} already exists, skipping...")
                continue
            
            plo = PLO(
                code=row['code'],
                title=row['title'],
                description=row['description'],
                category=row['category'],
                pi_codes=row['pi_codes']
            )
            
            db.session.add(plo)
            count += 1
        
        db.session.commit()
        print(f"Imported {count} PLOs")

def import_clos(csv_file_path):
    """Import CLOs from CSV file"""
    print(f"Importing CLOs from {csv_file_path}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            clo = CLO(
                code=row['code'],
                course_code=row['course_code'],
                course_name=row['course_name'],
                title=row['title'],
                description=row['description'],
                pi_code=row['pi_code'],
                assessment_level=row['assessment_level']
            )
            
            db.session.add(clo)
            count += 1
        
        db.session.commit()
        print(f"Imported {count} CLOs")

def import_clo_plo_mappings(csv_file_path):
    """Import CLO-PLO mappings from CSV file"""
    print(f"Importing CLO-PLO mappings from {csv_file_path}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            mapping = CLOPLOMapping(
                clo_id=int(row['clo_id']),
                plo_id=int(row['plo_id']),
                weight=float(row['weight']),
                mapping_type=row['mapping_type'],
                notes=row['notes']
            )
            
            db.session.add(mapping)
            count += 1
        
        db.session.commit()
        print(f"Imported {count} CLO-PLO mappings")

def import_clo_keywords(csv_file_path):
    """Import CLO keywords from CSV file"""
    print(f"Importing CLO keywords from {csv_file_path}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            keyword = CLOKeyword(
                clo_id=int(row['clo_id']),
                keyword_category=row['keyword_category'],
                keywords=row['keywords'],
                weight=float(row['weight']),
                description=row['description']
            )
            
            db.session.add(keyword)
            count += 1
        
        db.session.commit()
        print(f"Imported {count} CLO keywords")

def import_scoring_scales(csv_file_path):
    """Import scoring scales from CSV file"""
    print(f"Importing scoring scales from {csv_file_path}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        
        for row in reader:
            scoring = ScoringScale(
                clo_id=int(row['clo_id']),
                method=row['method'],
                full_score_threshold=float(row['full_score_threshold']),
                partial_score_floor=float(row['partial_score_floor']),
                max_score=float(row['max_score']),
                description=row['description']
            )
            
            db.session.add(scoring)
            count += 1
        
        db.session.commit()
        print(f"Imported {count} scoring scales")

def main():
    """Main import function"""
    with app.app_context():
        # Path to data directory
        data_dir = Path(__file__).parent.parent.parent / 'data'
        
        print("Starting data import...")
        print(f"Data directory: {data_dir}")
        
        # Import in order (PLOs first, then CLOs, then mappings)
        try:
            # Import PLOs
            plo_file = data_dir / 'plo.csv'
            if plo_file.exists():
                import_plos(plo_file)
            else:
                print(f"PLO file not found: {plo_file}")
            
            # Import CLOs
            clo_file = data_dir / 'clo.csv'
            if clo_file.exists():
                import_clos(clo_file)
            else:
                print(f"CLO file not found: {clo_file}")
            
            # Import CLO-PLO mappings
            mapping_file = data_dir / 'clo_plo_mapping.csv'
            if mapping_file.exists():
                import_clo_plo_mappings(mapping_file)
            else:
                print(f"Mapping file not found: {mapping_file}")
            
            # Import CLO keywords
            keywords_file = data_dir / 'clo_keywords.csv'
            if keywords_file.exists():
                import_clo_keywords(keywords_file)
            else:
                print(f"Keywords file not found: {keywords_file}")
            
            # Import scoring scales
            scoring_file = data_dir / 'scoring_scale.csv'
            if scoring_file.exists():
                import_scoring_scales(scoring_file)
            else:
                print(f"Scoring file not found: {scoring_file}")
            
            print("Data import completed successfully!")
            
        except Exception as e:
            print(f"Error during import: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()

