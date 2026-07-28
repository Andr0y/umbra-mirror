# Rapports de qualité (couverture, SonarCloud)

## Couverture de tests (pytest)

- Génération locale : `make test` ou `pytest` (produit `coverage.xml` à la racine, défini dans `pyproject.toml`).
- Lecture : ouvrir `coverage.xml` ou le résumé terminal « term-missing ».
- CI : le workflow **CI** upload l’artefact `coverage-xml` pour SonarCloud.

## SonarCloud

- Workflow : `.github/workflows/SonarCloud.yml` (déclenché après CI réussi ou à la main).
- Prérequis : secrets `SONAR_TOKEN` et projet configuré sur SonarCloud (`sonar.projectKey` dans le workflow).
- **Pour un livrable académique** : joindre une capture d’écran du tableau de bord Sonar ou exporter le rapport PDF depuis l’UI SonarCloud (non versionné ici pour éviter la duplication avec la vérité CI).

## Linting et types (équivalent ESLint / Pylint)

Le projet **Python** standardise sur :

- **Ruff** (lint + format) — remplace une grande partie de Flake8 / Pylint pour le style et erreurs fréquentes.
- **Mypy** — typage statique (imports ML souvent en `ignore_missing_imports`).

Pas d’ESLint (pas de frontend JS dans ce dépôt).
