# GitHub Pages Setup Guide

This guide helps you set up GitHub Pages for GUI Image Studio documentation.

## Quick Setup Checklist

- [ ] Repository Settings → Pages → Source: "GitHub Actions"
- [ ] Repository Settings → Actions → General → Workflow permissions: "Read and write"
- [ ] Push workflows to main branch
- [ ] Wait for "Documentation" workflow to complete
- [ ] Verify site is live at `https://yourusername.github.io/gui-image-studio/`

## Detailed Setup Steps

### 1. Configure Repository Settings

1. **Go to your repository on GitHub**
2. **Click "Settings" tab**
3. **Navigate to "Pages" in the left sidebar**
4. **Set Source to "GitHub Actions"** (not "Deploy from a branch")

### 2. Set Workflow Permissions

1. **In Settings, go to "Actions" → "General"**
2. **Under "Workflow permissions", select:**
   - ✅ "Read and write permissions"
   - ✅ "Allow GitHub Actions to create and approve pull requests"

### 3. Deploy Documentation

```bash
# Commit and push the documentation system
git add .github/workflows/ docs/ scripts/
git commit -m "Add documentation system with GitHub Pages"
git push origin main
```

### 4. Monitor Deployment

1. **Go to "Actions" tab in your repository**
2. **Watch the "Documentation" workflow run**
3. **Wait for successful completion (green checkmark)**

### 5. Verify Deployment

```bash
# Use the verification script
pip install requests
python scripts/verify-pages.py https://yourusername.github.io/gui-image-studio/
```

## Troubleshooting

### Issue: "Pages" section not visible in Settings

**Solution:**
- Ensure your repository is public, or you have GitHub Pro/Team
- Check that you have admin permissions on the repository

### Issue: Workflow fails with permission errors

**Solution:**
```yaml
# Verify these permissions are set in .github/workflows/docs.yml
permissions:
  contents: read
  pages: write
  id-token: write
```

**Also check:**
- Repository Settings → Actions → General → Workflow permissions: "Read and write"

### Issue: Documentation builds but doesn't deploy

**Symptoms:**
- Build job succeeds
- Deploy job fails or doesn't run

**Solutions:**
1. **Check branch name**: Deployment only happens on `main` branch
2. **Verify Pages source**: Must be set to "GitHub Actions"
3. **Check workflow file**: Ensure deploy job has correct conditions

### Issue: 404 errors on GitHub Pages

**Symptoms:**
- Main page loads but subpages return 404
- Links are broken

**Solutions:**
1. **Check file structure**: Ensure HTML files are in `docs/_build/html/`
2. **Verify build output**: Check Actions logs for build warnings
3. **Test locally**: Run `python scripts/build-docs.py build` and check output

### Issue: Documentation is outdated

**Symptoms:**
- Changes to docs/ don't appear on GitHub Pages
- Old content still showing

**Solutions:**
1. **Check workflow triggers**: Ensure changes to `docs/` trigger the workflow
2. **Manual trigger**: Go to Actions → Documentation → "Run workflow"
3. **Clear cache**: Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)

### Issue: Custom domain not working

**Symptoms:**
- Custom domain shows 404 or doesn't resolve
- HTTPS certificate issues

**Solutions:**
1. **Check CNAME file**: Must be in `docs/CNAME` (not root)
2. **Verify DNS**: CNAME should point to `yourusername.github.io`
3. **Wait for propagation**: DNS changes can take up to 24 hours
4. **Enable HTTPS**: In Pages settings, check "Enforce HTTPS"

## Advanced Configuration

### Custom Domain Setup

1. **Create CNAME file:**
   ```bash
   echo "docs.yourdomain.com" > docs/CNAME
   ```

2. **Configure DNS:**
   ```
   Type: CNAME
   Name: docs
   Value: yourusername.github.io
   ```

3. **Update repository settings:**
   - Settings → Pages → Custom domain: `docs.yourdomain.com`
   - Enable "Enforce HTTPS"

### Branch Protection

Protect your main branch to ensure documentation quality:

1. **Settings → Branches → Add rule**
2. **Branch name pattern:** `main`
3. **Enable:**
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Status checks: "docs-check"

### Workflow Customization

Customize deployment behavior in `.github/workflows/docs.yml`:

```yaml
# Deploy only on releases
deploy:
  if: github.event_name == 'release'

# Deploy on multiple branches
deploy:
  if: contains(fromJson('["main", "develop"]'), github.ref_name)
```

## Monitoring and Maintenance

### Regular Checks

