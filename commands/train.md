# Training

Run training from the Isaac Lab root directory.

```bash
cd /home/robot/l_lab/IsaacLab

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py \
  --task Isaac-Velocity-Flat-Flip-v0 \
  --num_envs 4096 \
  --headless \
  --max_iterations 8000
```

Training logs will be saved under:

```text
logs/rsl_rl/flip_flat_go2_metrics/
```

## TensorBoard

```bash
tensorboard \
  --logdir logs/rsl_rl/flip_flat_go2_metrics \
  --port 6006 \
  --bind_all
```

Open:

```text
http://localhost:6006
```
