# Installation

This project is an overlay task for **Isaac Lab 5.1 + robot_lab**.

It does not include the full Isaac Lab or robot_lab source tree.  
Users should install Isaac Lab and robot_lab separately, then install this Flip task into their local Isaac Lab task directory.

## Expected Environment

- Ubuntu 22.04
- Conda environment: `l_lab`
- Isaac Sim / Isaac Lab 5.1
- robot_lab from `fan-ziqi/robot_lab`
- RSL-RL support installed through Isaac Lab

## Clone This Repository

```bash
cd /home/robot/l_lab
git clone https://github.com/<your-username>/flip-isaaclab-rl.git
cd flip-isaaclab-rl
```

## Install the Flip Task into Isaac Lab

```bash
bash scripts/install_flip_task.sh /home/robot/l_lab/IsaacLab
```

## Verify Task Registration

```bash
cd /home/robot/l_lab/IsaacLab

./isaaclab.sh -p - <<'PY'
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

import gymnasium as gym
import isaaclab_tasks

print("Registered Flip tasks:")
for name in gym.registry.keys():
    if "Flip" in name:
        print(name)

simulation_app.close()
PY
```

Expected output:

```text
Isaac-Velocity-Flat-Flip-v0
```
