from __future__ import annotations

import numpy as np
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks

def simple_edge_score(img_gray: np.ndarray) -> float:
    """
    Toy metric: fraction of edge pixels (Canny) – useful as a quick anomaly proxy.
    """
    edges = canny(img_gray, sigma=2.0)
    return float(edges.mean())

def line_presence_score(img_gray: np.ndarray) -> float:
    """
    Toy metric: strength of straight-line structures via Hough transform.
    """
    edges = canny(img_gray, sigma=2.0)
    h, theta, d = hough_line(edges)
    accums, angles, dists = hough_line_peaks(h, theta, d)
    return float(np.sum(accums)) if accums is not None else 0.0
