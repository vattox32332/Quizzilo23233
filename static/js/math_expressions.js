
function Math_Expressions() {
    
    $('.add_question_modal').css('display','none');
    $('.modal_loader').css('display','block');
    
    /*=============== SHOW MODAL ===============*/
    modalContainer = document.getElementById('modal-container')
    modalContainer.classList.add('show-modal')

    // Send an AJAX request to the same URL with CSRF token
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { latex: 'latex'},
        headers: {
            'X-CSRFToken': getCSRFToken()
        },          
        success: function(response) {
            if ('DATA' in response) {
                let data = response.DATA;

                // Function to chunk an array into smaller arrays of given size
                function chunkArray(arr, chunkSize) {
                    let chunks = [];
                    for (let i = 0; i < arr.length; i += chunkSize) {
                        chunks.push(arr.slice(i, i + chunkSize));
                    }
                    return chunks;
                }

                let chunkedData = chunkArray(data, 5); // Smaller chunks for latex processing

                // Function to send each chunk sequentially
                function sendLatexChunksSequentially(chunks) {
                    // Check if there are no chunks left to process
                    if (chunks.length === 0) {
                        // All chunks have been sent
                        let currentUrl = window.location.href;

                        // Reload content using jQuery
                        $('#jquery_load').load(currentUrl + ' #Questions_body', function() {
                            feather.replace();
                            
                            // Make the divs inside parentDiv sortable
                            $("#Questions_body").sortable({
                                update: function(event, ui) {
                                    // Update the IDs of each child div according to their new position
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
                    console.log('Processing chunk:', JSON.stringify(chunk));

                    // Send the chunk to latex2
                    $.ajax({
                        url: window.location.href,
                        method: "POST",
                        data: { latex2: JSON.stringify(chunk) },
                        headers: { 'X-CSRFToken': getCSRFToken() },
                        success: function(response_2) {
                            if ('DATA' in response_2) {
                                console.log('Latex2 response:', JSON.stringify(response_2.DATA));
                                
                                // Send to latex4
                                $.ajax({
                                    url: window.location.href,
                                    method: "POST",
                                    data: { latex4: JSON.stringify(response_2.DATA) },
                                    headers: { 'X-CSRFToken': getCSRFToken() },
                                    success: function(response_4) {
                                        // Recursively call the function to send the next chunk
                                        sendLatexChunksSequentially(chunks);
                                    },
                                    error: function(xhr, status, error) {
                                        console.error('Error in latex4:', error);
                                        // Continue with next chunk even if one fails
                                        sendLatexChunksSequentially(chunks);
                                    }
                                });
                            } else {
                                // Continue with next chunk if no DATA
                                sendLatexChunksSequentially(chunks);
                            }
                        },
                        error: function(xhr, status, error) {
                            console.error('Error in latex2:', error);
                            // Continue with next chunk even if one fails
                            sendLatexChunksSequentially(chunks);
                        }
                    });
                }

                // Start sending chunks sequentially
                sendLatexChunksSequentially(chunkedData);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error in initial latex request:', error);
            $('.add_question_modal').css('display','block');
            $('.modal_loader').css('display','none');
            const modalContainer = document.getElementById('modal-container')
            modalContainer.classList.remove('show-modal')
        }
    });
}

function getCSRFToken() {
    return $('[name=csrfmiddlewaretoken]').val();
}
