"""Binary morphology + convolution kernel demo.

Part 1 (binary morphology): grayscale -> threshold to binary -> erosion,
dilation, opening, closing, hit-or-miss, boundary extraction,
skeletonization, and pruning.

Part 2 (kernels): classic 3x3 convolution kernels (blur, sharpen, edge
detection, Sobel, emboss) applied directly to the grayscale image.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

INPUT_PATH = "me.JPG.jpg"
MORPH_OUTPUT_DIR = "morphology_output"
KERNEL_OUTPUT_DIR = "kernel_output"
STRUCTURING_ELEMENT = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

CONV_KERNELS = {
    "box_blur": np.ones((3, 3), dtype=np.float32) / 9,
    "gaussian_blur": np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32) / 16,
    "sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32),
    "laplacian_edges": np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32),
    "sobel_x": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32),
    "sobel_y": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32),
    "emboss": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]], dtype=np.float32),
}


# --- Part 1: binary morphology -------------------------------------------

def to_binary(gray):
    """Otsu picks the threshold value T automatically from the image
    histogram; pixels below T become 0, pixels at/above T become 1."""
    _, binary = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def boundary(binary, kernel):
    """boundary = A - erosion(A)."""
    eroded = cv2.erode(binary, kernel)
    return cv2.subtract(binary, eroded)


def isolated_point_hitmiss(binary):
    """Hit-or-miss with a foreground SE (center=1) and background SE (all 8
    neighbors=-1) finds foreground pixels with no foreground neighbors."""
    kernel = np.array(
        [[-1, -1, -1],
         [-1,  1, -1],
         [-1, -1, -1]],
        dtype=np.int8,
    )
    return cv2.morphologyEx(binary, cv2.MORPH_HITMISS, kernel)


def skeletonize(binary):
    """cv2.ximgproc.thinning silently returns an empty image unless the input
    is scaled to 0/255, so binary (0/1) is rescaled before passing it in."""
    thinned = cv2.ximgproc.thinning(binary * 255, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return (thinned > 0).astype(np.uint8)


def prune(skeleton, iterations=5):
    """Iteratively remove endpoints (foreground pixels with exactly one
    foreground 8-neighbor) to clean up short spurs left after thinning."""
    pruned = skeleton.copy()
    neighbor_kernel = np.array(
        [[1, 1, 1],
         [1, 0, 1],
         [1, 1, 1]],
        dtype=np.uint8,
    )
    for _ in range(iterations):
        mask = (pruned > 0).astype(np.uint8)
        neighbor_counts = cv2.filter2D(mask, -1, neighbor_kernel, borderType=cv2.BORDER_CONSTANT)
        endpoints = (mask == 1) & (neighbor_counts == 1)
        pruned[endpoints] = 0
    return pruned


def morphology_results(gray):
    binary = to_binary(gray)
    skeleton = skeletonize(binary)
    return {
        "grayscale": gray,
        "binary": binary,
        "erosion": cv2.erode(binary, STRUCTURING_ELEMENT),
        "dilation": cv2.dilate(binary, STRUCTURING_ELEMENT),
        "opening": cv2.morphologyEx(binary, cv2.MORPH_OPEN, STRUCTURING_ELEMENT),
        "closing": cv2.morphologyEx(binary, cv2.MORPH_CLOSE, STRUCTURING_ELEMENT),
        "boundary": boundary(binary, STRUCTURING_ELEMENT),
        "hitmiss_isolated_points": isolated_point_hitmiss(binary),
        "skeleton": skeleton,
        "pruned_skeleton": prune(skeleton, iterations=5),
    }


# --- Part 2: convolution kernels ------------------------------------------

def apply_conv_kernel(gray, kernel):
    """Kernels with negative weights (sharpen/edges/sobel/emboss) can produce
    negative or >255 values; filter in float64 then take the absolute value
    and clip back to 0-255 for display via convertScaleAbs."""
    filtered = cv2.filter2D(gray, cv2.CV_64F, kernel)
    return cv2.convertScaleAbs(filtered)


def kernel_results(gray):
    results = {"grayscale": gray}
    for name, kernel in CONV_KERNELS.items():
        results[name] = apply_conv_kernel(gray, kernel)
    return results


# --- Saving / display -------------------------------------------------

def save_results(results, output_dir):
    """Binary-morphology results are stored as 0/1 so the array values match
    the erode/dilate/hit-or-miss math exactly; scale to 0/255 only here, for
    writing/plotting, so they're actually visible."""
    Path(output_dir).mkdir(exist_ok=True)
    displayable = {
        name: image * 255 if image.max() <= 1 else image
        for name, image in results.items()
    }
    for name, image in displayable.items():
        cv2.imwrite(f"{output_dir}/{name}.png", image)
    print(f"Saved {len(displayable)} images to {output_dir}/")
    return displayable


def build_grid(displayable, output_dir, filename="grid.png"):
    cols = 3
    rows = -(-len(displayable) // cols)  # ceil division
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    for ax, (name, image) in zip(axes.flat, displayable.items()):
        ax.imshow(image, cmap="gray")
        ax.set_title(name)
        ax.axis("off")
    for ax in axes.flat[len(displayable):]:
        ax.axis("off")
    fig.tight_layout()
    grid_path = Path(output_dir, filename).resolve()
    fig.savefig(grid_path, dpi=150)
    print(f"Saved comparison grid to {grid_path}")
    return fig


def main():
    img = cv2.imread(INPUT_PATH)
    if img is None:
        raise SystemExit(f"Could not read image at {INPUT_PATH}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    morph_displayable = save_results(morphology_results(gray), MORPH_OUTPUT_DIR)
    build_grid(morph_displayable, MORPH_OUTPUT_DIR)

    kernel_displayable = save_results(kernel_results(gray), KERNEL_OUTPUT_DIR)
    build_grid(kernel_displayable, KERNEL_OUTPUT_DIR)

    plt.show()


if __name__ == "__main__":
    main()
