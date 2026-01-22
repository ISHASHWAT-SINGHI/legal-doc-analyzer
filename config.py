import os

class Config:
    """
    Base configuration class.
    Contains default settings for the application.
    """
    # Project Info
    PROJECT_NAME = "Legal Doc Analyzer"
    VERSION = "1.0.0"

    # File Uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max upload size: 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}

    # Model Settings (Hugging Face)
    # Using a smaller model for faster inference in dev/demos
    MODEL_NAME = "nlpaueb/legal-bert-base-uncased"
    
    # Risk Thresholds
    RISK_LEVELS = {
        "HIGH": "High Risk",
        "MEDIUM": "Medium Risk",
        "LOW": "Low Risk"
    }

    # Secret Key (Load from env in production)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-prod'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In production, ensure these are set
    # SECRET_KEY = os.environ.get('SECRET_KEY')

# Mapping config names to classes
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
