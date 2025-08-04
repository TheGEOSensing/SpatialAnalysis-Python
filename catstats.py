#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Debangshu Banerjee
"""

import numpy as np

def catstats(ref: np.ndarray, pred: np.ndarray):
    """
    Compute categorical statistics between two 3D datasets (e.g., observations vs. predictions).
    ---------------------------------------------------------------------------------------------

    Parameters
    ----------
    ref : np.ndarray
        3D reference dataset (latitude x longitude x time)
    pred : np.ndarray
        3D predicted dataset (same shape as `ref`)

    Returns
    -------
    dict
        Dictionary containing:
        - POD   : Probability of Detection
        - FAR   : False Alarm Ratio
        - POFD  : Probability of False Detection
        - FBI   : Frequency Bias Index
        - ACC   : Accuracy
        - CSI   : Critical Success Index
        - TSS   : True Skill Statistic (Hanssen and Kuipers Discriminant)
        - HSS   : Heidke Skill Score
    ---------------------------------------------------------------------------------------------
    """

    # --- Input validation ---
    if not (isinstance(ref, np.ndarray) and isinstance(pred, np.ndarray)):
        raise TypeError("Both inputs must be NumPy arrays.")
    if ref.ndim != 3 or pred.ndim != 3:
        raise ValueError("Both inputs must be 3D arrays (lat x lon x time).")
    if ref.shape != pred.shape:
        raise ValueError("Input arrays must have the same shape.")

    # --- Flatten the arrays for pixel-wise statistics ---
    ref_flat = ref.ravel()
    pred_flat = pred.ravel()

    # --- Confusion matrix components ---
    a = np.sum((ref_flat > 0) & (pred_flat > 0))  # Hits
    b = np.sum((ref_flat == 0) & (pred_flat > 0))  # False Alarms
    c = np.sum((ref_flat > 0) & (pred_flat == 0))  # Misses
    d = np.sum((ref_flat == 0) & (pred_flat == 0))  # Correct Rejections
    N = a + b + c + d

    # --- Categorical statistics ---
    POD   = a / (a + c) if (a + c) > 0 else np.nan
    FAR   = b / (a + b) if (a + b) > 0 else np.nan
    POFD  = b / (b + d) if (b + d) > 0 else np.nan
    FBI   = (a + b) / (a + c) if (a + c) > 0 else np.nan
    ACC   = (a + d) / N     if N > 0 else np.nan
    CSI   = a / (a + b + c) if (a + b + c) > 0 else np.nan

    # True Skill Statistic (Hanssen–Kuipers Discriminant)
    denom_tss = (a + c) * (b + d)
    TSS   = (a * d - b * c) / denom_tss if denom_tss > 0 else np.nan
    # Heidke Skill Score
    denom_hss = (a + c)*(c + d) + (a + b)*(b + d)
    HSS   = 2 * (a * d - b * c) / denom_hss if denom_hss > 0 else np.nan

    return {
        'POD': POD,
        'FAR': FAR,
        'POFD': POFD,
        'FBI': FBI,
        'ACC': ACC,
        'CSI': CSI,
        'TSS': TSS,
        'HSS': HSS
    }