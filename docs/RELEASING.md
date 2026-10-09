# Release checklist

## Validate locally

- Use Python 3.10+ and `python -m pip install -r requirements.txt` in an isolated environment.
- Run `python -m unittest discover -s tests -v`.
- If skill-creator is installed, run its `scripts/quick_validate.py` against `skills/ppt-beautify-studio`.
- Verify all relative Markdown links and JSON examples; compile Python without publishing caches.
- If compose/render changed, run a real Office-rendered fixture and inspect it, not just the ZIP XML.
- Do not claim any backend has been live-tested unless it was actually called.

## Privacy and package contents

Publish only tracked source/README/requirements/VERSION/examples/tests/docs and skill files.
Exclude credentials, user preferences, captured HTTP bodies, logs, fonts, photos, test outputs, `.venv`, caches and user decks.
A raw request-body file may contain the entire private conversation. Never include it, even in a debug release.
Do not vendor imagegen, ifapi-image, relay-imagegen or ppt-master; they remain external dependencies.

## Version policy

1.7.0 replaces heuristic IF API size/tempo limits with a temporary measured-body gate and defaults to native.
A future version number such as 1.7.1 MUST NOT disable the gate by itself. Require an explicit user-confirmed fix,
record it in private preferences, and keep the ability to re-enable it. Preserve private settings across updates.

## User choices and side effects

No network calls or font/system installs in unit tests. No GitHub upload in packaging tools.
Choose a LICENSE explicitly before presenting the project as open-source licensed software.
Exact byte checks cannot certify a hidden Desktop wrapper. Include this limitation in release notes, do not mask it.
