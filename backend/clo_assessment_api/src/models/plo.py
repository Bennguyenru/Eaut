from src.models.user import db
from datetime import datetime

class PLO(db.Model):
    __tablename__ = 'plo'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    pi_codes = db.Column(db.Text)  # Comma-separated PI codes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'pi_codes': self.pi_codes.split(',') if self.pi_codes else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def from_dict(data):
        return PLO(
            code=data.get('code'),
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            pi_codes=','.join(data.get('pi_codes', []))
        )

