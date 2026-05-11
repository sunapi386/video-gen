#!/usr/bin/env python3
"""
Video generation script using TokenRouter API.

Usage:
    video-gen script.json                  # Generate all scenes
    video-gen script.json --scene 2        # Generate scene 2 only
    video-gen script.json --scene 2-4      # Generate scenes 2-4
    video-gen script.json --poll task_xxx   # Poll an existing task
    video-gen script.json --status          # Show status of all tasks
    video-gen script.json --dry-run         # Print prompts without calling API

Script format: see scripts/ directory for JSON scene files.

Requires: TOKENROUTER_API_KEY env var (or --api-key flag).
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime


API_BASE = "https://api.tokenrouter.com"
DEFAULT_MODEL = "kling-v3"
POLL_INTERVAL = 5
MAX_POLL_TIME = 600

MODELS = {
    "kling-v3": {"type": "t2v", "provider": "kling"},
    "kling-v2-6": {"type": "t2v", "provider": "kling"},
    "MiniMax-Hailuo-2.3": {"type": "t2v", "provider": "hailuo"},
    "dreamina-seedance-2-0-260128": {"type": "t2v", "provider": "seedance"},
    "dreamina-seedance-2-0-fast-260128": {"type": "t2v", "provider": "seedance"},
    "happyhorse-1.0-t2v": {"type": "t2v", "provider": "happyhorse"},
    "happyhorse-1.0-i2v": {"type": "i2v", "provider": "happyhorse"},
}


def api_request(method, path, api_key, data=None):
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"  API error {e.code}: {error_body}", file=sys.stderr)
        raise
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}", file=sys.stderr)
        raise


def create_video_task(api_key, scene):
    model = scene.get("model", DEFAULT_MODEL)
    prompt = scene["prompt"]
    duration = scene.get("duration", 5)
    metadata = scene.get("metadata", {})

    model_info = MODELS.get(model, {"provider": "unknown"})
    provider = model_info["provider"]

    payload = {"model": model, "prompt": prompt}

    if provider == "kling":
        payload["metadata"] = {
            "mode": metadata.get("mode", "pro"),
            "duration": str(duration),
            "aspect_ratio": metadata.get("aspect_ratio", "16:9"),
            "sound": metadata.get("sound", "off"),
            **{k: v for k, v in metadata.items() if k not in ("mode", "aspect_ratio", "sound")},
        }
    elif provider == "hailuo":
        payload["duration"] = duration
        payload["size"] = metadata.get("size", "768P")
    elif provider == "seedance":
        payload["metadata"] = {
            "duration": duration,
            "resolution": metadata.get("resolution", "1080p"),
            "ratio": metadata.get("ratio", "16:9"),
            "generate_audio": metadata.get("generate_audio", False),
        }
        if "images" in scene:
            payload["images"] = scene["images"]
    elif provider == "happyhorse":
        payload["size"] = metadata.get("size", "1920*1080")
        payload["duration"] = duration
        payload["metadata"] = {}
        if "input_reference" in scene:
            payload["input_reference"] = scene["input_reference"]

    if "image" in scene:
        payload["image"] = scene["image"]
    if "first_frame_image" in scene:
        payload["first_frame_image"] = scene["first_frame_image"]

    return api_request("POST", "/v1/video/generations", api_key, payload)


def poll_task(api_key, task_id, label=""):
    prefix = f"  [{label}] " if label else "  "
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > MAX_POLL_TIME:
            print(f"{prefix}Timed out after {MAX_POLL_TIME}s")
            return None

        result = api_request("GET", f"/v1/video/generations/{task_id}", api_key)
        data = result.get("data", result)
        status = data.get("status", "UNKNOWN")
        progress = data.get("progress", "?")

        print(f"{prefix}{status} ({progress}) [{int(elapsed)}s]")

        if status == "SUCCESS":
            url = data.get("result_url", "")
            print(f"{prefix}Done: {url}")
            return data
        elif status == "FAILURE":
            print(f"{prefix}Failed!")
            return data

        time.sleep(POLL_INTERVAL)


def download_video(url, output_path):
    print(f"  Downloading to {output_path} ...")
    urllib.request.urlretrieve(url, output_path)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Saved ({size_mb:.1f} MB)")


def load_script(path):
    with open(path) as f:
        return json.load(f)


def save_state(state_path, state):
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)


def load_state(state_path):
    if os.path.exists(state_path):
        with open(state_path) as f:
            return json.load(f)
    return {}


def parse_scene_range(spec, total):
    if "-" in spec:
        a, b = spec.split("-", 1)
        return list(range(int(a), int(b) + 1))
    return [int(spec)]


def main():
    parser = argparse.ArgumentParser(description="Generate videos from a scene script")
    parser.add_argument("script", help="Path to JSON script file")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("TOKENROUTER_API_KEY", ""),
        help="TokenRouter API key (or set TOKENROUTER_API_KEY)",
    )
    parser.add_argument("--scene", help="Scene number or range (e.g. 2, 2-4)")
    parser.add_argument("--poll", metavar="TASK_ID", help="Poll an existing task")
    parser.add_argument("--status", action="store_true", help="Show status of all tasks")
    parser.add_argument("--dry-run", action="store_true", help="Print payloads without calling API")
    parser.add_argument(
        "--output-dir", help="Output directory (default: ~/Downloads/<script-name>)"
    )
    parser.add_argument("--model", help="Override model for all scenes")
    parser.add_argument("--no-download", action="store_true", help="Skip downloading videos")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: set TOKENROUTER_API_KEY or pass --api-key", file=sys.stderr)
        sys.exit(1)

    script_path = Path(args.script)
    script = load_script(script_path)
    scenes = script.get("scenes", [])
    title = script.get("title", script_path.stem)

    default_output = Path.home() / "Downloads" / script_path.stem
    output_dir = Path(args.output_dir) if args.output_dir else default_output
    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / f"{script_path.stem}.state.json"
    state = load_state(state_path)

    if args.poll:
        poll_task(args.api_key, args.poll, label="manual")
        return

    if args.status:
        print(f"Script: {title} ({len(scenes)} scenes)")
        for i, scene in enumerate(scenes, 1):
            key = str(i)
            info = state.get(key, {})
            task_id = info.get("task_id", "-")
            status = info.get("status", "not started")
            result = info.get("result_url", "")
            print(
                f"  Scene {i}: {scene.get('name', 'untitled'):30s} | {status:12s} | {task_id}"
            )
            if result:
                print(f"           {result}")
        return

    if args.scene:
        indices = parse_scene_range(args.scene, len(scenes))
    else:
        indices = list(range(1, len(scenes) + 1))

    print(f"Script: {title}")
    print(f"Scenes: {len(indices)} to generate")
    print(f"Output: {output_dir}")
    print()

    for i in indices:
        if i < 1 or i > len(scenes):
            print(f"Scene {i}: out of range (1-{len(scenes)}), skipping")
            continue

        scene = scenes[i - 1].copy()
        name = scene.get("name", f"scene_{i:02d}")

        if args.model:
            scene["model"] = args.model

        model = scene.get("model", DEFAULT_MODEL)
        print(f"Scene {i}/{len(scenes)}: {name}")
        print(f"  Model: {model}")
        print(f"  Prompt: {scene['prompt'][:120]}...")

        if args.dry_run:
            print(f"  [dry-run] Would submit to {API_BASE}/v1/video/generations")
            print()
            continue

        existing = state.get(str(i), {})
        if existing.get("status") == "SUCCESS" and existing.get("result_url"):
            print(f"  Already complete: {existing['result_url']}")
            print()
            continue

        try:
            result = create_video_task(args.api_key, scene)
        except Exception as e:
            print(f"  Failed to create task: {e}")
            print()
            continue

        task_id = result.get("task_id", result.get("data", {}).get("task_id", ""))
        if not task_id:
            print(f"  No task_id returned: {json.dumps(result, indent=2)}")
            print()
            continue

        print(f"  Task: {task_id}")
        state[str(i)] = {
            "task_id": task_id,
            "name": name,
            "status": "SUBMITTED",
            "submitted_at": datetime.now().isoformat(),
        }
        save_state(state_path, state)

        final = poll_task(args.api_key, task_id, label=name)
        if final:
            state[str(i)]["status"] = final.get("status", "UNKNOWN")
            if final.get("result_url"):
                state[str(i)]["result_url"] = final["result_url"]
                if not args.no_download:
                    out_file = output_dir / f"{i:02d}_{name}.mp4"
                    try:
                        download_video(final["result_url"], str(out_file))
                        state[str(i)]["local_file"] = str(out_file)
                    except Exception as e:
                        print(f"  Download failed: {e}")
        else:
            state[str(i)]["status"] = "TIMEOUT"

        save_state(state_path, state)
        print()

    print("Done. State saved to:", state_path)


if __name__ == "__main__":
    main()
