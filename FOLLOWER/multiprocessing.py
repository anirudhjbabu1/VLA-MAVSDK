import multiprocessing as mp
from ultralytics import YOLO

def detection_process(shared_dict, frame_queue):
    model = YOLO('yolo11n.pt')
    while True:
        frame = frame_queue.get()
        results = model.predict(frame, verbose=False)
        if results[0].boxes:
            # Send top detection to VLA
            shared_dict['target'] = results[0].boxes[0].xyxyn.tolist()
            shared_dict['label'] = results[0].names[int(results[0].boxes[0].cls[0])]

async def vla_brain_process(shared_dict, drone):
    while True:
        if 'target' in shared_dict:
            bbox = shared_dict['target']
            instruction = f"Follow the {shared_dict['label']} accurately."
            
            # VLA generates action based on bbox and instruction
            # Output: [vx, vy, vz, yaw_rate]
            action = openvla.predict(current_frame, bbox, instruction)
            
            # Send to MAVSDK
            await drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(action[0], action[1], action[2], action[3])
            )
        await asyncio.sleep(0.1) # 10Hz thinking
