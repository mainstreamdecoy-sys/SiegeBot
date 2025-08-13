# Siege Chat Bot Dashboard

## Overview

Siege Chat Bot Dashboard is a full-stack web application for managing and monitoring a Telegram AI chatbot. The system provides real-time statistics, configuration management, and activity monitoring through a modern React-based dashboard interface. The bot integrates with Cohere's Command-R model to provide conversational AI responses in Telegram groups and private chats.

## User Preferences

Preferred communication style: Simple, everyday language.
Bot personality: Harley Quinn style - chaotic, unpredictable, enthusiastic with playful language and random exclamations.

## System Architecture

### Frontend Architecture
The client-side is built with React 18 using TypeScript and follows a component-based architecture:

- **Framework**: React with Vite as the build tool for fast development and optimized production builds
- **UI Components**: Shadcn/UI component library built on Radix UI primitives for accessible, customizable components
- **Styling**: Tailwind CSS with custom design tokens and CSS variables for theming
- **State Management**: TanStack Query (React Query) for server state management with automatic caching and synchronization
- **Routing**: Wouter for lightweight client-side routing
- **Type Safety**: Full TypeScript implementation with shared types between frontend and backend

### Backend Architecture
The server-side uses Express.js with TypeScript in an ESM configuration:

- **Framework**: Express.js with TypeScript for type-safe API development
- **API Design**: RESTful API endpoints for bot management, configuration, and statistics
- **Bot Integration**: Node Telegram Bot API for Telegram bot functionality
- **AI Integration**: Cohere Command-R model for generating conversational responses
- **Development**: Hot-reload development setup with Vite middleware integration

### Data Storage
The application uses a hybrid storage approach:

- **Database**: PostgreSQL with Drizzle ORM for type-safe database operations
- **Schema**: Defined database tables for users, bot configuration, statistics, and activity logs
- **Fallback Storage**: In-memory storage implementation for development and testing scenarios
- **Migrations**: Drizzle Kit for database schema migrations and management

### Authentication and Authorization
- **Session Management**: Express sessions with PostgreSQL session store using connect-pg-simple
- **User Management**: User authentication system with username/password login
- **Security**: Session-based authentication with secure cookie configuration

### Key Features and Components

#### Bot Management System
- Real-time bot status monitoring (online/offline states)
- Start/stop bot functionality through API endpoints
- Telegram bot integration with command handlers and message processing
- AI response generation with configurable probability settings

#### Configuration Management
- Dynamic bot configuration with real-time updates
- Adjustable reply probability and sticker frequency settings
- Group auto-respond and mention-only mode toggles
- Persistent configuration storage in database

#### Statistics and Monitoring
- Real-time bot performance metrics (total messages, active groups, response rates)
- Recent activity feed with categorized event types
- Automatic statistics updates and calculation
- Performance monitoring with response tracking

#### Dashboard Interface
- Responsive design with mobile-first approach
- Real-time data updates using React Query with polling
- Toast notifications for user feedback
- Loading states and error handling throughout the interface

### Development and Build Configuration
- **Build Process**: Vite for frontend bundling, esbuild for backend compilation
- **Development Tools**: Hot-reload for both frontend and backend development
- **TypeScript Configuration**: Strict type checking with path mapping for clean imports
- **Code Quality**: ESLint and Prettier integration (implied by project structure)

## External Dependencies

### Core Runtime Dependencies
- **Database**: PostgreSQL via Neon Database serverless connection
- **AI Service**: OpenAI API for GPT-4o model access
- **Telegram**: Telegram Bot API for bot functionality
- **Session Storage**: PostgreSQL for session persistence

### UI and Styling Libraries
- **Component Library**: Radix UI primitives for accessible components
- **Icons**: Font Awesome for icons, Lucide React for additional icons
- **Styling**: Tailwind CSS with PostCSS processing
- **Animations**: CSS-based animations with Tailwind utilities

### State Management and Data Fetching
- **Server State**: TanStack React Query for API state management
- **Form Handling**: React Hook Form with Zod validation resolvers
- **Date Handling**: date-fns for date manipulation and formatting

### Development and Build Tools
- **Build Tool**: Vite with React plugin and TypeScript support
- **Replit Integration**: Cartographer plugin and runtime error overlay for Replit environment
- **Database Tools**: Drizzle ORM and Drizzle Kit for database management
- **TypeScript**: Full TypeScript support with strict configuration

### Bot and AI Integration
- **Telegram Bot**: node-telegram-bot-api for Telegram bot functionality
- **AI Processing**: Cohere API for Command-R model integration
- **Validation**: Zod for runtime type validation and schema definitions