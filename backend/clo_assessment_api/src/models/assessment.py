from src.models.user import db
from datetime import datetime
import json

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(50))
    course_code = db.Column(db.String(10))
    document_type = db.Column(db.String(50))  # exam, assignment, report, etc.
    content_text = db.Column(db.Text)  # Extracted text content
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'course_code': self.course_code,
            'document_type': self.document_type,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'processed': self.processed
        }

class AssessmentResult(db.Model):
    __tablename__ = 'assessment_results'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    clo_id = db.Column(db.Integer, db.ForeignKey('clo.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float)
    details = db.Column(db.Text)  # JSON string with detailed analysis
    assessment_method = db.Column(db.String(50))
    assessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        details_dict = {}
        if self.details:
            try:
                details_dict = json.loads(self.details)
            except:
                details_dict = {'raw': self.details}
                
        return {
            'id': self.id,
            'document_id': self.document_id,
            'clo_id': self.clo_id,
            'score': self.score,
            'confidence': self.confidence,
            'details': details_dict,
            'assessment_method': self.assessment_method,
            'assessed_at': self.assessed_at.isoformat() if self.assessed_at else None
        }
    
    def set_details(self, details_dict):
        """Set details as JSON string"""
        self.details = json.dumps(details_dict, ensure_ascii=False)
    
    def get_details(self):
        """Get details as dictionary"""
        if self.details:
            try:
                return json.loads(self.details)
            except:
                return {'raw': self.details}
        return {}

class PLOAssessmentSummary(db.Model):
    __tablename__ = 'plo_assessment_summary'
    
    id = db.Column(db.Integer, primary_key=True)
    plo_id = db.Column(db.Integer, db.ForeignKey('plo.id'), nullable=False)
    course_code = db.Column(db.String(10))
    semester = db.Column(db.String(20))
    total_documents = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float)
    achievement_rate = db.Column(db.Float)  # Percentage of students achieving PLO
    summary_data = db.Column(db.Text)  # JSON with detailed statistics
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        summary_dict = {}
        if self.summary_data:
            try:
                summary_dict = json.loads(self.summary_data)
            except:
                summary_dict = {}
                
        return {
            'id': self.id,
            'plo_id': self.plo_id,
            'course_code': self.course_code,
            'semester': self.semester,
            'total_documents': self.total_documents,
            'average_score': self.average_score,
            'achievement_rate': self.achievement_rate,
            'summary_data': summary_dict,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

