/**
 * Created by lockistrike on 20.04.17.
 */

$(document).ready(function () {
    $("#send_button").click(function () {
        // var link = "https://0bb32a8d.ngrok.io/tweeting";
        // var data = {"text": $("#tweet_text").val()};
        // $.ajax({
        //     url: link,
        //     data: data,
        //     type: 'POST',
        //     success: function () {
        //         alert(1);
        //     },
        //     error: function () {
        //         alert(2);
        //     },
        //     });
        var http = new XMLHttpRequest();
        var url = "https://54967f2e.ngrok.io/send";
        var params = "?text="+ $("#tweet_text").val();
        http.open("POST", url, true);

        //Send the proper header information along with the request
        http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        http.send(params)
    });
    // $("#send_button").click(function () {
    //     alert("1")
    //     //location.reload();
    // });
});

function success(response) {
    alert("tweet was successfuly send with text: \n" + response.text);
}