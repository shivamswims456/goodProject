function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function success1(message) {

    $(".notification").css({ "display": "none" })

    let notification = $("#notificationSuccess");

    notification[0].innerText = message;

    notification.css("display", "flex");

    setTimeout(() => {
        $(".notification").css({ "display": "none" })
    }, 5000)
}

function updateCount(count) {

    $(".cart-count")[0].innerText = count;
}

function sendPost(data, url, cb) {

    console.log(url)

    $.ajax({

        type: "POST",
        url: url,
        data: data,
        success: cb,
        dataType: "text",
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('_xsrf'));
        }
    })

}

$(document).ready((e) => {

    //TODO add handler for cart counter update on reload

    sendPost(data = { "nature": "count" }, url = "/addToCart", cb = (response) => {

        response = JSON.parse(response);

        if (response["result"]) {

            updateCount(response["data"]["count"]);
        }
    })


    //addTOCart Click

    $("body").on("click", ".addToCart", (e) => {

        let id = $(e.currentTarget).attr("data-id"),
            nature = $(e.currentTarget).attr("data-nature"),
            message = id.includes("PACK") ? "Package Added Successfully" : "Test Added Successfully";



        sendPost(data = { "id": id, "pack": id.includes("PACK"), "nature": nature },
            url = "/addToCart", cb = (response) => {

                response = JSON.parse(response)

                console.log(response["result"]);

                if (response["result"]) {

                    success1(message);

                    updateCount(response["data"]["count"])


                }
            })

    })

})