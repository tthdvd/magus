$(document).ready(
    function () {

        $("#add_resources_proper").click(function () {
            $(this).hide()
            $('#new_resources_container').show();
        });

        $('#search').keyup(
            function () {
                if($(this).val().length > 0){
                search_text = $(this).val()
                    $.post({
                        type: "POST",
                        url: "/finder/search/",
                        data: {text: $(this).val()},
                        headers: {
                            "X-CSRFToken": $.cookie('csrftoken')
                        }

                    }).done(
                        function (data) {
                        r_count = 0;
                        u_count = 0;
                                $("#results").html(" ");
                                $("#results_count").html(" ")
                                $.each(data.resources, function (value, key) {
                                    $("#results").append(
                                        '<a class="list-group-item" href="/finder/resources/'
                                        +key.id+'">Resources: '+ key.name
                                        +'<br> found in: <i>' + key.key +' : <strong>'+ key.value +'</strong></i></a>');
                                        r_count++;
                                });

                                $.each(data.users, function (value, key) {
                                    $("#results").append(
                                        '<a class="list-group-item" href="/finder/user/'
                                        +key.id+'">User: '+ key.name
                                        +'<br> found in: <i>' + key.key +' : <strong>'+ key.value +'</strong></i></a>');
                                        u_count++;
                                });

                            if(r_count > 0){
                                $("#results_count").append("<p><strong>"+ r_count +"</strong> resources has this value: "+search_text+"</p>")
                            } else {
                                $("#results_count").append("<p><strong>"+ u_count +"</strong> user has this quality: "+search_text+"</p>")
                            }
                        }
                    );
                }
            }
        );
    }

);
