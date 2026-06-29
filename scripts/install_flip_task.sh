#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage:"
  echo "  bash scripts/install_flip_task.sh /path/to/IsaacLab"
  exit 1
fi

ISAACLAB_ROOT="$1"

TARGET_DIR="$ISAACLAB_ROOT/source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/flip"
CONFIG_INIT="$ISAACLAB_ROOT/source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/__init__.py"

echo "[INFO] IsaacLab root: $ISAACLAB_ROOT"
echo "[INFO] Installing Flip task to: $TARGET_DIR"

mkdir -p "$TARGET_DIR"
cp -r isaaclab_task/flip/* "$TARGET_DIR/"

if ! grep -q "from \. import flip" "$CONFIG_INIT"; then
  echo "" >> "$CONFIG_INIT"
  echo "from . import flip" >> "$CONFIG_INIT"
  echo "[INFO] Added 'from . import flip' to config/__init__.py"
else
  echo "[INFO] config/__init__.py already imports flip"
fi

echo "[INFO] Done."
echo ""
echo "You can verify task registration with:"
echo "  cd $ISAACLAB_ROOT"
echo "  ./isaaclab.sh -p - <<'PY'"
echo "from isaacsim import SimulationApp"
echo "simulation_app = SimulationApp({'headless': True})"
echo "import gymnasium as gym"
echo "import isaaclab_tasks"
echo "print([name for name in gym.registry.keys() if 'Flip' in name])"
echo "simulation_app.close()"
echo "PY"
