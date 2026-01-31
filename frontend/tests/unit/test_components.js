import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Navbar from '../../src/components/Navbar';
import PersonalizationButton from '../../src/components/PersonalizationButton';
import Module1 from '../../src/chapters/Module1';
import Module2 from '../../src/chapters/Module2';
import Module3 from '../../src/chapters/Module3';
import Module4 from '../../src/chapters/Module4';

describe('Navbar Component', () => {
  test('renders navbar with logo and menu items', () => {
    render(<Navbar />);

    const logoElement = screen.getByText(/Physical AI & Humanoid Robotics/i);
    expect(logoElement).toBeInTheDocument();

    const homeLink = screen.getByText(/Home/i);
    expect(homeLink).toBeInTheDocument();

    const aboutLink = screen.getByText(/About/i);
    expect(aboutLink).toBeInTheDocument();
  });

  test('navbar links are clickable', () => {
    render(<Navbar />);

    const homeLink = screen.getByText(/Home/i);
    fireEvent.click(homeLink);

    const aboutLink = screen.getByText(/About/i);
    fireEvent.click(aboutLink);

    // These clicks shouldn't throw errors
    expect(homeLink).toBeInTheDocument();
    expect(aboutLink).toBeInTheDocument();
  });
});

describe('PersonalizationButton Component', () => {
  test('renders personalization button', () => {
    const mockSetShowPersonalization = jest.fn();
    render(
      <PersonalizationButton
        showPersonalization={false}
        setShowPersonalization={mockSetShowPersonalization}
      />
    );

    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent(/Personalize/i);
  });

  test('button text changes when clicked', () => {
    const mockSetShowPersonalization = jest.fn();
    const { rerender } = render(
      <PersonalizationButton
        showPersonalization={false}
        setShowPersonalization={mockSetShowPersonalization}
      />
    );

    const button = screen.getByRole('button');
    fireEvent.click(button);

    // Re-render with updated props to simulate state change
    rerender(
      <PersonalizationButton
        showPersonalization={true}
        setShowPersonalization={mockSetShowPersonalization}
      />
    );

    const updatedButton = screen.getByRole('button');
    expect(updatedButton).toHaveTextContent(/Personalized/i);
  });
});


describe('Module Components', () => {
  test('Module1 renders correctly', () => {
    render(<Module1 isUrduEnabled={false} />);

    const titleElement = screen.getByText(/Module 1: ROS 2 Fundamentals/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('Module2 renders correctly', () => {
    render(<Module2 isUrduEnabled={false} />);

    const titleElement = screen.getByText(/Module 2: Digital Twin Technology/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('Module3 renders correctly', () => {
    render(<Module3 isUrduEnabled={false} />);

    const titleElement = screen.getByText(/Module 3: NVIDIA Isaac Platform/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('Module4 renders correctly', () => {
    render(<Module4 isUrduEnabled={false} />);

    const titleElement = screen.getByText(/Module 4: Vision-Language-Action Models/i);
    expect(titleElement).toBeInTheDocument();
  });

});