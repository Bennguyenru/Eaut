from flask import Blueprint, request, jsonify
from src.models.plo import PLO, db
from src.models.clo import CLOPLOMapping
import csv
import io

plo_bp = Blueprint('plo', __name__)

@plo_bp.route('/plo', methods=['GET'])
def get_all_plos():
    """Get all PLOs"""
    try:
        plos = PLO.query.all()
        return jsonify({
            'success': True,
            'data': [plo.to_dict() for plo in plos],
            'total': len(plos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@plo_bp.route('/plo/<int:plo_id>', methods=['GET'])
def get_plo(plo_id):
    """Get specific PLO by ID"""
    try:
        plo = PLO.query.get_or_404(plo_id)
        return jsonify({
            'success': True,
            'data': plo.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@plo_bp.route('/plo', methods=['POST'])
def create_plo():
    """Create new PLO"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['code', 'title', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Check if PLO code already exists
        existing_plo = PLO.query.filter_by(code=data['code']).first()
        if existing_plo:
            return jsonify({
                'success': False,
                'error': f'PLO with code {data["code"]} already exists'
            }), 400
        
        plo = PLO.from_dict(data)
        db.session.add(plo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': plo.to_dict(),
            'message': 'PLO created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@plo_bp.route('/plo/<int:plo_id>', methods=['PUT'])
def update_plo(plo_id):
    """Update existing PLO"""
    try:
        plo = PLO.query.get_or_404(plo_id)
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            plo.title = data['title']
        if 'description' in data:
            plo.description = data['description']
        if 'category' in data:
            plo.category = data['category']
        if 'pi_codes' in data:
            plo.pi_codes = ','.join(data['pi_codes'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': plo.to_dict(),
            'message': 'PLO updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@plo_bp.route('/plo/<int:plo_id>', methods=['DELETE'])
def delete_plo(plo_id):
    """Delete PLO"""
    try:
        plo = PLO.query.get_or_404(plo_id)
        
        # Check if PLO is referenced by any CLO mappings
        mappings = CLOPLOMapping.query.filter_by(plo_id=plo_id).count()
        if mappings > 0:
            return jsonify({
                'success': False,
                'error': f'Cannot delete PLO. It is referenced by {mappings} CLO mappings.'
            }), 400
        
        db.session.delete(plo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'PLO deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@plo_bp.route('/plo/import', methods=['POST'])
def import_plos_from_csv():
    """Import PLOs from CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({
                'success': False,
                'error': 'File must be CSV format'
            }), 400
        
        # Read CSV content
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        imported_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                # Check required fields
                if not all(field in row for field in ['code', 'title', 'description']):
                    errors.append(f'Row {row_num}: Missing required fields')
                    continue
                
                # Check if PLO already exists
                existing_plo = PLO.query.filter_by(code=row['code']).first()
                if existing_plo:
                    errors.append(f'Row {row_num}: PLO {row["code"]} already exists')
                    continue
                
                # Create PLO
                plo_data = {
                    'code': row['code'],
                    'title': row['title'],
                    'description': row['description'],
                    'category': row.get('category', ''),
                    'pi_codes': row.get('pi_codes', '').split(',') if row.get('pi_codes') else []
                }
                
                plo = PLO.from_dict(plo_data)
                db.session.add(plo)
                imported_count += 1
                
            except Exception as e:
                errors.append(f'Row {row_num}: {str(e)}')
        
        if imported_count > 0:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'imported_count': imported_count,
            'errors': errors,
            'message': f'Successfully imported {imported_count} PLOs'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@plo_bp.route('/plo/export', methods=['GET'])
def export_plos_to_csv():
    """Export all PLOs to CSV"""
    try:
        plos = PLO.query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['id', 'code', 'title', 'description', 'category', 'pi_codes'])
        
        # Write data
        for plo in plos:
            writer.writerow([
                plo.id,
                plo.code,
                plo.title,
                plo.description,
                plo.category or '',
                plo.pi_codes or ''
            ])
        
        output.seek(0)
        
        return jsonify({
            'success': True,
            'csv_content': output.getvalue(),
            'filename': 'plos_export.csv'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@plo_bp.route('/plo/<int:plo_id>/clo-mappings', methods=['GET'])
def get_plo_clo_mappings(plo_id):
    """Get all CLO mappings for a specific PLO"""
    try:
        plo = PLO.query.get_or_404(plo_id)
        mappings = CLOPLOMapping.query.filter_by(plo_id=plo_id).all()
        
        return jsonify({
            'success': True,
            'plo': plo.to_dict(),
            'mappings': [mapping.to_dict() for mapping in mappings],
            'total_mappings': len(mappings)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

