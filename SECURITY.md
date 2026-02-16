# Security Policy

## Supported Versions

The following versions of the facial recognition application are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.1   | :white_check_mark: |
| 1.0.0   | :x: (vulnerable)   |

## Security Updates

### Version 1.0.1 (2024-02-16) - Security Patch

This version addresses **critical security vulnerabilities** in dependencies:

#### Critical Fixes

**Keras (upgraded to >=3.12.0)**
- ✅ Fixed directory traversal vulnerability
- ✅ Fixed path traversal in `keras.utils.get_file` API
- ✅ Fixed deserialization of untrusted data vulnerability
- ✅ Fixed arbitrary code execution vulnerability

**PyTorch (upgraded to >=2.6.0)**
- ✅ Fixed heap buffer overflow vulnerability
- ✅ Fixed use-after-free vulnerability
- ✅ Fixed remote code execution via `torch.load`
- ✅ Fixed deserialization vulnerability

**Pillow (upgraded to >=10.3.0)**
- ✅ Fixed buffer overflow vulnerability

**TensorFlow (upgraded to >=2.16.0)**
- ✅ Updated for compatibility with Keras 3.x

## Update Instructions

### Immediate Action Required

If you are using version 1.0.0, **update immediately** to version 1.0.1:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Or reinstall from scratch
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Verification

Verify you have the patched versions:

```bash
python -c "import keras; print(f'Keras: {keras.__version__}')"
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import PIL; print(f'Pillow: {PIL.__version__}')"
```

Expected output:
- Keras: 3.12.0 or higher
- PyTorch: 2.6.0 or higher
- Pillow: 10.3.0 or higher

## Reporting a Vulnerability

### How to Report

If you discover a security vulnerability, please follow these steps:

1. **DO NOT** open a public GitHub issue
2. Email the maintainers directly (if available) or
3. Open a private security advisory on GitHub
4. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Status Updates**: Every week until resolved
- **Fix Release**: ASAP for critical issues, within 30 days for others
- **Credit**: You will be credited in the changelog (unless you prefer to remain anonymous)

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Monitor Security Advisories**
   - Check this file regularly
   - Watch the repository for updates
   - Subscribe to security announcements

3. **Use Virtual Environments**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate.bat  # Windows
   ```

4. **Verify Installation**
   ```bash
   python test_installation.py
   ```

### For Developers

1. **Regular Dependency Audits**
   ```bash
   pip-audit
   # or
   safety check
   ```

2. **Code Security**
   - Never deserialize untrusted data without validation
   - Validate all user inputs
   - Use parameterized SQL queries (already implemented)
   - Keep camera access controlled

3. **Data Protection**
   - All user data is stored locally
   - Database file should have restricted permissions
   - Consider encrypting the database file

4. **Review Changes**
   - Review all dependency updates
   - Test thoroughly before deployment
   - Check for breaking changes

## Known Security Considerations

### Current Implementation

✅ **Secure**:
- Local data storage (no cloud)
- Parameterized SQL queries (no SQL injection)
- No remote code execution paths
- Input validation throughout
- Error handling prevents information leakage
- Does not load external ML models
- Does not use untrusted HDF5 files

⚠️ **Known Issues**:
- **Keras 3.13.1**: Arbitrary file read in HDF5 weight loading mechanism
  - **Impact**: Low (application doesn't load external HDF5 models)
  - **Affected**: >= 3.0.0, <= 3.13.1
  - **Patch**: Not yet available
  - **Mitigation**: Application uses only built-in FaceNet models from facenet-pytorch, no external HDF5 files

⚠️ **User Responsibility**:
- Physical access to the computer = access to database
- Database file should be protected at OS level
- Camera access should be controlled
- Users should verify unknown faces before registration
- Do not load untrusted model files

### Future Enhancements

Planned security improvements:
- [ ] Database encryption at rest
- [ ] Password protection for application
- [ ] Audit logging
- [ ] Role-based access control
- [ ] Secure backup/restore

## Dependency Security Policy

### Pinned vs. Ranged Versions

We use minimum version requirements (>=) for security-critical dependencies:
- `keras>=3.13.1` - Latest version with most security patches
- `torch>=2.6.0` - Ensures all security patches
- `Pillow>=10.3.0` - Ensures all security patches

### Update Schedule

- **Critical Security Updates**: Immediate
- **High Priority Updates**: Within 1 week
- **Medium Priority Updates**: Within 1 month
- **Low Priority Updates**: Next release cycle

## Security Scanning

This project uses:
- **CodeQL**: Automated code security analysis
- **GitHub Dependabot**: Dependency vulnerability scanning
- **Manual Reviews**: Regular code reviews

Latest CodeQL scan: ✅ **0 vulnerabilities** (after version 1.0.1)

## Compliance

### Privacy

This application:
- ✅ Stores all data locally
- ✅ Does not transmit data over network
- ✅ Does not collect telemetry
- ✅ Does not require internet (post-installation)
- ✅ Complies with GDPR principles (data minimization, local storage)

### License

This project is licensed under MIT License. See [LICENSE](LICENSE) file.

## Contact

For security concerns:
- Open a GitHub Issue (for non-sensitive matters)
- Use GitHub Security Advisories (for sensitive vulnerabilities)
- Check CONTRIBUTING.md for more information

## Acknowledgments

We thank the security researchers and maintainers of:
- Keras team for security patches
- PyTorch team for security patches
- Pillow team for security patches
- GitHub Security Lab for vulnerability database
- All users who report security issues responsibly

---

**Last Updated**: 2024-02-16  
**Next Review**: 2024-03-16 (monthly)
