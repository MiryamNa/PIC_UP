"""
Wrapper for the ConvNeXt-Tiny wedding-event classifier.

Loads the model once at import time and exposes a thread-safe
predict_image_category() function.

Model: ConvNeXt-Tiny fine-tuned for 6 wedding categories.
Categories: bride_chair, chuppa, dance, meal, out, yichud
Fallback: "general" when classification fails.
"""
import os
import logging
from typing import Optional, Dict, Any, List

import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Path
# ---------------------------------------------------------------------------
MODEL_WEIGHTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ML_Event_classifier",
    "trained_convnext_model.pth",
)

# ---------------------------------------------------------------------------
# Categories (must match training order)
# ---------------------------------------------------------------------------
CLASS_NAMES: List[str] = [
    "bride_chair",
    "chuppa",
    "dance",
    "meal",
    "out",
    "yichud",
]

FALLBACK_CATEGORY = "general"

# ---------------------------------------------------------------------------
# Module-level lazy-loaded model
# ---------------------------------------------------------------------------
_model = None
_device = None
_preprocess = None
_classifier_available = False

def _load_model() -> bool:
    """Lazy-load the ConvNeXt model. Returns True on success.

    Called automatically on first call to predict_image_category().
    Thread-safe because Python's import lock ensures this runs exactly once
    (module-level; calls happen inside predict_image_category which may
    be invoked from multiple threads — but the bool flag is checked
    atomically and set only after all setup completes).
    """
    global _model, _device, _preprocess, _classifier_available

    if _classifier_available:
        return True

    try:
        import torch
        import torch.nn as nn
        import torchvision.models as models
        import torchvision.transforms as transforms

        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info("ML classifier using device: %s", _device)

        # Build ConvNeXt-Tiny with 6-class head
        _model = models.convnext_tiny(weights=None)
        in_features = _model.classifier[2].in_features
        _model.classifier[2] = nn.Linear(in_features, len(CLASS_NAMES))

        # Load trained weights
        state_dict = torch.load(MODEL_WEIGHTS_PATH, map_location=_device)
        _model.load_state_dict(state_dict)
        _model = _model.to(_device)
        _model.eval()

        # Preprocessing pipeline (ImageNet stats — same as training)
        _preprocess = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

        _classifier_available = True
        logger.info(
            "ML classifier loaded successfully (%d classes)", len(CLASS_NAMES)
        )
        return True

    except FileNotFoundError:
        logger.warning(
            "Model weights not found at %s — classification disabled",
            MODEL_WEIGHTS_PATH,
        )
        return False
    except Exception:
        logger.exception("Failed to load ML classifier")
        return False

def _predict_sync(
    image_path: Optional[str] = None,
    image: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """Synchronous inference — runs inside asyncio.to_thread.

    Args:
        image_path: Path to image file (used if ``image`` is None).
        image: Numpy array in BGR format (OpenCV default). When provided,
               skips disk read.

    Returns:
        Dict with keys: category, category_probabilities, confidence,
        classifier_available.
    """
    if not _classifier_available:
        if not _load_model():
            return _fallback_result()

    try:
        import torch
        from PIL import Image

        # --- Prepare PIL image ---
        if image is not None:
            import cv2

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb)
        elif image_path and os.path.exists(image_path):
            pil_image = Image.open(image_path).convert("RGB")
        else:
            logger.warning("No valid image source provided")
            return _fallback_result()

        # --- Preprocess ---
        input_tensor = _preprocess(pil_image).unsqueeze(0).to(_device)

        # --- Inference ---
        with torch.no_grad():
            outputs = _model(input_tensor)  # shape: [1, num_classes]
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

        probs_np = probabilities.cpu().numpy()
        max_idx = int(probs_np.argmax())
        max_prob = float(probs_np[max_idx])

        # Build sorted probability list
        prob_list = sorted(
            [
                {"category": CLASS_NAMES[i], "probability": float(probs_np[i])}
                for i in range(len(CLASS_NAMES))
            ],
            key=lambda x: x["probability"],
            reverse=True,
        )

        return {
            "category": CLASS_NAMES[max_idx],
            "category_probabilities": prob_list,
            "confidence": max_prob,
            "classifier_available": True,
        }

    except Exception:
        logger.exception("Prediction failed — returning fallback category")
        return _fallback_result()

def _fallback_result() -> Dict[str, Any]:
    """Return a safe fallback result."""
    return {
        "category": FALLBACK_CATEGORY,
        "category_probabilities": [],
        "confidence": 0.0,
        "classifier_available": False,
    }

# ---------------------------------------------------------------------------
# Public API — synchronous (meant to be called via asyncio.to_thread)
# ---------------------------------------------------------------------------
def predict_image_category(
    image_path: Optional[str] = None,
    image: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """Classify a wedding photo into one of 6 event categories.

    This is a synchronous function designed to be called via
    ``asyncio.to_thread`` in async contexts, or directly in sync code.

    Args:
        image_path: Path to image file on disk.
        image: Optional numpy array (BGR, as read by cv2.imread).
               When provided, disk read is skipped.

    Returns:
        Dict with:
        - category (str): Predicted category, or "general" on failure
        - category_probabilities (list): All categories with their probabilities,
          sorted descending
        - confidence (float): Probability of the top category (0-1)
        - classifier_available (bool): Whether the ML model is loaded
    """
    return _predict_sync(image_path=image_path, image=image)

# ---------------------------------------------------------------------------
# Utility: force reload (useful for testing / hot-reload scenarios)
# ---------------------------------------------------------------------------
def reload_model() -> bool:
    """Force-reload the model weights. Returns True on success."""
    global _model, _device, _preprocess, _classifier_available
    _model = None
    _device = None
    _preprocess = None
    _classifier_available = False
    return _load_model()


