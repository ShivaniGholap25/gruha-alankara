let activeStream = null;

function stopCamera() {
	if (!activeStream) {
		return;
	}

	activeStream.getTracks().forEach((track) => track.stop());
	activeStream = null;
}

// ── AR page: auto-init camera-feed if present ──────────────────────────────
(function initARCamera() {
	const videoEl = document.getElementById("camera-feed");
	if (!videoEl) return;
	const isMobile = /Mobi|Android/i.test(navigator.userAgent);
	const constraints = {
		video: isMobile
			? { facingMode: { ideal: "environment" } }
			: true
	};
	navigator.mediaDevices.getUserMedia(constraints)
		.then(stream => {
			activeStream = stream;
			videoEl.srcObject = stream;
		})
		.catch(() => alert("Camera access denied"));
})();

document.addEventListener("DOMContentLoaded", () => {
	const cameraFeed = document.getElementById("camera-feed");
	const startCameraBtn = document.getElementById("start-camera-btn");
	const captureRoomBtn = document.getElementById("capture-room-btn");
	const captureCanvas = document.getElementById("capture-canvas");
	const spinner = document.getElementById("upload-spinner");
	const recommendations = document.getElementById("ai-recommendations");
	const selectedStyleInput = document.getElementById("selected-style");

	// analyze page uses start-camera-btn; skip if not present
	if (!startCameraBtn) {
		return;
	}

	if (startCameraBtn) {
		startCameraBtn.addEventListener("click", async () => {
			if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
				alert("Camera access is not supported in this browser.");
				return;
			}

			try {
				stopCamera();
				const stream = await navigator.mediaDevices.getUserMedia({
					video: {
						facingMode: "environment",
						width: { ideal: 1280 },
						height: { ideal: 720 }
					}
				});

				activeStream = stream;
				cameraFeed.srcObject = stream;
				await cameraFeed.play();

				if (captureRoomBtn) {
					captureRoomBtn.style.display = "inline-flex";
				}
			} catch (error) {
				if (error && (error.name === "NotAllowedError" || error.name === "PermissionDeniedError")) {
					alert("Camera permission was denied. Please allow access in your browser settings and try again.");
					return;
				}

				alert("Unable to start camera. Please check your device camera and try again.");
			}
		});
	}

	if (captureRoomBtn && captureCanvas) {
		captureRoomBtn.addEventListener("click", async () => {
			if (!cameraFeed.videoWidth || !cameraFeed.videoHeight) {
				if (recommendations) {
					recommendations.textContent = "Camera is not ready yet. Please start the camera first.";
				}
				return;
			}

			captureCanvas.width = cameraFeed.videoWidth;
			captureCanvas.height = cameraFeed.videoHeight;
			const context = captureCanvas.getContext("2d");
			if (!context) {
				if (recommendations) {
					recommendations.textContent = "Unable to capture image from camera.";
				}
				return;
			}

			context.drawImage(cameraFeed, 0, 0, captureCanvas.width, captureCanvas.height);

			const captureBase64 = captureCanvas.toDataURL("image/jpeg", 0.85);
			if (!captureBase64) {
				if (recommendations) {
					recommendations.textContent = "Failed to capture image. Please try again.";
				}
				return;
			}

			if (typeof window.showLoading === "function") {
				window.showLoading();
			}

			if (spinner) {
				spinner.style.display = "block";
			}

			try {
				const blobResponse = await fetch(captureBase64);
				const blob = await blobResponse.blob();
				const formData = new FormData();
				formData.append("image", blob, "room-capture.jpg");
				formData.append("image_base64", captureBase64);
				if (selectedStyleInput && selectedStyleInput.value) {
					formData.append("style_theme", selectedStyleInput.value);
				}

				const response = await fetch("/upload-camera", {
					method: "POST",
					body: formData
				});

				if (!response.ok) {
					throw new Error("Upload failed");
				}

				const data = await response.json();
				if (recommendations) {
					recommendations.textContent =
						data.recommendations ||
						data.ai_output ||
						"Design recommendations generated successfully.";
				}
				if (data.redirect) {
					setTimeout(() => {
						window.location.href = data.redirect;
					}, 600);
				}
			} catch (error) {
				if (recommendations) {
					recommendations.textContent =
						"Could not upload image and fetch recommendations. Please try again.";
				}
			} finally {
				if (spinner) {
					spinner.style.display = "none";
				}
			}
		});
	}

	const styleCards = document.querySelectorAll(".style-card");
	if (styleCards.length > 0 && selectedStyleInput) {
		styleCards.forEach((card) => {
			card.addEventListener("click", () => {
				styleCards.forEach((item) => item.classList.remove("selected"));
				card.classList.add("selected");
				selectedStyleInput.value = card.dataset.style || card.textContent.trim();
			});
		});
	}
});

window.stopCamera = stopCamera;
