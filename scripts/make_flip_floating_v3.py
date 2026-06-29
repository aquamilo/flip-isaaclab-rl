from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

from pxr import Usd, UsdPhysics

src = "/home/robot/l_lab/flip_description/urdf/flip/flip_collision.usd"
dst = "/home/robot/l_lab/flip_description/urdf/flip/flip_floating_articulation.usd"

stage = Usd.Stage.Open(src)
stage.SetEditTarget(stage.GetRootLayer())

robot_path = "/Flip"
root_joint_path = "/Flip/root_joint"

robot_prim = stage.GetPrimAtPath(robot_path)
root_joint_prim = stage.GetPrimAtPath(root_joint_path)

print("Before:")
print("robot valid =", robot_prim.IsValid())
print("root_joint valid =", root_joint_prim.IsValid())
if root_joint_prim.IsValid():
    print("root_joint active =", root_joint_prim.IsActive())
    print("root_joint type =", root_joint_prim.GetTypeName())

# 1. 关闭固定 base 的 root_joint
if root_joint_prim.IsValid():
    root_joint_prim.SetActive(False)

# 2. 把 ArticulationRootAPI 加到机器人根节点 /Flip
if robot_prim.IsValid():
    UsdPhysics.ArticulationRootAPI.Apply(robot_prim)
    stage.SetDefaultPrim(robot_prim)

# 3. 保存 composed stage
stage.Export(dst)

print("\nSaved to:")
print(dst)

# 4. 重新打开检查
stage2 = Usd.Stage.Open(dst)

print("\nArticulation roots:")
has_articulation_root = False
for prim in stage2.Traverse():
    if prim.HasAPI(UsdPhysics.ArticulationRootAPI):
        print("  ", prim.GetPath())
        has_articulation_root = True

print("\nActive joints:")
has_active_root_joint = False
for prim in stage2.Traverse():
    if prim.IsA(UsdPhysics.Joint):
        print("  ", prim.GetPath(), prim.GetTypeName())
        if "root_joint" in str(prim.GetPath()):
            has_active_root_joint = True

print("\nHAS_ARTICULATION_ROOT =", has_articulation_root)
print("HAS_ACTIVE_ROOT_JOINT =", has_active_root_joint)

simulation_app.close()
