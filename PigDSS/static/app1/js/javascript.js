$(document).ready(function(){
    $('.btnNext').click(function(){
        $('.nav-tabs > .active').next('li').find('a').trigger('click');
    });

    $('.btnPrevious').click(function(){
        $('.nav-tabs > .active').prev('li').find('a').trigger('click');
    });
    
    $(".img-check").click(function(){
            $(this).toggleClass("check");
    });
    
    $('#id_other_symptoms').multiselect({
        maxHeight: 300,
        buttonWidth: '100%',
        numberDisplayed: 5,
        enableCaseInsensitiveFiltering: true,
        includeSelectAllOption: true,
        nonSelectedText: 'Choose Symptoms',
    });

    $('#id_address').multiselect({
        maxHeight: 300,
        buttonWidth: '100%',
        numberDisplayed: 5,
        enableCaseInsensitiveFiltering: true,
        nonSelectedText: 'Your address',
    });

    $("#id_address").change(function (e) {
        e.preventDefault();
        var selectedValue = $(this).val();
        // alert(" Value: " + selectedValue);
        $.ajax({
            url:"/ajax_request/",
            type:"POST",
            data: { user_address : selectedValue },
            cache: false,
            dataType: "json",
            success: function(json){
                $('#hospital_name').text(json.hospital);
                $('#hospital_address').text(json.address);
                $('#hospital_phone').text(json.phone);
                $('#hospital_state').text(json.state);
            }
        });
        return false;
    });

});

