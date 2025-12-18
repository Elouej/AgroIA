"""
Script de test pour vérifier la détection d'images non-tomate

Ce script simule l'envoi d'images au serveur Flask pour tester
la nouvelle fonctionnalité de rejet des images qui ne sont pas des tomates.

Usage:
    python test_non_tomato.py
"""

import requests
import json

# Configuration
API_URL = "http://localhost:5001/predict"  # Changez si votre serveur est ailleurs

def test_image(image_path, description):
    """
    Teste une image avec l'API de prédiction
    
    Args:
        image_path: Chemin vers l'image à tester
        description: Description du test pour l'affichage
    """
    print(f"\n{'='*60}")
    print(f"📸 Test: {description}")
    print(f"📁 Fichier: {image_path}")
    print('='*60)
    
    try:
        # Ouvrir et envoyer l'image
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            data = {
                'capteurId': 'TEST_CAPTEUR_001',
                'userId': 'TEST_USER_123'
            }
            
            response = requests.post(API_URL, files=files, data=data)
            
        # Afficher le résultat
        print(f"\n📊 Résultat:")
        print(f"   Status Code: {response.status_code}")
        
        try:
            result = response.json()
            print(f"   Success: {result.get('success', 'N/A')}")
            
            if result.get('success'):
                print(f"   ✅ IMAGE ACCEPTÉE")
                print(f"   Prédiction: {result.get('prediction', 'N/A')}")
                print(f"   Prédiction (FR): {result.get('predictionFr', 'N/A')}")
                print(f"   Confiance: {result.get('confidence', 0)*100:.2f}%")
                print(f"   Maladie détectée: {result.get('diseaseDetected', 'N/A')}")
                print(f"   Sévérité: {result.get('severity', 'N/A')}")
            else:
                print(f"   ❌ IMAGE REJETÉE")
                print(f"   Erreur: {result.get('error', 'N/A')}")
                print(f"   Message: {result.get('errorMessage', 'N/A')}")
                print(f"   Message (FR): {result.get('errorMessageFr', 'N/A')}")
                if 'confidence' in result:
                    print(f"   Confiance tentée: {result.get('confidence', 0)*100:.2f}%")
                if 'attempted_prediction' in result:
                    print(f"   Prédiction tentée: {result.get('attempted_prediction', 'N/A')}")
                    
        except json.JSONDecodeError:
            print(f"   ⚠️ Réponse non-JSON: {response.text}")
            
    except FileNotFoundError:
        print(f"   ❌ ERREUR: Fichier introuvable: {image_path}")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ ERREUR: Impossible de se connecter au serveur {API_URL}")
        print(f"   💡 Assurez-vous que le serveur Flask est démarré!")
    except Exception as e:
        print(f"   ❌ ERREUR: {type(e).__name__}: {str(e)}")

def main():
    """
    Fonction principale de test
    """
    print("\n" + "="*60)
    print("🧪 TESTS DE DÉTECTION D'IMAGES NON-TOMATE")
    print("="*60)
    print("\n💡 Ce script teste la capacité du modèle à rejeter")
    print("   les images qui ne sont pas des tomates.")
    print("\n⚠️  Assurez-vous que:")
    print("   1. Le serveur Flask est démarré (python app.py)")
    print(f"   2. Le serveur tourne sur {API_URL}")
    print("   3. Vous avez des images de test disponibles")
    
    # Liste des tests à effectuer
    # REMPLACEZ CES CHEMINS PAR VOS PROPRES IMAGES
    tests = [
        # Format: (chemin_image, description)
        ("test_images/tomate_saine.jpg", "Tomate saine - DOIT être acceptée"),
        ("test_images/tomate_malade.jpg", "Tomate malade - DOIT être acceptée"),
        ("test_images/pomme.jpg", "Pomme - DOIT être rejetée"),
        ("test_images/voiture.jpg", "Voiture - DOIT être rejetée"),
        ("test_images/personne.jpg", "Personne - DOIT être rejetée"),
        ("test_images/autre_plante.jpg", "Autre plante - DOIT être rejetée"),
    ]
    
    print("\n" + "="*60)
    print("📋 LISTE DES TESTS")
    print("="*60)
    for i, (path, desc) in enumerate(tests, 1):
        print(f"   {i}. {desc}")
        print(f"      Fichier: {path}")
    
    input("\n⏸️  Appuyez sur ENTRÉE pour commencer les tests...")
    
    # Exécuter les tests
    for image_path, description in tests:
        test_image(image_path, description)
    
    # Résumé
    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS")
    print("="*60)
    print("\n💡 Interprétation des résultats:")
    print("   • Images de tomates avec confiance > 60% : Acceptées ✅")
    print("   • Images de tomates avec confiance < 60% : Rejetées ⚠️ (améliorer qualité)")
    print("   • Images non-tomate : Rejetées ❌ (comportement attendu)")
    print("\n📝 Si une tomate est rejetée, essayez:")
    print("   1. Prendre une photo plus nette")
    print("   2. Améliorer l'éclairage")
    print("   3. Cadrer uniquement les feuilles")
    print("   4. Ajuster le seuil de confiance dans app.py (ligne ~205)")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
