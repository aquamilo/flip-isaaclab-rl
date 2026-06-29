from isaaclab.assets import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg
import isaaclab.sim as sim_utils


FLIP_USD_PATH = "/home/robot/l_lab/flip_description/urdf/flip/flip_floating_articulation.usd"


FLIP_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=FLIP_USD_PATH,
        activate_contact_sensors=True,

        collision_props=sim_utils.CollisionPropertiesCfg(
            contact_offset=0.02,
            rest_offset=0.0,
        ),

        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),

        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=4,
        ),
    ),

    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.40),
        joint_pos={
            "FL_hip_joint": 0.10,
            "FR_hip_joint": -0.10,
            "RL_hip_joint": 0.10,
            "RR_hip_joint": -0.10,

            "FL_thigh_joint": 0.80,
            "FR_thigh_joint": 0.80,
            "RL_thigh_joint": 0.80,
            "RR_thigh_joint": 0.80,

            "FL_calf_joint": -1.50,
            "FR_calf_joint": -1.50,
            "RL_calf_joint": -1.50,
            "RR_calf_joint": -1.50,
        },
        joint_vel={".*": 0.0},
    ),

    actuators={
        "leg_motors": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*_hip_joint",
                ".*_thigh_joint",
                ".*_calf_joint",
            ],
            effort_limit_sim=120.0,
            velocity_limit_sim=80.0,
            stiffness=60.0,
            damping=2.0,
        ),
    },

    soft_joint_pos_limit_factor=0.9,
)
