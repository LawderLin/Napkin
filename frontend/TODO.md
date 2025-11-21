# Frontend TODO / Future Improvements

## User Experience

### Replace alert() with Toast Notifications
Currently using browser `alert()` for user feedback. Consider implementing a toast notification system:

**Options:**
1. **Vue Toastification**: Popular Vue 3 toast library
   ```bash
   npm install vue-toastification@next
   ```

2. **Custom Toast Component**: Lightweight custom solution
   - Create a `Toast.vue` component
   - Use Vuex or provide/inject for global state
   - Animate with CSS transitions

**Benefits:**
- Better user experience
- Non-blocking notifications
- Can show multiple notifications
- Customizable styling and positioning

**Example Implementation:**
```javascript
// main.js
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

app.use(Toast, {
  position: "top-right",
  timeout: 3000
});

// In components
this.$toast.success("Link copied to clipboard!");
this.$toast.error("Failed to copy link");
```

## Security Enhancements

### Input Validation
- Add client-side content length validation
- Implement content sanitization for XSS prevention
- Add CAPTCHA for bot prevention

### Rate Limiting Display
- Show remaining API calls to user
- Display rate limit warnings

## Feature Enhancements

### Editor Improvements
1. **Markdown Preview Toggle**: Real-time preview while editing
2. **Syntax Highlighting**: Code block syntax highlighting in editor
3. **Toolbar**: Quick markdown formatting buttons
4. **Auto-save**: Save draft to localStorage

### Note Management
1. **Copy Link Button**: Dedicated button with visual feedback
2. **QR Code**: Generate QR code for easy mobile sharing
3. **Download**: Export note as .md or .txt file
4. **Print**: Print-friendly view

### Accessibility
1. **Keyboard Shortcuts**: Add keyboard navigation
2. **ARIA Labels**: Improve screen reader support
3. **Focus Management**: Better focus indicators
4. **Color Contrast**: Ensure WCAG compliance

## Performance

### Code Splitting
- Lazy load components
- Split vendor bundles
- Implement route-based code splitting

### Caching
- Implement service worker for offline support
- Cache static assets
- Add PWA support

## Testing

### Unit Tests
- Add Vitest or Jest for component testing
- Test form validation
- Test clipboard functionality
- Test markdown rendering

### E2E Tests
- Add Cypress or Playwright for end-to-end testing
- Test note creation flow
- Test password protection
- Test expiry functionality

## Build Optimization

### Production Build
- Minimize bundle size
- Optimize images
- Tree-shake unused code
- Enable gzip compression

## Internationalization (i18n)

### Multi-language Support
- Add vue-i18n
- Support English, Spanish, French, Chinese, etc.
- Localize date/time formats
- RTL support for Arabic, Hebrew

## Analytics (Optional)

### Privacy-Respecting Analytics
- Add Plausible or Matomo
- Track note creation rates
- Monitor error rates
- No user tracking, only aggregate data

## Implementation Priority

**High Priority:**
1. Toast notifications
2. Input validation
3. Accessibility improvements

**Medium Priority:**
1. Editor toolbar
2. Markdown preview
3. Unit tests

**Low Priority:**
1. i18n support
2. PWA features
3. Analytics

## Notes

- Maintain minimal dependencies
- Keep bundle size small
- Prioritize user privacy
- Ensure mobile responsiveness
