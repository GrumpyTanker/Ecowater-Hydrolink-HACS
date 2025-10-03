# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The EcoWater HydroLink integration team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **GitHub Security Advisories** (Preferred)
   - Navigate to the [Security tab](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/security/advisories/new) of this repository
   - Click "Report a vulnerability"
   - Fill out the advisory form with details

2. **Email**
   - Send an email with details to the repository owner through GitHub
   - Include "SECURITY" in the subject line

### What to Include

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to Expect

- You should receive an acknowledgment within 48 hours
- We will investigate and validate the security issue within 7 days
- We will work on a fix and coordinate the release with you
- We will credit you in the release notes (unless you prefer to remain anonymous)

## Security Best Practices

When using this integration:

1. **Credentials**: Never share your HydroLink credentials in logs, issues, or public forums
2. **API Keys**: Store credentials securely in Home Assistant's configuration
3. **Updates**: Keep the integration updated to the latest version
4. **Logs**: Be careful when sharing logs - they may contain sensitive information
5. **Network**: Ensure your Home Assistant instance is secured with SSL/TLS if exposed externally

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine the affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release new versions as soon as possible

## Comments on This Policy

If you have suggestions on how this process could be improved, please submit a pull request or open an issue.

Thank you for helping keep EcoWater HydroLink and its users safe!
