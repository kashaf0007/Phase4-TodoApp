# Quickstart Guide: ChatKit Frontend Integration

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- Access to Neon PostgreSQL database
- API keys for OpenAI and any other required services
- Git for version control

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual API keys and database URL
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install JavaScript dependencies
npm install

# Set up environment variables (only for build-time configurations)
cp .env.local.example .env.local
# Note: API keys should NOT be placed in frontend environment
```

### 4. Database Setup
```bash
# From the backend directory
python create_tables_in_neon.py
```

### 5. Running the Application

#### Backend
```bash
# From the backend directory
cd src
python -m uvicorn main:app --reload
# The API will be available at http://localhost:8000
```

#### Frontend
```bash
# From the frontend directory
npm run dev
# The frontend will be available at http://localhost:3000
```

## Configuration

### Frontend Configuration
- Update the API endpoint in `frontend/src/services/apiService.js` to point to your backend
- Configure domain allowlist settings if deploying to production

### Backend Configuration
- Ensure the Neon PostgreSQL connection string is properly set in environment variables
- Verify MCP tools are properly configured and accessible
- Set up authentication with Better Auth

## Testing the Integration
1. Start both backend and frontend servers
2. Open the frontend in your browser
3. Authenticate with a valid user account
4. Send a message in the chat interface
5. Verify that the message is processed by the backend and a response is returned
6. Check that tool calls are properly displayed in the UI using the ToolCallDisplay component
7. Verify that conversation context is maintained across messages
8. Test the "New Conversation" button to start fresh conversations
9. Confirm that confirmation messages appear after task operations