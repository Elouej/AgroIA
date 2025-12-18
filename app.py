
import os
import logging
from datetime import datetime
import traceback
import io
import requests
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf

# Supprimer les messages verbeux de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Configuration
app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

# Model configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'models/tomato_disease_model.h5')
MODEL_LOADED = False
model = None

# Image configuration
IMAGE_SIZE = (224, 224)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

# ═══════════════════════════════════════════════════════════
# DICTIONNAIRE DES MALADIES (TOMATOES - ALIGNÉ AVEC MODÈLE)
# ═══════════════════════════════════════════════════════════

DISEASE_CLASSES = [
    "Tomato_bacterial_spot",
    "Tomato_early_blight",
    "Tomato_healthy",
    "Tomato_late_blight",
    "Tomato_leaf_mold",
    "Tomato_septoria_leaf_spot",
    "Tomato_spider_mites_two-spotted_spider_mite",
    "Tomato_target_spot",
    "Tomato_mosaic_virus",
    "Tomato_yellow_leaf_curl_virus"
]

# Traduction en français pour affichage
DISEASE_NAMES_FR = {
    "Tomato_healthy": "Sain",
    "Tomato_bacterial_spot": "Tache bactérienne",
    "Tomato_early_blight": "Mildiou précoce",
    "Tomato_late_blight": "Mildiou tardif",
    "Tomato_leaf_mold": "Moisissure des feuilles",
    "Tomato_septoria_leaf_spot": "Tache septorienne",
    "Tomato_spider_mites_two-spotted_spider_mite": "Acariens",
    "Tomato_target_spot": "Tache cible",
    "Tomato_mosaic_virus": "Virus de la mosaïque",
    "Tomato_yellow_leaf_curl_virus": "Virus de l'enroulement jaune"
}

# Recommandations par maladie
RECOMMENDATIONS = {
    "Tomato_healthy": [
        "Plante saine, continuer les soins habituels",
        "Surveiller régulièrement vos plantes",
        "Maintenir un bon drainage"
    ],
    "Tomato_bacterial_spot": [
        "Retirer les feuilles infectées",
        "Appliquer un fongicide adapté",
        "Éviter l'arrosage par aspersion",
        "Nettoyer les outils de taille"
    ],
    "Tomato_early_blight": [
        "Retirer les feuilles touchées",
        "Traiter avec fongicide préventif",
        "Améliorer la circulation d'air",
        "Pailler le sol pour éviter les éclaboussures"
    ],
    "Tomato_late_blight": [
        "Isoler la plante immédiatement",
        "Appliquer un fongicide systémique",
        "Détruire les parties infectées",
        "Éviter l'humidité excessive"
    ],
    "Tomato_leaf_mold": [
        "Améliorer la ventilation",
        "Réduire l'humidité",
        "Espacer les plants",
        "Tailler pour aérer"
    ],
    "Tomato_septoria_leaf_spot": [
        "Supprimer les feuilles malades",
        "Traitement fongicide préventif",
        "Éviter de mouiller le feuillage",
        "Rotation des cultures"
    ],
    "Tomato_spider_mites_two-spotted_spider_mite": [
        "Pulvériser insecticide adapté",
        "Maintenir humidité élevée",
        "Utiliser des acariens prédateurs",
        "Nettoyer régulièrement les feuilles"
    ],
    "Tomato_target_spot": [
        "Enlever les feuilles infectées",
        "Appliquer fongicide local",
        "Améliorer le drainage",
        "Espacer les plantations"
    ],
    "Tomato_mosaic_virus": [
        "Isoler la plante infectée",
        "Détruire les plants gravement atteints",
        "Désinfecter tous les outils",
        "Contrôler les insectes vecteurs"
    ],
    "Tomato_yellow_leaf_curl_virus": [
        "Isoler la plante",
        "Contrôler les insectes vecteurs (aleurodes)",
        "Utiliser des filets anti-insectes",
        "Détruire les plants trop atteints"
    ]
}

# Classes nécessitant arrosage
ARROSAGE_CLASSES = [
    "Tomato_healthy",
    "Tomato_early_blight",
    "Tomato_late_blight",
    "Tomato_bacterial_spot"
]

# ═══════════════════════════════════════════════════════════
# CHARGEMENT DU MODÈLE
# ═══════════════════════════════════════════════════════════

