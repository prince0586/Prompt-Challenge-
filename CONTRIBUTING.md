# Contributing to AgriTrade Pro

Thank you for your interest in contributing to AgriTrade Pro! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, browser)
   - Screenshots if applicable

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Describe the feature** clearly and concisely
3. **Explain the use case** and benefits
4. **Consider implementation complexity**
5. **Be open to discussion** and feedback

### Contributing Code

#### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/agritrade-pro.git
   cd agritrade-pro
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

##### Code Style
- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

##### Code Formatting
```bash
# Format code with black
black src/ tests/ *.py

# Check style with flake8
flake8 src/ tests/ *.py

# Type checking with mypy
mypy src/
```

##### Testing
- Write tests for new features
- Maintain or improve test coverage
- Run tests before submitting PR
```bash
pytest tests/
pytest --cov=src tests/  # With coverage
```

##### Documentation
- Update README.md for new features
- Add docstrings to new functions/classes
- Update configuration documentation
- Include examples where helpful

#### Commit Guidelines

##### Commit Message Format
```
type(scope): brief description

Detailed explanation if needed

Fixes #issue-number
```

##### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

##### Examples
```
feat(ui): add market trends visualization

Add comprehensive market trends display with real-time data,
interactive charts, and filtering capabilities.

Fixes #123
```

```
fix(voice): resolve audio processing timeout

Increase timeout for voice processing to handle longer
audio clips and improve error handling.

Fixes #456
```

#### Pull Request Process

1. **Update documentation** as needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** if applicable
5. **Create pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
   - Testing instructions

##### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Screenshots
If applicable, add screenshots

## Related Issues
Fixes #issue-number
```

## Development Setup

### Environment Variables
Copy `.env.template` to `.env` and configure:
```bash
GEMINI_API_KEY=your_api_key_here
ENVIRONMENT=development
DEBUG=true
```

### Database Setup
The application uses SQLite for development:
- Database file: `data/mandi_setu.db`
- Automatically created on first run
- No additional setup required

### Running the Application
```bash
streamlit run app.py
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src

# Specific test file
pytest tests/test_specific.py

# With verbose output
pytest -v
```

## Project Structure

```
agritrade-pro/
├── app.py                    # Main application entry point
├── config/                   # Configuration management
├── src/mandi_setu/          # Main application code
│   ├── models/              # Data models
│   ├── ui/                  # User interface components
│   └── theme/               # Styling and themes
├── tests/                   # Test files
├── data/                    # Database files
└── docs/                    # Documentation
```

## Coding Standards

### Python Code
- Use Python 3.8+ features
- Follow PEP 8 style guide
- Add type hints for function parameters and return values
- Write comprehensive docstrings
- Handle exceptions appropriately
- Use logging instead of print statements

### UI Components
- Keep components small and focused
- Use consistent styling patterns
- Ensure accessibility compliance
- Test on different screen sizes
- Follow responsive design principles

### Database
- Use proper data validation
- Handle database errors gracefully
- Write efficient queries
- Maintain data consistency
- Document schema changes

## Testing Guidelines

### Test Types
- **Unit tests**: Test individual functions/classes
- **Integration tests**: Test component interactions
- **UI tests**: Test user interface behavior
- **Performance tests**: Test application performance

### Test Structure
```python
def test_function_name():
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

### Test Coverage
- Aim for >80% code coverage
- Focus on critical business logic
- Test error conditions
- Test edge cases

## Documentation

### Code Documentation
- Write clear docstrings for all public functions
- Include parameter types and descriptions
- Provide usage examples
- Document exceptions that may be raised

### User Documentation
- Keep README.md up to date
- Provide clear installation instructions
- Include usage examples
- Document configuration options

## Release Process

### Version Numbering
We follow Semantic Versioning (SemVer):
- MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] Update version number
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release in Git

## Getting Help

### Resources
- **Documentation**: Check README.md and inline docs
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: Request review from maintainers

### Contact
- Create GitHub issue for bugs/features
- Use GitHub Discussions for general questions
- Tag maintainers for urgent issues

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- GitHub contributor statistics

Thank you for contributing to AgriTrade Pro and helping improve agricultural trading in India!