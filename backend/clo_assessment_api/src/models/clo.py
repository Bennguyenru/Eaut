from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CLO(db.Model):
    __tablename__ = 'clo'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    course_name = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pi_code = db.Column(db.String(10))
    assessment_level = db.Column(db.String(5))  # T, U, A
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'title': self.title,
            'description': self.description,
            'pi_code': self.pi_code,
            'assessment_level': self.assessment_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def from_dict(data):
        return CLO(
            code=data.get('code'),
            course_code=data.get('course_code'),
            course_name=data.get('course_name'),
            title=data.get('title'),
            description=data.get('description'),
            pi_code=data.get('pi_code'),
            assessment_level=data.get('assessment_level')
        )

class CLOPLOMapping(db.Model):
    __tablename__ = 'clo_plo_mapping'
    
    id = db.Column(db.Integer, primary_key=True)
    clo_id = db.Column(db.Integer, db.ForeignKey('clo.id'), nullable=False)
    plo_id = db.Column(db.Integer, db.ForeignKey('plo.id'), nullable=False)
    weight = db.Column(db.Float, default=1.0)
    mapping_type = db.Column(db.String(20), default='direct')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'clo_id': self.clo_id,
            'plo_id': self.plo_id,
            'weight': self.weight,
            'mapping_type': self.mapping_type,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CLOKeyword(db.Model):
    __tablename__ = 'clo_keywords'
    
    id = db.Column(db.Integer, primary_key=True)
    clo_id = db.Column(db.Integer, db.ForeignKey('clo.id'), nullable=False)
    keyword_category = db.Column(db.String(50))
    keywords = db.Column(db.Text, nullable=False)  # Comma-separated keywords
    weight = db.Column(db.Float, default=1.0)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'clo_id': self.clo_id,
            'keyword_category': self.keyword_category,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'weight': self.weight,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ScoringScale(db.Model):
    __tablename__ = 'scoring_scale'
    
    id = db.Column(db.Integer, primary_key=True)
    clo_id = db.Column(db.Integer, db.ForeignKey('clo.id'), nullable=False)
    method = db.Column(db.String(50), nullable=False)  # keyword_frequency, content_analysis, etc.
    full_score_threshold = db.Column(db.Float, nullable=False)
    partial_score_floor = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, default=4.0)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'clo_id': self.clo_id,
            'method': self.method,
            'full_score_threshold': self.full_score_threshold,
            'partial_score_floor': self.partial_score_floor,
            'max_score': self.max_score,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

