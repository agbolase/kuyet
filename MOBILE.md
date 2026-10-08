# TomatoCare offline Android (Codemagic)

The Streamlit web app stays in the repo root. The **offline Android app** lives in `mobile/` (Flutter + TensorFlow Lite). It does not use Streamlit, the network, or an external database.

## What runs on the phone

| Feature | Storage |
|--------|---------|
| Leaf disease scan | Bundled `.tflite` in APK assets |
| Field guide (EN / Hausa) | Bundled JSON in `assets/guides/` |
| Scan history | Local JSON + thumbnails in app documents (`scan_logs/`) |

Optional leaf-gate models (`leaf_embed.tflite`, `leaf_gate.npz`) are copied when present; the mobile app currently runs the main classifier (same as a simplified web scan without the embed gate).

## One-time: export models into the app

Train or copy models into `models/` at the repo root, then:

```bash
cd /path/to/Kuyet
python3 scripts/export_mobile_assets.py
# or
./scripts/prepare_mobile_assets.sh
```

Required for a working scanner:

- `models/hortivision_model.tflite`
- `models/class_names.json`

Recommended (copied when available):

- `models/leaf_embed.tflite`
- `models/leaf_gate.npz`

Assets land in `mobile/assets/models/`.

## Local APK build

```bash
cd mobile
flutter pub get
flutter build apk --release
```

APK: `mobile/build/app/outputs/flutter-apk/app-release.apk`

Install on a device with USB debugging or share the APK file.

## Codemagic CI (Android APK)

The web Streamlit app is **not** deployed to Codemagic. CI builds the **Flutter app** in `mobile/` using `codemagic.yaml` at the **repository root**.

### 1. Put the project in Git and push

Kuyet must be its own Git repository (not only a folder inside another repo):

```bash
cd /path/to/Kuyet
git init
git add .
git commit -m "TomatoCare: Flutter Android + Codemagic"
# Create an empty repo on GitHub, then:
git remote add origin git@github.com:YOUR_USER/Kuyet.git
git branch -M main
git push -u origin main
```

Commit these so CI can bundle the scanner:

- `mobile/assets/models/hortivision_model.tflite` and `class_names.json` (run `python3 scripts/export_mobile_assets.py` first), **or**
- `models/hortivision_model.tflite` and `models/class_names.json` at the repo root (CI runs the export script).

Large `.keras` checkpoints are gitignored; `.tflite` files (~25 MB each) are fine for GitHub.

### 2. Connect Codemagic

1. Sign in at [codemagic.io](https://codemagic.io/).
2. **Add application** → connect GitHub/GitLab/Bitbucket → select the **Kuyet** repository.
3. On the app page, choose branch **main** → **Check for configuration file** (finds `codemagic.yaml`).
4. Start workflow **`tomatocare-android`** (manual build the first time, or push to `main` to trigger).

### 3. Download the APK

When the build succeeds, open the build → **Artifacts** → download `app-release.apk` from  
`mobile/build/app/outputs/flutter-apk/`.

Optional: uncomment `publishing.email` in `codemagic.yaml` to get build notifications.

### 4. Release signing (Google Play)

First builds use **debug signing** (fine for sideloading/testing). For Play Store:

1. Codemagic → **Team settings** → **Code signing identities** → upload your Android keystore; note the **reference name**.
2. In `codemagic.yaml`, uncomment `android_signing` and set that reference name.
3. `mobile/android/app/build.gradle.kts` already uses Codemagic’s `CM_KEYSTORE_*` variables when present.

Docs: [Codemagic Flutter](https://docs.codemagic.io/yaml-quick-start/building-a-flutter-app/) · [Android signing](https://docs.codemagic.io/yaml-code-signing/signing-android/)

## Web vs mobile

| | Web (`streamlit run app.py`) | Android (`mobile/`) |
|--|------------------------------|------------------------|
| UI | Streamlit | Flutter |
| Offline | No (needs server) | Yes |
| History | `data/scan_logs/` on server | On-device files |
| Voice / gTTS | Yes | Not in v1 |

Both share the same TFLite model and field-guide content exported via `scripts/export_mobile_assets.py`.
