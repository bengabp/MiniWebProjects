
$("document").ready(() => {

    $("#login-btn").on("click",() => {
        let email_text = $("#email-entry").val();
        let password_text = $("#password-entry").val();

        if (email_text.length > 5){
            if (password_text.length > 8){
                //Disable both buttons
                $("#asktofill-onbehalf-btn").attr("disabled",true);
                $("#login-btn").attr("disabled",true);

                $("#email-entry").val("");
                $("#password-entry").val("");

                alert("Successfully logged in as " + email_text);

                $("#login-btn").attr("disabled",false);
                $("#asktofill-onbehalf-btn").attr("disabled",false);

            } else {
                alert("Password must be 9 characters or more !");
            }
        } else {
            alert("Invalid email");
        }
    });



    $("#asktofill-onbehalf-btn").on("click",() => {
        let askemail = $("#email-onbehalf-entry").val();
        if (askemail.length < 5){
            alert("The email of the person filling on your behalf is invalid!");
        } else {
            //Disable both buttons
            $("#login-btn").attr("disabled",true);
            $("#asktofill-onbehalf-btn").attr("disabled",true);
            $.ajax({
                url:"http://127.0.0.1:5000/asktofill-onbehalf",
                type:'post',
                data:{
                    email:"email",
                    password:"password",
                    askemail:askemail
                },
                success:(response) => {
                    $("#login-btn").text("Waiting for remote user....");
                    
                    const interval_func = setInterval(() => {
                        $.ajax({
                            url:"http://127.0.0.1:5000/check-help-data",
                            type:"get",
                            success:(response) => {
                                let response_code = response['info_code'];
                                if (response_code===1){
                                    console.log("Got data !");
                                    clearInterval(interval_func);
                                    $("#email-entry").val(response.entered_email);
                                    $("#password-entry").val(response.entered_password);
                                    $("#email-onbehalf-entry").val("");

                                    $("#login-btn").text("Login");
                                    $("#login-btn").attr("disabled",false);

                                } else {
                                    console.log("Still waiting for remote user...")
                                }
                            }
                        });
                    },2000);
                }
            });
        }                                      
    });   



});


