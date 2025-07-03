# Material Design Dark/Light Mode Implementation

This document describes the implementation of Material Design dark/light mode functionality for the NIELIT O Level website.

## Features

### 🌙 Dark Mode
- **Surface Colors**: Dark backgrounds (#121212, #1e1e1e) for better contrast
- **Text Colors**: Light text (#ffffff, #b3b3b3) for readability
- **Primary Colors**: Adjusted blue tones (#90caf9, #42a5f5) for dark surfaces
- **Elevation**: Enhanced shadows for depth perception in dark environments

### ☀️ Light Mode
- **Surface Colors**: Light backgrounds (#ffffff, #f5f5f5) for clean appearance
- **Text Colors**: Dark text (#212121, #757575) for optimal readability
- **Primary Colors**: Standard Material Design blue (#1976d2, #1565c0)
- **Elevation**: Subtle shadows for depth

## Implementation Details

### CSS Custom Properties
The theme system uses CSS custom properties (variables) defined in `assets/css/style.css`:

```css
:root {
  /* Light Theme Variables */
  --md-primary: #1976d2;
  --md-surface: #ffffff;
  --md-background: #f4f6fa;
  --md-on-surface: #212121;
  /* ... more variables */
}

[data-theme="dark"] {
  /* Dark Theme Variables */
  --md-primary: #90caf9;
  --md-surface: #121212;
  --md-background: #0a0a0a;
  --md-on-surface: #ffffff;
  /* ... more variables */
}
```

### Theme Toggle Button
Located in the header (`_includes/header.html`):
- Material Design icons (light_mode/dark_mode)
- Smooth transitions between themes
- Ripple effect on click
- Responsive design

### JavaScript Theme Switcher
File: `assets/js/theme-switcher.js`

Features:
- **System Preference Detection**: Automatically detects OS theme preference
- **Local Storage Persistence**: Remembers user's theme choice
- **Smooth Transitions**: 300ms ease transitions for all theme changes
- **Ripple Effect**: Material Design ripple animation on theme toggle
- **Event System**: Custom events for other components to listen to theme changes

### Key Functions:
```javascript
// Toggle between light and dark themes
toggleTheme()

// Apply specific theme
applyTheme(theme)

// Get system preference
getSystemPreference()

// Store theme in localStorage
storeTheme(theme)
```

## Usage

### Automatic Theme Detection
The theme switcher automatically:
1. Checks for stored theme preference in localStorage
2. Falls back to system preference if no stored theme
3. Applies the appropriate theme on page load

### Manual Theme Switching
Users can click the theme toggle button in the header to switch between light and dark modes.

### System Theme Changes
If the user hasn't manually set a theme preference, the website will automatically follow system theme changes.

## Files Modified

### Core Theme Files
- `assets/css/style.css` - Main theme variables and styles
- `assets/css/pages.css` - Page-specific theme styles
- `assets/js/theme-switcher.js` - Theme switching logic
- `_includes/head.html` - Material Design icons and meta tags
- `_includes/header.html` - Theme toggle button
- `_layouts/default.html` - Theme switcher script inclusion

### Theme Variables Used
- `--md-primary` / `--md-primary-variant` - Primary brand colors
- `--md-surface` / `--md-surface-variant` - Card and component backgrounds
- `--md-background` / `--md-background-variant` - Page backgrounds
- `--md-on-surface` / `--md-on-surface-variant` - Text colors
- `--md-outline` / `--md-outline-variant` - Border colors
- `--md-elevation-1/2/3` - Shadow definitions
- `--md-hover` / `--md-focus` / `--md-selected` - Interactive states

## Browser Support

- **Modern Browsers**: Full support for CSS custom properties and theme switching
- **Fallback**: Light theme for older browsers that don't support CSS variables
- **Progressive Enhancement**: Theme functionality enhances the experience but doesn't break core functionality

## Accessibility

- **High Contrast**: Both themes meet WCAG contrast requirements
- **Keyboard Navigation**: Theme toggle is keyboard accessible
- **Screen Readers**: Proper ARIA labels and semantic markup
- **Reduced Motion**: Respects user's motion preferences

## Performance

- **CSS Variables**: Efficient theme switching without additional HTTP requests
- **Minimal JavaScript**: Lightweight theme switcher with no external dependencies
- **Optimized Transitions**: Hardware-accelerated CSS transitions
- **Local Storage**: Fast theme persistence without server requests

## Future Enhancements

Potential improvements for the theme system:
- **Custom Theme Colors**: Allow users to customize primary/secondary colors
- **Auto-switch by Time**: Automatically switch themes based on time of day
- **Theme Presets**: Additional theme options (high contrast, sepia, etc.)
- **Component-level Themes**: Individual components with their own theme overrides 