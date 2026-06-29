from isaaclab.utils import configclass
import isaaclab.sim as sim_utils

from robot_lab.tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg

from .flip_robot_cfg import FLIP_CFG


@configclass
class FlipEnvCfg(LocomotionVelocityRoughEnvCfg):
    """Flip flat velocity task, Go2-style metrics/rewards."""

    base_link_name = "base_link"
    foot_link_name = ".*_foot_link"

    # Match Flip's real 12 controllable joints.
    # Do NOT include fixed foot joints or root_joint.
    joint_names = [
        "FR_hip_joint", "FR_thigh_joint", "FR_calf_joint",
        "FL_hip_joint", "FL_thigh_joint", "FL_calf_joint",
        "RR_hip_joint", "RR_thigh_joint", "RR_calf_joint",
        "RL_hip_joint", "RL_thigh_joint", "RL_calf_joint",
    ]

    def __post_init__(self):
        super().__post_init__()

        # ------------------------------ Scene ------------------------------
        self.scene.robot = FLIP_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Flip base is base_link, not base.
        if self.scene.height_scanner is not None:
            self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/" + self.base_link_name
        if self.scene.height_scanner_base is not None:
            self.scene.height_scanner_base.prim_path = "{ENV_REGEX_NS}/Robot/" + self.base_link_name

        # Use flat ground first, like Go2 flat.
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None
        self.scene.terrain.physics_material = sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="multiply",
            restitution_combine_mode="multiply",
            static_friction=1.0,
            dynamic_friction=1.0,
            restitution=0.0,
        )
        self.sim.physics_material = self.scene.terrain.physics_material

        # No height scan on flat terrain.
        self.scene.height_scanner = None
        self.observations.policy.height_scan = None
        self.observations.critic.height_scan = None

        # No terrain curriculum on flat terrain.
        self.curriculum.terrain_levels = None

        # ------------------------------ Observations ------------------------------
        self.observations.policy.base_lin_vel.scale = 2.0
        self.observations.policy.base_ang_vel.scale = 0.25
        self.observations.policy.joint_pos.scale = 1.0
        self.observations.policy.joint_vel.scale = 0.05

        # Same as Go2: policy does not directly observe base linear velocity.
        self.observations.policy.base_lin_vel = None

        self.observations.policy.joint_pos.params["asset_cfg"].joint_names = self.joint_names
        self.observations.policy.joint_vel.params["asset_cfg"].joint_names = self.joint_names
        self.observations.critic.joint_pos.params["asset_cfg"].joint_names = self.joint_names
        self.observations.critic.joint_vel.params["asset_cfg"].joint_names = self.joint_names

        # ------------------------------ Actions ------------------------------
        # Go2-style action scale: smaller hip, larger thigh/calf.
        self.actions.joint_pos.scale = {".*_hip_joint": 0.125, "^(?!.*_hip_joint).*": 0.25}
        self.actions.joint_pos.clip = {".*": (-100.0, 100.0)}
        self.actions.joint_pos.joint_names = self.joint_names

        # ------------------------------ Commands ------------------------------
        # Random 2D velocity commands. Not forward-only.
        self.commands.base_velocity.ranges.lin_vel_x = (-1.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (-1.0, 1.0)
        self.commands.base_velocity.ranges.ang_vel_z = (-0.8, 0.8)

        # Random command vector lasts 3x longer than before.
        self.commands.base_velocity.resampling_time_range = (25.0, 35.0)

        # Use direct yaw velocity command instead of heading command.
        self.commands.base_velocity.heading_command = False
        self.commands.base_velocity.rel_heading_envs = 0.0
        self.commands.base_velocity.rel_standing_envs = 0.0

        # ------------------------------ Events ------------------------------
        self.events.randomize_reset_base.params = {
            "pose_range": {
                "x": (-0.5, 0.5),
                "y": (-0.5, 0.5),
                "z": (0.0, 0.2),
                "roll": (-3.14, 3.14),
                "pitch": (-3.14, 3.14),
                "yaw": (-3.14, 3.14),
            },
            "velocity_range": {
                "x": (-0.5, 0.5),
                "y": (-0.5, 0.5),
                "z": (-0.5, 0.5),
                "roll": (-0.5, 0.5),
                "pitch": (-0.5, 0.5),
                "yaw": (-0.5, 0.5),
            },
        }

        self.events.randomize_rigid_body_material.params["asset_cfg"].body_names = [".*"]
        self.events.randomize_rigid_body_material.params["static_friction_range"] = (0.8, 1.5)
        self.events.randomize_rigid_body_material.params["dynamic_friction_range"] = (0.6, 1.2)
        self.events.randomize_rigid_body_material.params["restitution_range"] = (0.0, 0.05)

        self.events.randomize_rigid_body_mass_base.params["asset_cfg"].body_names = [self.base_link_name]
        self.events.randomize_rigid_body_mass_others.params["asset_cfg"].body_names = [
            f"^(?!.*{self.base_link_name}).*"
        ]
        self.events.randomize_com_positions.params["asset_cfg"].body_names = [self.base_link_name]
        self.events.randomize_apply_external_force_torque.params["asset_cfg"].body_names = [self.base_link_name]
        self.events.randomize_actuator_gains.params["asset_cfg"].joint_names = self.joint_names

        # ------------------------------ Rewards ------------------------------
        # General
        self.rewards.is_terminated.weight = 0.0

        # Root penalties
        self.rewards.lin_vel_z_l2.weight = -2.0
        self.rewards.ang_vel_xy_l2.weight = -0.05
        self.rewards.flat_orientation_l2.weight = 0.0

        self.rewards.base_height_l2.weight = 0.0
        self.rewards.base_height_l2.params["sensor_cfg"] = None
        self.rewards.base_height_l2.params["target_height"] = 0.33
        self.rewards.base_height_l2.params["asset_cfg"].body_names = [self.base_link_name]

        self.rewards.body_lin_acc_l2.weight = 0.0
        self.rewards.body_lin_acc_l2.params["asset_cfg"].body_names = [self.base_link_name]

        # Joint penalties
        self.rewards.joint_torques_l2.weight = -2.5e-5
        self.rewards.joint_torques_l2.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.joint_vel_l2.weight = 0.0
        self.rewards.joint_vel_l2.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.joint_acc_l2.weight = -5.0e-7
        self.rewards.joint_acc_l2.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.joint_pos_limits.weight = -5.0
        self.rewards.joint_pos_limits.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.joint_vel_limits.weight = 0.0
        self.rewards.joint_vel_limits.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.joint_power.weight = -2.0e-5
        self.rewards.joint_power.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.stand_still.weight = -2.0
        self.rewards.stand_still.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.joint_pos_penalty.weight = -1.0
        self.rewards.joint_pos_penalty.params["asset_cfg"].joint_names = self.joint_names

        self.rewards.joint_mirror.weight = -0.05
        self.rewards.joint_mirror.params["mirror_joints"] = [
            ["FR_(hip|thigh|calf).*", "RL_(hip|thigh|calf).*"],
            ["FL_(hip|thigh|calf).*", "RR_(hip|thigh|calf).*"],
        ]

        # Action penalties
        self.rewards.action_rate_l2.weight = -0.015

        # Contact sensor
        self.rewards.undesired_contacts.weight = -1.0
        self.rewards.undesired_contacts.params["sensor_cfg"].body_names = [f"^(?!.*{self.foot_link_name}).*"]

        self.rewards.contact_forces.weight = -1.5e-4
        self.rewards.contact_forces.params["sensor_cfg"].body_names = [self.foot_link_name]

        # Velocity tracking
        self.rewards.track_lin_vel_xy_exp.weight = 3.0
        self.rewards.track_ang_vel_z_exp.weight = 2.5

        # Feet rewards
        self.rewards.feet_air_time.weight = 0.1
        self.rewards.feet_air_time.params["threshold"] = 0.5
        self.rewards.feet_air_time.params["sensor_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_air_time_variance.weight = -1.0
        self.rewards.feet_air_time_variance.params["sensor_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_contact.weight = 0.0
        self.rewards.feet_contact.params["sensor_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_contact_without_cmd.weight = 0.1
        self.rewards.feet_contact_without_cmd.params["sensor_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_stumble.weight = 0.0
        self.rewards.feet_stumble.params["sensor_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_slide.weight = -0.1
        self.rewards.feet_slide.params["sensor_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_slide.params["asset_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_height.weight = 0.0
        self.rewards.feet_height.params["target_height"] = 0.05
        self.rewards.feet_height.params["asset_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_height_body.weight = -5.0
        self.rewards.feet_height_body.params["target_height"] = -0.2
        self.rewards.feet_height_body.params["asset_cfg"].body_names = [self.foot_link_name]

        self.rewards.feet_gait.weight = 0.5
        self.rewards.feet_gait.params["synced_feet_pair_names"] = (
            ("FL_foot_link", "RR_foot_link"),
            ("FR_foot_link", "RL_foot_link"),
        )

        self.rewards.upward.weight = 1.0

        # ------------------------------ Terminations ------------------------------
        # Same as Go2: do not kill too aggressively for early locomotion learning.
        self.terminations.illegal_contact = None

        # ------------------------------ Curriculums ------------------------------
        self.curriculum.command_levels_lin_vel = None
        self.curriculum.command_levels_ang_vel = None
        self.curriculum.terrain_levels = None


        # ------------------------------------------------------------
        # Warm-start settings for Flip:
        # Do not spawn many robots upside-down at the beginning.
        # ------------------------------------------------------------
        self.events.randomize_reset_base.params = {
            "pose_range": {
                "x": (-0.2, 0.2),
                "y": (-0.2, 0.2),
                "z": (0.0, 0.05),
                "roll": (-0.05, 0.05),
                "pitch": (-0.05, 0.05),
                "yaw": (-3.14, 3.14),
            },
            "velocity_range": {
                "x": (-0.1, 0.1),
                "y": (-0.1, 0.1),
                "z": (-0.05, 0.05),
                "roll": (-0.05, 0.05),
                "pitch": (-0.05, 0.05),
                "yaw": (-0.1, 0.1),
            },
        }

        # Temporarily disable hard domain randomization for early Flip training.
        self.events.randomize_apply_external_force_torque = None
        self.events.randomize_push_robot = None
        self.events.randomize_actuator_gains = None

        # Keep material randomization mild.
        self.events.randomize_rigid_body_material.params["static_friction_range"] = (0.9, 1.2)
        self.events.randomize_rigid_body_material.params["dynamic_friction_range"] = (0.8, 1.1)
        self.events.randomize_rigid_body_material.params["restitution_range"] = (0.0, 0.02)

        # Keep mass / COM randomization mild.
        self.events.randomize_rigid_body_mass_base.params["mass_distribution_params"] = (-0.2, 0.5)
        self.events.randomize_rigid_body_mass_others.params["mass_distribution_params"] = (0.9, 1.1)
        self.events.randomize_com_positions.params["com_range"] = {
            "x": (-0.01, 0.01),
            "y": (-0.01, 0.01),
            "z": (-0.01, 0.01),
        }

        # Start with moderate planar commands.
        self.commands.base_velocity.ranges.lin_vel_x = (-0.8, 0.8)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.8, 0.8)
        self.commands.base_velocity.ranges.ang_vel_z = (-0.6, 0.6)
        self.commands.base_velocity.resampling_time_range = (25.0, 35.0)

        # Keep only non-zero rewards so logs look like Go2 logs.
        self.disable_zero_weight_rewards()
