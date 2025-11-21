# Contributing to Napkin

Thank you for your interest in contributing to Napkin! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Napkin.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Using Docker (Recommended)

```bash
docker-compose up -d
```

### Manual Setup

1. **Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

2. **Frontend**:
```bash
cd frontend
npm install
npm run serve
```

## Code Style

### Python (Backend)
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions focused and small

### JavaScript/Vue (Frontend)
- Use ES6+ syntax
- Follow Vue.js style guide
- Use meaningful component and variable names
- Keep components focused and reusable

## Testing

### Backend Tests
```bash
cd backend
python test_app.py  # Unit tests
python test_api.py  # API integration tests (requires running server)
```

### Frontend Tests
Frontend tests are currently minimal. Contributions to improve test coverage are welcome!

## Making Changes

### Backend Changes
- Add new endpoints in `backend/app.py`
- Update database schema in the `init_db()` function
- Test API endpoints with `test_api.py`

### Frontend Changes
- Create new components in `frontend/src/components/`
- Update routes in `frontend/src/main.js`
- Test UI changes manually in the browser

## Submitting Pull Requests

1. Ensure your code follows the style guidelines
2. Test your changes thoroughly
3. Update documentation if needed
4. Write a clear PR description explaining:
   - What changes you made
   - Why you made them
   - How to test the changes

## Reporting Issues

When reporting issues, please include:
- A clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, versions)

## Feature Requests

Feature requests are welcome! Please open an issue with:
- A clear description of the feature
- Use cases
- How it would benefit users
- Any implementation ideas

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Questions?

If you have questions, feel free to:
- Open an issue
- Start a discussion
- Reach out to the maintainers

Thank you for contributing to Napkin! 🎉
