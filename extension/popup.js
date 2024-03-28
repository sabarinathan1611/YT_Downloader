document.addEventListener("DOMContentLoaded", function () {
  const main = document.getElementById("main");
  const downloadBtn = document.getElementById("downloadBtn");
  const urlInput = document.getElementById("url");
  const resolutionSelect = document.getElementById("resolution");
  const message = document.getElementById("message");

  downloadBtn.addEventListener("click", function () {
    const url = urlInput.value.trim();
    const resolution = resolutionSelect.value;

    if (url === "") {
      showMessage("Please enter a YouTube URL.");
      return;
    }

    // Hide input elements
    urlInput.style.display = "none";
    resolutionSelect.style.display = "none";
    downloadBtn.style.display = "none";

    // Construct the API endpoint URL
    const apiUrl = "http://127.0.0.1:5000/download";

    // Show loading GIF
    const loadingGIF = document.createElement("iframe");
    loadingGIF.src = "images/loading.gif";
    loadingGIF.width = "200";
    loadingGIF.height = "200";
    loadingGIF.frameBorder = "0";
    loadingGIF.className = "giphy-embed";
    loadingGIF.allowFullScreen = true;
    main.appendChild(loadingGIF);

    // Make a POST request to the API
    fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ video_url: url, resolution: resolution }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Remove loading GIF
        main.removeChild(loadingGIF);

        if (data.success) {
          showMessage(data.message);
          // Call the download_file function passing the filename
          download_file(data.file);
        } else {
          showMessage("Error: " + data.error);
        }
      })
      .catch((error) => {
        // Remove loading GIF
        main.removeChild(loadingGIF);

        // Show input elements
        downloadBtn.style.display = "block";
        urlInput.style.display = "block";
        resolutionSelect.style.display = "block";

        showMessage("Error: Unable to connect to the server.");
        console.error("Error:", error);
      });
  });

  function showMessage(msg) {
    message.textContent = msg;
  }

  // Function to trigger download of file
  function download_file(filename) {
    // Construct the download URL
    const downloadUrl = `http://127.0.0.1:5000/download/${encodeURIComponent(
      filename
    )}`;

    // Open the download URL in a new tab
    window.open(downloadUrl, "_blank");
  }
});
