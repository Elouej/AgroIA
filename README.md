# ChatBot_AgroIA 🌱🤖

Assistant IA intelligent multilingue pour la détection des maladies des plantes de tomate avec analyse d'images.

![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Languages](https://img.shields.io/badge/languages-FR%20%7C%20EN%20%7C%20AR-orange.svg)

## 🌟 Fonctionnalités

### 🔍 Analyse IA

- **Détection automatique** de 10 maladies de tomates
- **Analyse d'images** avec intelligence artificielle
- **Recommandations personnalisées** de traitement
- **Niveau de confiance** pour chaque diagnostic

### 🌍 Support Multilingue

- **Français** - Interface et réponses complètes
- **English** - Full interface and responses
- **العربية** - واجهة وردود كاملة
- Détection automatique de la langue

### 💬 Conversations Naturelles

- Plus de 30 types de questions/réponses
- Salutations personnalisées avec nom d'utilisateur
- Explications détaillées des traitements
- Guide interactif pour les recommandations

### 📸 Upload d'Images

- Sélection d'images locale
- Prévisualisation avant analyse
- Affichage de l'image dans la conversation
- Support de multiples formats d'images

## 🚀 Installation

### Prérequis

- Navigateur web moderne (Chrome, Firefox, Edge, Safari)
- Python 3.8+ (pour l'API backend)
- Flask et TensorFlow (voir `requirements.txt`)

### Configuration

1. **Cloner le repository**

```bash
git clone https://github.com/doosr/ChatBot_AgroIA.git
cd ChatBot_AgroIA
```

2. **Installer les dépendances Python**

```bash
pip install -r requirements.txt
```

3. **Lancer l'API Flask**

```bash
python app.py
```

4. **Ouvrir le chatbot**

```bash
# Ouvrir chatbot.html dans votre navigateur
start chatbot.html
```

## 📋 Structure du Projet

```
ChatBot_AgroIA/
├── chatbot.html           # Interface utilisateur
├── chatbot-style.css      # Styles et animations
├── chatbot-script.js      # Logique du chatbot
├── app.py                 # API Flask pour l'analyse IA
├── model/                 # Modèle TensorFlow (non inclus)
└── README.md              # Documentation
```

## 🎯 Utilisation

### 1. Configuration Initiale

- Cliquez sur l'icône ⚙️ (Paramètres)
- Entrez l'URL de l'API IA : `http://localhost:5001`
- (Optionnel) Entrez votre nom d'utilisateur
- Cliquez sur "Enregistrer"

### 2. Analyser une Plante

1. Cliquez sur le bouton caméra 📷
2. Sélectionnez une photo de votre plant de tomate
3. L'image s'affiche dans la conversation
4. Cliquez sur ➤ pour analyser
5. Consultez le diagnostic et les recommandations

### 3. Demander de l'Aide

- "Bonjour" - Salutation personnalisée
- "Aide" - Menu d'aide
- "Maladies supportées" - Liste complète
- "Comment utiliser le fongicide ?" - Guide détaillé
- "Expliquer la taille" - Instructions de taille

## 🌱 Maladies Détectées

| Maladie | Français | English | العربية |
|---------|----------|---------|---------|
| Healthy | Sain | Healthy | سليم |
| Bacterial spot | Tache bactérienne | Bacterial spot | بقعة بكتيرية |
| Early blight | Mildiou précoce | Early blight | لفحة مبكرة |
| Late blight | Mildiou tardif | Late blight | لفحة متأخرة |
| Leaf mold | Moisissure | Leaf mold | عفن الأوراق |
| Septoria leaf spot | Tache septorienne | Septoria leaf spot | بقعة سبتوريا |
| Spider mites | Acariens | Spider mites | عث العنكبوت |
| Target spot | Tache cible | Target spot | بقعة مستهدفة |
| Mosaic virus | Virus mosaïque | Mosaic virus | فيروس الموزاييك |
| Yellow leaf curl | Enroulement jaune | Yellow leaf curl | تجعد الأوراق |

## 💡 Guides Détaillés Disponibles

Le chatbot fournit des guides complets pour :

- 🍄 Traitement fongicide (produits, application, précautions)
- 💨 Amélioration de la circulation d'air
- 💧 Gestion de l'arrosage (fréquence, bonnes pratiques)
- ✂️ Taille et entretien (techniques, désinfection)
- 🛡️ Prévention des maladies (rotation, surveillance)

## 🎨 Fonctionnalités Techniques

### Frontend

- **HTML5** - Structure sémantique
- **CSS3** - Animations, glassmorphism, responsive design
- **JavaScript ES6** - Logique moderne avec classes
- **LocalStorage** - Persistance des données

### Backend

- **Flask** - API REST
- **TensorFlow** - Modèle de détection CNN
- **PIL** - Traitement d'images
- **NumPy** - Calculs matriciels

### Design

- Thème sombre professionnel (vert/noir)
- Animations fluides et micro-interactions
- Interface responsive (mobile, tablet, desktop)
- Support RTL pour l'arabe

## 🔧 Configuration de l'API

Variables d'environnement (optionnelles) :

```bash
BACKEND_URL=http://your-backend-url
BACKEND_API_KEY=your-api-key
SEND_TO_BACKEND=true
PORT=5001
```

## 📱 Compatibilité

### Navigateurs Supportés

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Appareils

- 💻 Desktop (Windows, macOS, Linux)
- 📱 Mobile (iOS, Android)
- 🖥️ Tablet

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Dawser** - [GitHub](https://github.com/doosr)

## 🙏 Remerciements

- TensorFlow pour le framework de deep learning
- Flask pour l'API REST légère
- Font Awesome pour les icônes
- Google Fonts pour la typographie

## 📞 Support

Pour toute question ou problème :

- 📧 Email: [dawserbelgacem122@gmail.com]
- 🐛 Issues: [GitHub Issues](https://github.com/doosr/ChatBot_AgroIA/issues)

---

**⭐ Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile sur GitHub !**
