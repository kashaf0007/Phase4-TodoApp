# Todo App Frontend with Chat Interface

This is the frontend for the Todo application with an integrated AI chat assistant. Built with Next.js and React, it provides a user-friendly interface for managing tasks and interacting with an AI assistant.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **AI Chat Assistant**: Interact with an AI assistant for help with tasks
- **Conversation Context**: Maintain context across multiple interactions
- **Tool Transparency**: See when the AI uses backend tools
- **Secure Authentication**: Protected by Better Auth

## Tech Stack

- **Framework**: Next.js
- **Language**: React with TypeScript
- **UI Components**: @chatscope/chat-ui-kit-react
- **State Management**: React hooks
- **Authentication**: Better Auth
- **API Queries**: @tanstack/react-query

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-app-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.local.example .env.local
   ```
   
   Update the values in `.env.local` with your actual configuration.

### Running the Application

To run the application in development mode:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── ChatInterface.jsx  # Main chat interface
│   │   ├── Layout.jsx         # Base layout component
│   │   ├── MessageList.jsx    # Message display component
│   │   ├── MessageInput.jsx   # Message input component
│   │   └── ToolCallDisplay.jsx # Tool call visualization
│   ├── services/        # API and business logic services
│   │   └── apiService.js      # API communication
│   ├── utils/           # Utility functions and constants
│   │   ├── constants.js       # Application constants
│   │   └── errorHandler.js    # Error handling utilities
│   └── pages/           # Next.js pages
│       └── index.js     # Main application page
├── .env.local          # Environment variables (not committed)
├── next.config.js      # Next.js configuration
├── package.json        # Dependencies and scripts
└── README.md           # This file
```

## API Integration

The frontend communicates with the backend API at the configured URL. The main endpoints used are:

- `POST /api/{user_id}/chat` - Send messages to the AI assistant
- `POST /api/{user_id}/conversations` - Create new conversations
- `GET /api/{user_id}/conversations/{conversation_id}` - Get conversation history

## Environment Variables

- `NEXT_PUBLIC_API_URL` - The URL of the backend API
- `BETTER_AUTH_SECRET` - Secret for authentication (should match backend)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License.