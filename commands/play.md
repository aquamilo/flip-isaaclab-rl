# Playback

Find the latest checkpoint:

```bash
cd /home/robot/l_lab/IsaacLab

CKPT=$(find logs/rsl_rl/flip_flat_go2_metrics -type f \( -name "model_*.pt" -o -name "*.pt" \) | sort -V | tail -n 1)

echo "$CKPT"
```

Play the trained policy:

```bash
./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py \
  --task Isaac-Velocity-Flat-Flip-v0 \
  --checkpoint "$CKPT" \
  --num_envs 16
```

Do not use `--headless` if you want to watch the robot in the simulator window.
