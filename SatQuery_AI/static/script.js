const form =
    document.getElementById("analysisForm");

const resultText =
    document.getElementById("resultText");


form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const formData =
            new FormData(form);


        resultText.innerText =
            "Processing satellite image...";


        try {

            const response =
                await fetch(
                    "/analyze",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            resultText.innerText =
                "Status: " +
                data.status +

                "\n\nQuery: " +
                data.query +

                "\n\nImage: " +
                data.image +

                "\n\n" +
                data.message;


        } catch (error) {

            resultText.innerText =
                "Error while processing the request.";

            console.error(error);

        }

    }
);
