# Examples

`low-layout.json` is directly composable and does not require generated assets:

```text
python 01-skills/ppt-beautify-studio/scripts/compose_slide.py 03-examples/low-layout.json -o work/low-example.pptx
```

`generated-panel-layout.json` is a schema example, not an included generated asset.
Produce and inspect a genuine text-free panel through the selected backend, save it at the indicated path (or change the path),
then compose it. Missing asset intentionally fails; do not fabricate a native rectangle fallback.
The JSON's `material_source` is a declaration, not proof of generation; retain the actual backend receipt in your private project logs.

No API credentials, copyrighted font files, user screenshots or completed decks are included.
