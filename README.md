# Password-Hash-Tool

**Outil en ligne de commande pour hacher, vérifier et évaluer les performances de mots de passe à l'aide d'algorithmes modernes (bcrypt, argon2, scrypt). Inclut un serveur FastAPI optionnel pour une intégration via API REST.**

---

## Table des matières

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Algorithmes supportés](#algorithmes-supportés)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Mode CLI](#mode-cli)
  - [Mode serveur API](#mode-serveur-api)
- [Développement](#développement)
- [Tests](#tests)
- [Architecture du projet](#architecture-du-projet)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## Présentation

La gestion sécurisée des mots de passe est un pilier fondamental de toute application moderne. **Password-Hash-Tool** offre une interface unifiée — en ligne de commande ou via API REST — pour effectuer les opérations cryptographiques essentielles sur les mots de passe :

- **Hachage** : transformer un mot de passe clair en un hash irréversible, prêt à être stocké en base de données.
- **Vérification** : comparer un mot de passe candidat à un hash existant pour valider une authentification.
- **Benchmark** : mesurer le temps de calcul des différents algorithmes et calibrer les paramètres de coût selon les contraintes de performance de votre infrastructure.

Cet outil est conçu pour les développeurs, les ingénieurs sécurité et les équipes DevOps qui souhaitent standardiser et auditer les pratiques de hachage de mots de passe au sein de leurs projets.

---

## Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| Hachage multi-algorithmes | Prise en charge de bcrypt, argon2 (argon2id) et scrypt |
| Vérification de hash | Validation d'un mot de passe contre un hash existant |
| Benchmark | Mesure du temps de calcul par algorithme avec paramètres configurables |
| Serveur API REST | Point d'accès HTTP via FastAPI (optionnel) pour intégration dans des pipelines |
| Sortie structurée | Résultats en JSON pour faciliter l'intégration avec d'autres outils |
| Paramètres ajustables | Contrôle fin du coût mémoire, du nombre d'itérations et du parallélisme |

---

## Algorithmes supportés

### bcrypt

Algorithme éprouvé, largement déployé. Le facteur de coût (work factor) est ajustable pour augmenter la résistance aux attaques par force brute à mesure que le matériel évolue.

### argon2id

Vainqueur de la Password Hashing Competition (2015). Combine résistance aux attaques GPU (memory-hard) et protection contre les attaques par canaux auxiliaires. C'est l'algorithme recommandé par l'OWASP pour les nouveaux projets.

### scrypt

Algorithme memory-hard conçu pour rendre les attaques matérielles coûteuses. Paramétrable en termes de mémoire (N), de blocs (r) et de parallélisme (p).

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation depuis les sources

```bash
git clone https://github.com/valorisa/Password-Hash-Tool.git
cd Password-Hash-Tool
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -e ".[dev]"
```

### Installation rapide (pip)

```bash
pip install password-hash-tool
```

---

## Utilisation

### Mode CLI

#### Hacher un mot de passe

```bash
password-hash-tool hash --algorithm argon2id --password "MonMotDePasse123!"
```

Sortie :

```json
{
  "algorithm": "argon2id",
  "hash": "$argon2id$v=19$m=65536,t=3,p=4$c2FsdGV4YW1wbGU$hashedvalue...",
  "time_ms": 87.3
}
```

#### Vérifier un mot de passe contre un hash

```bash
password-hash-tool verify \
  --password "MonMotDePasse123!" \
  --hash '$argon2id$v=19$m=65536,t=3,p=4$c2FsdGV4YW1wbGU$hashedvalue...'
```

Sortie :

```json
{
  "valid": true,
  "time_ms": 91.1
}
```

#### Benchmark des algorithmes

```bash
password-hash-tool benchmark --iterations 100
```

Sortie :

```json
{
  "results": [
    {"algorithm": "bcrypt", "cost": 12, "avg_ms": 210.4},
    {"algorithm": "argon2id", "memory_cost": 65536, "time_cost": 3, "avg_ms": 87.9},
    {"algorithm": "scrypt", "n": 16384, "r": 8, "p": 1, "avg_ms": 95.2}
  ]
}
```

### Mode serveur API

Lancer le serveur FastAPI :

```bash
password-hash-tool serve --host 0.0.0.0 --port 8000
```

Le serveur expose les endpoints suivants :

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/hash` | Hacher un mot de passe |
| POST | `/verify` | Vérifier un mot de passe |
| GET | `/benchmark` | Lancer un benchmark |
| GET | `/health` | Vérifier l'état du serveur |

Exemple d'appel avec `curl` :

```bash
curl -X POST http://localhost:8000/hash \
  -H "Content-Type: application/json" \
  -d '{"password": "ExempleMotDePasse", "algorithm": "bcrypt", "cost": 12}'
# example only — never hardcode real credentials
```

Documentation interactive disponible à : `http://localhost:8000/docs` (Swagger UI)

---

## Développement

### Mise en place de l'environnement local

```bash
git clone https://github.com/valorisa/Password-Hash-Tool.git
cd Password-Hash-Tool
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Commandes disponibles

```bash
# Linter (ruff)
ruff check src/

# Formateur (ruff format)
ruff format src/

# Tests
pytest

# Tests avec couverture
pytest --cov=src --cov-report=term-missing

# Lancer le serveur en mode développement
uvicorn src.password_hash_tool.api:app --reload
```

---

## Tests

Le projet utilise `pytest` comme framework de test. Les tests couvrent :

- Le hachage et la vérification pour chaque algorithme supporté
- La validation des entrées (mots de passe vides, paramètres invalides)
- Les endpoints de l'API REST
- Les cas limites (hash corrompu, algorithme non supporté)

Lancer les tests :

```bash
pytest -v
```

---

## Architecture du projet

```
Password-Hash-Tool/
├── src/
│   └── password_hash_tool/
│       ├── __init__.py          # Point d'entrée du package
│       ├── cli.py               # Interface ligne de commande (Click/Typer)
│       ├── api.py               # Serveur FastAPI
│       ├── hashers/
│       │   ├── __init__.py
│       │   ├── bcrypt.py        # Implémentation bcrypt
│       │   ├── argon2.py        # Implémentation argon2id
│       │   └── scrypt.py        # Implémentation scrypt
│       ├── benchmark.py         # Logique de benchmarking
│       └── models.py            # Modèles Pydantic (requêtes/réponses)
├── tests/
│   ├── test_cli.py
│   ├── test_api.py
│   └── test_hashers.py
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline CI (lint + tests)
├── pyproject.toml               # Configuration du projet et dépendances
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Contribuer

Les contributions sont les bienvenues ! Consultez le fichier [CONTRIBUTING.md](CONTRIBUTING.md) pour connaître les conventions et le processus de soumission de pull requests.

---

## Licence

Ce projet est distribué sous licence [MIT](LICENSE).

---

*Développé avec des pratiques de sécurité modernes. Ne jamais stocker de mots de passe en clair.*
