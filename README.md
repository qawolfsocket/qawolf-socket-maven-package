# qawolf-socket-maven-package

Minimal Java library scaffold and GitHub Actions workflow to publish a signed artifact to Maven Central (OSSRH).

See `.github/workflows/release.yml` for the release workflow.

Required GitHub secrets before publishing:
- `OSSRH_USERNAME` - Sonatype OSSRH username
- `OSSRH_PASSWORD` - Sonatype OSSRH password
- `GPG_PRIVATE_KEY` - ASCII-armored GPG private key (used to sign artifacts)
- `GPG_PASSPHRASE` - passphrase for the GPG key (if any)

License: MIT
