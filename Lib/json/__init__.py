import json, shutil, subprocess, sys, tempfile
from pathlib import Path
from common import load_project, ROOT

def run(cmd):
    print("+", " ".join(map(str, cmd)))
    subprocess.run(list(map(str, cmd)), check=True)

def probe_duration(path):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)],capture_output=True,text=True,check=True)
    return float(r.stdout.strip())

def main(project_file):
    data = load_project(project_file)
    cfg = json.loads((ROOT/"config.json").read_text())
    width, height, fps = cfg.get("width",1920), cfg.get("height",1080), cfg.get("fps",30)
    outdir = Path(data["_project_dir"])
    temp = outdir/"segments"
    temp.mkdir(exist_ok=True)
    segments = []
    subtitle_rows = []
    timeline = 0.0
    for i, scene in enumerate(data["scenes"],1):
        img = Path(scene.get("image_path") or (outdir/"images"/f'{scene["id"]}.png'))
