# Technical Stack

## Simulator and RL Framework

- Isaac Sim / Isaac Lab 5.1
- robot_lab locomotion velocity task framework
- RSL-RL PPO
- Gymnasium task registration
- Isaac Lab manager-based RL environment

## Robot

- Robot: Flip quadruped
- Asset type: USD articulation
- Base type: floating base
- Actuated joints: 12

The policy controls the following joint groups:

```text
.*_hip_joint
.*_thigh_joint
.*_calf_joint
```

Fixed foot joints are not used as policy actions.

## Task

The task is planar velocity tracking.

The robot receives randomized commands:

```text
lin_vel_x
lin_vel_y
ang_vel_z
```

The command resampling interval is:

```text
25.0 to 35.0 seconds
```

## Policy

- Algorithm: PPO
- Library: RSL-RL
- Actor network: `[512, 256, 128]`
- Critic network: `[512, 256, 128]`
- Activation: ELU
- Control mode: joint position target

## Key Engineering Fixes

Several fixes were needed to make the imported Flip USD usable for RL training:

1. Removed or deactivated the imported fixed `root_joint`.
2. Applied `ArticulationRootAPI` to the robot root.
3. Enabled contact sensors.
4. Added or repaired foot collision support.
5. Mapped Go2-style reward terms to Flip body names:
   - `base_link`
   - `.*_foot_link`
   - `.*_hip_link`
   - `.*_thigh_link`
   - `.*_calf_link`
6. Restricted actions to the 12 actuated joints:
   - hip
   - thigh
   - calf

## Training Output

The training logs include Go2-style metrics such as:

```text
Episode_Reward/track_lin_vel_xy_exp
Episode_Reward/track_ang_vel_z_exp
Episode_Reward/feet_air_time
Episode_Reward/feet_slide
Metrics/base_velocity/error_vel_xy
Metrics/base_velocity/error_vel_yaw
Episode_Termination/time_out
```

## Author Contribution

Author: Chunmiao Li

University of California, Berkeley

This project is not a direct reproduction of an existing built-in Isaac Lab robot task. The Flip robot is a custom, non-standard quadruped platform rather than a common public benchmark robot.

The author implemented the core integration work, including:

- Isaac Lab task registration
- Flip robot articulation configuration
- robot_lab-style locomotion environment adaptation
- Go2-style reward and metric mapping
- floating-base USD repair
- foot collision/contact sensor setup
- PPO training configuration
- TensorBoard evaluation workflow
- keyboard-controlled playback script

This repository is designed to demonstrate a complete robotics RL workflow that can be reviewed for research, internship, and engineering applications.
