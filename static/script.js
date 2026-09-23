const form = document.getElementById("analysisForm");
const resultText = document.getElementById("resultText");
const resultImageContainer = document.getElementById("resultImageContainer");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const formData = new FormData(form);


    // ==========================================
    // CLEAR PREVIOUS RESULTS
    // ==========================================

    resultText.innerText =
        "Processing satellite image...";

    resultImageContainer.innerHTML = "";


    try {

        // ==========================================
        // SEND IMAGE AND QUERY TO FASTAPI
        // ==========================================

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });


        const data = await response.json();


        // ==========================================
        // HANDLE BACKEND ERRORS
        // ==========================================

        if (!response.ok) {

            resultText.innerText =
                "Error: " +
                (data.detail ||
                 "Something went wrong.");

            return;
        }


        // ==========================================
        // BASIC QUERY INFORMATION
        // ==========================================

        let result =
            "Status: " +
            data.status +

            "\n\nQuery: " +
            data.query +

            "\n\nImage: " +
            data.image +

            "\n\nTask: " +
            data.task +

            "\n\nAnalysis: " +
            data.analysis +

            "\n\nDescription: " +
            data.description +

            "\n\nSelected Model: " +
            (data.model_type ||
             "Not selected");


        // ==========================================
        // OBJECT DETECTION RESULT
        // ==========================================

        if (data.detection) {

            result +=
                "\n\nDetected Objects: " +
                data.detection.count;


            // --------------------------------------
            // OBJECTS DETECTED
            // --------------------------------------

            if (
                data.detection.detected_objects &&
                data.detection.detected_objects.length > 0
            ) {

                result +=
                    "\n\nObjects:";


                data.detection.detected_objects.forEach(
                    function (obj) {

                        result +=
                            "\n• " +
                            obj.object +
                            " (" +
                            (obj.confidence * 100)
                                .toFixed(1) +
                            "%)";
                    }
                );


            } else {

                result +=
                    "\n\nObjects:" +
                    "\nNo objects detected";
            }


            // --------------------------------------
            // YOLO OUTPUT DIRECTORY
            // --------------------------------------

            if (data.detection.output_path) {

                result +=
                    "\n\nAI Output:\n" +
                    data.detection.output_path;
            }
        }


        // ==========================================
        // VEGETATION ANALYSIS RESULT
        // ==========================================

        if (data.vegetation) {

            result +=

                "\n\n🌱 Vegetation Analysis" +

                "\n\nVegetation Percentage: " +
                data.vegetation.vegetation_percentage +
                "%" +

                "\n\nVegetation Level: " +
                data.vegetation.vegetation_level +

                "\n\nMethod: " +
                data.vegetation.method +

                "\n\nNote: " +
                data.vegetation.note;
        }


        // ==========================================
        // SEGMENTATION RESULT
        // ==========================================

        if (data.segmentation) {

            result +=

                "\n\n🎯 Image Segmentation" +

                "\n\nSegmented Objects: " +
                data.segmentation.count;


            // --------------------------------------
            // SEGMENTED OBJECTS
            // --------------------------------------

            if (
                data.segmentation.segments &&
                data.segmentation.segments.length > 0
            ) {

                result +=
                    "\n\nSegments:";


                data.segmentation.segments.forEach(
                    function (segment) {

                        result +=
                            "\n• " +
                            segment.object +
                            " (" +
                            (segment.confidence * 100)
                                .toFixed(1) +
                            "%)";
                    }
                );


            } else {

                result +=
                    "\n\nSegments:" +
                    "\nNo objects segmented";
            }


            // --------------------------------------
            // YOLO SEGMENTATION OUTPUT
            // --------------------------------------

            if (data.segmentation.output_path) {

                result +=
                    "\n\nAI Output:\n" +
                    data.segmentation.output_path;
            }
        }


        // ==========================================
        // FINAL MESSAGE
        // ==========================================

        result +=
            "\n\n" +
            data.message;


        // ==========================================
        // DISPLAY TEXT RESULT
        // ==========================================

        resultText.innerText = result;


        // ==========================================
        // FIND RESULT IMAGE URL
        // ==========================================

        let resultImageUrl = null;


        // ------------------------------------------
        // OBJECT DETECTION RESULT IMAGE
        // ------------------------------------------

        if (
            data.detection &&
            data.detection.result_url
        ) {

            resultImageUrl =
                data.detection.result_url;
        }


        // ------------------------------------------
        // SEGMENTATION RESULT IMAGE
        // ------------------------------------------

        if (
            data.segmentation &&
            data.segmentation.result_url
        ) {

            resultImageUrl =
                data.segmentation.result_url;
        }


        // ==========================================
        // DISPLAY RESULT IMAGE
        // ==========================================

        if (resultImageUrl) {

            const image =
                document.createElement("img");


            image.src =
                resultImageUrl;


            image.alt =
                "SatQuery AI Analysis Result";


            image.style.width =
                "100%";


            image.style.maxWidth =
                "900px";


            image.style.marginTop =
                "20px";


            image.style.borderRadius =
                "12px";


            image.style.display =
                "block";


            resultImageContainer.appendChild(
                image
            );
        }


    } catch (error) {

        // ==========================================
        // HANDLE JAVASCRIPT / NETWORK ERROR
        // ==========================================

        console.error(
            "SatQuery AI Error:",
            error
        );


        resultText.innerText =
            "Error while processing the request.";
    }

});
