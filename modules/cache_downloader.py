import os
import sys
import json
import time
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

BASE_CDN_FILES = "https://fastdl.ragerussia.online/files/"
MANIFEST_URL = "https://fastdl.ragerussia.online/client/patch_index.json"
HASH_URL = "https://fastdl.ragerussia.online/hash.json"

TARGET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
HEADERS = {"User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0)"}


def download_file(rel_path, expected_size=None, retries=5):
    local_path = os.path.join(TARGET_DIR, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    temp_path = local_path + ".tmp"

    # If file already exists and size matches, skip
    if os.path.exists(local_path) and expected_size:
        actual_size = os.path.getsize(local_path)
        if actual_size == expected_size:
            return local_path, actual_size, "SKIPPED"

    url = BASE_CDN_FILES + rel_path
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30, context=CTX) as resp:
                downloaded = 0
                with open(temp_path, "wb") as f:
                    while True:
                        chunk = resp.read(256 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                if os.path.exists(local_path):
                    os.remove(local_path)
                os.replace(temp_path, local_path)
                return local_path, downloaded, "OK"
        except Exception as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            if attempt == retries:
                return local_path, 0, f"FAILED: {e}"
            time.sleep(2)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "map"
    print("=" * 60, flush=True)
    print("  RAGE RUSSIA GAME CACHE DOWNLOADER", flush=True)
    print("=" * 60, flush=True)
    print(f"Target Directory: {TARGET_DIR}", flush=True)
    print(f"Mode: {mode} (use 'map' for Map & Logic, 'all' for full cache)", flush=True)

    os.makedirs(TARGET_DIR, exist_ok=True)

    # 1. Fetch manifest patch_index.json
    print("\n[1/3] Fetching manifest patch_index.json...", flush=True)
    req = urllib.request.Request(MANIFEST_URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15, context=CTX) as resp:
        manifest_data = json.loads(resp.read().decode("utf-8"))
    with open(os.path.join(TARGET_DIR, "patch_index.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    # 2. Select files based on mode
    files_to_download = []
    for item in manifest_data.get("files", []):
        p = item["path"]
        rule = item.get("rule_file", "")
        # skip apk, etc2 textures, and missing nologo
        if p.endswith(".apk") or "etc2" in rule or "_nologo" in p:
            continue

        if mode == "map":
            # Map meshes, collision, road network, base configs & UI
            if not any(k in p.lower() for k in ["map", "collision", "roads", "garel", "common", "gui", "radarmap"]):
                continue

        files_to_download.append((p, item.get("filesize", 0)))

    total_bytes = sum(sz for _, sz in files_to_download)
    print(f"[2/3] Selected {len(files_to_download)} files to download ({total_bytes / (1024**3):.2f} GB)", flush=True)

    # 3. Parallel download with ThreadPoolExecutor
    print(f"[3/3] Downloading files with 6 parallel connections...\n", flush=True)
    start_time = time.time()
    downloaded_bytes = 0
    success_count = 0
    fail_count = 0
    skip_count = 0

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_map = {
            executor.submit(download_file, p, sz): (p, sz)
            for p, sz in files_to_download
        }

        for future in as_completed(future_map):
            p, sz = future_map[future]
            path, actual_sz, status = future.result()
            if status == "OK":
                success_count += 1
                downloaded_bytes += actual_sz
                pct = (downloaded_bytes / max(1, total_bytes)) * 100
                print(f"[OK] ({pct:5.1f}%) {p} ({actual_sz / (1024*1024):.2f} MB)", flush=True)
            elif status == "SKIPPED":
                skip_count += 1
                downloaded_bytes += actual_sz
                pct = (downloaded_bytes / max(1, total_bytes)) * 100
                print(f"[SKIP] ({pct:5.1f}%) Already exists: {p}", flush=True)
            else:
                fail_count += 1
                print(f"[ERR] Failed: {p} -> {status}", flush=True)

    elapsed = time.time() - start_time
    print("\n" + "=" * 60, flush=True)
    print("  DOWNLOAD COMPLETED", flush=True)
    print("=" * 60, flush=True)
    print(f"Downloaded: {success_count} files", flush=True)
    print(f"Skipped (already cached): {skip_count} files", flush=True)
    print(f"Failed: {fail_count} files", flush=True)
    print(f"Total downloaded size: {downloaded_bytes / (1024*1024):.2f} MB in {elapsed:.1f}s", flush=True)


if __name__ == "__main__":
    main()
