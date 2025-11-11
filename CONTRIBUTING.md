# Contributing to Codessian Cortex

Thank you for your interest in contributing to Codessian Cortex! This document provides guidelines and instructions for contributing to the project.

## 🎯 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect different viewpoints and experiences
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- A GitHub account
- Git installed on your machine
- Basic knowledge of the technologies used in this project
- Understanding of the project's architecture and coding standards

### Development Environment Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/codessian-cortex.git
   cd codessian-cortex
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/original-org/codessian-cortex.git
   ```

3. **Set up development environment**
   ```bash
   # Install dependencies
   npm install
   pip install -r requirements.txt
   go mod download
   
   # Install pre-commit hooks
   pre-commit install
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Contribution Process

### 1. Finding Issues to Work On

- Check the [Issues](https://github.com/your-org/codessian-cortex/issues) tab
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to express your interest
- Wait for confirmation before starting work

### 2. Making Changes

#### Code Style Guidelines

Follow the established coding standards for each language:

**JavaScript/TypeScript:**
- Use ESLint configuration provided
- Follow the existing code patterns
- Use meaningful variable and function names
- Add JSDoc comments for public functions

**Python:**
- Follow PEP 8 style guide
- Use Black formatter with 88-character line length
- Add docstrings for functions and classes
- Use type hints where appropriate

**Go:**
- Follow Go formatting standards (gofmt)
- Use meaningful package and function names
- Add comprehensive godoc comments
- Follow error handling best practices

#### General Guidelines

- Write clean, readable, and maintainable code
- Follow the existing code structure and patterns
- Add appropriate comments for complex logic
- Ensure your code is well-tested
- Update documentation as needed

### 3. Testing Your Changes

**Unit Tests:**
```bash
# Run unit tests
npm run test:unit
python -m pytest tests/unit/
go test ./src/core/...
```

**Integration Tests:**
```bash
# Run integration tests
npm run test:integration
python -m pytest tests/integration/
go test ./tests/integration/...
```

**End-to-End Tests:**
```bash
# Run E2E tests
npm run test:e2e
```

**Code Quality Checks:**
```bash
# Run linting
npm run lint
python -m flake8 src/
golangci-lint run

# Run formatting checks
npm run format:check
python -m black --check src/
gofmt -l .
```

### 4. Committing Your Changes

#### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `chore`: Build process or auxiliary tool changes

**Examples:**
```
feat(api): add user authentication endpoint
fix(core): resolve memory leak in data processor
docs(readme): update installation instructions
test(services): add unit tests for payment service
```

#### Commit Process

1. **Stage your changes**
   ```bash
   git add .
   ```

2. **Commit with proper message**
   ```bash
   git commit -m "feat(api): add user authentication endpoint"
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

### 5. Submitting a Pull Request

1. **Create Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select the target branch (usually `main` or `develop`)
   - Fill out the PR template completely

2. **PR Template**
   ```markdown
   ## Description
   Brief description of the changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] Tests added/updated
   ```

3. **Address Review Feedback**
   - Respond to reviewer comments promptly
   - Make requested changes
   - Push additional commits if needed
   - Request re-review when ready

## 🧪 Testing Guidelines

### Test Coverage Requirements

- Maintain minimum 80% code coverage
- Write tests for all new features
- Update tests for modified functionality
- Include both positive and negative test cases

### Test Organization

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── e2e/           # End-to-end tests
```

### Writing Good Tests

- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Test edge cases and error conditions
- Mock external dependencies appropriately
- Keep tests independent and isolated

## 📚 Documentation

### Code Documentation

- Add docstrings to functions and classes
- Include parameter and return value descriptions
- Provide usage examples for complex functions
- Update README files when adding new features

### API Documentation

- Update OpenAPI specifications
- Include request/response examples
- Document error codes and messages
- Keep API documentation in sync with code

## 🔒 Security Guidelines

- Never commit secrets or credentials
- Use environment variables for sensitive data
- Follow secure coding practices
- Report security issues privately
- Keep dependencies updated

## 🐛 Bug Reports

When reporting bugs, include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, browser, versions)
- Error messages and stack traces
- Screenshots if applicable

## 💡 Feature Requests

When suggesting features, provide:

- Clear description of the feature
- Use cases and benefits
- Proposed implementation approach
- Acceptance criteria
- Priority level
- Effort estimation

## 🏷️ Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or improvement
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority:high`: High priority issues
- `priority:low`: Low priority issues

## 🔄 Release Process

1. **Version Numbering**
   - Follow [Semantic Versioning](https://semver.org/)
   - Format: `MAJOR.MINOR.PATCH`

2. **Release Notes**
   - Document all changes
   - Include breaking changes
   - List new features and bug fixes
   - Provide upgrade instructions

## 📞 Getting Help

- **Documentation**: Check existing docs first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions
- **Community**: Join our community channels
- **Maintainers**: Contact maintainers for complex issues

## 🏆 Recognition

Contributors are recognized in:

- README.md contributors section
- Release notes
- Special mentions in community updates
- Contributor badges/profiles

## 📋 Checklist for Contributors

Before submitting your contribution:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No breaking changes (or properly documented)
- [ ] Commit messages follow conventions
- [ ] PR template filled out completely
- [ ] Self-review completed
- [ ] No sensitive data in commits

## 🎉 Thank You!

Your contributions make Codessian Cortex better for everyone. We appreciate your time and effort in helping improve this project!

---

*Happy contributing! 🚀*