def load_model():
    """Charge le modèle TensorFlow/Keras"""
    global model, MODEL_LOADED
    
    try:
        if os.path.exists(MODEL_PATH):
            logger.info(f"📦 Chargement du modèle depuis {MODEL_PATH}")
            model = tf.keras.models.load_model(MODEL_PATH)
            MODEL_LOADED = True
            logger.info("✅ Modèle chargé avec succès")
        else:
            logger.warning(f"⚠️ Modèle introuvable: {MODEL_PATH}")
            logger.warning("⚠️ Mode DÉMO activé - Prédictions aléatoires")
            MODEL_LOADED = False
    except Exception as e:
        logger.error(f"❌ Erreur chargement modèle: {e}")
        MODEL_LOADED = False

# Charger le modèle au démarrage
load_model()

# ═══════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════

def preprocess_image(image_bytes):
    """Prétraite l'image pour le modèle"""
    try:
        # Ouvrir l'image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir en RGB si nécessaire
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionner
        image = image.resize(IMAGE_SIZE)
        
        # Convertir en array numpy et normaliser
        img_array = np.array(image) / 255.0
        
        # Ajouter dimension batch
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        logger.error(f"❌ Erreur preprocessing: {e}")
        raise

def predict_disease(img_array):
    """Prédit la maladie à partir de l'image prétraitée"""
    global model, MODEL_LOADED
    
    # ⚡ SEUILS TRÈS STRICTS pour éviter les faux positifs
    CONFIDENCE_THRESHOLD = 0.85  # 85% (augmenté pour être très strict)
    MIN_PREDICTION_GAP = 0.30  # 30% d'écart minimum (augmenté de 20%)
    MAX_ENTROPY_THRESHOLD = 1.5  # Entropie maximale acceptable
    
    try:
        if MODEL_LOADED and model is not None:
            # Prédiction réelle avec le modèle
            predictions = model.predict(img_array, verbose=0)
            
            # Trier les prédictions pour obtenir les top 2
            sorted_indices = np.argsort(predictions[0])[::-1]
            class_idx = int(sorted_indices[0])
            second_class_idx = int(sorted_indices[1]) if len(sorted_indices) > 1 else None
            
            confidence = float(predictions[0][class_idx])
            second_confidence = float(predictions[0][second_class_idx]) if second_class_idx is not None else 0.0
            prediction_gap = confidence - second_confidence
            
            # Calculer l'entropie (mesure de l'incertitude de la distribution)
            # Une entropie élevée = probabilités distribuées uniformément = pas une tomate claire
            epsilon = 1e-10  # Pour éviter log(0)
            entropy = -np.sum(predictions[0] * np.log(predictions[0] + epsilon))
            
            predicted_class = DISEASE_CLASSES[class_idx]
            
            logger.info(f"🤖 Prédiction modèle: {predicted_class}")
            logger.info(f"   Confiance: {confidence:.2%}")
            logger.info(f"   Écart avec 2ème: {prediction_gap:.2%}")
            logger.info(f"   Entropie: {entropy:.3f}")
            
            # ✅ VÉRIFICATION 1: Confiance trop faible
            if confidence < CONFIDENCE_THRESHOLD:
                logger.warning(f"⚠️ REJETÉ - Confiance trop faible ({confidence:.2%} < {CONFIDENCE_THRESHOLD:.0%})")
                return {
                    'success': False,
                    'error': 'image_not_tomato',
                    'errorMessage': f'Cette image ne semble pas être une plante de tomate. Confiance insuffisante: {confidence:.1%}',
                    'errorMessageFr': 'Cette image ne semble pas être une plante de tomate. Veuillez utiliser une photo claire de feuilles de tomate.',
                    'confidence': confidence,
                    'threshold': CONFIDENCE_THRESHOLD,
                    'attempted_prediction': predicted_class,
                    'timestamp': datetime.now().isoformat(),
                    'modelUsed': 'tomato_disease_model'
                }
            
            # ✅ VÉRIFICATION 2: Écart de prédiction trop faible (indécision)
            if prediction_gap < MIN_PREDICTION_GAP:
                logger.warning(f"⚠️ REJETÉ - Écart trop faible ({prediction_gap:.2%} < {MIN_PREDICTION_GAP:.0%})")
                return {
                    'success': False,
                    'error': 'image_not_tomato',
                    'errorMessage': f'Cette image ne correspond pas clairement à une tomate. Le modèle hésite (écart: {prediction_gap:.1%})',
                    'errorMessageFr': 'Image ambiguë. Veuillez utiliser une photo nette de feuilles de tomate.',
                    'confidence': confidence,
                    'prediction_gap': prediction_gap,
                    'gap_threshold': MIN_PREDICTION_GAP,
                    'attempted_prediction': predicted_class,
                    'timestamp': datetime.now().isoformat(),
                    'modelUsed': 'tomato_disease_model'
                }
            
            # ✅ VÉRIFICATION 3: Entropie trop élevée (distribution plate = pas une tomate)
            if entropy > MAX_ENTROPY_THRESHOLD:
                logger.warning(f"⚠️ REJETÉ - Entropie trop élevée ({entropy:.3f} > {MAX_ENTROPY_THRESHOLD})")
                return {
                    'success': False,
                    'error': 'image_not_tomato',
                    'errorMessage': f'Cette image ne ressemble pas à une tomate. Distribution des probabilités trop uniforme (entropie: {entropy:.2f})',
                    'errorMessageFr': 'Image non reconnue comme une plante de tomate. Veuillez soumettre une vraie photo de feuilles de tomate.',
                    'confidence': confidence,
                    'entropy': entropy,
                    'entropy_threshold': MAX_ENTROPY_THRESHOLD,
                    'attempted_prediction': predicted_class,
                    'timestamp': datetime.now().isoformat(),
                    'modelUsed': 'tomato_disease_model'
                }
            
        else:
            # Mode DÉMO - Prédiction aléatoire pour tests
            logger.warning("⚠️ Mode DÉMO - Prédiction simulée")
            predicted_class = np.random.choice(DISEASE_CLASSES)
            confidence = np.random.uniform(0.75, 0.98)
        
        # Nom de la maladie en français
        disease_name_fr = DISEASE_NAMES_FR.get(predicted_class, predicted_class)
        
        # Déterminer si c'est une maladie
        is_diseased = (predicted_class != "Tomato_healthy")
        
        # Déterminer la sévérité
        if not is_diseased:
            severity = 'none'
        elif confidence >= 0.9:
            severity = 'high'
        elif confidence >= 0.7:
            severity = 'medium'
        else:
            severity = 'low'
        
        # Déterminer si arrosage nécessaire
        should_water = predicted_class in ARROSAGE_CLASSES
        
        # Récupérer les recommandations
        recommendations = RECOMMENDATIONS.get(predicted_class, [
            'Consulter un expert agronome',
            'Isoler la plante affectée',
            'Surveiller l\'évolution'
        ])
        
        # Retourner le résultat COMPLET pour le backend
        return {
            # Format original (compatibilité)
            'maladie': predicted_class,
            'confiance': confidence,
            'recommandations': recommendations,
            'arroser': should_water,
            
            # Format backend attendu
            'prediction': predicted_class,
            'predictionFr': disease_name_fr,
            'confidence': confidence,
            'diseaseDetected': is_diseased,
            'severity': severity,
            'recommendations': recommendations,
            'shouldWater': should_water,
            
            # Métadonnées
            'timestamp': datetime.now().isoformat(),
            'modelUsed': 'tomato_disease_model' if MODEL_LOADED else 'demo_mode',
            'success': True
        }
    
    except Exception as e:
        logger.error(f"❌ Erreur prédiction: {e}")
        raise