1. **Weekly**: Verify all links work (`make linkcheck`)
2. **Monthly**: Update documentation dependencies
3. **Per release**: Update version numbers and changelog

### Automated Monitoring

Set up monitoring for your documentation site:

```python
# Add to your monitoring system
import requests

def check_docs_health():
    url = "https://yourusername.github.io/gui-image-studio/"
    response = requests.get(url)
    return response.status_code == 200
```

### Performance Optimization

1. **Optimize images**: Compress images in `docs/_static/`
2. **Minimize CSS/JS**: Use minified versions
3. **Enable compression**: GitHub Pages automatically compresses content

## Support

If you encounter issues:

1. **Check Actions logs**: Detailed error messages in workflow runs
2. **GitHub Status**: Check [GitHub Status](https://www.githubstatus.com/) for outages
3. **Community**: Ask in GitHub Discussions or Stack Overflow
4. **Documentation**: [GitHub Pages docs](https://docs.github.com/en/pages)

## Success Indicators

Your GitHub Pages setup is working correctly when:

- ✅ Documentation workflow completes successfully
- ✅ Site is accessible at your GitHub Pages URL
- ✅ All major sections load without errors
- ✅ Search functionality works
- ✅ Navigation between pages works
- ✅ Mobile responsiveness works
- ✅ HTTPS is enabled and working

## Next Steps

After successful setup:

1. **Share the URL** with your team and users
2. **Add the URL** to your repository description
3. **Link from README** to the documentation
4. **Set up monitoring** for uptime and performance
5. **Plan regular updates** and maintenance# GitHub Pages Setup Guide

This guide helps you set up GitHub Pages for GUI Image Studio documentation.

## Quick Setup Checklist

- [ ] Repository Settings → Pages → Source: "GitHub Actions"
- [ ] Repository Settings → Actions → General → Workflow permissions: "Read and write"
- [ ] Push workflows to main branch
- [ ] Wait for "Documentation" workflow to complete
- [ ] Verify site is live at `https://yourusername.github.io/gui-image-studio/`

## Detailed Setup Steps

### 1. Configure Repository Settings

1. **Go to your repository on GitHub**
2. **Click "Settings" tab**
3. **Navigate to "Pages" in the left sidebar**
4. **Set Source to "GitHub Actions"** (not "Deploy from a branch")

### 2. Set Workflow Permissions

1. **In Settings, go to "Actions" → "General"**
2. **Under "Workflow permissions", select:**
   - ✅ "Read and write permissions"
   - ✅ "Allow GitHub Actions to create and approve pull requests"

### 3. Deploy Documentation

```bash
# Commit and push the documentation system
git add .github/workflows/ docs/ scripts/
git commit -m "Add documentation system with GitHub Pages"
git push origin main
```

### 4. Monitor Deployment

1. **Go to "Actions" tab in your repository**
2. **Watch the "Documentation" workflow run**
3. **Wait for successful completion (green checkmark)**

### 5. Verify Deployment

```bash
# Use the verification script
pip install requests
python scripts/verify-pages.py https://yourusername.github.io/gui-image-studio/
```

## Troubleshooting

### Issue: "Pages" section not visible in Settings

**Solution:**
- Ensure your repository is public, or you have GitHub Pro/Team
- Check that you have admin permissions on the repository

### Issue: Workflow fails with permission errors

**Solution:**
```yaml
# Verify these permissions are set in .github/workflows/docs.yml
permissions:
  contents: read
  pages: write
  id-token: write
```

**Also check:**
- Repository Settings → Actions → General → Workflow permissions: "Read and write"

### Issue: Documentation builds but doesn't deploy

**Symptoms:**
- Build job succeeds
- Deploy job fails or doesn't run

**Solutions:**
1. **Check branch name**: Deployment only happens on `main` branch
2. **Verify Pages source**: Must be set to "GitHub Actions"
3. **Check workflow file**: Ensure deploy job has correct conditions

### Issue: 404 errors on GitHub Pages

**Symptoms:**
- Main page loads but subpages return 404
- Links are broken

**Solutions:**
1. **Check file structure**: Ensure HTML files are in `docs/_build/html/`
2. **Verify build output**: Check Actions logs for build warnings
3. **Test locally**: Run `python scripts/build-docs.py build` and check output

### Issue: Documentation is outdated

**Symptoms:**
- Changes to docs/ don't appear on GitHub Pages
- Old content still showing

**Solutions:**
1. **Check workflow triggers**: Ensure changes to `docs/` trigger the workflow
2. **Manual trigger**: Go to Actions → Documentation → "Run workflow"
3. **Clear cache**: Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)

### Issue: Custom domain not working

**Symptoms:**
- Custom domain shows 404 or doesn't resolve
- HTTPS certificate issues

**Solutions:**
1. **Check CNAME file**: Must be in `docs/CNAME` (not root)
2. **Verify DNS**: CNAME should point to `yourusername.github.io`
3. **Wait for propagation**: DNS changes can take up to 24 hours
4. **Enable HTTPS**: In Pages settings, check "Enforce HTTPS"

## Advanced Configuration

### Custom Domain Setup

1. **Create CNAME file:**
   ```bash
   echo "docs.yourdomain.com" > docs/CNAME
   ```

2. **Configure DNS:**
   ```
   Type: CNAME
   Name: docs
   Value: yourusername.github.io
   ```

3. **Update repository settings:**
   - Settings → Pages → Custom domain: `docs.yourdomain.com`
   - Enable "Enforce HTTPS"

### Branch Protection

Protect your main branch to ensure documentation quality:

1. **Settings → Branches → Add rule**
2. **Branch name pattern:** `main`
3. **Enable:**
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Status checks: "docs-check"

### Workflow Customization

Customize deployment behavior in `.github/workflows/docs.yml`:

```yaml
# Deploy only on releases
deploy:
  if: github.event_name == 'release'

# Deploy on multiple branches
deploy:
  if: contains(fromJson('["main", "develop"]'), github.ref_name)
```

## Monitoring and Maintenance

### Regular Checks

1. **Weekly**: Verify all links work (`make linkcheck`)
2. **Monthly**: Update documentation dependencies
3. **Per release**: Update version numbers and changelog

### Automated Monitoring

Set up monitoring for your documentation site:

```python
# Add to your monitoring system
import requests

def check_docs_health():
    url = "https://yourusername.github.io/gui-image-studio/"
    response = requests.get(url)
    return response.status_code == 200
```

### Performance Optimization

1. **Optimize images**: Compress images in `docs/_static/`
2. **Minimize CSS/JS**: Use minified versions
3. **Enable compression**: GitHub Pages automatically compresses content

## Support

If you encounter issues:

1. **Check Actions logs**: Detailed error messages in workflow runs
2. **GitHub Status**: Check [GitHub Status](https://www.githubstatus.com/) for outages
3. **Community**: Ask in GitHub Discussions or Stack Overflow
4. **Documentation**: [GitHub Pages docs](https://docs.github.com/en/pages)

## Success Indicators

Your GitHub Pages setup is working correctly when:

- ✅ Documentation workflow completes successfully
- ✅ Site is accessible at your GitHub Pages URL
- ✅ All major sections load without errors
- ✅ Search functionality works
- ✅ Navigation between pages works
- ✅ Mobile responsiveness works
- ✅ HTTPS is enabled and working

## Next Steps

After successful setup:

1. **Share the URL** with your team and users
2. **Add the URL** to your repository description
3. **Link from README** to the documentation
4. **Set up monitoring** for uptime and performance
5. **Plan regular updates** and maintenance# GitHub Pages Setup Guide

This guide helps you set up GitHub Pages for GUI Image Studio documentation.

## Quick Setup Checklist

- [ ] Repository Settings → Pages → Source: "GitHub Actions"
- [ ] Repository Settings → Actions → General → Workflow permissions: "Read and write"
- [ ] Push workflows to main branch
- [ ] Wait for "Documentation" workflow to complete
- [ ] Verify site is live at `https://yourusername.github.io/gui-image-studio/`

## Detailed Setup Steps

### 1. Configure Repository Settings

1. **Go to your repository on GitHub**
2. **Click "Settings" tab**
3. **Navigate to "Pages" in the left sidebar**
4. **Set Source to "GitHub Actions"** (not "Deploy from a branch")

### 2. Set Workflow Permissions

1. **In Settings, go to "Actions" → "General"**
2. **Under "Workflow permissions", select:**
   - ✅ "Read and write permissions"
   - ✅ "Allow GitHub Actions to create and approve pull requests"

### 3. Deploy Documentation

```bash
# Commit and push the documentation system
git add .github/workflows/ docs/ scripts/
git commit -m "Add documentation system with GitHub Pages"
git push origin main
```

### 4. Monitor Deployment

1. **Go to "Actions" tab in your repository**
2. **Watch the "Documentation" workflow run**
3. **Wait for successful completion (green checkmark)**

### 5. Verify Deployment

```bash
# Use the verification script
pip install requests
python scripts/verify-pages.py https://yourusername.github.io/gui-image-studio/
```

## Troubleshooting

### Issue: "Pages" section not visible in Settings

**Solution:**
- Ensure your repository is public, or you have GitHub Pro/Team
- Check that you have admin permissions on the repository

### Issue: Workflow fails with permission errors

**Solution:**
```yaml
# Verify these permissions are set in .github/workflows/docs.yml
permissions:
  contents: read
  pages: write
  id-token: write
```

**Also check:**
- Repository Settings → Actions → General → Workflow permissions: "Read and write"

### Issue: Documentation builds but doesn't deploy

**Symptoms:**
- Build job succeeds
- Deploy job fails or doesn't run

**Solutions:**
1. **Check branch name**: Deployment only happens on `main` branch
2. **Verify Pages source**: Must be set to "GitHub Actions"
3. **Check workflow file**: Ensure deploy job has correct conditions

### Issue: 404 errors on GitHub Pages

**Symptoms:**
- Main page loads but subpages return 404
- Links are broken

**Solutions:**
1. **Check file structure**: Ensure HTML files are in `docs/_build/html/`
2. **Verify build output**: Check Actions logs for build warnings
3. **Test locally**: Run `python scripts/build-docs.py build` and check output

### Issue: Documentation is outdated

**Symptoms:**
- Changes to docs/ don't appear on GitHub Pages
- Old content still showing

**Solutions:**
1. **Check workflow triggers**: Ensure changes to `docs/` trigger the workflow
2. **Manual trigger**: Go to Actions → Documentation → "Run workflow"
3. **Clear cache**: Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)

### Issue: Custom domain not working

**Symptoms:**
- Custom domain shows 404 or doesn't resolve
- HTTPS certificate issues

**Solutions:**
1. **Check CNAME file**: Must be in `docs/CNAME` (not root)
2. **Verify DNS**: CNAME should point to `yourusername.github.io`
3. **Wait for propagation**: DNS changes can take up to 24 hours
4. **Enable HTTPS**: In Pages settings, check "Enforce HTTPS"

## Advanced Configuration

### Custom Domain Setup

1. **Create CNAME file:**
   ```bash
   echo "docs.yourdomain.com" > docs/CNAME
   ```

2. **Configure DNS:**
   ```
   Type: CNAME
   Name: docs
   Value: yourusername.github.io
   ```

3. **Update repository settings:**
   - Settings → Pages → Custom domain: `docs.yourdomain.com`
   - Enable "Enforce HTTPS"

### Branch Protection

Protect your main branch to ensure documentation quality:

1. **Settings → Branches → Add rule**
2. **Branch name pattern:** `main`
3. **Enable:**
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Status checks: "docs-check"

### Workflow Customization

Customize deployment behavior in `.github/workflows/docs.yml`:

```yaml
# Deploy only on releases
deploy:
  if: github.event_name == 'release'

# Deploy on multiple branches
deploy:
  if: contains(fromJson('["main", "develop"]'), github.ref_name)
```

## Monitoring and Maintenance

### Regular Checks

1. **Weekly**: Verify all links work (`make linkcheck`)
2. **Monthly**: Update documentation dependencies
3. **Per release**: Update version numbers and changelog

### Automated Monitoring

Set up monitoring for your documentation site:

```python
# Add to your monitoring system
import requests

def check_docs_health():
    url = "https://yourusername.github.io/gui-image-studio/"
    response = requests.get(url)
    return response.status_code == 200
```

### Performance Optimization

1. **Optimize images**: Compress images in `docs/_static/`
2. **Minimize CSS/JS**: Use minified versions
3. **Enable compression**: GitHub Pages automatically compresses content

## Support

If you encounter issues:

1. **Check Actions logs**: Detailed error messages in workflow runs
2. **GitHub Status**: Check [GitHub Status](https://www.githubstatus.com/) for outages
3. **Community**: Ask in GitHub Discussions or Stack Overflow
4. **Documentation**: [GitHub Pages docs](https://docs.github.com/en/pages)

## Success Indicators

Your GitHub Pages setup is working correctly when:

- ✅ Documentation workflow completes successfully
- ✅ Site is accessible at your GitHub Pages URL
- ✅ All major sections load without errors
- ✅ Search functionality works
- ✅ Navigation between pages works
- ✅ Mobile responsiveness works
- ✅ HTTPS is enabled and working

## Next Steps

After successful setup:

1. **Share the URL** with your team and users
2. **Add the URL** to your repository description
3. **Link from README** to the documentation
4. **Set up monitoring** for uptime and performance
5. **Plan regular updates** and maintenance
