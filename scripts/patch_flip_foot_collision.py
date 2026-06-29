from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade

try:
    from pxr import PhysxSchema
except Exception:
    PhysxSchema = None


src = "/home/robot/l_lab/flip_description/urdf/flip/flip.usd"
dst = "/home/robot/l_lab/flip_description/urdf/flip/flip_collision.usd"

stage = Usd.Stage.Open(src)

foot_names = [
    "FL_foot_link",
    "FR_foot_link",
    "RL_foot_link",
    "RR_foot_link",
]

# High friction material
mat_path = "/PhysicsMaterials/high_friction"
mat = UsdShade.Material.Define(stage, mat_path)
mat_api = UsdPhysics.MaterialAPI.Apply(mat.GetPrim())
mat_api.CreateStaticFrictionAttr().Set(3.0)
mat_api.CreateDynamicFrictionAttr().Set(2.5)
mat_api.CreateRestitutionAttr().Set(0.0)

patched = 0

for prim in list(stage.Traverse()):
    name = prim.GetName()

    if name not in foot_names:
        continue

    foot_path = str(prim.GetPath())
    print(f"Found foot link: {foot_path}")

    # Bind high friction material to foot link
    UsdShade.MaterialBindingAPI.Apply(prim).Bind(mat)

    # Add an explicit spherical collider under the foot link
    sphere_path = foot_path + "/foot_collision_sphere"
    sphere = UsdGeom.Sphere.Define(stage, sphere_path)
    sphere.CreateRadiusAttr(0.035)

    # Put sphere at the foot link origin
    xform = UsdGeom.Xformable(sphere.GetPrim())
    xform.AddTranslateOp().Set((0.0, 0.0, 0.0))

    # Hide visual sphere but keep collision
    UsdGeom.Imageable(sphere.GetPrim()).MakeInvisible()

    # Enable collision
    UsdPhysics.CollisionAPI.Apply(sphere.GetPrim())

    if PhysxSchema is not None:
        physx_col = PhysxSchema.PhysxCollisionAPI.Apply(sphere.GetPrim())
        physx_col.CreateContactOffsetAttr().Set(0.02)
        physx_col.CreateRestOffsetAttr().Set(0.0)

    UsdShade.MaterialBindingAPI.Apply(sphere.GetPrim()).Bind(mat)

    patched += 1

print(f"Patched foot colliders: {patched}")

stage.GetRootLayer().Export(dst)
print(f"Saved patched USD to: {dst}")

simulation_app.close()