# ═══════════════════════════════════════════════════════════
# ROUTES API
# ═══════════════════════════════════════════════════════════


@app.route('/health', methods=['GET'])
def health_check():
    """Vérification de l'état du service"""
    return jsonify({
        'status': 'online',
        'service': 'Plant Disease Detection AI',
        'version': '2.0.0',
        'model_loaded': MODEL_LOADED,
        'model_path': MODEL_PATH,
        'supported_classes': len(DISEASE_CLASSES),
        'timestamp': datetime.now().isoformat()
    })
@app.route('/predict', methods=['POST'])
def predict():
    """
    Analyse d'image directe depuis ESP32-CAM
    L'image est analysée puis supprimée
    
    Parameters:
    - image (file): Image à analyser
    - capteurId (form): ID du capteur (optionnel)
    - userId (form): ID de l'utilisateur (optionnel)
    """
    try:
        # Vérifier présence image
        if 'image' not in request.files:
            logger.error("❌ Aucune image fournie")
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        # Récupération des IDs
        capteurId = request.form.get('capteurId', None)
        userId = request.form.get('userId', None)
        
        # Lire l'image
        image_bytes = file.read()
        
        # Vérifier taille
        if len(image_bytes) > MAX_IMAGE_SIZE:
            logger.error(f"❌ Image trop large: {len(image_bytes)} bytes")
            return jsonify({'success': False, 'error': 'Image too large (max 10MB)'}), 400
        
        logger.info(f"📸 Image reçue")
        logger.info(f"   Capteur ID: {capteurId or 'Non spécifié'}")
        logger.info(f"   User ID: {userId or 'Non spécifié'}")
        logger.info(f"   Taille: {len(image_bytes)} bytes ({len(image_bytes)/1024:.1f} KB)")
        
        # Prétraiter l'image
        logger.info("🔄 Prétraitement de l'image...")
        img_array = preprocess_image(image_bytes)
        
        # Prédiction
        logger.info("🔍 Analyse en cours...")
        result = predict_disease(img_array)
        
        logger.info(f"✅ Analyse terminée:")
        logger.info(f"   Maladie: {result['prediction']}")
        logger.info(f"   Confiance: {result['confidence']*100:.1f}%")
        logger.info(f"   Sévérité: {result['severity']}")
        logger.info(f"   Arrosage: {'✓' if result['shouldWater'] else '✗'}")
        
        result['success'] = True
        
        # L'IMAGE EST AUTOMATIQUEMENT SUPPRIMÉE ICI
        logger.info("🗑️ Image supprimée de la mémoire")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Erreur analyse: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'type': type(e).__name__
        }), 500
