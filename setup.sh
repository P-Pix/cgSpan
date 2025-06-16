#!/bin/sh

set -eu  # pipefail n'est pas compatible avec sh

error_exit() {
  echo "Erreur : $1" >&2
  exit 1
}

echo "[INFO] Téléchargement de spmf.jar..."
wget -q --show-progress --timeout=30 https://www.philippe-fournier-viger.com/spmf/spmf.jar -O spmf.jar || error_exit "Échec du téléchargement de spmf.jar"

echo "[INFO] Vérification que le fichier existe..."
[ -f spmf.jar ] || error_exit "Le fichier spmf.jar n'a pas été téléchargé"

echo "[INFO] Création du dossier src/ s’il n'existe pas..."
mkdir -p src || error_exit "Impossible de créer le dossier src/"

echo "[INFO] Déplacement de spmf.jar vers src/..."
mv -f spmf.jar src/ || error_exit "Échec du déplacement de spmf.jar"

echo "[INFO] Installation du package Python spmf via pip..."
pip install spmf || error_exit "Échec de l'installation du package Python spmf"

echo "[SUCCÈS] Installation complète."
