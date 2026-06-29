# Keyboard Control

This project includes a custom keyboard playback script:

```text
scripts/play_flip_keyboard.py
```

The script allows manual control of the trained Flip policy by overriding the `base_velocity` command during policy rollout.

## Install the Keyboard Script

Copy the script into the Isaac Lab RSL-RL script directory:

```bash
cp scripts/play_flip_keyboard.py \
/home/robot/l_lab/IsaacLab/scripts/reinforcement_learning/rsl_rl/
```

## Run Keyboard-Controlled Playback

Run from the Isaac Lab root directory:

```bash
cd /home/robot/l_lab/IsaacLab

CKPT=$(find logs/rsl_rl/flip_flat_go2_metrics -type f \( -name "model_*.pt" -o -name "*.pt" \) | sort -V | tail -n 1)

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play_flip_keyboard.py \
  --task Isaac-Velocity-Flat-Flip-v0 \
  --checkpoint "$CKPT" \
  --num_envs 1
```

Do not use `--headless`, because keyboard control requires the Isaac Sim window.

## Keyboard Controls

Click the Isaac Sim window first so that it receives keyboard input.

Recommended controls:

```text
↑ / Numpad 8     move forward
↓ / Numpad 2     move backward
← / Numpad 4     move left
→ / Numpad 6     move right
Z / Numpad 7     rotate left
X / Numpad 9     rotate right
```

The command sent to the policy is:

```text
[v_x, v_y, omega_z]
```

where:

```text
v_x      forward / backward velocity
v_y      lateral velocity
omega_z  yaw angular velocity
```

## Behavior

During keyboard playback:

- random command refreshing is disabled
- timeout reset is disabled
- terrain out-of-bounds reset is disabled
- illegal contact reset is disabled
- the robot position will not automatically refresh while being controlled

This makes the playback mode suitable for manual demonstrations and video recording.

## Notes

If the robot does not respond to keyboard input:

1. Click the Isaac Sim viewport.
2. Make sure the window has focus.
3. Avoid running in `--headless` mode.
4. If using remote desktop software, key-hold behavior may not work reliably.
5. Try pressing keys repeatedly if holding keys does not produce continuous motion.

If the robot falls, the script may not automatically reset it because reset terms are disabled for manual control. Restart the playback script if needed.
