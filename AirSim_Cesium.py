# X val of first image of first row: -269601.5
# X val of last image of first row: 314498.5

# In settings.json first activate computer vision mode: 
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode

# SAVES TO: C:\Users\haven\AppData\Local\Temp\airsim_drone

#import setup_path 
import airsim
import pprint
import tempfile
import os
import time

pp = pprint.PrettyPrinter(indent=4)

client = airsim.VehicleClient()

for camera_id in range(4):
    camera_info = client.simGetCameraInfo(str(camera_id))
    print("CameraInfo %d: %s" % (camera_id, pp.pprint(camera_info)))

tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
print ("Saving images to %s" % tmp_dir)
try:
    for n in range(3):
        os.makedirs(os.path.join(tmp_dir, str(n)))
except OSError:
    if not os.path.isdir(tmp_dir):
        raise
modifier = 1
y = 59/modifier
z = 100/modifier
r = 10*modifier
time.sleep(0.3)

current_position = client.simGetVehiclePose().position

objects = client.simListSceneObjects()
# NE: 9 NW: 10 SW: 11 SE: 12
NE = objects[9]
NW = objects[10]
SE = objects[12]
SW = objects[11]

NE_pos = client.simGetObjectPose(NE)
NW_pos = client.simGetObjectPose(NW)
SE_pos = client.simGetObjectPose(SE)
SW_pos = client.simGetObjectPose(SW)

print("NORTHEAST: ", NE_pos.position)
print("NORTHWEST: ", NW_pos.position)
print("SOUTHEAST: ", SE_pos.position)
print("SOUTHWEST: ", SW_pos.position)

# X-Min: SW_pos.position.x_val (-606600.4375)  
# X-Max: NE_pos.position.x_val (0)
# Y-Min: NW_pos.position.y_val (-1777.0)
# Y-Max: SE_pos.position.y_val (423680.9375)

def east_to_west(current_position, j):
    x = 1
    while current_position.x_val > SW_pos.position.x_val:
        client.simSetVehiclePose(airsim.Pose(airsim.Vector3r((-1000*y),0,0), airsim.to_quaternion(2*-0.8,0, 0)), True)
        current_position.x_val = current_position.x_val - 1000*y
        time.sleep(3)
        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene),
            #airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, False),
            #airsim.ImageRequest("2", airsim.ImageType.Scene)
            ])
        for i, response in enumerate(responses):
            if response.pixels_as_float:
                #print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_float), pprint.pformat(response.camera_position)))
                airsim.write_pfm(os.path.normpath(os.path.join(tmp_dir, "P" + str(j) + "_" + str(x) + "_" + str(i) + '.pfm')), airsim.get_pfm_array(response))
            else:
                #print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_uint8), pprint.pformat(response.camera_position)))
                airsim.write_file(os.path.normpath(os.path.join(tmp_dir, str(i), "P" + str(j) + "_" + str(x) + "_" + str(i) + '.png')), response.image_data_uint8)

        pose = client.simGetVehiclePose()
        pp.pprint(current_position)

        time.sleep(3)
        x = x + 1

    return current_position

def west_to_east(current_position, j):
    x = 1
    while current_position.x_val < NE_pos.position.x_val:
        client.simSetVehiclePose(airsim.Pose(airsim.Vector3r((1000*y),0,0), airsim.to_quaternion(2*-0.8,0, 0)), True)
        current_position.x_val = current_position.x_val + 1000*y
        time.sleep(3)
        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene),
            #airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, False),
            #airsim.ImageRequest("2", airsim.ImageType.Scene)
            ])
        
        for i, response in enumerate(responses):
            if response.pixels_as_float:
                #print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_float), pprint.pformat(response.camera_position)))
                airsim.write_pfm(os.path.normpath(os.path.join(tmp_dir, "P" + str(j) + "_" + str(x) + "_" + str(i) + '.pfm')), airsim.get_pfm_array(response))
            else:
                #print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_uint8), pprint.pformat(response.camera_position)))
                airsim.write_file(os.path.normpath(os.path.join(tmp_dir, str(i), "P" + str(j) + "_" + str(x) + "_" + str(i) + '.png')), response.image_data_uint8)

        pose = client.simGetVehiclePose()
        pp.pprint(current_position)

        time.sleep(3)
        x = x + 1

    return current_position

def north_to_south(current_position,j):
    x = 0
    client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0,(1000*y),0), airsim.to_quaternion(2*-0.8,0, 0)), True)
    current_position.y_val = current_position.y_val + 1000*y
    time.sleep(3)
    responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene),
            #airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, False),
            #airsim.ImageRequest("2", airsim.ImageType.Scene)
            ])

    for i, response in enumerate(responses):
        if response.pixels_as_float:
            #print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_float), pprint.pformat(response.camera_position)))
            airsim.write_pfm(os.path.normpath(os.path.join(tmp_dir, "P" + str(j) + "_" + str(x) + "_" + str(i) + '.pfm')), airsim.get_pfm_array(response))
        else:
            #print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_uint8), pprint.pformat(response.camera_position)))
            airsim.write_file(os.path.normpath(os.path.join(tmp_dir, str(i), "P" + str(j) + "_" + str(x) + "_" + str(i) + '.png')), response.image_data_uint8)

    pose = client.simGetVehiclePose()
    pp.pprint(current_position)

    time.sleep(3)

    return current_position


j = 1
while current_position.y_val < SE_pos.position.y_val:

    current_position = east_to_west(current_position, j)

    j = j + 1

    current_position = north_to_south(current_position,j)

    current_position = west_to_east(current_position,j)

    j = j + 1

    current_position = north_to_south(current_position,j)

print("FINISHED")
