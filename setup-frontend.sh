#!/bin/bash

echo "🚀 Setting up Canada Fire Watch React Frontend with Kibo UI Design Principles..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not available. Please install npm."
    exit 1
fi

echo "✅ npm $(npm -v) detected"

# Install dependencies
echo "📦 Installing dependencies (shadcn/ui components with Kibo UI design principles)..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create .env.local file
echo "🔧 Creating environment configuration..."
cat > .env.local << EOF
# Frontend Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_APP_NAME=Canada Fire Watch
EOF

echo "✅ Environment configuration created"

# Check if Flask backend is running
echo "🔍 Checking Flask backend status..."
if curl -s http://localhost:5000/api/enhanced/provinces > /dev/null 2>&1; then
    echo "✅ Flask backend is running on port 5000"
else
    echo "⚠️  Flask backend is not running on port 5000"
    echo "   Please start the Flask backend first:"
    echo "   cd src && python main.py"
fi

echo ""
echo "🎉 Setup complete! To start the frontend:"
echo ""
echo "   npm run dev"
echo ""
echo "   Then open http://localhost:3000 in your browser"
echo ""
echo "📚 For more information, see FRONTEND_README.md"
echo ""
echo "🔗 Backend API: http://localhost:5000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo ""