@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """Analyse plusieurs images en une requête"""
    try:
        if 'images' not in request.files:
            return jsonify({'success': False, 'error': 'No images provided'}), 400
        
        files = request.files.getlist('images')
        capteurId = request.form.get('capteurId', None)
        
        results = []
        success_count = 0
        
        for idx, file in enumerate(files):
            try:
                logger.info(f"📸 Analyse image {idx+1}/{len(files)}")
                
                image_bytes = file.read()
                img_array = preprocess_image(image_bytes)
                result = predict_disease(img_array)
                
                result['success'] = True
                
                results.append(result)
                success_count += 1
                
            except Exception as e:
                logger.error(f"❌ Erreur image {idx+1}: {e}")
                results.append({
                    'success': False,
                    'image_index': idx,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'total': len(files),
            'success_count': success_count,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erreur batch: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Statistiques du service IA"""
    return jsonify({
        'model_loaded': MODEL_LOADED,
        'model_path': MODEL_PATH,
        'supported_classes': DISEASE_CLASSES,
        'total_classes': len(DISEASE_CLASSES)
    })

@app.route('/reload-model', methods=['POST'])
def reload_model():
    """Recharge le modèle (utile après mise à jour)"""
    try:
        load_model()
        return jsonify({
            'success': True,
            'model_loaded': MODEL_LOADED,
            'message': 'Modèle rechargé avec succès' if MODEL_LOADED else 'Modèle introuvable'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ═══════════════════════════════════════════════════════════
# DÉMARRAGE
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    # Récupérer le port dynamique de Render
    port = int(os.getenv('PORT', 5001))
    
    # Affichage informations démarrage
    print("\n" + "="*60)
    print("🤖 Service IA - Détection Maladies des Tomates")
    print("="*60)
    print(f"📍 Port: {port}")
    print(f" Modèle: {'✅ Chargé' if MODEL_LOADED else '❌ Non chargé (mode DÉMO)'}")
    print(f"🌱 Classes supportées: {len(DISEASE_CLASSES)}")
    print("="*60)
    print("\n📋 Routes disponibles:")
    print("   GET  /health           - État du service")
    print("   POST /predict          - Analyser une image")
    print("   POST /predict-batch    - Analyser plusieurs images")
    print("   GET  /stats            - Statistiques")
    print("   POST /reload-model     - Recharger le modèle")
    print("\n💡 Notes:")
    print("   • Les images sont supprimées après analyse")
    print("   • Backup local disponible sur ESP32 (carte SD)")
    print("="*60 + "\n")
    
    # Démarrer le serveur
    # IMPORTANT : debug=False en production sur Render
    app.run(
        host='0.0.0.0',
        port=port,  # ← Port dynamique
        debug=False  # ← Toujours False sur Render
    )
    