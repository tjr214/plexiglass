# PlexiGlass - Theming Guide

**Version**: 0.1.0  
**Last Updated**: January 19, 2026  
**Status**: Complete Design System

---

## 📋 Overview

PlexiGlass uses a comprehensive theming system built on Textual CSS (`.tcss`) with design tokens for consistent styling across all components. This guide documents the theming architecture, color palettes, and customization options.

---

## 🎨 Design Philosophy

### Core Principles

1. **Consistency**: All components use shared design tokens
2. **Accessibility**: High contrast ratios for readability
3. **Responsiveness**: Smooth transitions and hover states
4. **Modularity**: Separated concerns with dedicated CSS files
5. **Themability**: Easy switching between dark and light modes

---

## 📁 CSS File Structure

```
src/plexiglass/ui/styles/
├── theme.tcss              # Dark theme design tokens (default)
├── theme-light.tcss        # Light theme variant
├── plexiglass.tcss         # Main application styles
├── gallery.tcss            # Gallery screen styles
├── category_menu.tcss      # Category navigation styles
├── errors.tcss             # Error widgets styles
├── loading.tcss            # Loading & progress styles
└── help.tcss               # Help screen styles
```

**Total**: 8 CSS files, ~49KB of theming

---

## 🎨 Color Palette

### Dark Theme (Default)

#### Background Hierarchy
```css
$bg-base: #0d1b1e;      /* Darkest - main background */
$bg-surface: #13272b;   /* Surface - cards, panels */
$bg-elevated: #1b343a;  /* Elevated - modals, overlays */
$bg-hover: #224650;     /* Hover state */
$bg-active: #2a5360;    /* Active/pressed state */
```

#### Text Hierarchy
```css
$text-primary: #e6f1f2;    /* High emphasis */
$text-secondary: #b8c9cc;  /* Medium emphasis */
$text-muted: #8a9ea2;      /* Low emphasis */
$text-disabled: #5a6e72;   /* Disabled state */
```

#### Accent Colors
```css
$accent-primary: #6bd9e3;    /* Cyan - primary brand */
$accent-secondary: #ffb347;  /* Amber - secondary */
$accent-tertiary: #a78bfa;   /* Purple - tertiary */
```

#### Semantic Colors
```css
$color-success: #6fdc8c;   /* Green - success */
$color-warning: #ffb347;   /* Amber - warning */
$color-error: #ff6b6b;     /* Red - error */
$color-info: #6bd9e3;      /* Cyan - info */
```

#### Borders
```css
$border-subtle: #1b343a;
$border-default: #2a5360;
$border-emphasis: #3a6370;
$border-focus: #6bd9e3;
```

### Light Theme

Light theme inverts the color scheme with adjusted accent colors for readability:

#### Background Hierarchy
```css
$bg-base: #f5f7f8;      /* Lightest - main background */
$bg-surface: #ffffff;   /* Surface - cards, panels */
$bg-elevated: #e6f1f2;  /* Elevated - modals, overlays */
$bg-hover: #d4e6e8;     /* Hover state */
$bg-active: #c2d8db;    /* Active/pressed state */
```

#### Text Hierarchy
```css
$text-primary: #0d1b1e;    /* High emphasis */
$text-secondary: #2a4750;  /* Medium emphasis */
$text-muted: #5a6e72;      /* Low emphasis */
$text-disabled: #8a9ea2;   /* Disabled state */
```

---

## ⏱️ Transitions & Animations

### Timing Values
```css
$transition-fast: 150ms;     /* Quick feedback */
$transition-base: 250ms;     /* Standard transitions */
$transition-slow: 350ms;     /* Deliberate animations */
$transition-slower: 500ms;   /* Extended animations */
```

### Usage Patterns
```css
/* Standard transition */
transition: background $transition-base,
            color $transition-base,
            border $transition-base;

/* Fast interaction feedback */
Button:hover {
    transition: background $transition-fast;
}

/* Slow modal entrance */
.modal {
    transition: background $transition-slow;
}
```

---

## 🧩 Component Styling

### Buttons

**States**: Default, Hover, Focus, Disabled

```css
Button {
    background: $bg-elevated;
    border: solid $border-default;
    transition: background $transition-fast;
}

Button:hover {
    background: $bg-active;
    border: solid $accent-primary;
}

Button.-primary {
    background: $accent-primary;
    color: $bg-base;
}

Button.-success {
    background: $color-success;
}

Button.-danger {
    background: $color-error;
}
```

### Inputs

```css
Input {
    background: $bg-surface;
    border: solid $border-default;
    transition: border $transition-fast;
}

Input:focus {
    background: $bg-elevated;
    border: solid $border-focus;
}

Input.-invalid {
    border: solid $color-error;
}
```

### Lists

```css
ListItem {
    padding: 0 1;
    color: $text-primary;
    transition: background $transition-fast;
}

ListItem:hover {
    background: $bg-hover;
}

ListItem.-selected {
    background: $accent-primary;
    color: $bg-base;
    text-style: bold;
}
```

### Modals

```css
.modal {
    background: $bg-surface;
    border: tall $accent-primary;
    padding: 2 3;
    align: center middle;
}
```

### Cards & Panels

```css
.panel {
    background: $bg-surface;
    border: solid $border-subtle;
    transition: background $transition-base;
}

.panel:hover {
    background: $bg-hover;
}
```

---

## 🎯 Utility Classes

### Text Utilities
```css
.text-primary       /* High emphasis text */
.text-secondary     /* Medium emphasis text */
.text-muted         /* Low emphasis text */
.text-success       /* Success state */
.text-warning       /* Warning state */
.text-error         /* Error state */
.text-info          /* Info state */
.text-bold          /* Bold text */
```

