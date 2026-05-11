# video-gen

Generate videos from structured scene scripts using the [TokenRouter](https://tokenrouter.com) API. Supports Kling, Hailuo, Seedance, and Happyhorse models through a unified interface.

## Setup

```bash
uv sync
cp .env.example .env
# Edit .env with your TokenRouter API key
```

## Usage

```bash
# Generate all scenes from a script
video-gen scripts/k8s-migration.json

# Generate specific scenes
video-gen scripts/k8s-migration.json --scene 3
video-gen scripts/k8s-migration.json --scene 2-5

# Preview without calling API
video-gen scripts/k8s-migration.json --dry-run

# Check progress
video-gen scripts/k8s-migration.json --status

# Override model for all scenes
video-gen scripts/k8s-migration.json --model MiniMax-Hailuo-2.3

# Poll an existing task
video-gen scripts/k8s-migration.json --poll task_xxxxx

# Custom output directory
video-gen scripts/k8s-migration.json --output-dir ./my-output
```

Output defaults to `~/Downloads/<script-name>/`. State is tracked per-script so interrupted runs resume where they left off.

## Script Format

Scripts are JSON files with an array of scenes:

```json
{
  "title": "My Video Project",
  "scenes": [
    {
      "name": "scene_name",
      "prompt": "Detailed description of the video scene...",
      "model": "kling-v3",
      "duration": 5,
      "metadata": {
        "aspect_ratio": "16:9",
        "mode": "pro",
        "sound": "off"
      }
    }
  ]
}
```

## Supported Models

| Model | Provider | Type | Notes |
|-------|----------|------|-------|
| `kling-v3` | Kling | text-to-video | Default. Good cinematic quality |
| `kling-v2-6` | Kling | text-to-video | Previous generation |
| `MiniMax-Hailuo-2.3` | Hailuo | text-to-video | Natural motion |
| `dreamina-seedance-2-0-260128` | Seedance | text/image/multimodal | Full quality, supports audio/video refs |
| `dreamina-seedance-2-0-fast-260128` | Seedance | text/image | Speed optimized |
| `happyhorse-1.0-t2v` | Happyhorse | text-to-video | |
| `happyhorse-1.0-i2v` | Happyhorse | image-to-video | Requires `input_reference` field |

### Provider-Specific Metadata

**Kling:** `mode` (pro/standard), `aspect_ratio`, `sound` (on/off), `negative_prompt`

**Hailuo:** `size` (768P, 1080P)

**Seedance:** `resolution` (720p, 1080p), `ratio`, `generate_audio` (bool). Supports `images`, `audios`, `videos` arrays for multimodal generation.

**Happyhorse:** `size` (1920*1080, 720p). Use `input_reference` for image-to-video.

## Example Scripts

- `scripts/k8s-migration.json` — 13-scene instructional video about self-hosted Kubernetes migration
- `scripts/model-comparison.json` — Same prompt across all models for quality comparison
