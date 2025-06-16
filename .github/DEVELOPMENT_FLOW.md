# Development Flow Setup Guide

This guide will help you configure GitHub to use the recommended development
flow for this project.

## 🌟 Overview

**Recommended Development Flow:**

1. **Feature Development** → Feature branches (`feature/feature-name`)
2. **Testing** → Merge to `develop` branch (triggers TestPyPI upload)
3. **Validation** → Test package from TestPyPI
4. **Production Release** → Create GitHub release from `main` (triggers PyPI upload)

## 🔧 Branch Structure

- **`main`** - Production-ready code, protected branch
- **`develop`** - Integration branch for testing, triggers TestPyPI uploads
- **`feature/*`** - Feature development branches

## ⚙️ GitHub Repository Setup

### Step 1: Configure Branch Protection Rules

Go to your repository **Settings** → **Branches** and set up these protection rules:

#### For `main` branch

```text
✅ Require a pull request before merging
✅ Require approvals (1 approval minimum)
✅ Dismiss stale PR approvals when new commits are pushed
✅ Require status checks to pass before merging
   - Select: CI / test (ubuntu-latest, 3.9) [or your preferred test matrix]
✅ Require branches to be up to date before merging
✅ Require conversation resolution before merging
✅ Restrict pushes that create files larger than 100 MB
```

#### For `develop` branch

```text
✅ Require a pull request before merging
✅ Require status checks to pass before merging
   - Select: CI / test (ubuntu-latest, 3.9)
✅ Require branches to be up to date before merging
✅ Restrict pushes that create files larger than 100 MB
```

### Step 2: Set Default Branch

1. Go to **Settings** → **General**
2. Under **Default branch**, set it to `develop`
3. This makes new PRs target `develop` by default

### Step 3: Configure Repository Secrets

Go to **Settings** → **Secrets and variables** → **Actions**:

Add these repository secrets:

- **`PYPI_API_TOKEN`** - Your PyPI production token
- **`TEST_PYPI_API_TOKEN`** - Your TestPyPI testing token

### Step 4: Set Up Branch Naming Convention

Configure automatic branch naming in your Git client or IDE:

- **Features**: `feature/description` (e.g., `feature/add-new-loader`)
- **Bugfixes**: `bugfix/description` (e.g., `bugfix/fix-image-scaling`)
- **Hotfixes**: `hotfix/description` (e.g., `hotfix/critical-security-fix`)

## 🚀 Development Workflow

### For New Features

1. **Create Feature Branch**:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Develop Your Feature**:

   ```bash
   # Make your changes
   git add .
   git commit -m "Add new feature: description"
   git push -u origin feature/your-feature-name
   ```

3. **Create Pull Request**:
   - **Target**: `develop` branch
   - **Title**: Clear description of the feature
   - **Description**: What the feature does, how to test it

4. **After PR Approval**:
   - Merge to `develop`
   - **TestPyPI workflow automatically runs**
   - Test the uploaded package from TestPyPI

### For Releases

1. **Create Release PR**:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b release/v1.0.1
   git merge develop
   ```

2. **Update Version**:
   - Update version in `pyproject.toml`
   - Update `CHANGELOG.md` if you have one
   - Commit changes

3. **Create PR to Main**:
   - **Target**: `main` branch
   - **Title**: "Release v1.0.1"
   - **Description**: Release notes

4. **Create GitHub Release**:
   - After merging to `main`
   - Go to **Releases** → **Create a new release**
   - **Tag**: `v1.0.1` (create new tag)
   - **Target**: `main` branch
   - **Title**: "Release v1.0.1"
   - **Description**: Release notes
   - **Publish release** → **PyPI workflow automatically runs**

### For Hotfixes

1. **Create Hotfix Branch from Main**:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-fix
   ```

2. **Fix and Test**:

   ```bash
   # Make your fix
   git add .
   git commit -m "Fix critical issue: description"
   git push -u origin hotfix/critical-fix
   ```

3. **Create PRs to Both Branches**:
   - PR to `main` for immediate release
   - PR to `develop` to keep branches in sync

## 🔄 Automated Workflows

### TestPyPI Workflow (test-pypi.yml)

**Triggers on**:

- Push to `develop` branch
- Manual trigger via Actions UI

**What it does**:

- Creates test version with timestamp
- Uploads to TestPyPI for testing
- Validates package installation

### Production PyPI Workflow (release.yml)

**Triggers on**:

- GitHub release creation

**What it does**:

- Uses exact version from `pyproject.toml`
- Uploads to production PyPI
- Creates release assets

### CI Workflow (ci.yml)

**Triggers on**:

- Push to `main` or `develop`
- Pull requests to `main`

**What it does**:

- Runs tests across multiple Python versions
- Validates code quality
- Ensures package can be imported

## 📋 Quick Reference Commands

### Starting New Feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-new-feature
# ... make changes ...
git add .
git commit -m "Add my new feature"
git push -u origin feature/my-new-feature
# Create PR to develop via GitHub UI
```

### Testing from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  gui-image-studio==1.0.0.dev20241201123456
```

### Creating Release

```bash
git checkout main
git pull origin main
git merge develop
# Update version in pyproject.toml
git add pyproject.toml
git commit -m "Bump version to 1.0.1"
git push origin main
# Create GitHub release via UI
```

## 🛡️ Security Best Practices

1. **Never commit secrets** to any branch
2. **Use repository secrets** for API tokens
3. **Require PR reviews** for main branch
4. **Test thoroughly** on develop before releasing
5. **Use semantic versioning** for releases

## 🎯 Benefits of This Flow

- ✅ **Safe releases** - All code tested before production
- ✅ **Automated testing** - TestPyPI validates packages
- ✅ **Code quality** - PR reviews and CI checks
- ✅ **Easy rollbacks** - Clear version history
- ✅ **Parallel development** - Multiple features can be developed simultaneously

## 🔧 Troubleshooting

### Common Issues

1. **PR blocked by status checks**:
   - Wait for CI to complete
   - Fix any failing tests
   - Ensure branch is up to date

2. **TestPyPI upload fails**:
   - Check if `TEST_PYPI_API_TOKEN` is configured
   - Verify token permissions

3. **PyPI upload fails**:
   - Check if `PYPI_API_TOKEN` is configured
   - Ensure version number is incremented
   - Verify package builds successfully

4. **Merge conflicts**:

   ```bash
   git checkout your-branch
   git pull origin develop
   # Resolve conflicts
   git add .
   git commit -m "Resolve merge conflicts"
   git push origin your-branch
   ```

This development flow ensures high code quality, thorough testing, and safe
releases! 🚀