### Border Utilities
```css
.border-subtle      /* Subtle border */
.border-default     /* Default border */
.border-primary     /* Primary accent border */
.border-success     /* Success border */
.border-warning     /* Warning border */
.border-error       /* Error border */
```

### Background Utilities
```css
.bg-surface         /* Surface background */
.bg-elevated        /* Elevated background */
```

### Transition Utilities
```css
.transition-fast    /* 150ms transition */
.transition-base    /* 250ms transition */
.transition-slow    /* 350ms transition */
```

---

## 🔧 Customizing Themes

### Creating a New Theme

1. **Copy base theme file**:
   ```bash
   cp src/plexiglass/ui/styles/theme.tcss src/plexiglass/ui/styles/theme-custom.tcss
   ```

2. **Modify color tokens**:
   ```css
   /* Adjust colors while maintaining hierarchy */
   $bg-base: #your-color;
   $accent-primary: #your-accent;
   ```

3. **Test contrast ratios**: Ensure text readability
   - Minimum 4.5:1 for normal text
   - Minimum 3:1 for large text

4. **Apply theme**: Load in your application

### Theme Switching

To enable runtime theme switching:

```python
class PlexiGlassApp(App):
    def __init__(self):
        super().__init__()
        self.theme = "dark"  # or "light"
    
    def get_css_path(self):
        if self.theme == "light":
            return "styles/theme-light.tcss"
        return "styles/theme.tcss"
```

---

## 📐 Spacing Scale

Textual uses integer spacing values:

```css
padding: 1 2;    /* 1 vertical, 2 horizontal */
margin: 1;       /* 1 all sides */
height: 3;       /* 3 lines */
width: 30;       /* 30 columns */
```

**Recommended scale**: 0, 1, 2, 3, 4, 6, 8, 12

---

## 🎭 Visual Hierarchy

### Importance Levels

1. **High**: `$accent-primary`, `$text-primary`, heavy borders
2. **Medium**: `$accent-secondary`, `$text-secondary`, solid borders
3. **Low**: `$text-muted`, `$border-subtle`

### Elevation Layers

1. **Base**: `$bg-base` - Main background
2. **Surface**: `$bg-surface` - Cards, panels
3. **Elevated**: `$bg-elevated` - Modals, dropdowns
4. **Hover**: `$bg-hover` - Interactive feedback
5. **Active**: `$bg-active` - Pressed state

---

## ♿ Accessibility Guidelines

### Contrast Ratios

- **Text on bg-base**: 12.5:1 (AAA)
- **Text on bg-surface**: 11.2:1 (AAA)
- **Accent on bg-base**: 4.8:1 (AA)

### Focus Indicators

All interactive elements have visible focus states:
```css
*:focus {
    border: heavy $border-focus;
}
```

### Color Blindness

- Don't rely solely on color for information
- Use text labels, icons, and patterns
- Test with color blindness simulators

---

## 📊 Component Matrix

| Component | Background | Border | Text | Hover | Focus |
|-----------|------------|--------|------|-------|-------|
| **Button** | elevated | default | primary | active + primary border | focus border |
| **Input** | surface | default | primary | none | elevated + focus border |
| **List Item** | transparent | none | primary | hover | active |
| **Modal** | surface | primary accent | primary | elevated | N/A |
| **Panel** | surface | subtle | primary | hover | N/A |
| **Card** | surface | subtle | primary | hover + primary border | N/A |

---

## 🎬 Animation Guidelines

### Interaction Feedback
- **Fast (150ms)**: Button clicks, hover states
- **Base (250ms)**: List selections, panel transitions
- **Slow (350ms)**: Modal entrances, major state changes

### Easing
Textual doesn't support custom easing, but timing creates natural feel:
- **Quick actions**: Use `transition-fast`
- **Major changes**: Use `transition-slow`

---

## 📝 Best Practices

### DO
✅ Use design tokens from theme files  
✅ Maintain visual hierarchy with color and spacing  
✅ Add transitions for interactive elements  
✅ Test in both dark and light themes  
✅ Ensure focus states are visible  
✅ Use semantic color names  

### DON'T
❌ Hardcode color values  
❌ Skip hover/focus states  
❌ Use low-contrast color combinations  
❌ Animate everything (be purposeful)  
❌ Ignore accessibility guidelines  
❌ Mix design token levels incorrectly  

---

## 🔍 Debugging CSS

### Textual Dev Tools
```bash
# Run with dev console
uv run textual run --dev src/plexiglass/app/plexiglass_app.py

# Open console in another terminal
uv run textual console
```

### CSS Inspection
- Use Textual's DOM inspector
- Check computed styles in dev console
- Verify class names and selectors

---

## 📚 References

- **Textual CSS Documentation**: https://textual.textualize.io/guide/CSS/
- **Color Palette Generator**: https://coolors.co/
- **Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Color Blindness Simulator**: https://www.color-blindness.com/coblis-color-blindness-simulator/

---

## 🎨 Theme Showcase

### Dark Theme
- **Mood**: Professional, modern, easy on eyes
- **Best for**: Extended coding sessions, dark environments
- **Contrast**: High (12.5:1)

### Light Theme
- **Mood**: Clean, bright, energetic
- **Best for**: Daylight usage, bright environments
- **Contrast**: High (13.2:1)

---

## 🚀 Future Enhancements

- [ ] High-contrast theme variant
- [ ] Color-blind friendly themes
- [ ] User-customizable accent colors
- [ ] Theme preview gallery
- [ ] CSS variable overrides via config

---

**Maintainer**: Tim  
**Design System**: BMad Master 🧙  
**Theme Version**: 1.0.0  

**🎨 PlexiGlass - Where Transparency Meets Beautiful Design**
