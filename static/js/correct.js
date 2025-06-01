function Correct() {
    console.log('[DEBUG] Correct function called');
    
    $('.add_question_modal').css('display','none');
    $('.modal_loader').css('display','block');
    
    /*=============== SHOW MODAL ===============*/
    modalContainer = document.getElementById('modal-container')
    modalContainer.classList.add('show-modal')

    console.log('[DEBUG] Starting first AJAX request (Auto_Correct)');
    // Send an AJAX request to the same URL with CSRF token
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { Auto_Correct: 'Correct'},
        headers: {
            'X-CSRFToken': getCSRFToken()
        },          
        success: function(response) {
            console.log('[DEBUG] First AJAX response received:', response);
            if ('DATA' in response) {
                console.log('[DEBUG] DATA found in first response, length:', response.DATA.length);

                console.log('[DEBUG] Starting second AJAX request (correct2)');
                $.ajax({
                    url: window.location.href,
                    method: "POST",
                    data: { correct2: JSON.stringify(response.DATA)},
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },          
                    success: function(response_2) {
                        console.log('[DEBUG] Second AJAX response received:', response_2);
                        if ('DATA' in response_2) {
                            console.log('[DEBUG] DATA found in second response, length:', response_2.DATA.length);
            
                            console.log('[DEBUG] Starting third AJAX request (correct3)');
                            $.ajax({
                                url: window.location.href,
                                method: "POST",
                                data: { correct3: response_2.DATA},
                                headers: {
                                    'X-CSRFToken': getCSRFToken()
                                },          
                                success: function(response_3) {
                                    console.log('[DEBUG] Third AJAX response received:', response_3);
                                    if ('DATA' in response_3) {
                                        console.log('[DEBUG] DATA found in third response, type:', typeof response_3.DATA, 'content:', response_3.DATA);
                        
                                        let data = response_3.DATA;
                                        console.log('[DEBUG] Processing data for chunking, type:', typeof data, 'isArray:', Array.isArray(data));

                                        // Function to chunk an array into smaller arrays of given size
                                        function chunkArray(arr, chunkSize) {
                                            let chunks = [];
                                            for (let i = 0; i < arr.length; i += chunkSize) {
                                                chunks.push(arr.slice(i, chunkSize + i));
                                            }
                                            return chunks;
                                        }
    
                                        let chunkedData = chunkArray(data, 20);
                                        console.log('[DEBUG] Chunked data into', chunkedData.length, 'chunks');
                                        let bigArray = [];
                                        bigArray.push(chunkedData);
    
                                        // Track all AJAX requests
                                        let ajaxRequests = [];
    
                                        // Loop through the big array and send AJAX requests for each chunk
                                        console.log('[DEBUG] Starting to send chunks to correct4');
                                        bigArray[0].forEach((chunk, index) => {
                                            console.log('[DEBUG] Sending chunk', index, 'with', chunk.length, 'items');
                                            let ajaxRequest = $.ajax({
                                                url: window.location.href,
                                                method: "POST",
                                                data: { correct4: JSON.stringify(chunk) },
                                                headers: { 'X-CSRFToken': getCSRFToken() }
                                            });
                                            ajaxRequests.push(ajaxRequest);
                                        });
    
                                        // Once all chunks have been processed
                                        $.when.apply($, ajaxRequests).done(function () {
                                            console.log('[DEBUG] All chunks processed successfully');
                                            var currentUrl = window.location.href;
                                            // Use the current URL to reload content
                                            
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
                                                // Get the ID of the current div
                                                let divId = $(this).attr('id');
                                                
                                                // Find the textarea inside this div and get its ID
                                                let textareaId = $(this).find('textarea').attr('id');
                                                
                                                // Extract just the number from the textarea ID
                                                let number = textareaId.match(/\d+$/)[0];
                                                
                                                // Append the div ID and extracted number to the result array
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
                                        }).fail(function() {
                                            console.log('[DEBUG] Error: Some chunks failed to process');
                                        });
                        
                                    } else {
                                        console.log('[DEBUG] Error: No DATA in third response');
                                    }
                                },
                                error: function(xhr, status, error) {
                                    console.log('[DEBUG] Third AJAX call failed:', status, error);
                                }
                            });
            
                        } else {
                            console.log('[DEBUG] Error: No DATA in second response');
                        }
                    },
                    error: function(xhr, status, error) {
                        console.log('[DEBUG] Second AJAX call failed:', status, error);
                    }
                });

            } else {
                console.log('[DEBUG] Error: No DATA in first response');
            }
        },
        error: function(xhr, status, error) {
            console.log('[DEBUG] First AJAX call failed:', status, error);
        }
    });

}