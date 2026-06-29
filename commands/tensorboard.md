# TensorBoard

Start TensorBoard from the Isaac Lab root directory:

```bash
cd /home/robot/l_lab/IsaacLab

tensorboard \
  --logdir logs/rsl_rl/flip_flat_go2_metrics \
  --port 6006 \
  --bind_all
```

Open in browser:

```text
http://localhost:6006
```

## Recommended Metrics

```text
Train/mean_reward
Train/mean_episode_length
Episode_Reward/track_lin_vel_xy_exp
Episode_Reward/track_ang_vel_z_exp
Metrics/base_velocity/error_vel_xy
Metrics/base_velocity/error_vel_yaw
Episode_Termination/time_out
Episode_Reward/feet_slide
Episode_Reward/action_rate_l2
Episode_Reward/undesired_contacts
```

## How to Read the Curves

- `Train/mean_reward`: should generally increase.
- `Episode_Termination/time_out`: closer to `1.0` means the robot survives the full episode.
- `Metrics/base_velocity/error_vel_xy`: lower is better.
- `Metrics/base_velocity/error_vel_yaw`: lower is better.
- `Episode_Reward/feet_slide`: should not become strongly negative.
- `Episode_Reward/undesired_contacts`: should stay close to zero.
