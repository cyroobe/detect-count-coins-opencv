import os
import re
import cv2
import argparse
import numpy as np


def detect_coins(image_path: str, show_imgs: bool, show_centroids: bool) -> int:
    """
        Function to detect coins and their statistics
    """
    coins_img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(coins_img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    num_coins: None
    binary_img = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    circles = cv2.HoughCircles(binary_img, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=50)

    if circles is not None:
        circles = circles.round().astype("int")
        num_coins = len(circles[0])
        _, labels, stats, centroids = cv2.connectedComponentsWithStats((binary_img > 0).astype(np.uint8))

        if show_centroids:
            print(f"\nCoin Centroids:\n")
            for i in range(1, num_coins + 1):  
                area = stats[i, cv2.CC_STAT_AREA]
                centroid = centroids[i]
                print(f"   * Coin {i}: Area = {area}, Centroid = {centroid}")

        for (x, y, r) in circles[0]:
            cv2.circle(coins_img, (x, y), r, (0, 255, 0), 2)

        if show_imgs:
            cv2.imshow("Detected Coins", coins_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    return num_coins


def relative_error(true_value, estimated_value) -> float:
    """
        Function to determinate the Relative Error (RE)
    """
    return abs(true_value - estimated_value) / true_value * 100


def build_images_list(folder_path: str) -> dict:
    """
        Function to build the dictionary list with the images information
    """
    images = []
    current_dir = os.getcwd()
    img_dir = os.path.join(current_dir, folder_path)
    for filename in os.listdir(img_dir):
        if filename.endswith(".jpg"):
            coins_number = re.search(r'\D(\d+)\D', filename)
            image_path = os.path.join(img_dir, filename)
            images.append({
                "image": filename,
                "true_coins_number": int(coins_number.group(1)),
                "path": os.path.join(img_dir, filename),
            })
    return images


args_parser = argparse.ArgumentParser()

args_parser.add_argument(
    "-fp", "--folder-path", required=True,
    help="Folder for the coins images."
)

args_parser.add_argument(
    "-si", "--show-images", required=False,
    choices=["True", "False"],
    help="Specify if you want to see the images or not."
)

args_parser.add_argument(
    "-sc", "--show-centroids", required=False,
    choices=["True", "False"],
    help="Specify if you want to see the images centroids or not."
)

args = vars(args_parser.parse_args())


def main() -> None:
    coin_imgs = build_images_list(args["folder_path"])
    imgs_number = len(coin_imgs)
    total_relative_error = 0
    total_squared_error = 0
    for index, coin_img in enumerate(coin_imgs):
        print(f"\n{'-' * 10} COIN IMAGE {index + 1} {'-' * 10}")
        predicted_value = detect_coins(
          coin_img["path"], 
          bool(args["show_images"]), 
          bool(args["show_centroids"])
        )
        rel_error = relative_error(coin_img["true_coins_number"], predicted_value)
        total_relative_error += rel_error
        total_squared_error += (coin_img["true_coins_number"] - predicted_value) ** 2
        
        average_relative_error = total_relative_error / imgs_number
        mean_squared_error = total_squared_error / imgs_number
        
        print(f"\nDetected coins: {predicted_value}")
        print("True coins number: " + str(coin_img["true_coins_number"]))
        print(f'Relative Error (RE): {rel_error:.2f}%')
        print(f'Mean Square Error (MSE): {mean_squared_error:.2f}')
        print(f'Relative Error Average (REV): {average_relative_error:.2f}%')
        print(f'Mean Square Error (MSE): {mean_squared_error:.2f}\n')


if __name__ == "__main__":
    main()
