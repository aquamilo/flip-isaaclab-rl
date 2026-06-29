# Flip Isaac Lab RL

**Author:** Chunmiao Li  
**Project Type:** Custom quadruped reinforcement learning project  
**Simulator:** Isaac Sim / Isaac Lab 5.1  
**RL Framework:** robot_lab + RSL-RL PPO  

This repository presents a reproducible reinforcement learning pipeline for training a **custom Flip quadruped robot** in Isaac Lab 5.1.

Unlike common public benchmark robots such as Unitree Go2, ANYmal, or Spot, **Flip is not a standard built-in Isaac Lab robot asset** and is not one of the common public benchmark robots supported out of the box. This project focuses on integrating a non-standard quadruped robot into Isaac Lab, fixing USD articulation issues, adapting locomotion reward terms, training a PPO policy, and building a keyboard-controlled playback workflow.

The goal of this repository is to demonstrate a complete robotics RL engineering pipeline that can be reviewed for research, internship, and engineering applications.

## Project Highlights

- Integrated a custom quadruped robot into Isaac Lab 5.1.
- Fixed imported USD issues, including floating-base articulation setup.
- Adapted Go2-style locomotion reward terms to the Flip robot.
- Trained a PPO policy for randomized planar velocity tracking.
- Implemented a custom keyboard playback script for manual velocity control.
- Provided reproducible code, configuration files, training commands, model checkpoint, screenshots, GIFs, and videos.

## My Contributions

This project was developed by **Chunmiao Li** as an independent robotics reinforcement learning engineering project.

The Flip robot used in this project is **not a standard built-in Isaac Lab robot asset** and is not one of the common public benchmark robots such as Unitree Go2, ANYmal, or Spot. Instead of directly training an existing supported robot, I built a custom Isaac Lab training pipeline around a non-standard quadruped robot asset.

Main contributions include:

- Integrated a custom Flip quadruped USD asset into Isaac Lab 5.1.
- Repaired the imported robot articulation by removing the fixed `root_joint` issue and applying `ArticulationRootAPI` to the correct robot root.
- Fixed floating-base simulation behavior so the robot could move freely instead of being fixed in place.
- Added and verified foot collision and contact sensor support for locomotion training.
- Created a custom Isaac Lab task registration for `Isaac-Velocity-Flat-Flip-v0`.
- Adapted Go2-style locomotion rewards and training metrics to the Flip robot by remapping body names, foot links, and controllable joints.
- Restricted the action space to the 12 actuated leg joints: hip, thigh, and calf joints.
- Configured randomized 2D planar velocity tracking with commands for `lin_vel_x`, `lin_vel_y`, and `ang_vel_z`.
- Trained a PPO locomotion policy using RSL-RL.
- Tracked training behavior with TensorBoard metrics such as velocity tracking error, feet slide, timeout rate, and reward terms.
- Implemented a custom keyboard-controlled playback script that allows manual control of the trained policy through planar velocity commands.
- Organized the project into a reproducible repository with task configs, training commands, playback commands, TensorBoard instructions, model checkpoints, screenshots, GIFs, and videos.

This repository demonstrates a complete custom robot RL workflow: asset debugging, Isaac Lab task integration, PPO training, evaluation, and interactive policy deployment.

## Task Description

The policy is trained for randomized planar velocity tracking.

The robot receives target commands:

```text
lin_vel_x
lin_vel_y
ang_vel_z
```

The command direction and velocity are randomized during training, allowing the robot to move in the 2D plane instead of only walking forward.

## Technical Stack

- Ubuntu 22.04
- Conda environment: `l_lab`
- Isaac Sim / Isaac Lab 5.1
- robot_lab
- RSL-RL PPO
- Gymnasium task registration
- Manager-based RL environment
- TensorBoard

## Robot and Control

The Flip robot is treated as a floating-base quadruped articulation.

The policy controls 12 actuated leg joints:

```text
.*_hip_joint
.*_thigh_joint
.*_calf_joint
```

Fixed foot joints and the imported root joint are not used as policy actions.

Important engineering steps included:

- removing or deactivating the imported fixed `root_joint`
- applying `ArticulationRootAPI` to the robot root
- enabling contact sensors
- repairing foot collision support
- mapping body names to Flip-specific links:
  - `base_link`
  - `.*_foot_link`
  - `.*_hip_link`
  - `.*_thigh_link`
  - `.*_calf_link`

## Repository Structure

```text
.
├── assets/
│   └── flip/
│       └── flip_floating_articulation.usd
├── isaaclab_task/
│   └── flip/
│       ├── __init__.py
│       ├── flip_env_cfg.py
│       ├── flip_robot_cfg.py
│       └── agents/
│           ├── __init__.py
│           └── rsl_rl_ppo_cfg.py
├── scripts/
│   ├── install_flip_task.sh
│   ├── play_flip_keyboard.py
│   ├── make_flip_floating_v3.py
│   └── patch_flip_foot_collision.py
├── commands/
│   ├── install.md
│   ├── train.md
│   ├── play.md
│   ├── keyboard_control.md
│   └── tensorboard.md
├── docs/
│   └── technical_stack.md
├── models/
│   └── flip_latest.pt
├── media/
│   ├── screenshots/
│   ├── gifs/
│   └── videos/
└── README.md
```

## Results

### Training Curve

![Mean Reward](media/screenshots/tensorboard_mean_reward.png)

### Training Metrics

![Training Metrics](media/screenshots/training_metrics.png)

### Demo GIF

![Flip Demo](media/gifs/flip_demo.gif)

### Demo Video

```text
media/videos/flip_demo.mp4
```

## Installation

See:

```text
commands/install.md
```

Basic installation command:

```bash
bash scripts/install_flip_task.sh /home/robot/l_lab/IsaacLab
```

After installation, verify task registration:

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

## Training

See:

```text
commands/train.md
```

Example command:

```bash
cd /home/robot/l_lab/IsaacLab

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py \
  --task Isaac-Velocity-Flat-Flip-v0 \
  --num_envs 4096 \
  --headless \
  --max_iterations 8000
```

## Playback

See:

```text
commands/play.md
```

Example command:

```bash
cd /home/robot/l_lab/IsaacLab

CKPT=$(find logs/rsl_rl/flip_flat_go2_metrics -type f \( -name "model_*.pt" -o -name "*.pt" \) | sort -V | tail -n 1)

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py \
  --task Isaac-Velocity-Flat-Flip-v0 \
  --checkpoint "$CKPT" \
  --num_envs 16
```

## Keyboard Control

See:

```text
commands/keyboard_control.md
```

A custom keyboard playback script is included:

```text
scripts/play_flip_keyboard.py
```

It overrides the robot's `base_velocity` command during playback, allowing manual planar velocity control.

## TensorBoard

See:

```text
commands/tensorboard.md
```

Example command:

```bash
cd /home/robot/l_lab/IsaacLab

tensorboard \
  --logdir logs/rsl_rl/flip_flat_go2_metrics \
  --port 6006 \
  --bind_all
```

## Model

The trained model checkpoint is stored in:

```text
models/flip_latest.pt
```

## Notes

This repository is intended as a reproducible robotics RL project overlay, not a full Isaac Lab distribution.

Users should install Isaac Lab and robot_lab separately, then copy the Flip task configuration from this repository into their local Isaac Lab task directory using:

```bash
bash scripts/install_flip_task.sh /path/to/IsaacLab
```

