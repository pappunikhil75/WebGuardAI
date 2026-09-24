const API_URL = "https://webguardai-da6a.onrender.com/predict";


async function scanWebsite() {

    const urlInput = document.getElementById("urlInput");
    const scanButton = document.getElementById("scanButton");

    const loading = document.getElementById("loading");
    const resultSection = document.getElementById("resultSection");
    const errorMessage = document.getElementById("errorMessage");

    const url = urlInput.value.trim();


    // Clear previous messages
    errorMessage.textContent = "";
    resultSection.classList.add("hidden");


    // Validate input
    if (!url) {

        errorMessage.textContent =
            "Please enter a website URL.";

        return;
    }


    // Basic URL validation
    let formattedURL = url;

    if (
        !url.startsWith("http://") &&
        !url.startsWith("https://")
    ) {
        formattedURL = "https://" + url;
    }


    try {

        new URL(formattedURL);

    } catch {

        errorMessage.textContent =
            "Please enter a valid URL.";

        return;
    }


    // Show loading
    loading.classList.remove("hidden");
    scanButton.disabled = true;
    scanButton.textContent = "Scanning...";


    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: formattedURL
            })

        });


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error || "Unable to analyze URL."
            );

        }


        // Display result
        displayResult(data);


    } catch (error) {

        console.error(error);

        errorMessage.textContent =
            "Unable to connect to WebGuard AI backend. " +
            "Make sure Flask is running on port 5000.";

    } finally {

        loading.classList.add("hidden");

        scanButton.disabled = false;

        scanButton.textContent =
            "Scan Website";
    }
}


function displayResult(data) {

    const resultSection =
        document.getElementById("resultSection");

    const prediction =
        document.getElementById("prediction");

    const riskBadge =
        document.getElementById("riskBadge");

    const scannedUrl =
        document.getElementById("scannedUrl");

    const phishingProbability =
        document.getElementById("phishingProbability");

    const legitimateProbability =
        document.getElementById("legitimateProbability");

    const phishingBar =
        document.getElementById("phishingBar");

    const legitimateBar =
        document.getElementById("legitimateBar");

    const resultMessage =
        document.getElementById("resultMessage");


    // URL
    scannedUrl.textContent = data.url;


    // Prediction
    prediction.textContent =
        data.prediction;


    // Probabilities
    phishingProbability.textContent =
        data.phishing_probability + "%";

    legitimateProbability.textContent =
        data.legitimate_probability + "%";


    // Progress bars
    phishingBar.style.width =
        data.phishing_probability + "%";

    legitimateBar.style.width =
        data.legitimate_probability + "%";


    // Risk level
    riskBadge.textContent =
        data.risk_level + " RISK";


    // Reset risk classes
    riskBadge.style.background = "";
    riskBadge.style.color = "";


    if (data.risk_level === "LOW") {

        riskBadge.style.background =
            "#18392f";

        riskBadge.style.color =
            "#55e1c4";

    } else if (data.risk_level === "MEDIUM") {

        riskBadge.style.background =
            "#3d3518";

        riskBadge.style.color =
            "#f4c95d";

    } else {

        riskBadge.style.background =
            "#421f25";

        riskBadge.style.color =
            "#ff7777";
    }


    // Prediction message
    if (data.prediction === "LEGITIMATE") {

        resultMessage.textContent =
            "The machine learning model classified " +
            "this URL as legitimate. Continue to " +
            "use normal online safety practices.";

        prediction.style.color =
            "#35d0ba";

    } else {

        resultMessage.textContent =
            "The machine learning model classified " +
            "this URL as potentially phishing. " +
            "Avoid entering passwords, payment details, " +
            "or other sensitive information unless you " +
            "can independently verify the website.";

        prediction.style.color =
            "#ff6262";
    }


    // Show result
    resultSection.classList.remove("hidden");

    // Scroll to result
    resultSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// Allow Enter key to scan
document
    .getElementById("urlInput")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {

            scanWebsite();

        }

    });