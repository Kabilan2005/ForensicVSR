import cv2

def apply_denoising(frame, method="deep_nlm", h=10):
    # Forensic Denoising: Removes sensor grain while preserving 'Forensic Microstructures'
    # as described in MVFNet research.
    if method == "median":
        return cv2.medianBlur(frame, 5)
    
    # h: Weighting function (Luminance), hColor: Weighting function (Color)
    # 7: Template window size, 21: Search window size
    denoised = cv2.fastNlMeansDenoisingColored(
        frame, 
        None, 
        h_luminance=h, 
        h_color=h, 
        templateWindowSize=7, 
        searchWindowSize=21
    )

    # It is like finding similar words so that i can learn what it is
    # Find Similar patches and averages them and smooth them.
    return denoised