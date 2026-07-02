# HISD Design Tokens — React / CSS Reference

## CSS Custom Properties

```css
:root {
  /* Primary Brand */
  --hisd-teal: #00A3AF;
  --hisd-dark-grey: #24383C;
  --hisd-dark-green: #006F5B;
  --hisd-light-green: #6DB83D;

  /* Secondary */
  --hisd-yellow: #F9D04E;
  --hisd-purple: #474F99;
  --hisd-blue: #4975BD;
  --hisd-red: #D96364;
  --hisd-light-grey: #D4D4D5;
  --hisd-off-white: #FFFFED;

  /* 60% Tints (prior year / secondary series) */
  --hisd-teal-tint: #66C8CF;
  --hisd-dark-grey-tint: #7C888A;
  --hisd-dark-green-tint: #66A99D;
  --hisd-purple-tint: #9195C2;
  --hisd-blue-tint: #92ACD7;

  /* Semantic (status only — NOT decorative) */
  --hisd-good: #6DB83D;    /* white text */
  --hisd-bad: #D96364;     /* white text */
  --hisd-caution: #F9D04E; /* dark grey text */

  /* Backgrounds */
  --hisd-bg-page: #FBFBFB;
  --hisd-bg-card: #FFFFFF;
  --hisd-bg-header: #24383C;

  /* Text */
  --hisd-text-primary: #24383C;
  --hisd-text-secondary: #7C888A;
  --hisd-text-on-dark: #FFFFFF;
  --hisd-text-on-teal: #FFFFFF;
  --hisd-text-on-yellow: #24383C;

  /* Typography */
  --hisd-font: 'Radio Canada', Arial, sans-serif;
  --hisd-font-display: 'Parkin Sans', 'Arial Black', sans-serif;

  /* Borders */
  --hisd-border-color: #A7AFB1;
  --hisd-border-radius: 6px;
  --hisd-border-radius-lg: 10px;
}
```

## Data Series Color Priority

| Priority | Name | HEX | Use |
|---|---|---|---|
| P1 | Teal | #00A3AF | Primary / Current Year |
| P2 | Dark Green | #006F5B | Secondary series |
| P3 | Purple | #474F99 | Third series |
| P4 | Blue | #4975BD | Fourth series |
| P5 | Yellow | #F9D04E | Fifth series (dark text on top) |
| P6 | Teal Tint | #66C8CF | Prior year paired with P1 |
| P7 | Dark Grey Tint | #7C888A | Fallback |
| P8 | Dark Green Tint | #66A99D | Fallback |
| P9 | Purple Tint | #9195C2 | Fallback |
| P10 | Blue Tint | #92ACD7 | Fallback |

## Text Contrast Rules
- P1–P5 and semantic Good/Bad colors → **White** text labels
- P6–P10 and semantic Caution (Yellow) → **Dark Grey (#24383C)** text labels

## Component Patterns

### KPI Card
```jsx
<div style={{
  background: 'var(--hisd-bg-card)',
  borderRadius: 'var(--hisd-border-radius)',
  padding: '16px 20px',
  boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
  borderTop: '3px solid var(--hisd-teal)'
}}>
  <div style={{ fontSize: 12, color: 'var(--hisd-text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Metric Label</div>
  <div style={{ fontSize: 32, fontWeight: 700, color: 'var(--hisd-text-primary)', marginTop: 4 }}>94.2%</div>
  <div style={{ fontSize: 12, color: 'var(--hisd-good)' }}>▲ 0.8 pts vs. prior year</div>
</div>
```

### Status Badge
```jsx
const statusStyle = {
  Met:      { background: 'var(--hisd-good)',    color: '#fff' },
  'At Risk':{ background: 'var(--hisd-caution)', color: 'var(--hisd-text-primary)' },
  'Not Met':{ background: 'var(--hisd-bad)',     color: '#fff' },
};
<span style={{ ...statusStyle[status], padding: '2px 10px', borderRadius: 99, fontSize: 11, fontWeight: 600 }}>
  {status}
</span>
```

### Nav Header
```jsx
<header style={{
  background: 'var(--hisd-bg-header)',
  color: 'var(--hisd-text-on-dark)',
  padding: '0 24px',
  height: 52,
  display: 'flex',
  alignItems: 'center',
  gap: 24
}}>
  <span style={{ fontWeight: 700, fontSize: 18, color: 'var(--hisd-teal)', letterSpacing: '0.08em' }}>HISD</span>
  <span style={{ fontSize: 14, opacity: 0.7 }}>|</span>
  <span style={{ fontSize: 14 }}>Dashboard Title</span>
</header>
```

### Nav Button Bar
```jsx
<nav style={{ background: '#fff', borderBottom: '1px solid var(--hisd-border-color)', padding: '0 24px', display: 'flex', gap: 4 }}>
  {tabs.map(tab => (
    <button key={tab} onClick={() => setActive(tab)} style={{
      padding: '10px 16px',
      border: 'none',
      background: 'transparent',
      borderBottom: active === tab ? '3px solid var(--hisd-teal)' : '3px solid transparent',
      color: active === tab ? 'var(--hisd-teal)' : 'var(--hisd-text-primary)',
      fontWeight: active === tab ? 600 : 400,
      cursor: 'pointer',
      fontSize: 13
    }}>{tab}</button>
  ))}
</nav>
```
