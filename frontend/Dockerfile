# Étape 1 : Construire l'application React
FROM node:14 AS build

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le code source
COPY . .

# Construire l'application
RUN npm run build

# Étape 2 : Servir l'application avec Nginx
FROM nginx:alpine

# Copier les fichiers construits depuis l'étape précédente
COPY --from=build /app/build /usr/share/nginx/html
