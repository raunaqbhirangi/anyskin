import time
import numpy as np
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from datetime import datetime
from reskin_sensor import ReSkinProcess
import argparse

if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser(description="Test code to run a ReSkin streaming process in the background. Allows data to be collected without code blocking")
    parser.add_argument("-p", "--port", type=str, help="port to which the microcontroller is connected", default="/dev/cu.usbmodem1101")
    parser.add_argument("-f", "--file", type=str, help="path to load data from", default=None)
    parser.add_argument("-v", "--viz_mode", type=str, help="visualization mode", default="3d_viz", choices=["magnitude", "3d_viz"])
    parser.add_argument("-s", "--scaling", type=float, help="scaling factor for visualization", default=7.0)
    parser.add_argument('-r', '--record', action='store_true', help='record data')
    args = parser.parse_args()
    # fmt: on
    if args.file is None:
        sensor_stream = ReSkinProcess(
            num_mags=5,
            port=args.port,
        )
        # Start sensor stream
        sensor_stream.start()
        time.sleep(1.0)
        filename = "data/data_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    else:
        load_data = np.loadtxt(args.file)

    pygame.init()
    bg_image_path = "./images/viz_bg.png"
    # bg_image = plt.imread("anyskin.png")
    bg_image = pygame.image.load(bg_image_path)
    image_width, image_height = bg_image.get_size()
    aspect_ratio = image_height / image_width
    desired_width = 400
    desired_height = int(desired_width * aspect_ratio)

    chip_locations = np.array(
        [
            [204, 222],  # center
            [130, 222],  # left
            [279, 222],  # right
            [204, 157],  # up
            [204, 290],  # down
        ]
    )
    chip_xy_rotations = np.array([-np.pi / 2, -np.pi / 2, np.pi, np.pi / 2, 0.0])

    # Resize the background image to the new dimensions
    bg_image = pygame.transform.scale(bg_image, (desired_width, desired_height))
    # Create the pygame display window
    window = pygame.display.set_mode((desired_width, desired_height), pygame.SRCALPHA)
    background_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)
    background_color = (234, 237, 232, 255)
    background_surface.fill(background_color)
    background_surface.blit(bg_image, (0, 0))
    pygame.display.set_caption("Sensor Data Visualization")

    def visualize_data(data):
        data = data.reshape(-1, 3)
        data_mag = np.linalg.norm(data, axis=1)
        # print(angles)
        # Draw the chip locations
        for magid, chip_location in enumerate(chip_locations):
            if args.viz_mode == "magnitude":
                pygame.draw.circle(
                    window, (255, 83, 72), chip_location, data_mag[magid] / args.scaling
                )
            elif args.viz_mode == "3d_viz":
                if data[magid, -1] < 0:
                    width = 2
                else:
                    width = 0
                pygame.draw.circle(
                    window,
                    (255, 0, 0),
                    chip_location,
                    np.abs(data[magid, -1]) / args.scaling,
                    width,
                )
                arrow_start = chip_location
                rotation_mat = np.array(
                    [
                        [
                            np.cos(chip_xy_rotations[magid]),
                            -np.sin(chip_xy_rotations[magid]),
                        ],
                        [
                            np.sin(chip_xy_rotations[magid]),
                            np.cos(chip_xy_rotations[magid]),
                        ],
                    ]
                )
                data_xy = np.dot(rotation_mat, data[magid, :2])
                arrow_end = (
                    chip_location[0] + data_xy[0] / args.scaling,
                    chip_location[1] + data_xy[1] / args.scaling,
                )
                pygame.draw.line(window, (0, 255, 0), arrow_start, arrow_end, 2)

    def get_baseline():
        baseline_data = sensor_stream.get_data(num_samples=5)
        baseline_data = np.array(baseline_data)[:, 1:]
        baseline = np.mean(baseline_data, axis=0)
        return baseline

    frames = []

    def capture_frame(screen, frame_num):
        filename = f"frame_{frame_num}.png"
        pygame.image.save(screen, filename)  # Save the current screen as a PNG file
        frames.append(filename)  # Keep track of the saved frames

    time.sleep(0.1)
    if args.file is None:
        baseline = get_baseline()
    frame_num = 0
    running = True
    data = []
    data_len = 30000
    data_offset = 0
    start_time = time.time()
    clock = pygame.time.Clock()
    FPS = 60
    while running:
        # window.blit(bg_image, (0, 0))
        window.blit(background_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(f"Mouse clicked at ({x}, {y})")
            # Check if user pressed b
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    baseline_data = sensor_stream.get_data(num_samples=5)
                    baseline_data = np.array(baseline_data)[:, 1:]
                    baseline = np.mean(baseline_data, axis=0)
        if args.file is not None:
            sensor_data = load_data[data_len]
            data_len += 24
            baseline = np.zeros_like(sensor_data)
            # print(f"curr_time: {time.time() - start_time}")
        else:
            sensor_data = sensor_stream.get_data(num_samples=1)[0][1:]
            data.append(sensor_data - baseline)
        visualize_data(sensor_data - baseline)
        frame_num += 1
        # print(sensor_data - baseline)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    if args.file is None:
        sensor_stream.pause_streaming()
        sensor_stream.join()
        data = np.array(data)
        if args.record:
            np.savetxt(f"{filename}.txt", data)
