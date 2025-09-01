from flask import Blueprint, request, jsonify
from src.models.clo import CLO, CLOPLOMapping, CLOKeyword, ScoringScale, db
import csv
import io

clo_bp = Blueprint('clo', __name__)

@clo_bp.route('/clo', methods=['GET'])
def get_all_clos():
    """Get all CLOs with optional filtering"""
    try:
        course_code = request.args.get('course_code')
        
        query = CLO.query
        if course_code:
            query = query.filter_by(course_code=course_code)
        
        clos = query.all()
        
        # Include related data
        result = []
        for clo in clos:
            clo_dict = clo.to_dict()
            
            # Add keywords
            keywords = CLOKeyword.query.filter_by(clo_id=clo.id).all()
            clo_dict['keywords'] = [kw.to_dict() for kw in keywords]
            
            # Add scoring config
            scoring = ScoringScale.query.filter_by(clo_id=clo.id).first()
            clo_dict['scoring_config'] = scoring.to_dict() if scoring else None
            
            # Add PLO mappings
            mappings = CLOPLOMapping.query.filter_by(clo_id=clo.id).all()
            clo_dict['plo_mappings'] = [mapping.to_dict() for mapping in mappings]
            
            result.append(clo_dict)
        
        return jsonify({
            'success': True,
            'data': result,
            'total': len(result)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/clo/<int:clo_id>', methods=['GET'])
def get_clo(clo_id):
    """Get specific CLO by ID"""
    try:
        clo = CLO.query.get_or_404(clo_id)
        clo_dict = clo.to_dict()
        
        # Add related data
        keywords = CLOKeyword.query.filter_by(clo_id=clo.id).all()
        clo_dict['keywords'] = [kw.to_dict() for kw in keywords]
        
        scoring = ScoringScale.query.filter_by(clo_id=clo.id).first()
        clo_dict['scoring_config'] = scoring.to_dict() if scoring else None
        
        mappings = CLOPLOMapping.query.filter_by(clo_id=clo.id).all()
        clo_dict['plo_mappings'] = [mapping.to_dict() for mapping in mappings]
        
        return jsonify({
            'success': True,
            'data': clo_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@clo_bp.route('/clo', methods=['POST'])
def create_clo():
    """Create new CLO"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['code', 'course_code', 'course_name', 'title', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        clo = CLO.from_dict(data)
        db.session.add(clo)
        db.session.flush()  # Get the ID
        
        # Add keywords if provided
        if 'keywords' in data:
            for kw_data in data['keywords']:
                keyword = CLOKeyword(
                    clo_id=clo.id,
                    keyword_category=kw_data.get('keyword_category'),
                    keywords=','.join(kw_data.get('keywords', [])),
                    weight=kw_data.get('weight', 1.0),
                    description=kw_data.get('description')
                )
                db.session.add(keyword)
        
        # Add scoring config if provided
        if 'scoring_config' in data:
            sc_data = data['scoring_config']
            scoring = ScoringScale(
                clo_id=clo.id,
                method=sc_data.get('method', 'keyword_frequency'),
                full_score_threshold=sc_data.get('full_score_threshold', 3.0),
                partial_score_floor=sc_data.get('partial_score_floor', 0.3),
                max_score=sc_data.get('max_score', 4.0),
                description=sc_data.get('description')
            )
            db.session.add(scoring)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': clo.to_dict(),
            'message': 'CLO created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/clo/<int:clo_id>', methods=['PUT'])
def update_clo(clo_id):
    """Update existing CLO"""
    try:
        clo = CLO.query.get_or_404(clo_id)
        data = request.get_json()
        
        # Update basic fields
        for field in ['title', 'description', 'pi_code', 'assessment_level', 'course_name']:
            if field in data:
                setattr(clo, field, data[field])
        
        # Update keywords if provided
        if 'keywords' in data:
            # Delete existing keywords
            CLOKeyword.query.filter_by(clo_id=clo_id).delete()
            
            # Add new keywords
            for kw_data in data['keywords']:
                keyword = CLOKeyword(
                    clo_id=clo.id,
                    keyword_category=kw_data.get('keyword_category'),
                    keywords=','.join(kw_data.get('keywords', [])),
                    weight=kw_data.get('weight', 1.0),
                    description=kw_data.get('description')
                )
                db.session.add(keyword)
        
        # Update scoring config if provided
        if 'scoring_config' in data:
            sc_data = data['scoring_config']
            scoring = ScoringScale.query.filter_by(clo_id=clo_id).first()
            
            if scoring:
                # Update existing
                for field in ['method', 'full_score_threshold', 'partial_score_floor', 'max_score', 'description']:
                    if field in sc_data:
                        setattr(scoring, field, sc_data[field])
            else:
                # Create new
                scoring = ScoringScale(
                    clo_id=clo.id,
                    method=sc_data.get('method', 'keyword_frequency'),
                    full_score_threshold=sc_data.get('full_score_threshold', 3.0),
                    partial_score_floor=sc_data.get('partial_score_floor', 0.3),
                    max_score=sc_data.get('max_score', 4.0),
                    description=sc_data.get('description')
                )
                db.session.add(scoring)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': clo.to_dict(),
            'message': 'CLO updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/clo/<int:clo_id>', methods=['DELETE'])
def delete_clo(clo_id):
    """Delete CLO and all related data"""
    try:
        clo = CLO.query.get_or_404(clo_id)
        
        # Delete related data
        CLOKeyword.query.filter_by(clo_id=clo_id).delete()
        ScoringScale.query.filter_by(clo_id=clo_id).delete()
        CLOPLOMapping.query.filter_by(clo_id=clo_id).delete()
        
        # Delete CLO
        db.session.delete(clo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'CLO deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/clo/import', methods=['POST'])
def import_clos_from_csv():
    """Import CLOs from CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
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
                required_fields = ['code', 'course_code', 'course_name', 'title', 'description']
                if not all(field in row for field in required_fields):
                    errors.append(f'Row {row_num}: Missing required fields')
                    continue
                
                # Create CLO
                clo_data = {
                    'code': row['code'],
                    'course_code': row['course_code'],
                    'course_name': row['course_name'],
                    'title': row['title'],
                    'description': row['description'],
                    'pi_code': row.get('pi_code'),
                    'assessment_level': row.get('assessment_level', 'U')
                }
                
                clo = CLO.from_dict(clo_data)
                db.session.add(clo)
                imported_count += 1
                
            except Exception as e:
                errors.append(f'Row {row_num}: {str(e)}')
        
        if imported_count > 0:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'imported_count': imported_count,
            'errors': errors,
            'message': f'Successfully imported {imported_count} CLOs'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/clo/courses', methods=['GET'])
def get_courses():
    """Get list of unique courses"""
    try:
        courses = db.session.query(CLO.course_code, CLO.course_name).distinct().all()
        
        course_list = [
            {'course_code': course[0], 'course_name': course[1]}
            for course in courses
        ]
        
        return jsonify({
            'success': True,
            'data': course_list,
            'total': len(course_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/mapping', methods=['GET'])
def get_clo_plo_mappings():
    """Get all CLO-PLO mappings"""
    try:
        mappings = CLOPLOMapping.query.all()
        
        result = []
        for mapping in mappings:
            mapping_dict = mapping.to_dict()
            
            # Add CLO and PLO details
            if mapping.clo:
                mapping_dict['clo'] = {
                    'code': mapping.clo.code,
                    'title': mapping.clo.title,
                    'course_code': mapping.clo.course_code
                }
            
            if mapping.plo:
                mapping_dict['plo'] = {
                    'code': mapping.plo.code,
                    'title': mapping.plo.title
                }
            
            result.append(mapping_dict)
        
        return jsonify({
            'success': True,
            'data': result,
            'total': len(result)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/mapping', methods=['POST'])
def create_clo_plo_mapping():
    """Create new CLO-PLO mapping"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'clo_id' not in data or 'plo_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: clo_id, plo_id'
            }), 400
        
        # Check if mapping already exists
        existing = CLOPLOMapping.query.filter_by(
            clo_id=data['clo_id'],
            plo_id=data['plo_id']
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'Mapping already exists'
            }), 400
        
        mapping = CLOPLOMapping(
            clo_id=data['clo_id'],
            plo_id=data['plo_id'],
            weight=data.get('weight', 1.0),
            mapping_type=data.get('mapping_type', 'direct'),
            notes=data.get('notes')
        )
        
        db.session.add(mapping)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': mapping.to_dict(),
            'message': 'Mapping created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clo_bp.route('/mapping/<int:mapping_id>', methods=['DELETE'])
def delete_clo_plo_mapping(mapping_id):
    """Delete CLO-PLO mapping"""
    try:
        mapping = CLOPLOMapping.query.get_or_404(mapping_id)
        
        db.session.delete(mapping)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mapping deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

