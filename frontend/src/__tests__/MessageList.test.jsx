// frontend/src/__tests__/MessageList.test.jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import MessageList from '../components/MessageList';

describe('MessageList Component', () => {
  const mockMessages = [
    {
      id: '1',
      message: 'Hello there!',
      sender: 'user',
      timestamp: new Date(),
    },
    {
      id: '2',
      message: 'Hi, how can I help you?',
      sender: 'assistant',
      timestamp: new Date(),
      toolCalls: [{ tool_name: 'get_weather', parameters: { city: 'London' }, result: '20°C' }],
      confirmation: 'Weather information retrieved',
    },
  ];

  test('renders messages correctly', () => {
    render(<MessageList messages={mockMessages} isLoading={false} error={null} />);

    expect(screen.getByText('Hello there!')).toBeInTheDocument();
    expect(screen.getByText('Hi, how can I help you?')).toBeInTheDocument();
  });

  test('displays tool calls when present', () => {
    render(<MessageList messages={mockMessages} isLoading={false} error={null} />);

    expect(screen.getByText('Tools Used:')).toBeInTheDocument();
    expect(screen.getByText('get_weather:')).toBeInTheDocument();
  });

  test('displays confirmation messages when present', () => {
    render(<MessageList messages={mockMessages} isLoading={false} error={null} />);

    expect(screen.getByText('✓ Weather information retrieved')).toBeInTheDocument();
  });

  test('shows loading state', () => {
    render(<MessageList messages={[]} isLoading={true} error={null} />);

    expect(screen.getByText('Thinking...')).toBeInTheDocument();
  });

  test('shows error state', () => {
    render(<MessageList messages={[]} isLoading={false} error={'Connection failed'} />);

    expect(screen.getByText('Connection failed')).toBeInTheDocument();
  });

  test('renders empty state when no messages', () => {
    render(<MessageList messages={[]} isLoading={false} error={null} />);

    // Just ensure the component renders without errors
    expect(screen.queryByText('Hello there!')).not.toBeInTheDocument();
  });
});