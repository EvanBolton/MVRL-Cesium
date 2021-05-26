import unreal
from unreal import Vector

lst_actors = unreal.EditorLevelLibrary.get_all_level_actors()
print(lst_actors)

cam = lst_actors[-1]

cam_loc = cam.get_actor_location()

print(cam_loc)
