#!/bin/bash

# Atualizar sistema
echo "🔄 Atualizando sistema..."
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
echo "🐳 Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
echo "📦 Instalando Docker Compose..."
sudo apt-get install -y docker-compose-plugin

# Criar diretórios
mkdir -p validacao-documentos-backend
mkdir -p validacao-documentos-frontend

# Clonar repositórios (Substitua pelas URLs reais se necessário)
# echo "📥 Clonando repositórios..."
# git clone https://github.com/cultodemoniocelestial-tech/validacao-documentos-backend.git
# git clone https://github.com/cultodemoniocelestial-tech/validacao-documentos-frontend.git

echo "🚀 Iniciando serviços..."
# Assumindo que os arquivos docker-compose.yml e nginx/ estão na pasta atual
sudo docker compose up -d --build

echo "✅ Deploy concluído! Acesse pelo IP público da sua instância."
