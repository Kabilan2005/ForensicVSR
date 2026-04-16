import streamlit as st
import cv2
import tempfile
import os
import zipfile
from pipelines.processing_engine import ForensicVSR_Pipeline2

def show():
    st.markdown("###Final Forensic Review")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Evidence")
        if 'original_preview' in st.session_state:
            st.image(st.session_state.original_preview, channels="BGR", use_container_width=True)
        
    with col2:
        st.subheader("Enhanced Reconstruction")
        if 'working_frame' in st.session_state:
            st.image(st.session_state.working_frame, channels="BGR", use_container_width=True)

    st.markdown("#### 📝 Applied Techniques (Audit Log)")
    if 'choices' in st.session_state:
        # Create an organized list of what was done for court compliance
        for tech, applied in st.session_state.choices.items():
            status = "✅ **APPLIED**" if applied else "⚪ *SKIPPED*"
            st.write(f"- {tech}: {status}")
    else:
        st.warning("No technique choices found. Please complete the Techniques page.")

    st.markdown("---")
    
    st.subheader("📦 Step 1: Generate Export Files")
    st.info("This process will apply your chosen techniques to every frame of the video. This may take some time depending on video length.")

    if st.button("🚀 Prepare High-Quality Evidence", use_container_width=True):
        # UI Elements for progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Load Video Data
        input_path = st.session_state.target_video
        cap = cv2.VideoCapture(input_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        is_upscaled = st.session_state.choices.get("Spatial Upscaling", False)
        
        if is_upscaled:
            width *= 2
            height *= 2

        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        # Initialize Writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video.name, fourcc, fps, (width, height))
        
        try:
            with zipfile.ZipFile(temp_zip.name, 'w') as img_zip:
                for i in range(total_frames):
                    ret, frame = cap.read()
                    if not ret: break
                    
                    engine = ForensicVSR_Pipeline2(frame)
                    
                    processed = engine.step_1_bitrate(st.session_state.choices.get("Bitrate Recovery", False))
                    processed = engine.step_2_environment(
                        relight=st.session_state.choices.get("Environmental Fix", False),
                        dehaze=st.session_state.choices.get("Environmental Fix", False)
                    )
                    processed = engine.step_3_denoise(st.session_state.choices.get("Denoising", False))
                    processed = engine.step_4_upscale(2 if is_upscaled else 1)
                    processed = engine.step_5_sharpen(st.session_state.choices.get("Sharpening", False))
                    
                    out.write(processed)
                    
                    if i % 5 == 0:
                        img_name = f"forensic_frame_{i:04d}.png"
                        _, img_encoded = cv2.imencode('.png', processed)
                        img_zip.writestr(img_name, img_encoded.tobytes())
                    
                    current_progress = (i + 1) / total_frames
                    progress_bar.progress(current_progress)
                    status_text.text(f"Processing Frame {i+1} of {total_frames}...")

            st.session_state.final_video = temp_video.name
            st.session_state.final_zip = temp_zip.name
            status_text.success("✅ Evidence generation complete!")
            st.rerun()

        except Exception as e:
            st.error(f"Error during batch processing: {e}")
        finally:
            cap.release()
            out.release()

    if 'final_video' in st.session_state:
        st.markdown("---")
        st.subheader("📥 Step 2: Download Admissible Evidence")
        d_col1, d_col2 = st.columns(2)
        
        with d_col1:
            with open(st.session_state.final_video, "rb") as f:
                st.download_button(
                    label="🎥 Download Full Video (.mp4)",
                    data=f,
                    file_name="Forensic_VSR_Export.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            st.caption("Optimized for courtroom playback.")
            
        with d_col2:
            with open(st.session_state.final_zip, "rb") as f:
                st.download_button(
                    label="🖼️ Download Evidence ZIP (.zip)",
                    data=f,
                    file_name="Forensic_Frames_Exhibit.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            st.caption("Contains high-res PNG stills for forensic reports.")