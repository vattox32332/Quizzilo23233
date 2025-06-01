function Correct() {

    $('.add_question_modal').css('display','none');
    $('.modal_loader').css('display','block');

    /*=============== SHOW MODAL ===============*/
    modalContainer = document.getElementById('modal-container')
    modalContainer.classList.add('show-modal')

    // Send an AJAX request to the same URL with CSRF token
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { Auto_Correct: 'Correct'},
        headers: {
            'X-CSRFToken': getCSRFToken()
        },          
        success: function(response) {
            if ('DATA' in response) {

                $.ajax({
                    url: window.location.href,
                    method: "POST",
                    data: { correct2: JSON.stringify(response.DATA)},
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },          
                    success: function(response_2) {
                        if ('DATA' in response_2) {

                            $.ajax({
                                url: window.location.href,
                                method: "POST",
                                data: { correct3: response_2.DATA},
                                headers: {
                                    'X-CSRFToken': getCSRFToken()
                                },          
                                success: function(response_3) {
                                    if ('DATA' in response_3) {

                                        let data = response_3.DATA;

                                        // Function to chunk an array into smaller arrays of given size
                                        function chunkArray(arr, chunkSize) {
                                            let chunks = [];
                                            for (let i = 0; i < arr.length; i += chunkSize) {
                                                chunks.push(arr.slice(i, i + chunkSize));
                                            }
                                            return chunks;
                                        }

                                        let chunkedData = chunkArray(data, 10); // Reduced chunk size for corrector

                                        // Function to send each chunk sequentially
                                        function sendChunksSequentially(chunks) {
                                            // Check if there are no chunks left to process
                                            if (chunks.length === 0) {
                                                // All chunks have been sent
                                                var currentUrl = window.location.href;

                                                $('#jquery_load').load(currentUrl + ' #Questions_body', function() {
                                                    feather.replace();

                                                    // Make the divs inside parentDiv sortable
                                                    $("#Questions_body").sortable({
                                                        update: function(event, ui) {
                                                            // Update the IDs of each child div according to their new 
                                                            $("#Questions_body .Question").each(function(index) {
                                                                $(this).attr("id", (index + 1));
                                                            });

                                                            let resultArray = [];

                                                            $('.Question').each(function() {
                                                                let divId = $(this).attr('id');
                                                                let textareaId = $(this).find('textarea').attr('id');
                                                                let number = textareaId.match(/\d+$/)[0];
                                                                resultArray.push([divId, number]);
                                                            });

                                                            $.ajax({
                                                                url: window.location.href,
                                                                method: "POST",
                                                                data: { New_Questions_Order : JSON.stringify(resultArray) },
                                                                headers: {
                                                                    'X-CSRFToken': getCSRFToken()
                                                                }
                                                            });
                                                        }
                                                    });
                                                });

                                                setTimeout(function() {
                                                    $('.add_question_modal').css('display','block');
                                                    $('.modal_loader').css('display','none');
                                                }, 500);   
                                                const modalContainer = document.getElementById('modal-container')
                                                modalContainer.classList.remove('show-modal')
                                                return;
                                            }

                                            // Get the first chunk from the array
                                            let chunk = chunks.shift();

                                            // Send the chunk
                                            $.ajax({
                                                url: window.location.href,
                                                method: "POST",
                                                data: { correct4: JSON.stringify(chunk) },
                                                headers: { 'X-CSRFToken': getCSRFToken() },
                                                success: function(response) {
                                                    // Recursively call the function to send the next chunk
                                                    sendChunksSequentially(chunks);
                                                },
                                                error: function(xhr, status, error) {
                                                    console.error('Error sending chunk:', error);
                                                    // Continue with next chunk even if one fails
                                                    sendChunksSequentially(chunks);
                                                }
                                            });
                                        }

                                        // Start sending chunks sequentially
                                        sendChunksSequentially(chunkedData);

                                    }
                                }
                            });

                        }
                    }
                });

            }
        }
    });

}