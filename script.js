
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({
    video: true
}).then(stream => {
    video.srcObject = stream;
});

video.addEventListener('play', () => {
    setInterval(async () => {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');
        const blob = await fetch(imageData).then(res => res.blob());
        const formData = new FormData();
        formData.append('image', blob, 'image.jpg');

        const response = await fetch('http://localhost:8000/detect', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        displayResult(result.posture);
    }, 1000);
});

function displayResult(posture) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    context.fillStyle = 'red';
    context.font = '30px Arial';
    context.fillText(posture, 10, 50);
}

function showHomepage() {
    document.getElementById('homepage').style.display = 'block';
    document.getElementById('analysispage').style.display = 'none';
}

function showAnalysisPage() {
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('analysispage').style.display = 'block';
}

// Initialize homepage
showHomepage();
