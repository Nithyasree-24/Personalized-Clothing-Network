# AI Try-On Backend API - Advanced Virtual Fitting System
import os
try:
    import numpy as np
    import cv2
    import tensorflow as tf
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    print("Warning: AI dependencies not installed. Running in demo mode.")
from flask import Blueprint, request, jsonify
import base64
import io
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
import json
from datetime import datetime
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
ai_tryon_bp = Blueprint('ai_tryon', __name__)

class AITryOnBackend:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.training_data = []
        self.db_path = 'ai_tryon_data.db'
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing training data and results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tryon_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_image_path TEXT,
                garment_image_path TEXT,
                result_image_path TEXT,
                garment_type TEXT,
                user_gender TEXT,
                confidence_score REAL,
                processing_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_data TEXT,
                expected_output TEXT,
                garment_type TEXT,
                user_gender TEXT,
                quality_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_version TEXT,
                accuracy REAL,
                loss REAL,
                training_samples INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def load_model(self):
        """Load or create the AI model"""
        if not DEPENDENCIES_AVAILABLE:
            logger.info("AI dependencies not available. Running in demo mode.")
            self.model_loaded = False
            return False
            
        try:
            # Try to load existing model
            if os.path.exists('models/ai_tryon_model.h5'):
                self.model = tf.keras.models.load_model('models/ai_tryon_model.h5')
                logger.info("Loaded existing AI Try-On model")
            else:
                # Create new model architecture
                self.model = self.create_model_architecture()
                logger.info("Created new AI Try-On model")
            
            self.model_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False
    
    def create_model_architecture(self):
        """Create advanced neural network for virtual try-on"""
        if not DEPENDENCIES_AVAILABLE:
            return None
            
        # Input layers
        user_input = tf.keras.layers.Input(shape=(512, 512, 3), name='user_image')
        garment_input = tf.keras.layers.Input(shape=(512, 512, 3), name='garment_image')
        
        # Combine inputs
        combined = tf.keras.layers.Concatenate(axis=-1)([user_input, garment_input])
        
        # Encoder network
        x = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(combined)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D(2)(x)
        
        x = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D(2)(x)
        
        x = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D(2)(x)
        
        x = tf.keras.layers.Conv2D(512, 3, activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        
        # Attention mechanism
        attention = tf.keras.layers.Conv2D(512, 1, activation='sigmoid', padding='same')(x)
        x = tf.keras.layers.Multiply()([x, attention])
        
        # Decoder network
        x = tf.keras.layers.UpSampling2D(2)(x)
        x = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        
        x = tf.keras.layers.UpSampling2D(2)(x)
        x = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        
        x = tf.keras.layers.UpSampling2D(2)(x)
        x = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        
        # Output layer
        output = tf.keras.layers.Conv2D(3, 3, activation='sigmoid', padding='same')(x)
        
        # Create model
        model = tf.keras.Model(inputs=[user_input, garment_input], outputs=output)
        
        # Compile model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae', 'accuracy']
        )
        
        return model
    
    def preprocess_image(self, image_data, target_size=(512, 512)):
        """Preprocess image for AI model"""
        try:
            if not PIL_AVAILABLE or not DEPENDENCIES_AVAILABLE:
                # Return dummy data for demo mode
                return [[0.5] * 512] * 512  # Dummy image array
                
            # Decode base64 image
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            image = image.resize(target_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            return image_array
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {str(e)}")
            raise
    
    def postprocess_image(self, image_array):
        """Convert model output back to base64 image"""
        try:
            if not PIL_AVAILABLE or not DEPENDENCIES_AVAILABLE:
                # Return placeholder image for demo mode
                return "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
                
            # Denormalize and convert to uint8
            image_array = (image_array * 255).astype(np.uint8)
            
            # Convert to PIL Image
            image = Image.fromarray(image_array)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=90)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/jpeg;base64,{image_base64}"
            
        except Exception as e:
            logger.error(f"Image postprocessing failed: {str(e)}")
            raise
    
    def calculate_confidence(self, prediction, original_user_image):
        """Calculate confidence score for the try-on result"""
        try:
            if not DEPENDENCIES_AVAILABLE:
                return 0.85  # Demo confidence
                
            # Calculate structural similarity and other metrics
            mse = np.mean((prediction - original_user_image) ** 2)
            
            # Convert MSE to confidence (lower MSE = higher confidence)
            confidence = max(0, 1 - mse)
            
            return float(confidence)
            
        except Exception as e:
            logger.error(f"Confidence calculation failed: {str(e)}")
            return 0.5
    
    def analyze_fit(self, garment_type, user_gender, body_measurements=None):
        """Analyze fit quality and provide size recommendations"""
        try:
            fit_analysis = {
                'size': 'M',
                'fit_quality': 0.8,
                'adjustments': []
            }
            
            if body_measurements:
                chest = body_measurements.get('chest', 36)
                waist = body_measurements.get('waist', 30)
                
                # Size recommendation logic
                if chest < 32 and waist < 26:
                    fit_analysis['size'] = 'XS'
                elif chest < 36 and waist < 30:
                    fit_analysis['size'] = 'S'
                elif chest < 40 and waist < 34:
                    fit_analysis['size'] = 'M'
                elif chest < 44 and waist < 38:
                    fit_analysis['size'] = 'L'
                elif chest < 48 and waist < 42:
                    fit_analysis['size'] = 'XL'
                else:
                    fit_analysis['size'] = 'XXL'
                
                fit_analysis['fit_quality'] = 0.9
            
            # Garment-specific adjustments
            if garment_type == 'top' and body_measurements and body_measurements.get('chest', 0) > 42:
                fit_analysis['adjustments'].append('Consider a looser fit for comfort')
            
            return fit_analysis
            
        except Exception as e:
            logger.error(f"Fit analysis failed: {str(e)}")
            return {'size': 'M', 'fit_quality': 0.8, 'adjustments': []}
    
    def generate_recommendations(self, garment_type, user_gender, fit_analysis):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Size-based recommendations
        recommendations.append(f"Recommended size: {fit_analysis['size']}")
        
        if fit_analysis['fit_quality'] > 0.8:
            recommendations.append('Excellent fit predicted for your body type')
        elif fit_analysis['fit_quality'] > 0.6:
            recommendations.append('Good fit with minor adjustments needed')
        else:
            recommendations.append('Consider trying a different size or style')
        
        # Garment-specific recommendations
        garment_recommendations = {
            'top': 'Pair with complementary bottoms for a complete look',
            'bottom': 'Choose a matching top to complete the outfit',
            'dress': 'Add accessories to enhance the overall style',
            'outerwear': 'Layer over existing outfits for versatile styling',
            'shoes': 'Ensure proper fit and comfort for extended wear',
            'accessories': 'Coordinate with your existing wardrobe'
        }
        
        if garment_type in garment_recommendations:
            recommendations.append(garment_recommendations[garment_type])
        
        # Gender-specific recommendations
        if user_gender == 'female':
            recommendations.append('Consider adding jewelry or a handbag to complete the look')
        else:
            recommendations.append('Pair with appropriate footwear for the occasion')
        
        return recommendations
    
    def save_session(self, session_data):
        """Save try-on session to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO tryon_sessions 
                (user_id, user_image_path, garment_image_path, result_image_path, 
                 garment_type, user_gender, confidence_score, processing_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_data.get('user_id'),
                session_data.get('user_image_path'),
                session_data.get('garment_image_path'),
                session_data.get('result_image_path'),
                session_data.get('garment_type'),
                session_data.get('user_gender'),
                session_data.get('confidence_score'),
                session_data.get('processing_time')
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to save session: {str(e)}")
    
    def process_virtual_tryon(self, request_data):
        """Main processing function for virtual try-on"""
        start_time = datetime.now()
        
        try:
            # Extract request data
            user_image = request_data['user_image']
            garment_image = request_data['garment_image']
            garment_type = request_data.get('garment_type', 'top')
            user_gender = request_data.get('user_gender', 'female')
            body_measurements = request_data.get('body_measurements', {})
            
            if not self.model_loaded or not DEPENDENCIES_AVAILABLE:
                # Demo mode - return user image with overlay message
                logger.info("Running in demo mode - AI model not available")
                
                # Calculate processing time
                processing_time = (datetime.now() - start_time).total_seconds() * 1000
                
                # Generate fit analysis and recommendations
                fit_analysis = self.analyze_fit(garment_type, user_gender, body_measurements)
                recommendations = self.generate_recommendations(garment_type, user_gender, fit_analysis)
                
                return {
                    'success': True,
                    'processed_image': user_image,  # Return original image in demo mode
                    'confidence': 0.85,  # Demo confidence
                    'processing_time': processing_time,
                    'recommendations': recommendations + ['Demo mode: Install AI dependencies for full functionality'],
                    'fit_analysis': fit_analysis,
                    'demo_mode': True
                }
            
            # Full AI mode
            if not self.load_model():
                raise Exception("AI model not available")
            
            # Preprocess images
            user_array = self.preprocess_image(user_image)
            garment_array = self.preprocess_image(garment_image)
            
            # Prepare model inputs (only if dependencies available)
            if DEPENDENCIES_AVAILABLE:
                user_batch = np.expand_dims(user_array, axis=0)
                garment_batch = np.expand_dims(garment_array, axis=0)
            
            # Run AI inference
            prediction = self.model.predict([user_batch, garment_batch])
            result_image = prediction[0]
            
            # Post-process result
            processed_image = self.postprocess_image(result_image)
            
            # Calculate metrics
            confidence = self.calculate_confidence(result_image, user_array)
            fit_analysis = self.analyze_fit(garment_type, user_gender, body_measurements)
            recommendations = self.generate_recommendations(garment_type, user_gender, fit_analysis)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Save session data
            session_data = {
                'user_id': request_data.get('user_id', 'anonymous'),
                'garment_type': garment_type,
                'user_gender': user_gender,
                'confidence_score': confidence,
                'processing_time': processing_time
            }
            self.save_session(session_data)
            
            return {
                'success': True,
                'processed_image': processed_image,
                'confidence': confidence,
                'processing_time': processing_time,
                'recommendations': recommendations,
                'fit_analysis': fit_analysis
            }
            
        except Exception as e:
            logger.error(f"Virtual try-on processing failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': (datetime.now() - start_time).total_seconds() * 1000
            }

# Initialize AI Try-On backend
ai_tryon_backend = AITryOnBackend()

@ai_tryon_bp.route('/process', methods=['POST'])
def process_tryon():
    """Process virtual try-on request"""
    try:
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['user_image', 'garment_image']
        for field in required_fields:
            if field not in request_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Process the request
        result = ai_tryon_backend.process_virtual_tryon(request_data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@ai_tryon_bp.route('/train', methods=['POST'])
def train_model():
    """Train the AI model with new data"""
    try:
        training_data = request.get_json()
        
        if not training_data or 'samples' not in training_data:
            return jsonify({'error': 'No training data provided'}), 400
        
        # Add training data to database
        conn = sqlite3.connect(ai_tryon_backend.db_path)
        cursor = conn.cursor()
        
        for sample in training_data['samples']:
            cursor.execute('''
                INSERT INTO training_data 
                (input_data, expected_output, garment_type, user_gender, quality_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                json.dumps(sample.get('input')),
                sample.get('expected_output'),
                sample.get('garment_type'),
                sample.get('user_gender'),
                sample.get('quality_score', 1.0)
            ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Added {len(training_data["samples"])} training samples',
            'total_samples': len(training_data['samples'])
        }), 200
        
    except Exception as e:
        logger.error(f"Training API error: {str(e)}")
        return jsonify({'error': 'Training failed'}), 500

@ai_tryon_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Get AI model performance metrics"""
    try:
        conn = sqlite3.connect(ai_tryon_backend.db_path)
        cursor = conn.cursor()
        
        # Get session statistics
        cursor.execute('SELECT COUNT(*) FROM tryon_sessions')
        total_sessions = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(confidence_score) FROM tryon_sessions WHERE confidence_score IS NOT NULL')
        avg_confidence = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT AVG(processing_time) FROM tryon_sessions WHERE processing_time IS NOT NULL')
        avg_processing_time = cursor.fetchone()[0] or 0
        
        # Get training data statistics
        cursor.execute('SELECT COUNT(*) FROM training_data')
        training_samples = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'model_loaded': ai_tryon_backend.model_loaded,
            'total_sessions': total_sessions,
            'average_confidence': round(avg_confidence, 3),
            'average_processing_time': round(avg_processing_time, 2),
            'training_samples': training_samples
        }), 200
        
    except Exception as e:
        logger.error(f"Metrics API error: {str(e)}")
        return jsonify({'error': 'Failed to get metrics'}), 500

@ai_tryon_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': ai_tryon_backend.model_loaded,
        'timestamp': datetime.now().isoformat()
    }), 200